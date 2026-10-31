"""
Database initialization and seeding script.
Creates tables, seeds verified records and eligibility rules,
generates random admin and demo citizen credentials,
and saves them to LOCAL_CREDENTIALS.txt.
"""

import os
import secrets
from pathlib import Path

from backend.app.core.config import settings
from backend.app.core.database import Base, SessionLocal, engine
from backend.app.core.security import hash_password
from backend.app.models.database import User
from backend.app.seed import seed_database


def init():
    print("=" * 60)
    print("  Initializing CitizenAssist AI Database...")
    print("=" * 60)

    # 1. Create tables
    Base.metadata.create_all(bind=engine)
    print("[✓] Database tables created")

    db = SessionLocal()
    try:
        # 2. Seed schemes and services
        count = seed_database(db)
        print(f"[✓] Seeded {count} schemes and services with FTS5 search index")

        # 3. Create users
        is_production = os.getenv("PRODUCTION", "").lower() in ("true", "1", "yes") or bool(os.getenv("AWS_EXECUTION_ENV") or os.getenv("KUBERNETES_SERVICE_HOST"))
        admin_email = settings.ADMIN_EMAIL
        admin_pass = settings.ADMIN_PASSWORD

        if admin_pass:
            # Explicit admin password provided via environment variable
            admin = db.query(User).filter(User.email == admin_email.lower().strip()).first()
            if not admin:
                admin = User(
                    email=admin_email.lower().strip(),
                    hashed_password=hash_password(admin_pass),
                    full_name="System Administrator",
                    role="admin",
                    language_preference="en",
                    profile_data={"role": "admin"},
                )
                db.add(admin)
            else:
                admin.hashed_password = hash_password(admin_pass)
            db.commit()
            print("[✓] Admin account configured from environment variables")
        elif is_production:
            print("[i] Admin creation disabled: ADMIN_PASSWORD environment variable not set")

        # Ensure demo citizen account is always available
        demo_citizen_email = "citizen@citizenassist.local"
        demo_citizen_pass = os.getenv("CITIZEN_PASSWORD", "CitizenDemo2026!")
        citizen = db.query(User).filter(User.email == demo_citizen_email).first()
        if not citizen:
            citizen = User(
                email=demo_citizen_email,
                hashed_password=hash_password(demo_citizen_pass),
                full_name="Rajesh Kumar",
                role="citizen",
                language_preference="en",
                profile_data={
                    "age": 20,
                    "state": "Punjab",
                    "annual_family_income": 200000,
                    "occupation": "student",
                    "category": "SC",
                    "gender": "male",
                },
            )
            db.add(citizen)
            db.commit()
            print("[✓] Demo Citizen account created")
        else:
            print("[✓] Demo Citizen account verified")

        if not is_production and not admin_pass:
            # Local development fallback only
            admin_pass = secrets.token_urlsafe(12)
            demo_citizen_email = "citizen@citizenassist.local"
            demo_citizen_pass = secrets.token_urlsafe(12)

            admin = db.query(User).filter(User.email == admin_email).first()
            if not admin:
                admin = User(
                    email=admin_email,
                    hashed_password=hash_password(admin_pass),
                    full_name="System Administrator",
                    role="admin",
                    language_preference="en",
                    profile_data={"role": "admin"},
                )
                db.add(admin)
            else:
                admin.hashed_password = hash_password(admin_pass)

            citizen = db.query(User).filter(User.email == demo_citizen_email).first()
            if not citizen:
                citizen = User(
                    email=demo_citizen_email,
                    hashed_password=hash_password(demo_citizen_pass),
                    full_name="Rajesh Kumar",
                    role="citizen",
                    language_preference="en",
                    profile_data={
                        "age": 20,
                        "state": "Punjab",
                        "annual_family_income": 200000,
                        "occupation": "student",
                        "category": "SC",
                        "gender": "male",
                    },
                )
                db.add(citizen)
            else:
                citizen.hashed_password = hash_password(demo_citizen_pass)

            db.commit()
            print("[✓] Local development accounts created")

            root_dir = Path(__file__).resolve().parent.parent.parent
            creds_file = root_dir / "LOCAL_CREDENTIALS.txt"
            creds_text = f"""============================================================
  CITIZENASSIST AI - LOCAL CREDENTIALS
============================================================

ADMIN ACCOUNT:
  Email:    {admin_email}
  Password: {admin_pass}
  Role:     admin

DEMO CITIZEN ACCOUNT:
  Email:    {demo_citizen_email}
  Password: {demo_citizen_pass}
  Role:     citizen
  Sample Profile: 20yo SC student from Punjab, Income ₹2,00,000

NOTE: This file is automatically generated and gitignored.
Keep these credentials safe for hackathon testing and demo.
============================================================
"""
            with open(creds_file, "w", encoding="utf-8") as f:
                f.write(creds_text)
            print(f"[✓] Credentials saved to: {creds_file}")

    finally:
        db.close()


if __name__ == "__main__":
    init()
