# Progress Tracker - CitizenAssist AI

## Environment
- **OS**: macOS ARM64 (Darwin 27.0.0)
- **Python**: 3.14.6
- **Node**: 26.13.0
- **npm**: 11.20.0

## Milestone 1 - DEMO CORE (git tag: milestone-1)
- [x] Environment inspection (macOS, Python 3.14, Node 26, npm 11)
- [x] Project structure created
- [x] Brief saved word-for-word to `docs/BUILD_BRIEF.md`
- [x] `AGENTS.md` created with Section 1 and Section 3
- [x] Backend: models, database, API routes
- [x] Backend: seeded verified records (10 schemes + 4 citizen services)
- [x] Backend: deterministic eligibility engine (MET/NOT_MET/UNKNOWN)
- [x] Backend: SQLite FTS5 keyword search
- [x] Backend: auth (Argon2-cffi + PyJWT in httpOnly cookies)
- [x] Frontend: Vite + React 19 + Tailwind CSS setup
- [x] Frontend: i18n (en/hi/pa) persistent switcher
- [x] Frontend: landing page matching required headline & copy
- [x] Frontend: scheme/service list + search & multi-facet filters
- [x] Frontend: detail pages with source excerpts & official links
- [x] Frontend: deterministic eligibility form with lakhs support
- [x] Frontend: document checklist with print-friendly stylesheet
- [x] Frontend: AI assistant with Retrieval-Only fallback mode
- [x] Setup & start scripts (`setup.sh`, `start.sh`, `setup.bat`, `start.bat`)
- [x] Tests pass (43 automated unit, integration, and security tests)

## Milestone 2 - AI CORE (git tag: milestone-2)
- [x] Grounded Gemini assistant with citations and evidence labels (verified/inferred/missing)
- [x] Profile extraction from natural language (age, state, income, caste, occupation)
- [x] "What I understood" profile panel with editable chips
- [x] Hybrid RAG (FTS5 + dense vector embeddings)
- [x] Auth persistence (profile, saved items, chat history, checklist progress)

## Milestone 3 - EXTRACTION AND ADMIN (git tag: milestone-3)
- [x] PDF information-extraction pipeline via PyMuPDF
- [x] URL import pipeline with strict SSRF protection (HTTPS only, private IP blocking)
- [x] Protected admin panel with role-based access control (403 for citizens)
- [x] Supervised draft review -> approve & publish -> instant FTS5 reindexing
- [x] Side-by-side comparison of up to 3 schemes
- [x] Feedback reporting for incorrect data or broken links
- [x] Readiness view on scheme details & user dashboard
- [x] Print-friendly document checklist export

## Milestone 4 - POLISH (git tag: milestone-4)
- [x] Full pytest suite (43 tests, 25+ eligibility tests including boundaries, 10 RAG benchmark queries)
- [x] Prompt-injection immunity test
- [x] Official sample PDF downloaded in `data/documents/`
- [x] Documentation complete (`README.md`, `BEGINNER_GUIDE.md`, `DEMO_SCRIPT.md`, `PITCH.md`, `DEPLOYMENT.md`, `DATA_SOURCES.md`, `DECISIONS.md`, `I18N_REVIEW.md`)
- [x] `scripts/smoke_test.py` verified against running server
- [x] `scripts/demo_check.py` verified 100% stage-ready in English and Punjabi
- [x] Fresh-install readiness verified

## Milestone 5 - AUDIT & REINFORCEMENT (Sections 6 & 7 Compliance)
- [x] **Section 7 Eligibility Engine Rules Logic**:
  - Filtered query strictly to `is_approved.is_(True)` to isolate draft/unapproved rules
  - Records with zero approved rules return exact brief requirement: `"Insufficient information - eligibility rules not yet extracted"`
  - Overall status evaluation strictly conforms: any NOT_MET -> `"Not eligible based on known criteria"`, none NOT_MET and all MET -> `"Potentially eligible - further verification required"`, otherwise -> `"Insufficient information"`
  - `kind="document"` rules non-blocking: never block eligibility; flagged as `"to be verified at application"`
  - `RuleResult` schema enriched with `kind`, `source_url`, and `source_excerpt`
  - Multi-format number and lakh string parser supporting `"2.5 lakh"`, `"₹2,50,000"`, `"200000"`
  - Expanded unit test suite to 32 tests covering boundaries, missing fields, lakh strings, document rules, and zero-approved-rule isolation
- [x] **Section 6 AI Assistant Citation Checking & Prompt-Injection Defense**:
  - Grounded claims schema (`label: verified|inferred|missing`, `source_ids[]`, `source_title`, `source_url`)
  - Dedicated citation validator `validate_citations()`: filters out hallucinated doc IDs and downgrades unbacked verified claims to `inferred` or `missing`
  - Anti-injection tag escaping: sanitizes `</retrieved_document>` and untrusted user input
  - Strict system prompt declaring all retrieved documents and user queries as inert UNTRUSTED DATA
  - Low-confidence retrieval threshold fallback preventing model hallucination for unindexed queries
  - Automatic grounded wording enforcement substituting absolute approvals with `"may be eligible (confirm on the official portal)"`
  - Multilingual profile extraction for English, Hindi (Devanagari), and Punjabi (Gurmukhi) without ASCII `\b` word boundary failures
  - Schema validation guaranteeing zero hallucinated fields outside `ALLOWED_PROFILE_FIELDS`
- [x] **Verification**:
  - 66 of 66 backend pytest tests passing (100% pass rate, including live Gemini API integration)
  - Frontend TypeScript build: 0 errors (`npm run build`)
  - Playwright E2E browser demo journey: 13/13 steps passed, 0 page errors, 0 console errors (Desktop 1280x800 and Mobile 390px iPhone width)
  - `scripts/smoke_test.py`: 100% pass
  - `scripts/demo_check.py`: 100% stage-ready in English and Punjabi (Gemini AI active)
  - `scripts/check_links.py`: 11 of 12 government portals verified with 200 OK
