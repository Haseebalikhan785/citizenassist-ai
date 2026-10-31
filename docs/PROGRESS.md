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
