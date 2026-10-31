# CitizenAssist AI — 4-Minute Live Hackathon Demo Script

> **Event:** GRAVITON 2026 (CGC University, Mohali)  
> **Problem Statement #11:** Multilingual Assistant for Public Service Discovery, Eligibility Reasoning, and Document Navigation.  
> **Target Audience:** Hackathon Judges and Evaluators.

---

## 🎙️ Part 1: The 2-Minute Pitch (Spoken Before Opening the Website)

> *"Good morning, respected judges. Today in India, hundreds of welfare schemes exist to provide scholarships to students, income support to farmers, and healthcare to families. Yet, over 40% of eligible citizens never receive them. Why?*
> 
> *Because understanding government criteria is like deciphering a legal puzzle. Circulars are in dense bureaucratic English, portals are fragmented, and citizens are routinely turned away at government offices because they didn't know they needed an authorized Tehsildar income certificate.*
> 
> *We built **CitizenAssist AI: Intelligent Public Service Navigator** to solve this exact problem. It is not a generic chatbot. It is a strictly grounded, multilingual public service navigator built around the three required AI techniques:*
> 1. *Hybrid Retrieval-Augmented Generation that works 100% offline with zero hallucination,*
> 2. *Native multilingual NLP in English, Hindi, and Punjabi, and*
> 3. *An audited Information Extraction pipeline that turns complex government PDFs into verified eligibility rules.*
> 
> *Let us walk you through the journey of Rajesh, a 20-year-old student from Punjab."*

---

## 🖥️ Part 2: Step-by-Step Live Demo Journey (3 Minutes)

### Step 1: Multilingual Language Switcher (0:00 - 0:30)
* **Action:** Open `http://localhost:8000`.
* **Action:** Click **ਪੰ** (Punjabi) in the top right language switcher.
* **Talking Point:** *"Notice how instantly the entire interface adapts to Punjabi, including navigational terms, category cards, and headings. We believe public services should speak the citizen's mother tongue."*

---

### Step 2: Grounded Assistant & Natural Language Discovery (0:30 - 1:30)
* **Action:** Click **"AI Assistant"** (AI ਸਹਾਇਕ).
* **Action:** Click the button **"Use Sample Demo Profile"** (or type):
  > *"ਮੈਂ ਪੰਜਾਬ ਤੋਂ 20 ਸਾਲਾ ਐੱਸ.ਸੀ. ਵਿਦਿਆਰਥੀ ਹਾਂ ਅਤੇ ਪਰਿਵਾਰਕ ਆਮਦਨ 2 ਲੱਖ ਹੈ।"*  
  *(English equivalent: "I am a 20-year-old SC student from Punjab with family income of 2 lakh.")*
* **Observation to Show Judges:**
  1. **"What I Understood" Profile Panel:** Show how the system extracted:
     - `Age: 20`
     - `State: Punjab`
     - `Income: ₹2,00,000`
     - `Occupation: Student`
     - `Category: SC`
  2. **Grounded Answer with Citations:** Point out the official citations referencing the **Post-Matric Scholarship for SC Students** and **Punjab Ashirwad Scheme**.
  3. **"How I got this answer" collapsible panel:** Show the 5-step agentic pipeline: Understand → Retrieve → Assess → Compose → Validate.
* **Talking Point:** *"Notice that our AI refuses to hallucinate facts. It does not guess. Every claim is cross-checked against our verified database."*

---

### Step 3: Transparent Deterministic Eligibility Breakdown (1:30 - 2:30)
* **Action:** Navigate to **"Check Eligibility"** or click on the **Post-Matric Scholarship for SC Students** card.
* **Action:** Show the rule-level breakdown:
  - *Income Criterion (<= ₹2,50,000):* **MET** (User: ₹2,00,000) — Citation: *"Income ceiling of parents/guardians is Rs. 2.50 lakh per annum."*
  - *Category Criterion (== SC):* **MET** (User: SC)
  - *Occupation Criterion (== student):* **MET**
* **Talking Point:** *"Notice our core philosophy: we never use probabilistic LLMs to guess whether someone qualifies. We evaluate deterministic rules with boundary checks, and we never say 'You ARE approved'. We say 'Potentially eligible - confirm on the official portal' to maintain civic responsibility."*

---

### Step 4: Document Checklist & Where to Obtain (2:30 - 3:15)
* **Action:** Click **"Document Checklist"**.
* **Action:** Check off *Aadhaar Card* and *Class 10 Marksheet*.
* **Action:** Show the missing document: **"Income Certificate"**.
* **Action:** Click the **"Where to obtain"** badge next to Income Certificate.
* **Observation:** Notice how it routes directly to the verified **"Issuance of Income Certificate"** citizen service explaining the Tehsildar procedure!
* **Action:** Click **"Print / Save as PDF"** to show the print-friendly stylesheet that formats cleanly without font corruption.

---

### Step 5: Admin Document Extraction Pipeline (3:15 - 4:00)
* **Action:** Sign in as Admin (`admin@citizenassist.local`).
* **Action:** Go to the protected `/admin` panel.
* **Action:** Upload the sample government PDF: `data/documents/official_sc_scholarship_guidelines.pdf`.
* **Action:** Show the AI extracting the text via `PyMuPDF`, proposing draft criteria with excerpts, and requiring human approval before publication.
* **Action:** Click **"Approve & Publish"**, then demonstrate that the new scheme is immediately queryable in search and assistant.

---

## 🛡️ Part 3: Fallback & Stage Safety Plan

### Before Going on Stage:
1. Run the automated pre-stage safety check:
   ```bash
   python scripts/demo_check.py
   ```
2. Confirm you see: `STAGE READINESS: 100% READY FOR LIVE DEMO!`

### What if Hackathon Wi-Fi Drops?
* **Zero Panic:** CitizenAssist AI runs locally on port 8000 with a local SQLite FTS5 database and compiled frontend.
* The search, deterministic eligibility engine, document checklists, and retrieval-only chat function **100% offline** without needing internet or an active Gemini key.

### Backup Screen Recording:
* A quick screen recording can be captured using QuickTime on macOS (`Cmd + Shift + 5` -> Record Screen) walking through Steps 1 to 5 as an absolute failsafe.
