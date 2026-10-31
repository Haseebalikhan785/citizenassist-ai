# CITIZENASSIST AI: INTELLIGENT PUBLIC SERVICE NAVIGATOR - AUTONOMOUS BUILD BRIEF

You are an autonomous principal full-stack engineer (also AI/RAG engineer, security engineer and designer). Build and deliver a COMPLETE, WORKING website called "CitizenAssist AI: Intelligent Public Service Navigator" for GRAVITON 2026 (CGC University, Mohali), Problem Statement #11.

OFFICIAL PROBLEM STATEMENT (build exactly this): "Create a multilingual assistant that helps citizens locate relevant public services, understand eligibility criteria, prepare document checklists, and find official application links." Required AI techniques: RAG, multilingual NLP, information extraction.
JUDGING emphasizes: impact, AI relevance, originality, feasibility, and demo readiness within 24 hours.
SCOPE RULE: every feature must serve one of the four capabilities (locate services, explain eligibility, prepare document checklists, find official links) or one of the three AI techniques. Cut anything else.

The person who will run this is a COMPLETE BEGINNER. They can only copy-paste a few commands. Therefore: everything must work with minimal steps, errors must be handled gracefully, and you must find and fix your own errors. Never ask me questions; make sensible decisions yourself and record them in docs/DECISIONS.md.

Product: AI-powered public-service navigator WEBSITE for Indian citizens. Tagline: "Government Services. Simplified for Everyone." It helps people discover schemes and services, understand eligibility, prepare documents, and reach official portals, in English, Hindi and Punjabi. Target users: students (scholarships), farmers, low-income families, people unfamiliar with government portals.

This is a WEBSITE (opened in a browser on desktop, tablet and mobile), NOT a native mobile app. It is NOT a mockup or a landing page only. Build a real, fully working website with a frontend, backend, database, authentication, RAG pipeline and AI integration.

======================================================================
## 1. HOW TO WORK (rules for you, the agent)
======================================================================
1. FIRST inspect the environment: OS (Windows/Mac/Linux), Python version, Node version, npm, git. Generate setup/start scripts for the detected OS (and the others if cheap). If Python or Node is missing or too old (check Vite's current Node requirement; Python 3.11 or 3.12 preferred), STOP and tell me in plain language exactly what to install and from which official link. This is the only allowed reason to stop.
2. Work only inside the current workspace folder. Run git init if needed and commit after every phase.
3. Create AGENTS.md in the project root containing sections 1 and 3 of this brief (work rules + data-integrity rules) so they persist if the session resets.
4. Keep docs/PROGRESS.md as a live checklist of milestones and phases. Update it after each phase so work can be resumed.
5. Keep the website runnable after every phase. Run tests after every phase. Never continue on top of failing tests or a failing build.
6. NEVER write package APIs from memory. Check installed versions (pip show, --help, official docs) before using them. Do not invent endpoints or methods.
7. Use the current official Google Gen AI SDK (Python package google-genai, import: from google import genai). Do NOT use the deprecated google-generativeai package. Look up currently available Gemini model names in official docs; put them in env vars GEMINI_MODEL (a fast "flash"-class model) and GEMINI_EMBEDDING_MODEL.
8. Prefer packages with prebuilt wheels that need no C++ build tools (many users are on Windows). After installing, pin exact versions in backend/requirements.txt and commit the frontend lockfile. Verify a clean install works in a fresh virtual environment.
9. Do not claim anything works unless you ran it. Final reporting must be honest, with real test output.
10. TIME MATTERS (the hackathon is 24 hours). Reach Milestone 1 as fast as possible and tag it in git, so a demo-able website always exists. Do not gold-plate early milestones.

======================================================================
## 2. MILESTONES (finish and verify each before starting the next)
======================================================================
MILESTONE 1 - DEMO CORE (git tag milestone-1): setup and start scripts work; seeded verified records (schemes AND services); list/search/filter (category, state, beneficiary type, record type); detail pages with sources and official links; eligibility form with deterministic results; document checklist (printable); English/Hindi/Punjabi interface switcher; the assistant working at least in retrieval-only mode.
MILESTONE 2 - AI CORE (tag milestone-2): grounded Gemini assistant with citations and verified/inferred/missing labels; profile extraction from natural language; hybrid RAG; authentication and persistence (profile, saved items, chat history, checklist progress).
MILESTONE 3 - EXTRACTION AND ADMIN (tag milestone-3): PDF/URL information-extraction pipeline (draft -> admin review -> approve -> publish -> reindex); protected admin panel; comparison of up to 3 schemes; feedback on incorrect information; readiness view; print-friendly summaries.
MILESTONE 4 - POLISH (tag milestone-4): full tests, documentation, demo script, pitch, demo_check script, fresh-install test.
OPTIONAL (only if everything above passes): streaming responses (SSE), voice input using the browser's built-in speech recognition (hi-IN, pa-IN), text-to-speech.

======================================================================
## 3. GOVERNMENT DATA INTEGRITY (highest priority)
======================================================================
- NEVER invent schemes, services, eligibility, benefits, deadlines, documents or URLs.
- Records have record_type: "scheme" (benefit or welfare scheme) or "service" (citizen service such as a certificate, ID document or registration).
- Seed 8-10 real schemes AND 3-4 real citizen services, but ONLY ones whose official pages you actually opened in this session with your browser/fetch tools. Starting points: myscheme.gov.in, scholarships.gov.in, india.gov.in, punjab.gov.in, web.umang.gov.in. Suggested scheme candidates (use only those you can verify): PM-KISAN, Ayushman Bharat PM-JAY, PM Awas Yojana, a National Scholarship Portal scholarship, Sukanya Samriddhi Yojana, Atal Pension Yojana, PM Vishwakarma, plus at least 2 Punjab-specific schemes if verifiable. Suggested service candidates (verify first): income certificate, caste certificate, domicile/residence certificate, ration card, Aadhaar update, DigiLocker.
- For every fact store: value, source_url, a short source excerpt, and fetched_at (real date from the system clock). If the source does not state a field, store null and display "Not stated in source - confirm on the official portal." Never fill gaps from memory.
- Record fields: name, record_type, description, department, central/state, state applicability, target beneficiaries, age/income/education criteria, other conditions, benefits, required documents, application procedure, application URL, official source URL, last_verified_date, source document, verification_status.
- verification_status: "verified" (checked against official source, with excerpt), "draft" (imported, awaiting admin review), "demo" (hand-made sample, shown with a visible DEMO DATA badge, never called verified). Citizens see only verified (and clearly labelled demo) records.
- Documents in a checklist may link to a verified service record that explains where to obtain that document (e.g. income certificate). Only link when such a verified record exists.
- Application URLs only from pages you visited. Write scripts/check_links.py to confirm every stored URL responds; fix or null out failures.
- If a site blocks automated access or needs JavaScript, read it through the browser tool like a human would, respect robots.txt and terms of use, never bulk-crawl. If you cannot verify a record, do not seed it as verified. Provide manual PDF/URL import as the fallback.
- Download one real official PDF during this session into data/documents/ (record its source URL and date) to use for the live extraction demo.
- Write docs/DATA_SOURCES.md listing each record and exactly what was and was not verified.
- Do NOT use the Government of India emblem, Ashoka symbol or any government logo. Footer and About page must say: independent hackathon project, not affiliated with or endorsed by the Government of India; always confirm on the official portal.

======================================================================
## 4. FIXED TECHNOLOGY DECISIONS
======================================================================
Frontend: React + TypeScript + Vite + Tailwind CSS (use the setup method from the CURRENT official Tailwind-for-Vite docs), react-router, lucide-react, Recharts only if actually used. Fonts: Inter plus Noto Sans Devanagari and Noto Sans Gurmukhi (with fallback stacks) so Hindi/Punjabi render correctly.
Backend: Python, FastAPI, Pydantic v2, SQLAlchemy 2.x, SQLite, Uvicorn. Swagger docs enabled. Structured logging that never logs passwords, tokens, API keys or personal data.
Auth: password hashing with argon2-cffi (or bcrypt used directly). Do NOT use passlib. Signed tokens (JWT), preferably in an httpOnly cookie, with the Vite dev proxy so dev and production are same-origin. Roles: citizen and admin.
RAG (hybrid, built behind a swappable VectorStore interface):
 - Keyword retrieval (SQLite FTS5 or BM25) that always works with no API key.
 - Dense retrieval using Gemini embeddings when GEMINI_API_KEY exists; store vectors in SQLite and rank with numpy cosine similarity. Corpus is small, so FAISS/ChromaDB is unnecessary and risks install errors; note this decision in DECISIONS.md.
 - Local sentence-transformers only as an optional flag, off by default. If used, it must be a multilingual model (never an English-only model).
 - Chunk by section (eligibility, benefits, documents, procedure), keep record_id, section and source_url as chunk metadata.
Documents: PyMuPDF for PDFs, BeautifulSoup for permitted public web pages.
Single-process production mode: FastAPI serves the built frontend, so the whole website runs on one port (8000).

======================================================================
## 5. ONE-COMMAND OPERATION (critical)
======================================================================
Create these at the project root:
 - setup (setup.bat and setup.sh): creates venv, installs backend + frontend dependencies, builds the frontend, creates .env from .env.example with a randomly generated SECRET_KEY, initializes the database, seeds records, builds the search index, creates one admin and one demo citizen with RANDOM passwords, writes them to LOCAL_CREDENTIALS.txt (gitignored) and prints them. No credentials in source code.
 - start (start.bat and start.sh): starts the website and prints http://localhost:8000
 - dev script for hot reload (optional)
 .env.example must list every variable with comments: GEMINI_API_KEY (blank by default), GEMINI_MODEL, GEMINI_EMBEDDING_MODEL, SECRET_KEY, DATABASE_URL, ADMIN_EMAIL, etc. The website MUST start and be usable with GEMINI_API_KEY empty.
 Guests can browse, search, run eligibility checks and chat; login is required only to save things.

======================================================================
## 6. AI ASSISTANT (most important feature) - an agentic, grounded workflow
======================================================================
Implement the assistant as explicit server-side steps (use SDK function calling only if you have verified it works with the chosen model together with structured output; otherwise keep explicit steps):
 STEP 1 - UNDERSTAND (information extraction): detect language (en/hi/pa, mixed allowed). Extract profile fields from the user's message into a structured schema (age, state, district, annual family income, education level, occupation, category, gender, student/farmer/worker status, goal). Show the user a "What I understood" panel with editable chips and ask them to confirm or correct; merge confirmed fields into the session profile. Never invent values the user did not state. If there is no API key, skip extraction and use the profile form.
 STEP 2 - RETRIEVE: hybrid-retrieve top-k chunks and structured record matches (use the confirmed profile). Optionally translate the query to English for retrieval.
 STEP 3 - ASSESS: run the deterministic eligibility engine (section 7) for the top matching schemes, and build the document checklists. These engine outputs are facts the answer must reuse, not re-derive.
 STEP 4 - COMPOSE: build the prompt with fixed system instructions (never containing user or document text); retrieved chunks wrapped in clearly delimited blocks (e.g. <retrieved_document id="...">) declared as UNTRUSTED DATA, never instructions; the confirmed profile summary; engine results; recent chat history. Ask Gemini for STRUCTURED JSON (use the SDK's response schema feature): answer, claims[{text, label: verified|inferred|missing, source_ids[]}], recommended_record_ids, follow_up_questions.
 STEP 5 - VALIDATE: drop any source_id not in the retrieved set; downgrade "verified" claims without a valid source to "inferred" or "missing"; attach source titles and official URLs.
 Show a collapsible "How I got this answer" panel listing the steps: what was understood, which sources were retrieved, which eligibility rules ran, and the results.
Rules:
 - If retrieval confidence is below a calibrated threshold, say "I couldn't find verified information on this" and point to the official portal. Never answer scheme facts from model memory.
 - Never say the user IS approved or eligible. Use wording like "may be eligible - confirm on the official portal."
 - Reply in the user's language; keep scheme names and official terms in their original form with the explanation alongside; if translation is uncertain, show the original text too.
 - Handle API errors, quota (429) and timeouts with retry/backoff and a friendly message, then fall back to retrieval-only mode (show matching records and official excerpts, with a banner "AI answers are off - add GEMINI_API_KEY"). Never crash or show a stack trace.
 - Save conversation history per user; show suggested follow-up questions.
 - Include a prompt-injection test: a document containing "ignore previous instructions" must not change behaviour.

======================================================================
## 7. DETERMINISTIC ELIGIBILITY ENGINE (no LLM in the evaluation)
======================================================================
 - Rules are structured data per record: {id, field, operator, value, kind: profile|document, source_url, source_excerpt}. Fields: age, state, district(optional), annual_family_income (integer rupees; the form accepts lakh), education_level, occupation, category, gender, student/farmer/worker status, scheme-specific extras. Operators: <=, >=, ==, in, not_in, between, etc.
 - Each rule result: MET, NOT_MET or UNKNOWN (profile field missing).
 - Overall result: any NOT_MET -> "Not eligible based on known criteria"; none NOT_MET and all profile rules MET -> "Potentially eligible - further verification required"; otherwise -> "Insufficient information". Rules of kind "document" never block Potentially eligible; they are listed as "to be verified at application".
 - If a record has no approved rules, return "Insufficient information - eligibility rules not yet extracted". Never invent thresholds.
 - LLMs may only PROPOSE draft rules during ingestion; an admin must approve them.
 - Show every rule with its result, the source excerpt and the source URL, explained in plain language in the user's chosen language.
 - At least 25 unit tests, including boundary values (income exactly at the limit), missing fields, wrong state, and multiple schemes.

======================================================================
## 8. OTHER FEATURES
======================================================================
Readiness view (on each scheme and in the dashboard's saved list): eligibility status + documents ready (x of y) + missing documents with where to obtain them + the official application link, in one card.
Checklist: documents come from the record only; user marks documents as available; missing ones are highlighted; progress saved per user; export through a print-friendly stylesheet so the user can "Save as PDF" from the browser (this avoids broken Hindi/Punjabi text in JS PDF libraries).
Comparison: up to 3 schemes side by side (benefits, eligibility, income, education, documents, procedure, official links); highlight missing or uncertain fields.
Multilingual: interface strings in en/hi/pa files; switcher persists; fall back to English per missing key. Do not machine-translate stored official text. Translate on demand via the AI with the original shown alongside. Create docs/I18N_REVIEW.md noting that Hindi/Punjabi interface strings are machine-generated and should be reviewed by a native speaker.
Pages: Landing, Dashboard, Scheme/service list and search, Detail, AI Assistant, Eligibility, Checklist, Comparison, Profile, Login/Register, Admin. Landing hero headline: "Government Benefits Shouldn't Be Difficult to Find." Supporting text: "Discover government schemes, understand your eligibility, and get application guidance in your preferred language - all in one place." Primary CTA "Explore Government Schemes", secondary CTA "Ask CitizenAssist". Landing sections: category cards, how it works, features, featured verified records, trust and transparency, footer with official links. Show "Intelligent Public Service Navigator" in the page title, hero or header, and footer. No fake statistics, user counts, partnerships or endorsements.
Categories: Education and Scholarships; Agriculture and Farmers; Healthcare; Employment; Financial Assistance; Women and Child Welfare; Housing; Social Security; Other Citizen Services.
Dashboard: welcome, search, recommended, recently viewed, saved, checklist, assistant shortcut, profile completion, categories.
Design: premium, clean, modern website look; deep navy and royal blue, white and light grey surfaces, restrained green only for positive eligibility states; rounded cards; consistent spacing; no cartoon illustrations; minimal animation. Fully responsive at 360px, 768px and 1280px widths. Keyboard accessible with visible focus, good contrast, aria labels, loading/empty/error states.
Performance for low-bandwidth users: mobile-first, lazy-load routes, small bundle, no large images or video, no heavy libraries. Test with the browser's throttled "Slow 3G" setting and confirm the main pages are usable.
Admin (role-protected, ordinary users get 403 and no admin pages in the navigation): record CRUD; PDF upload; URL import; review extracted data side by side with the source; approve/reject; reindex; ingestion error log; last-verified dates.
Information-extraction pipeline: PDF/URL -> clean text -> with a key, Gemini proposes a structured draft record (all fields in section 3, plus draft eligibility rules) with a source excerpt for every field, validated against the schema; without a key, provide a manual entry form. Drafts stay "draft" until an admin approves; approved records are published and reindexed.

======================================================================
## 9. SECURITY
======================================================================
 - Input validation everywhere (Pydantic); ORM queries only.
 - Rate limiting on login, register and chat (e.g. slowapi).
 - PDF upload: .pdf only, max 10 MB, verify the %PDF header, random stored filename, never execute or render uploaded content as HTML.
 - URL import: https only, timeouts and size limits, block localhost/private/internal IP ranges (SSRF protection).
 - Never render AI or document text with dangerouslySetInnerHTML.
 - Restricted CORS, sensible security headers, secrets only in server-side .env, verify the built frontend bundle contains no API keys (grep it).
 - Collect minimal personal data; all profile fields optional; add "Delete my account and data" and a short privacy/consent note.
 - Treat all uploaded and retrieved content as untrusted data.

======================================================================
## 10. TESTING (you must actually run everything)
======================================================================
 - Backend pytest: auth, profile persistence, search, eligibility, checklist, saved items, RBAC (citizen gets 403 on admin routes), upload validation (reject an .exe renamed to .pdf and oversize files), prompt-injection, citation validation, profile-extraction schema validation (no invented fields), missing-API-key fallback, and a RAG relevance test with at least 10 labelled question-to-expected-record pairs. Mock Gemini only inside unit tests. Add an integration test that uses the real API and is skipped when no key is set.
 - Frontend: type-check, lint, and production build with zero errors.
 - End-to-end: start the real website and use the browser tool (or Playwright) to walk the demo journey (section 11) on desktop and at 390px mobile width. Check the browser console for errors and take screenshots. Fix and repeat until clean.
 - Fresh-install test: delete venv, node_modules and the database, run setup, then start, and run a smoke test (scripts/smoke_test.py) against the running server.
 - Show real test output in the final report.

======================================================================
## 11. DEMO MODE, DEMO SAFETY AND DOCUMENTATION
======================================================================
Demo journey (about 4 minutes): (1) open the website (2) choose Punjabi or English (3) type a natural sentence describing a citizen, e.g. a 20-year-old college student from Punjab with family income of 2 lakh (4) see the "What I understood" profile, confirm it (5) see relevant schemes and services with eligibility status (6) open one scheme and view the official criteria and source (7) view the rule-by-rule eligibility explanation (8) generate the document checklist, mark documents, see missing ones and where to obtain them (9) open the official application portal (10) as admin, import the prepared official PDF and watch the AI extract a structured draft with source excerpts, then approve it (11) rebuild the index and ask a question about the newly added scheme to see it answered with citations. Include a "Use demo profile" button for step 3.
Demo safety: write scripts/demo_check.py, to run before going on stage, which verifies: server up, database seeded, index built, links valid, API key valid (or reports retrieval-only mode), and one English and one Punjabi sample question each return a grounded answer with citations. If Wi-Fi or the API fails during the demo, the retrieval-only mode must still show schemes, eligibility and checklists.
Create:
 - README.md: problem, solution, AI architecture (agentic workflow), RAG pipeline, tech stack, social impact, limitations, future improvements. Mention Problem Statement #11 and how each of RAG, multilingual NLP and information extraction is used.
 - docs/BEGINNER_GUIDE.md: step-by-step with exact commands for my OS; how to get a free Gemini API key from Google AI Studio and where to paste it in .env; how to run the website; how to log in; how to run the demo; troubleshooting for the 10 most likely errors.
 - docs/DEMO_SCRIPT.md: the demo steps with sample inputs in English and Punjabi, expected results, a 2-minute pitch, and a fallback plan (including how to record a backup screen video of the demo).
 - docs/PITCH.md: problem, intended users, solution, the AI techniques used (RAG, multilingual NLP, information extraction, agentic workflow), what makes it different (evidence-labelled answers, rule-level explainable eligibility, readiness view, missing-document guidance), impact, feasibility, limitations, future work. Suggested SDG alignment: SDG 1 (No Poverty), SDG 10 (Reduced Inequalities), SDG 16 (access to information and effective, transparent institutions), with a one-line explanation each and a note that it is the team's own suggestion. Every statistic must come from a source you opened (include the URL) or be omitted.
 - docs/DEPLOYMENT.md: running locally is the primary path. Optional single Docker container and free hosting options for putting the website online, with honest limits (free tiers sleep, the disk may be wiped so SQLite resets, so seed on startup). Do not assume paid services.

======================================================================
## 12. FINAL REPORT (plain language, for a beginner)
======================================================================
Provide: what is implemented and genuinely tested; what was NOT done; which records are verified versus demo or draft; features needing the API key; the exact commands to run (setup, start); the website URL and the login details file; how to run the demo and demo_check; known limitations and next steps. The ONLY things the human does: (1) paste a free Gemini API key into .env, (2) run setup, then start. Everything else is your job.

If time-constrained, prioritize in this order: scheme and service discovery, grounded assistant with profile extraction, eligibility checker, checklist, persistent data, multilingual interface, extraction pipeline and admin, comparison, optional voice.

START NOW. Do not stop after planning. Build, run, test, fix, and deliver the website.
