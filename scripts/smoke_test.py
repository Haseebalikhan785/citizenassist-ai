"""
Smoke test script for CitizenAssist AI.
Checks that all endpoints respond properly on the running server at http://localhost:8000.
"""

import sys
import httpx

BASE_URL = "http://127.0.0.1:8000"


def run_smoke_test():
    print("=" * 60)
    print(f"  CitizenAssist AI - Smoke Test against {BASE_URL}")
    print("=" * 60)

    endpoints = [
        ("GET", "/", "Frontend Single Page Application"),
        ("GET", "/api/health", "Health Check"),
        ("GET", "/api/records", "Records List API"),
        ("GET", "/api/records/categories", "Categories API"),
        ("GET", "/api/records/pm-kisan", "Single Record API"),
        ("GET", "/api/checklist/pm-kisan", "Checklist API"),
    ]

    all_passed = True

    with httpx.Client(base_url=BASE_URL, timeout=10.0, follow_redirects=True) as client:
        for method, path, desc in endpoints:
            try:
                if method == "GET":
                    resp = client.get(path)
                status = resp.status_code
                if status == 200:
                    print(f"  [✓] 200 OK: {path:<25} ({desc})")
                else:
                    print(f"  [!] {status} WARN: {path:<25} ({desc})")
                    all_passed = False
            except Exception as e:
                print(f"  [✗] FAILED: {path:<25} ({desc}) -> {str(e)[:40]}")
                all_passed = False

        # POST Search
        try:
            resp = client.post("/api/search", json={"query": "kisan farmer", "limit": 3})
            if resp.status_code == 200 and len(resp.json()["results"]) > 0:
                print(f"  [✓] 200 OK: {'/api/search':<25} (Search returns {len(resp.json()['results'])} results)")
            else:
                print(f"  [!] Search response issue: {resp.status_code}")
                all_passed = False
        except Exception as e:
            print(f"  [✗] Search failed: {e}")
            all_passed = False

        # POST Eligibility Check
        try:
            resp = client.post(
                "/api/eligibility/check",
                json={
                    "record_id": "pm-kisan",
                    "profile": {"occupation": "farmer", "age": 25},
                },
            )
            if resp.status_code == 200:
                res_data = resp.json()
                print(f"  [✓] 200 OK: {'/api/eligibility/check':<25} (Evaluated: {res_data['overall_status']})")
            else:
                print(f"  [!] Eligibility check failed: {resp.status_code}")
                all_passed = False
        except Exception as e:
            print(f"  [✗] Eligibility test failed: {e}")
            all_passed = False

    print("=" * 60)
    if all_passed:
        print("  ALL SMOKE TESTS PASSED SUCCESSFULLY!")
        print("=" * 60)
        return 0
    else:
        print("  SOME SMOKE TESTS FAILED. Check logs above.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(run_smoke_test())
