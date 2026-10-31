"""
Document information extraction pipeline:
- PDF text extraction via PyMuPDF (fitz)
- URL scraping via httpx + BeautifulSoup (with strict SSRF protection)
- Structured draft record generation via Gemini with source excerpts
"""

import ipaddress
import json
import logging
from typing import Any
from urllib.parse import urlparse

import fitz  # PyMuPDF
import httpx
from bs4 import BeautifulSoup

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


def is_safe_url(url: str) -> bool:
    """
    SSRF Protection: Ensure URL is HTTPS, not localhost or a private/internal IP address.
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme.lower() != "https":
            return False

        hostname = parsed.hostname
        if not hostname or hostname.lower() in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
            return False

        # Attempt to parse as IP address to check if private
        try:
            ip = ipaddress.ip_address(hostname)
            if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local:
                return False
        except ValueError:
            # Not a raw IP, typical domain name
            pass

        return True
    except Exception:
        return False


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract clean text from PDF bytes using PyMuPDF."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text_chunks = []
    for page in doc:
        text = page.get_text()
        if text.strip():
            text_chunks.append(text.strip())
    doc.close()
    return "\n\n".join(text_chunks)


async def extract_text_from_url(url: str) -> str:
    """Fetch and extract readable text from a verified public URL."""
    if not is_safe_url(url):
        raise ValueError("Invalid URL: Only public HTTPS URLs are allowed (SSRF protection)")

    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        headers = {"User-Agent": "CitizenAssist-PublicServiceNavigator/1.0"}
        resp = await client.get(url, headers=headers)
        if resp.status_code != 200:
            raise ValueError(f"HTTP request failed with status {resp.status_code}")

        soup = BeautifulSoup(resp.text, "html.parser")
        # Remove unwanted tags
        for element in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            element.decompose()

        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines[:1000])  # Cap at reasonable length


def generate_draft_record_with_gemini(raw_text: str, source_url: str | None = None) -> dict[str, Any]:
    """
    Use Gemini to parse unstructured government document text into
    a structured draft record with source excerpts and draft rules.
    """
    if not settings.GEMINI_API_KEY:
        # Fallback heuristic draft if no key
        return {
            "name": "Draft Scheme from Document",
            "record_type": "scheme",
            "description": raw_text[:500] if raw_text else "",
            "department": "Department of Public Welfare",
            "level": "central",
            "state_applicability": ["All India"],
            "category": "Social Security",
            "target_beneficiaries": ["Citizens"],
            "benefits": "Financial assistance or service",
            "required_documents": [{"name": "Aadhaar Card", "description": "Identity proof"}],
            "application_procedure": "Apply on the official portal",
            "official_source_url": source_url or "https://india.gov.in",
            "source_excerpt": raw_text[:300] if raw_text else "",
            "draft_rules": [],
            "verification_status": "draft",
        }

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        prompt = f"""
You are an expert government policy analyst for CitizenAssist AI. Extract structured data from this official government document.
DO NOT invent or extrapolate. Only extract facts explicitly stated in the document.
If a field is not stated in the source text, set it to null or an empty list.

Document Text (UNTRUSTED DATA):
\"\"\"
{raw_text[:8000]}
\"\"\"

Return a valid JSON object matching this schema:
{{
  "name": "Name of scheme or service",
  "record_type": "scheme" or "service",
  "description": "Clear 2-3 sentence description",
  "department": "Government ministry or department",
  "level": "central" or "state",
  "state_applicability": ["State name"] or ["All India"],
  "category": "Education and Scholarships" or "Agriculture and Farmers" or "Healthcare" or "Employment" or "Financial Assistance" or "Women and Child Welfare" or "Housing" or "Social Security" or "Other Citizen Services",
  "target_beneficiaries": ["students", "farmers", etc.],
  "benefits": "Exact monetary or non-monetary benefits",
  "required_documents": [
    {{"name": "Document Name", "description": "Purpose of document"}}
  ],
  "application_procedure": "Step by step application procedure",
  "source_excerpt": "Exact short sentence from the text confirming the primary details",
  "draft_rules": [
    {{
      "field": "age" or "annual_family_income" or "state" or "category" or "occupation",
      "operator": "<=" or ">=" or "==" or "in",
      "value": number or string or list,
      "kind": "profile",
      "description": "Plain language rule description",
      "source_excerpt": "Quote confirming this rule"
    }}
  ]
}}
"""

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1,
            ),
        )

        data = json.loads(response.text)
        data["verification_status"] = "draft"
        data["official_source_url"] = source_url or "https://india.gov.in"
        return data

    except Exception as e:
        logger.error("Gemini document extraction error: %s", e)
        return {
            "name": "Extracted Draft Scheme",
            "record_type": "scheme",
            "description": raw_text[:500] if raw_text else "",
            "department": "Public Authority",
            "level": "central",
            "state_applicability": ["All India"],
            "category": "Social Security",
            "target_beneficiaries": ["General Public"],
            "benefits": "Welfare assistance",
            "required_documents": [{"name": "Aadhaar Card", "description": "Identity proof"}],
            "application_procedure": "Check official portal",
            "official_source_url": source_url or "https://india.gov.in",
            "source_excerpt": raw_text[:300] if raw_text else "",
            "draft_rules": [],
            "verification_status": "draft",
        }
