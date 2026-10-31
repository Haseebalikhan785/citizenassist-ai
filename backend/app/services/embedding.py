"""
Embedding service using Google GenAI SDK.
Falls back gracefully when GEMINI_API_KEY is not set.
"""

import logging
from typing import Optional

import numpy as np

from backend.app.core.config import settings

logger = logging.getLogger(__name__)

_client = None


def _get_client():
    """Lazily initialise the GenAI client."""
    global _client
    if _client is not None:
        return _client
    if not settings.GEMINI_API_KEY:
        return None
    try:
        from google import genai
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
        return _client
    except Exception as e:
        logger.error("Failed to initialise GenAI client: %s", e)
        return None


def get_embedding(text: str) -> Optional[list[float]]:
    """Get an embedding vector for a single text string."""
    client = _get_client()
    if client is None:
        return None
    try:
        result = client.models.embed_content(
            model=settings.GEMINI_EMBEDDING_MODEL,
            contents=text,
        )
        # result.embeddings is a list; take the first one
        if result.embeddings:
            return list(result.embeddings[0].values)
        return None
    except Exception as e:
        logger.error("Embedding error: %s", e)
        return None


def batch_embed(texts: list[str]) -> list[Optional[list[float]]]:
    """Get embeddings for a batch of texts."""
    client = _get_client()
    if client is None:
        return [None] * len(texts)

    results: list[Optional[list[float]]] = []
    # Process in batches of 20 to respect API limits
    batch_size = 20
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        try:
            result = client.models.embed_content(
                model=settings.GEMINI_EMBEDDING_MODEL,
                contents=batch,
            )
            for emb in result.embeddings:
                results.append(list(emb.values))
        except Exception as e:
            logger.error("Batch embedding error at index %d: %s", i, e)
            results.extend([None] * len(batch))
    return results


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    va = np.array(a, dtype=np.float32)
    vb = np.array(b, dtype=np.float32)
    dot = np.dot(va, vb)
    norm_a = np.linalg.norm(va)
    norm_b = np.linalg.norm(vb)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot / (norm_a * norm_b))
