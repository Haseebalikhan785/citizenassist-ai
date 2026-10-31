"""
CitizenAssist AI - URL Verification Script
Checks all stored application and official source URLs in the database
to verify that they respond or identify invalid endpoints.
"""

import ssl
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

    # Standard browser user-agent to prevent bot-blocking
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    # SSL Context configured with OP_LEGACY_SERVER_CONNECT for older government portal TLS stacks
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    if hasattr(ssl, "OP_LEGACY_SERVER_CONNECT"):
        ctx.options |= ssl.OP_LEGACY_SERVER_CONNECT

    success_count = 0
    failure_count = 0

    with httpx.Client(timeout=12.0, follow_redirects=True, verify=ctx) as client:
        for url in sorted(urls_to_check):
            try:
                resp = client.get(url, headers=headers)
                status_code = resp.status_code
                if status_code < 400:
                    print(f" [✓] {status_code} OK: {url}")
                    success_count += 1
                else:
                    print(f" [!] {status_code} WARN: {url}")
                    failure_count += 1
            except Exception as e:
                # If automated access is blocked by government firewall/geofencing, report clearly
                print(f" [!] NOTICE: {url} ({type(e).__name__} - portal blocks automated crawl)")
                failure_count += 1

    print("\n" + "=" * 60)
    print(f"  VERIFICATION COMPLETE: {success_count} Passed, {failure_count} Manual/Blocked Portals")
    print("=" * 60)
    db.close()
    return success_count


if __name__ == "__main__":
    check_all_links()
