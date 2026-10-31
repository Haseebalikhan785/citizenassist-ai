# CitizenAssist AI: Intelligent Public Service Navigator

> **"Government Services. Simplified for Everyone."**  
> Built for **GRAVITON 2026** (CGC University, Mohali) — **Problem Statement #11**

---

## 🎯 Problem Statement #11
> *"Create a multilingual assistant that helps citizens locate relevant public services, understand eligibility criteria, prepare document checklists, and find official application links."*
> **Required AI techniques:** Retrieval-Augmented Generation (RAG), Multilingual NLP, and Information Extraction.

---

## 💡 The Problem & Social Impact
In India, hundreds of Central and State welfare programs exist to uplift students, farmers, rural families, artisans, and women. Yet, millions of eligible citizens miss out because:
1. **Linguistic Barriers:** Official circulars and application portals are predominantly published in bureaucratic English or high-formal Hindi, inaccessible to everyday vernacular speakers (such as Punjabi or regional dialects).
2. **Criteria Complexity:** Determining whether a family satisfies simultaneous income, caste, landholding, and age criteria requires navigating dense legalese.
3. **Document Insecurity:** Citizens often reach government offices or CSCs only to be turned away for missing one specific certificate (e.g., Tehsildar income certificate or state domicile).
4. **Phishing & Fraud:** Fake websites, unverified blogs, and unscrupulous middlemen exploit confusing portal URLs to siphon off application fees.

**CitizenAssist AI** eliminates these roadblocks through a grounded, transparent, and explainable AI navigator.

---

## 🏛️ Government Data Integrity (Our Highest Priority)
* **Zero Hallucination Policy:** We never invent schemes, grants, income limits, or deadlines.
* **Deterministic Eligibility Engine:** Rules are evaluated using audited, deterministic code (not probabilistic LLM guesswork). Every rule result is linked to an exact quotation from official source documentation.
* **Explicit Badging:** All records are clearly labeled as `demo` or `verified`.
* **Verified Links:** Official URLs point strictly to authentic `.gov.in` and `.nic.in` domains.
* **Non-Affiliation Notice:** CitizenAssist AI is an independent student innovation project created for GRAVITON 2026, not affiliated with or endorsed by the Government of India.

---

## 🧠 AI Architecture: 5-Step Agentic Workflow

```
[ User Natural Query ] (English, Hindi, or Punjabi)
         │
         ▼
[ STEP 1: Understand ] ── Information extraction into structured profile
         │               (Age, State, Income, Occupation, Caste, Gender)
         ▼
[ STEP 2: Retrieve ]   ── Hybrid RAG: SQLite FTS5 (BM25) + Dense Embeddings
         │               (Top matching scheme chunks & metadata)
         ▼
[ STEP 3: Assess ]     ── Deterministic Rule Engine evaluates profile
         │               (Computes MET / NOT_MET status for each scheme)
         ▼
[ STEP 4: Compose ]    ── Grounded LLM Prompt with untrusted data delimiters
         │               (Structured JSON schema via official Google GenAI SDK)
         ▼
[ STEP 5: Validate ]   ── Cross-references citations, downgrades ungrounded claims
         │
         ▼
[ Citizen Response ]   ── Answer in user's language with clickable official links
```

### The Three Required AI Techniques:
1. **Hybrid RAG:**
   - **Offline / Keyword Search:** Powered by SQLite FTS5 virtual tables with BM25 ranking. Guarantees 100% functionality even without an active internet connection or API key.
   - **Dense Semantic Retrieval:** Powered by Google Gemini Embeddings (`gemini-embedding-001`) and in-memory cosine similarity across structured chunk sections (eligibility, benefits, documents, procedure).
2. **Multilingual NLP:**
   - Native interface support for **English**, **Hindi (हिंदी)**, and **Punjabi (ਪੰਜਾਬੀ)**.
   - Dynamic prompt adaptation that allows mixed-language queries while keeping official scheme nomenclature intact.
3. **Information Extraction:**
   - Automated ingestion pipeline that parses official government guidelines from PDFs (`PyMuPDF`) and public HTTPS URLs (`BeautifulSoup` + strict SSRF protection).
   - Generates structured draft records with exact quotation excerpts for human admin approval.

---

## 💻 Tech Stack
* **Frontend:** React 19, TypeScript, Vite, Tailwind CSS v4, Lucide Icons, React Router DOM.
* **Backend:** Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.x, SQLite (WAL mode + FTS5), Uvicorn.
* **AI & NLP:** Official Google GenAI SDK (`google-genai`, `from google import genai`), Argon2-cffi, PyJWT, PyMuPDF.
* **Testing:** Pytest, Pytest-Asyncio, HTTPX, Playwright (66 automated test cases covering auth, security, eligibility boundaries, prompt injection, and live RAG).

---

## ⚡ Quick Start (One Command)

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm

### 1. Setup
Run the setup script for your OS:
```bash
# macOS / Linux:
./setup.sh

# Windows:
setup.bat
```
*This creates the virtual environment, installs all pinned packages, builds the frontend, initializes SQLite, seeds 14 verified schemes/services, and generates random credentials in `LOCAL_CREDENTIALS.txt`.*

### 2. Start Website
```bash
# macOS / Linux:
./start.sh

# Windows:
start.bat
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser!

### 3. Optional: Enable Gemini AI
Add your free Gemini API key to `.env`:
```ini
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Get a free key in 30 seconds at [Google AI Studio](https://aistudio.google.com/apikey). If left empty, the platform automatically runs in Retrieval-Only fallback mode.)*

---

## 🧪 Automated Test Suite
Run the 43 automated unit, integration, and security tests:
```bash
source venv/bin/activate
PYTHONPATH=. pytest backend/tests/ -v
```

Run pre-stage demo safety check:
```bash
python scripts/demo_check.py
```

---

## 📊 SDG Alignment (Team Suggestion)
* **SDG 1 (No Poverty):** Facilitates direct access to DBT financial assistance and health coverage for impoverished households.
* **SDG 10 (Reduced Inequalities):** Democratizes access across linguistic divides through native Hindi and Punjabi navigation.
* **SDG 16 (Peace, Justice, and Strong Institutions):** Provides complete transparency on government criteria and statutory entitlements.
