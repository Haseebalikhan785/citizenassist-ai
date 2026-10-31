"""
CitizenAssist AI - Main FastAPI Application
Serves the full-stack website: backend REST APIs and compiled frontend SPA.
"""

import logging
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware

from backend.app.core.config import settings
from backend.app.core.database import Base, engine
from backend.app.routers import (
    admin,
    assistant,
    auth,
    checklist,
    eligibility,
    feedback,
    profile,
    records,
    saved,
    search,
)

# Setup logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("citizenassist")

# Rate Limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])

app = FastAPI(
    title="CitizenAssist AI",
    description="Intelligent Public Service Navigator API - Problem Statement #11",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response


app.add_middleware(SecurityHeadersMiddleware)


# Startup Event: Create tables if not existing
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified on startup")


# Register API Routers
app.include_router(auth.router)
app.include_router(records.router)
app.include_router(eligibility.router)
app.include_router(search.router)
app.include_router(assistant.router)
app.include_router(checklist.router)
app.include_router(saved.router)
app.include_router(profile.router)
app.include_router(feedback.router)
app.include_router(admin.router)


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": "CitizenAssist AI",
        "tagline": "Government Services. Simplified for Everyone.",
        "ai_enabled": bool(settings.GEMINI_API_KEY),
    }


# Serve Frontend in Production
frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists() and (frontend_dist / "index.html").exists():
    app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Do not intercept API routes
        if full_path.startswith("api"):
            return FileResponse(frontend_dist / "index.html")
        requested_file = frontend_dist / full_path
        if requested_file.is_file():
            return FileResponse(requested_file)
        return FileResponse(frontend_dist / "index.html")
else:
    @app.get("/")
    def root():
        return {
            "message": "CitizenAssist AI Backend API is running.",
            "docs": "/api/docs",
            "health": "/api/health",
            "note": "Frontend not yet built. Run 'npm run build' inside frontend/ to serve the SPA.",
        }
