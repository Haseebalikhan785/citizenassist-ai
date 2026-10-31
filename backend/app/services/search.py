"""
Search service: FTS5 keyword search + optional embedding-based semantic search.
"""

import logging
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.app.models.database import Record, SearchChunk
from backend.app.models.schemas import SearchResultItem
from backend.app.services.embedding import cosine_similarity, get_embedding

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# FTS5 index management
# ---------------------------------------------------------------------------

def build_fts_index(db: Session) -> int:
    """Create / rebuild the FTS5 virtual table from search_chunks."""
    conn = db.connection()

    # Drop and recreate
    conn.execute(text("DROP TABLE IF EXISTS search_chunks_fts;"))
    conn.execute(text("""
        CREATE VIRTUAL TABLE search_chunks_fts USING fts5(
            content,
            record_id UNINDEXED,
            section UNINDEXED
        );
    """))

    # Insert all chunks
    chunks = db.query(SearchChunk).all()
    for chunk in chunks:
        conn.execute(
            text("INSERT INTO search_chunks_fts(content, record_id, section) VALUES (:content, :record_id, :section)"),
            {"content": chunk.content, "record_id": chunk.record_id, "section": chunk.section},
        )

    db.commit()
    logger.info("FTS5 index rebuilt with %d chunks", len(chunks))
    return len(chunks)


# ---------------------------------------------------------------------------
# Keyword search via FTS5
# ---------------------------------------------------------------------------

def keyword_search(
    query: str,
    db: Session,
    category: str | None = None,
    state: str | None = None,
    record_type: str | None = None,
    limit: int = 10,
) -> list[SearchResultItem]:
    """Full-text keyword search using SQLite FTS5."""

    # Sanitise query for FTS5 – wrap each word in double quotes for safety
    words = query.strip().split()
    if not words:
        return []
    fts_query = " OR ".join(f'"{w}"' for w in words)

    try:
        rows = db.execute(
            text("""
                SELECT
                    f.record_id,
                    f.section,
                    snippet(search_chunks_fts, 0, '<b>', '</b>', '...', 32) AS snippet,
                    rank
                FROM search_chunks_fts f
                WHERE search_chunks_fts MATCH :query
                ORDER BY rank
                LIMIT :limit
            """),
            {"query": fts_query, "limit": limit * 3},  # fetch extra to filter later
        ).fetchall()
    except Exception as e:
        logger.error("FTS5 search error: %s", e)
        return []

    # Deduplicate by record_id, keeping the best rank
    seen: dict[str, dict] = {}
    for row in rows:
        rid = row[0]
        if rid not in seen or row[3] < seen[rid]["rank"]:
            seen[rid] = {
                "record_id": rid,
                "section": row[1],
                "snippet": row[2],
                "rank": row[3],
            }

    # Fetch record metadata and apply filters
    results: list[SearchResultItem] = []
    for item in sorted(seen.values(), key=lambda x: x["rank"]):
        record = db.query(Record).filter(Record.id == item["record_id"], Record.is_active.is_(True)).first()
        if not record:
            continue

        # Apply filters
        if category and record.category and record.category.lower() != category.lower():
            continue
        if record_type and record.record_type != record_type:
            continue
        if state and record.state_applicability:
            states_lower = [s.lower() for s in record.state_applicability]
            if "all india" not in states_lower and state.lower() not in states_lower:
                continue

        results.append(SearchResultItem(
            record_id=record.id,
            record_name=record.name,
            record_type=record.record_type,
            category=record.category,
            description=record.description,
            score=abs(item["rank"]),
            matched_section=item["section"],
            snippet=item["snippet"],
            verification_status=record.verification_status,
        ))

        if len(results) >= limit:
            break

    return results


# ---------------------------------------------------------------------------
# Embedding search
# ---------------------------------------------------------------------------

def embedding_search(
    query: str,
    db: Session,
    top_k: int = 10,
) -> list[SearchResultItem]:
    """Semantic search using embeddings + cosine similarity."""
    query_emb = get_embedding(query)
    if query_emb is None:
        return []

    # Load all chunks that have embeddings
    chunks = db.query(SearchChunk).filter(SearchChunk.embedding.isnot(None)).all()
    if not chunks:
        return []

    # Score all chunks
    scored: list[tuple[SearchChunk, float]] = []
    for chunk in chunks:
        if chunk.embedding:
            sim = cosine_similarity(query_emb, chunk.embedding)
            scored.append((chunk, sim))

    scored.sort(key=lambda x: x[1], reverse=True)

    # Deduplicate by record_id
    seen: set[str] = set()
    results: list[SearchResultItem] = []
    for chunk, score in scored:
        if chunk.record_id in seen:
            continue
        seen.add(chunk.record_id)

        record = db.query(Record).filter(Record.id == chunk.record_id, Record.is_active.is_(True)).first()
        if not record:
            continue

        results.append(SearchResultItem(
            record_id=record.id,
            record_name=record.name,
            record_type=record.record_type,
            category=record.category,
            description=record.description,
            score=score,
            matched_section=chunk.section,
            snippet=chunk.content[:200],
            verification_status=record.verification_status,
        ))

        if len(results) >= top_k:
            break

    return results


# ---------------------------------------------------------------------------
# Hybrid search
# ---------------------------------------------------------------------------

def hybrid_search(
    query: str,
    db: Session,
    category: str | None = None,
    state: str | None = None,
    record_type: str | None = None,
    top_k: int = 10,
) -> tuple[list[SearchResultItem], str]:
    """
    Hybrid search combining FTS5 keyword search and embedding search.
    Returns (results, method_used).
    """
    # Always do keyword search
    kw_results = keyword_search(query, db, category, state, record_type, limit=top_k)

    # Try embedding search
    emb_results = embedding_search(query, db, top_k=top_k)

    if not emb_results:
        return kw_results, "keyword"

    if not kw_results:
        # Filter embedding results by category/state/type
        filtered = []
        for r in emb_results:
            record = db.query(Record).filter(Record.id == r.record_id).first()
            if not record:
                continue
            if category and record.category and record.category.lower() != category.lower():
                continue
            if record_type and record.record_type != record_type:
                continue
            if state and record.state_applicability:
                states_lower = [s.lower() for s in record.state_applicability]
                if "all india" not in states_lower and state.lower() not in states_lower:
                    continue
            filtered.append(r)
        return filtered[:top_k], "embedding"

    # Merge: combine scores with reciprocal rank fusion
    record_scores: dict[str, dict[str, Any]] = {}

    for rank, item in enumerate(kw_results):
        rrf_score = 1.0 / (60 + rank)  # RRF constant k=60
        record_scores[item.record_id] = {
            "item": item,
            "score": rrf_score,
        }

    for rank, item in enumerate(emb_results):
        rrf_score = 1.0 / (60 + rank)
        if item.record_id in record_scores:
            record_scores[item.record_id]["score"] += rrf_score
        else:
            record_scores[item.record_id] = {
                "item": item,
                "score": rrf_score,
            }

    # Sort by combined score
    sorted_items = sorted(record_scores.values(), key=lambda x: x["score"], reverse=True)

    results = []
    for entry in sorted_items[:top_k]:
        item = entry["item"]
        item.score = entry["score"]
        results.append(item)

    return results, "hybrid"
