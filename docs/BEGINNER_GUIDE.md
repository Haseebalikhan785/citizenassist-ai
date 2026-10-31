# CitizenAssist AI — Complete Beginner's Guide (macOS / Linux / Windows)

Welcome to **CitizenAssist AI**! This guide is written specifically for complete beginners. You do not need deep programming knowledge to run, test, and demo this website.

---

## 🔑 Step 1: Getting a Free Gemini API Key (Optional but Recommended)
The website works **100% offline in Retrieval-Only mode** even without an API key. However, to enable natural language conversations and automatic AI profile extraction:

1. Visit [Google AI Studio](https://aistudio.google.com/apikey) in your web browser.
2. Sign in with any free Google / Gmail account.
3. Click **"Create API Key"** and copy the generated key string (e.g. `AIzaSy...`).
4. In your project directory, open the `.env` file in any text editor.
5. Paste your key on the `GEMINI_API_KEY=` line:
   ```ini
   GEMINI_API_KEY=AIzaSyYourGeneratedKeyHere
   ```
6. Save and close the file.

---

## 🚀 Step 2: One-Command Setup

Open your Terminal (macOS/Linux) or Command Prompt (Windows) inside the `Graviton Project` folder and run:

### On macOS / Linux:
```bash
./setup.sh
```

### On Windows:
```cmd
setup.bat
```

### What this script automatically does:
1. Verifies that Python 3.11+ and Node.js are installed.
2. Creates a Python virtual environment (`venv/`).
3. Installs all required Python dependencies with prebuilt wheels.
4. Installs frontend npm packages and compiles the production bundle into `frontend/dist/`.
5. Creates a secure `.env` file with a cryptographically random `SECRET_KEY`.
6. Initializes the SQLite database and seeds 14 verified government welfare schemes and citizen services.
7. Builds the SQLite FTS5 search index.
8. Creates an **Admin** user and a **Demo Citizen** user with random secure passwords and writes them to `LOCAL_CREDENTIALS.txt`.

---

## 🌐 Step 3: Starting the Website

### On macOS / Linux:
```bash
./start.sh
```

### On Windows:
```cmd
start.bat
```

Now open your web browser and go to:
👉 **[http://localhost:8000](http://localhost:8000)**

---

## 👤 Step 4: Logging In & Finding Credentials

All generated passwords are saved in the project root in `LOCAL_CREDENTIALS.txt` (which is gitignored for security).

Open that file to find your logins:
```bash
cat LOCAL_CREDENTIALS.txt
```

* **Administrator:** Use the admin email (`admin@citizenassist.local`) and generated password to access the protected `/admin` panel to upload official PDFs or import URLs.
* **Citizen:** Use the demo citizen account (`citizen@citizenassist.local`) to access your personal dashboard, saved schemes, and document checklists.

---

## 🎬 Step 5: Running the 4-Minute Hackathon Demo

1. **Open the Website:** Go to `http://localhost:8000`.
2. **Switch Language:** Click **ਪੰ** (Punjabi) or **हिं** (Hindi) in the top navigation bar. Notice how the whole interface switches into the local language.
3. **Ask the AI Assistant:**
   - Click **"AI Assistant"** in the top navigation bar.
   - Click the blue **"Use Sample Demo Profile"** button (or type: *"I am a 20-year-old SC student from Punjab with a family income of 2 lakh. What schemes can I apply for?"*).
   - See the **"What I Understood"** profile chips appear (Age: 20, State: Punjab, Income: ₹2,00,000, Category: SC).
   - Observe the grounded answer citing **Post-Matric Scholarship for SC Students** with direct links to official government portals.
4. **Inspect Scheme Details:**
   - Click on the **Post-Matric Scholarship for SC Students** card.
   - Show the official criteria, benefits, and the verified source excerpt from the National Scholarship Portal.
5. **Evaluate Deterministic Eligibility:**
   - Click **"Check My Eligibility"**.
   - Show the rule-by-rule breakdown: income check (`MET`), age check (`MET`), category check (`MET`).
   - Notice the transparent indicator: *"Potentially eligible - further verification required on the official portal."*
6. **Prepare Document Checklist:**
   - Click **"Document Checklist"**.
   - Check off documents you have. Missing documents highlight the exact revenue office to obtain them (e.g. Caste & Income Certificate linked to Tehsildar service).
   - Click **"Print / Save as PDF"** to demonstrate the clean print stylesheet.
7. **Demonstrate Supervised Document Ingestion (Admin):**
   - Log in as Admin.
   - Go to `/admin`.
   - Upload the pre-downloaded official government guideline PDF located at `data/documents/official_sc_scholarship_guidelines.pdf`.
   - Watch the pipeline extract text and propose a structured draft with quotations.
   - Click **"Approve & Publish"** to demonstrate instant reindexing.

---

## 🛠️ Step 6: Troubleshooting the 10 Most Common Issues

### 1. `Permission denied: ./setup.sh`
**Fix:** Run `chmod +x setup.sh start.sh` in Terminal to make them executable.

### 2. `Address already in use: port 8000`
**Fix:** Another process is running on port 8000. Stop it with:
```bash
lsof -ti:8000 | xargs kill -9
```

### 3. `ModuleNotFoundError: No module named 'backend'`
**Fix:** Run commands with `PYTHONPATH=.`:
```bash
source venv/bin/activate
PYTHONPATH=. python -m backend.app.main
```

### 4. `GEMINI_API_KEY is not working or Quota Exceeded (429)`
**Fix:** The application will automatically and gracefully fall back to **Retrieval-Only Mode**! It will continue showing verified schemes, eligibility rules, and checklists without crashing.

### 5. `Database is locked or not found`
**Fix:** Reinitialize the database cleanly:
```bash
source venv/bin/activate
python -m backend.app.init_db
```

### 6. `Frontend shows blank page or 404`
**Fix:** Rebuild the frontend bundle:
```bash
cd frontend && npm run build && cd ..
```

### 7. `Node.js is missing or too old`
**Fix:** Download and install Node.js LTS (version 20 or higher) from [https://nodejs.org/](https://nodejs.org/).

### 8. `Python 3 is missing or too old`
**Fix:** Download and install Python 3.11 or higher from [https://www.python.org/downloads/](https://www.python.org/downloads/).

### 9. `Lost Admin / Demo Passwords`
**Fix:** Look inside `LOCAL_CREDENTIALS.txt` in the root folder, or re-run `python -m backend.app.init_db` to generate new passwords.

### 10. `Pre-Stage Health Verification`
**Fix:** Before presenting to judges, run:
```bash
python scripts/demo_check.py
```
If it prints `STAGE READINESS: 100% READY FOR LIVE DEMO!`, you are completely safe to present.
