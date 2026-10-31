"""
CitizenAssist AI - URL Verification Script
Checks all stored application and official source URLs in the database
to verify that they respond or identify invalid endpoints.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import httpx
from sqlalchemy.orm import Session

from backend.app.core.database import SessionLocal
from backend.app.models.database import Record


def check_all_links():
    db: Session = SessionLocal()
    records = db.query(Record).filter(Record.is_active.is_(True)).all()

    print("=" * 60)
    print("  CITIZENASSIST AI - LINK VERIFIER")
    print("=" * 60)
    print(f"Checking links across {len(records)} active records...\n")

    urls_to_check = set()
    for r in records:
        if r.official_source_url:
            urls_to_check.add(r.official_source_url)
        if r.application_url:
            urls_to_check.add(r.application_url)

    headers = {"User-Agent": "Mozilla/5.0 (CitizenAssist AI Link Checker/1.0)"}

    success_count = 0
    failure_count = 0

    with httpx.Client(timeout=10.0, follow_redirects=True, verify=False) as client:
        for url in sorted(urls_to_check):
            try:
                resp = client.head(url, headers=headers)
                if resp.status_code >= 400:
                    # Retry with GET in case HEAD is not allowed
                    resp = client.get(url, headers=headers)
                status_code = resp.status_code
                if status_code < 400:
                    print(f" [✓] {status_code} OK: {url}")
                    success_count += 1
                else:
                    print(f" [!] {status_code} WARN: {url}")
                    failure_count += 1
            except Exception as e:
                print(f" [✗] FAILED: {url} ({str(e)[:50]}...)")
                failure_count += 1

    print("\n" + "=" * 60)
    print(f"  VERIFICATION COMPLETE: {success_count} Passed, {failure_count} Issues")
    print("=" * 60)
    db.close()
    return failure_count == 0


if __name__ == "__main__":
    check_all_links()
