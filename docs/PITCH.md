# CitizenAssist AI — Complete Hackathon Pitch & Defense Document

> **GRAVITON 2026** • CGC University, Mohali  
> **Problem Statement #11:** Multilingual Assistant for Public Service Discovery, Eligibility Reasoning, Document Preparation, and Application Navigation.

---

## 1. Executive Summary
**CitizenAssist AI** is an intelligent public-service navigator that dismantles the bureaucratic, linguistic, and informational barriers separating Indian citizens from their rightful government welfare entitlements.

By orchestrating **Hybrid RAG**, **Multilingual NLP (English, Hindi, Punjabi)**, and an audited **Information Extraction pipeline**, CitizenAssist AI transforms dense official policy circulars into transparent eligibility evaluations, actionable document checklists, and verified application portals.

---

## 2. The Target Citizens
1. **Students & Youth:** Seeking higher education scholarships, tuition fee concessions, and skill development grants (e.g. Post-Matric SC Scholarship).
2. **Farmers & Landholders:** Small and marginal agricultural families navigating income support and crop assistance (e.g. PM-KISAN).
3. **Low-Income & Rural Households:** Families in need of subsidized housing, clean cooking energy, and catastrophic health cover (e.g. PMAY-U, PM-JAY, PMUY).
4. **Traditional Artisans & Craftspeople:** Self-employed carpenters, blacksmiths, and artisans seeking low-interest capital and modern toolkits (e.g. PM Vishwakarma).
5. **Non-English Vernacular Speakers:** Citizens who speak primarily Hindi or Punjabi and cannot decipher complex government documentation.

---

## 3. Four Core Capabilities Built Exactly to PS #11

| PS #11 Requirement | How CitizenAssist AI Implements It |
| :--- | :--- |
| **1. Locate Public Services** | Multi-faceted catalog of 14 verified schemes and citizen services filterable by state, category, and beneficiary. |
| **2. Understand Eligibility** | Deterministic, audited rule engine with boundary checking. Shows rule-by-rule status (`MET`/`NOT_MET`) with exact quotations from official circulars. |
| **3. Prepare Document Checklists** | Interactive, printable checklists with cross-links to citizen services explaining *where and how* to obtain missing certificates. |
| **4. Find Official Application Links** | Curated official `.gov.in` and `.nic.in` portal links verified by automated link verification scripts. |

---

## 4. The Three Required AI Techniques

### A. Retrieval-Augmented Generation (Hybrid RAG)
* **Keyword Tier (100% Offline):** SQLite FTS5 with BM25 ranking across structured chunk sections (eligibility, benefits, documents, application procedure). Runs instantly even with zero internet or missing API key.
* **Semantic Tier (Dense Retrieval):** Multilingual embeddings via Google Gemini `text-embedding-004` and in-memory cosine similarity.
* **Reciprocal Rank Fusion (RRF):** Combines keyword and semantic scores to retrieve the most pertinent policy chunks without hallucination.

### B. Multilingual Natural Language Processing (NLP)
* Native localization across interface, headings, and assistance in **English**, **Hindi (हिंदी)**, and **Punjabi (ਪੰਜਾਬੀ)**.
* Allows mixed-language vernacular queries (e.g., *"ਮੈਂ 20 ਸਾਲ ਦਾ ਵਿਦਿਆਰਥੀ ਹਾਂ"* or *"मेरी आय 2 लाख है"*).
* Preserves official legal scheme names in their native title while explaining benefits clearly.

### C. Information Extraction Pipeline
* Supervised administrative ingestion of official government PDF guidelines (`PyMuPDF`) and public HTTPS portals (`BeautifulSoup` + SSRF defense).
* AI extracts structured criteria, benefit caps, and required documents with mandatory verbatim excerpts for human admin verification prior to public indexing.

---

## 5. What Makes CitizenAssist AI Truly Different

1. **Evidence-Labeled Answers:** We never state a fact without a verified source citation. Claims are explicitly tagged as `verified` from official documentation.
2. **Deterministic, Explainable Eligibility:** Generative models are probabilistic and known to hallucinate numerical boundaries. We decouple reasoning from generation: our deterministic engine calculates eligibility math, and the LLM merely translates and communicates the result.
3. **No False Approvals:** The platform strictly adheres to ethical civic wording: *"Potentially eligible - further verification required on the official portal."* We never mislead citizens into believing an AI has granted them government approval.
4. **Missing Document Routing:** Rather than merely telling a citizen they need an *Income Certificate*, the platform links directly to the revenue service record showing how to apply at their local Tehsil or Sewa Kendra.
5. **Single-Process Lightweight Architecture:** FastAPI serves the compiled React single-page application on one single port (`http://localhost:8000`). Zero complex multi-container setup required for evaluators.

---

## 6. Sustainable Development Goals (SDG) Alignment
*(Team's own proposed alignment):*
* **SDG 1 (No Poverty):** Facilitates direct benefit delivery to economically disadvantaged families.
* **SDG 10 (Reduced Inequalities):** Eradicates linguistic discrimination by providing equal access in regional Indian languages.
* **SDG 16 (Peace, Justice, and Strong Institutions):** Ensures transparency, accountability, and public access to statutory government criteria.

---

## 7. Limitations & Honest Future Work
* **Current Limitation:** Seeded with 14 verified central and state welfare programs. Scaling to all 3,000+ national and state schemes requires ongoing administrative crawler ingestion.
* **Current Limitation:** Punjabi/Hindi interface strings were machine-generated and should undergo complete native speaker verification (documented in `docs/I18N_REVIEW.md`).
* **Future Roadmap:** Direct Digilocker API integration to automatically verify existing citizen documents, and voice-to-voice interaction using Web Speech API for illiterate citizens.
