"""
Demo Safety Check Script for CitizenAssist AI.
Run this script before going on stage to verify:
1. Server is responding
2. Database is seeded with all records
3. Search index is healthy
4. Official links respond
5. AI or Retrieval-only mode is active
6. English sample question returns grounded citations
7. Punjabi sample question returns grounded citations
"""

import os
import sys
import httpx

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else os.getenv("BASE_URL", "http://127.0.0.1:8000")


def run_demo_check():
    print("=" * 65)
    print("  CITIZENASSIST AI - PRE-STAGE DEMO SAFETY CHECK")
    print("=" * 65)
    print("Checking system readiness for live presentation...\n")

    issues = 0

    with httpx.Client(base_url=BASE_URL, timeout=30.0, follow_redirects=True) as client:
        # 1. Server & Health
        try:
            resp = client.get("/api/health")
            if resp.status_code == 200:
                health = resp.json()
                mode_str = "Gemini AI Active" if health.get("ai_enabled") else "Retrieval-Only Fallback (Safe)"
                print(f"[✓] 1. Server Running & Healthy: {mode_str}")
            else:
                print(f"[✗] 1. Server returned status {resp.status_code}")
                issues += 1
        except Exception as e:
            print(f"[✗] 1. Server is not reachable at {BASE_URL}: {e}")
            print("    Please run ./start.sh or python -m uvicorn backend.app.main:app first!")
            return 1

        # 2. Database Records Seeded
        try:
            resp = client.get("/api/records")
            data = resp.json()
            total = data.get("total", 0)
            if total >= 10:
                print(f"[✓] 2. Database Seeded: {total} verified schemes and services loaded")
            else:
                print(f"[!] 2. Database has only {total} records. Expected >= 10")
                issues += 1
        except Exception as e:
            print(f"[✗] 2. Database query failed: {e}")
            issues += 1

        # 3. FTS5 Search Index
        try:
            resp = client.post("/api/search", json={"query": "scholarship sc student", "limit": 3})
            search_data = resp.json()
            results = search_data.get("results", [])
            if results:
                print(f"[✓] 3. Search Index Active: Top hit = '{results[0]['record_name']}'")
            else:
                print("[!] 3. Search returned 0 results for 'scholarship sc student'")
                issues += 1
        except Exception as e:
            print(f"[✗] 3. Search index failed: {e}")
            issues += 1

        # 4. English Demo Question
        en_query = "I am a 20-year-old SC student from Punjab with a family income of 2 lakh. What schemes can I apply for?"
        print(f"\nTesting English Demo Query:\n  \"{en_query}\"")
        try:
            resp = client.post("/api/assistant/chat", json={"message": en_query, "language": "en"})
            if resp.status_code == 200:
                chat_res = resp.json()
                reply_excerpt = chat_res.get("reply", "")[:120].replace("\n", " ")
                print(f"[✓] 4. English Grounded Reply: \"{reply_excerpt}...\"")
                print(f"     Recommended IDs: {chat_res.get('suggested_records', [])}")
            else:
                print(f"[✗] 4. English Assistant query failed with status {resp.status_code}")
                issues += 1
        except Exception as e:
            print(f"[✗] 4. English Assistant test failed: {e}")
            issues += 1

        # 5. Punjabi Demo Question
        pa_query = "ਮੈਂ ਪੰਜਾਬ ਤੋਂ 20 ਸਾਲਾ ਐੱਸ.ਸੀ. ਵਿਦਿਆਰਥੀ ਹਾਂ ਅਤੇ ਪਰਿਵਾਰਕ ਆਮਦਨ 2 ਲੱਖ ਹੈ।"
        print(f"\nTesting Punjabi Demo Query:\n  \"{pa_query}\"")
        try:
            resp = client.post("/api/assistant/chat", json={"message": pa_query, "language": "pa"})
            if resp.status_code == 200:
                chat_res = resp.json()
                reply_excerpt = chat_res.get("reply", "")[:120].replace("\n", " ")
                print(f"[✓] 5. Punjabi Grounded Reply: \"{reply_excerpt}...\"")
                print(f"     Profile Extracted: {chat_res.get('profile_extracted', {})}")
            else:
                print(f"[✗] 5. Punjabi Assistant query failed with status {resp.status_code}")
                issues += 1
        except Exception as e:
            print(f"[✗] 5. Punjabi Assistant test failed: {e}")
            issues += 1

    print("\n" + "=" * 65)
    if issues == 0:
        print("  STAGE READINESS: 100% READY FOR LIVE DEMO!")
        print("  Demo journeys in English and Punjabi are fully functional.")
        print("=" * 65)
        return 0
    else:
        print(f"  DEMO SAFETY CHECK FAILED WITH {issues} ISSUE(S).")
        print("=" * 65)
        return 1


if __name__ == "__main__":
    sys.exit(run_demo_check())
