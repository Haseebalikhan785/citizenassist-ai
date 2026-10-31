# Decisions Log - CitizenAssist AI

## Decision 1: Vector Store
**Decision**: Use SQLite + numpy cosine similarity instead of FAISS/ChromaDB
**Reason**: Corpus is small (<100 records). FAISS/ChromaDB add install complexity (C++ build tools on Windows). SQLite + numpy is sufficient and has prebuilt wheels everywhere.

## Decision 2: Password Hashing
**Decision**: Use argon2-cffi directly (not passlib)
**Reason**: Brief explicitly prohibits passlib. argon2-cffi has prebuilt wheels and is the recommended algorithm.

## Decision 3: JWT Library
**Decision**: Use PyJWT for token signing
**Reason**: Lightweight, widely used, prebuilt wheels. Tokens stored in httpOnly cookies for security.

## Decision 4: PDF Processing
**Decision**: Use PyMuPDF (fitz) for PDF text extraction
**Reason**: Fast, prebuilt wheels available, handles Indian language text well.

## Decision 5: Seed Data Status
**Decision**: All seed data marked as "demo" verification_status
**Reason**: Cannot guarantee real-time verification of government data. All demo data shown with visible DEMO DATA badge. Users directed to official portals for confirmation.

## Decision 6: Tailwind CSS Version
**Decision**: Use Tailwind CSS v4 with the @tailwindcss/vite plugin
**Reason**: Current official docs for Vite recommend v4 with the Vite plugin.

## Decision 7: Embedding Model
**Decision**: Use Gemini text-embedding-004 when API key available, fall back to FTS5-only
**Reason**: Gemini embeddings are multilingual and free tier is generous. sentence-transformers kept as optional flag only.

## Decision 8: Python Compatibility  
**Decision**: Target Python 3.11+ (system has 3.14.6)
**Reason**: Python 3.14 is newest; all chosen packages have wheels. requirements.txt pins versions tested with 3.14.

## Decision 9: Single Process Production
**Decision**: FastAPI serves built frontend static files on port 8000
**Reason**: Simplifies deployment for beginners - one command starts everything. Vite dev proxy used in development.

## Decision 10: Strict Eligibility Rule Approval and Non-blocking Document Rules
**Decision**: Only evaluate rules with `is_approved == True` in the deterministic engine. Records with zero approved rules return `"Insufficient information - eligibility rules not yet extracted"`. Rules of `kind == "document"` are strictly non-blocking.
**Reason**: BUILD_BRIEF.md Section 7 mandates that LLMs may only propose draft rules during ingestion, and admins must review/approve before execution. Documents require physical/procedural verification and must never falsely report a citizen as ineligible.

## Decision 11: Citation Validation and Untrusted Data Delimiters
**Decision**: Post-process assistant claims with a dedicated `validate_citations()` step that strips hallucinated source IDs and downgrades unverified claims to `inferred` or `missing`. Wrap retrieved documents in escaped `<retrieved_document>` tags treated strictly as inert data.
**Reason**: Guarantees zero hallucinations and prevents prompt-injection attacks from overriding deterministic engine findings or inventing welfare claims.

