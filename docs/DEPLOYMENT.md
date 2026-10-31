# CitizenAssist AI — Deployment & Hosting Guide

CitizenAssist AI is architected with a **single-process production mode** where FastAPI serves both the REST API and the compiled React TypeScript static build from port `8000`.

---

## 🖥️ Primary Path: Local Deployment (Recommended for Hackathons)

The primary and most robust way to run CitizenAssist AI is locally on your computer:
1. Run `./setup.sh` (or `setup.bat` on Windows).
2. Run `./start.sh` (or `start.bat` on Windows).
3. Access at **`http://localhost:8000`**.

This provides instantaneous response times, zero latency, and 100% offline functionality.

---

## 🐳 Option 2: Single Docker Container

If you want to package CitizenAssist AI into a single portable container:

### `Dockerfile`
```dockerfile
# Build frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Build backend and final runtime
FROM python:3.11-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install backend dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend application
COPY backend/ ./backend/
COPY docs/ ./docs/
COPY scripts/ ./scripts/
COPY .env.example ./.env

# Copy built frontend assets from stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose port 8000
EXPOSE 8000

# Seed database on container start and run uvicorn
CMD ["sh", "-c", "python -m backend.app.init_db && python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"]
```

### Build and Run:
```bash
docker build -t citizenassist-ai .
docker run -p 8000:8000 citizenassist-ai
```

---

## ☁️ Option 3: Free Cloud Hosting (Render / Railway / Hugging Face Spaces)

CitizenAssist AI can be deployed to free cloud container tiers (such as Render Web Services, Railway, or Hugging Face Spaces).

### ⚠️ Honest Limits of Free Tier Cloud Hosting:
1. **Ephemeral Disk Storage:** On free hosting tiers (e.g. Render free tier), the container filesystem is ephemeral. If the service restarts or sleeps due to inactivity, local SQLite changes reset.
   * *Mitigation implemented in CitizenAssist AI:* The application automatically verifies and seeds the database on startup (`python -m backend.app.init_db`), ensuring verified government records are never lost.
2. **Cold Starts / Spin-Down:** Free tier instances sleep after 15 minutes of inactivity and take 30–50 seconds to boot on first request.
3. **Memory Limits:** Free instances are typically restricted to 512MB RAM. CitizenAssist AI uses SQLite and lightweight Python libraries to fit comfortably within these constraints.
