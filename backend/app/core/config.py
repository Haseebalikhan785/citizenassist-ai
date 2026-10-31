"""
Application configuration loaded from environment variables / .env file.
"""

import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the project root (two levels up from this file)
_project_root = Path(__file__).resolve().parent.parent.parent.parent  # backend/../..
_env_path = _project_root / ".env"
if _env_path.exists():
    load_dotenv(_env_path)

# Also try backend/.env
_backend_env = Path(__file__).resolve().parent.parent.parent / ".env"
if _backend_env.exists():
    load_dotenv(_backend_env, override=True)


class Settings:
    """Application settings with sensible defaults."""

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    GEMINI_EMBEDDING_MODEL: str = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")

    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))

    # SQLite database stored in data/ at project root
    _db_dir = _project_root / "data"
    _db_dir.mkdir(parents=True, exist_ok=True)
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{_db_dir / 'citizenassist.db'}")

    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@citizenassist.local")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "")

    COOKIE_SECURE: bool = os.getenv("COOKIE_SECURE", "false").lower() in ("true", "1", "yes")
    DAILY_AI_CALL_CAP: int = int(os.getenv("DAILY_AI_CALL_CAP", "500"))

    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

    USE_LOCAL_EMBEDDINGS: bool = os.getenv("USE_LOCAL_EMBEDDINGS", "false").lower() in ("true", "1", "yes")

    # CORS origins – restrict in production
    raw_origins = os.getenv("ALLOWED_ORIGINS") or os.getenv("CORS_ORIGINS") or "http://localhost:5173,http://localhost:3000,http://localhost:8000"
    ALLOWED_ORIGINS: list[str] = [o.strip() for o in raw_origins.split(",") if o.strip()]
    CORS_ORIGINS: list[str] = ALLOWED_ORIGINS

    # JWT settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24 hours


settings = Settings()
