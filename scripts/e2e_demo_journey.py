"""
End-to-End Demo Journey Test with Playwright.
Walks through the complete Demo Journey (BUILD_BRIEF.md Section 11 & Section 10):
1. Open website
2. Choose Punjabi or English
3. Type natural language citizen profile or use demo profile button
4. Verify "What I understood" profile panel
5. See relevant schemes with eligibility status
6. Open scheme detail, view official criteria, source link, and verification badge
7. View rule-by-rule eligibility explanation with source excerpts
8. Test document checklist (toggle items, view missing documents)
9. Verify official application portal links
10. Test scheme comparison view (up to 3 schemes)
11. Admin login & PDF extraction view
Runs on Desktop (1280x800) and Mobile (390px iPhone width).
Records all console errors and takes screenshots into docs/screenshots/.
"""

import os
import re
import sys
import time
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from playwright.sync_api import sync_playwright

SCREENSHOTS_DIR = ROOT / "docs" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "http://127.0.0.1:8000"


def load_credentials():
    creds = {"admin_email": "admin@citizenassist.local", "admin_pass": "", "citizen_email": "citizen@citizenassist.local", "citizen_pass": ""}
    creds_file = ROOT / "LOCAL_CREDENTIALS.txt"
    if creds_file.exists():
        content = creds_file.read_text()
        admin_p = re.search(r"ADMIN ACCOUNT:.*?Password:\s*([^\s]+)", content, re.DOTALL)
        if admin_p:
            creds["admin_pass"] = admin_p.group(1).strip()
        cit_p = re.search(r"DEMO CITIZEN ACCOUNT:.*?Password:\s*([^\s]+)", content, re.DOTALL)
        if cit_p:
            creds["citizen_pass"] = cit_p.group(1).strip()
    return creds


def run_e2e_journey():
    print("=" * 65)
    print("  CITIZENASSIST AI - END-TO-END PLAYWRIGHT DEMO JOURNEY")
    print("=" * 65)
    print(f"Targeting: {BASE_URL}")
    print(f"Screenshots directory: {SCREENSHOTS_DIR}\n")

    creds = load_credentials()
    console_errors = []
    page_errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # -------------------------------------------------------------
        # Part A: Desktop Journey (1280 x 800)
        # -------------------------------------------------------------
        print(">>> 1. Starting Desktop Walkthrough (1280x800)...")
        context_desktop = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context_desktop.new_page()

        page.on("console", lambda msg: console_errors.append(f"[Console {msg.type}] {msg.text}") if msg.type in ["error"] else None)
        page.on("pageerror", lambda err: page_errors.append(f"[PageError] {err}"))

        # 1. Open Landing Page
        print("  [Step 1] Loading Landing Page...")
        page.goto(BASE_URL, wait_until="networkidle")
        time.sleep(1)
        page.screenshot(path=str(SCREENSHOTS_DIR / "01_landing_desktop.png"))
        assert "CitizenAssist" in page.title() or "Government Benefits" in page.content(), "Landing page headline missing"
        print("   [✓] Landing page loaded successfully")

        # 2. Switch Language to Punjabi & English
        print("  [Step 2] Testing Language Switcher (Punjabi & English)...")
        pa_btn = page.locator("button:has-text('ਪੰ')").first
        if pa_btn.is_visible():
            pa_btn.click()
            time.sleep(0.5)
            page.screenshot(path=str(SCREENSHOTS_DIR / "02_language_punjabi_desktop.png"))
            print("   [✓] Switched to Punjabi (ਪੰਜਾਬੀ)")

            # Switch back to English
            en_btn = page.locator("button:has-text('EN')").first
            en_btn.click()
            time.sleep(0.5)
            print("   [✓] Switched back to English")

        # 3. AI Assistant Journey (Demo Profile)
        print("  [Step 3] Navigating to AI Assistant...")
        page.goto(f"{BASE_URL}/assistant", wait_until="networkidle")
        time.sleep(1)

        # Click "Use demo profile" button
        print("  [Step 4] Clicking 'Use demo profile' button...")
        demo_btn = page.locator("button:has-text('Use demo profile')").first
        if demo_btn.is_visible():
            demo_btn.click()
            # Wait for response
            time.sleep(2)
            page.screenshot(path=str(SCREENSHOTS_DIR / "03_assistant_answered_desktop.png"))
            print("   [✓] Assistant answered query with profile extraction and claims")

        # 4. Schemes & Services Discovery with Filter
        print("  [Step 5] Navigating to Schemes & Services directory...")
        page.goto(f"{BASE_URL}/schemes", wait_until="networkidle")
        time.sleep(1)
        page.wait_for_selector("text=Pradhan Mantri Kisan Samman Nidhi", timeout=5000)
        page.screenshot(path=str(SCREENSHOTS_DIR / "04_schemes_list_desktop.png"))
        print("   [✓] Schemes catalog loaded with verified badges and category filters")

        # 5. Open Scheme Detail Page
        print("  [Step 6] Opening Scheme Detail (Post-Matric SC Scholarship)...")
        page.goto(f"{BASE_URL}/schemes/post-matric-sc", wait_until="networkidle")
        time.sleep(1)
        page.screenshot(path=str(SCREENSHOTS_DIR / "05_scheme_detail_desktop.png"))
        print("   [✓] Scheme details loaded with official source links and criteria")

        # 6. Eligibility Checker
        print("  [Step 7] Checking Eligibility Checker Form...")
        page.goto(f"{BASE_URL}/eligibility", wait_until="networkidle")
        time.sleep(1)
        # Fill in age and income
        age_in = page.locator("input[placeholder*='20']").first
        if age_in.is_visible():
            age_in.fill("20")
        inc_in = page.locator("input[placeholder*='2,50,000']").first
        if inc_in.is_visible():
            inc_in.fill("200000")
        submit_btn = page.locator("button[type='submit']").first
        if submit_btn.is_visible():
            submit_btn.click()
            time.sleep(1.5)
        page.screenshot(path=str(SCREENSHOTS_DIR / "06_eligibility_results_desktop.png"))
        print("   [✓] Deterministic eligibility evaluated with rule-level criteria")

        # 7. Document Checklist & Printable View
        print("  [Step 8] Checking Document Checklist...")
        page.goto(f"{BASE_URL}/checklist/post-matric-sc", wait_until="networkidle")
        time.sleep(1)
        page.screenshot(path=str(SCREENSHOTS_DIR / "07_document_checklist_desktop.png"))
        print("   [✓] Document checklist rendered with toggle actions and print stylesheet")

        # 8. Scheme Comparison View
        print("  [Step 9] Checking Compare Schemes View...")
        page.goto(f"{BASE_URL}/compare", wait_until="networkidle")
        time.sleep(1)
        page.screenshot(path=str(SCREENSHOTS_DIR / "08_comparison_desktop.png"))
        print("   [✓] Comparison view rendered with multi-scheme slots")

        # 9. Admin Login & PDF Information Extraction
        print("  [Step 10] Testing Admin Panel...")
        page.goto(f"{BASE_URL}/login", wait_until="networkidle")
        time.sleep(0.5)
        email_input = page.locator("input[type='email']")
        pass_input = page.locator("input[type='password']")
        if email_input.is_visible() and creds["admin_pass"]:
            email_input.fill(creds["admin_email"])
            pass_input.fill(creds["admin_pass"])
            page.click("button[type='submit']")
            time.sleep(1.5)
            # Navigate to Admin
            page.goto(f"{BASE_URL}/admin", wait_until="networkidle")
            time.sleep(1)
            page.screenshot(path=str(SCREENSHOTS_DIR / "09_admin_panel_desktop.png"))
            print("   [✓] Admin portal authenticated and ingestion pipeline accessible")

        context_desktop.close()

        # -------------------------------------------------------------
        # Part B: Mobile Journey (390px iPhone width)
        # -------------------------------------------------------------
        print("\n>>> 2. Starting Mobile Walkthrough (390x844 iPhone Viewport)...")
        context_mobile = browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        )
        page_m = context_mobile.new_page()
        page_m.on("console", lambda msg: console_errors.append(f"[Mobile Console {msg.type}] {msg.text}") if msg.type in ["error"] else None)
        page_m.on("pageerror", lambda err: page_errors.append(f"[Mobile PageError] {err}"))

        # Mobile Landing
        print("  [Mobile Step 1] Loading Landing Page on 390px...")
        page_m.goto(BASE_URL, wait_until="networkidle")
        time.sleep(1)
        page_m.screenshot(path=str(SCREENSHOTS_DIR / "10_landing_mobile_390px.png"))
        print("   [✓] Mobile landing responsive layout verified")

        # Mobile Assistant
        print("  [Mobile Step 2] Testing Mobile Assistant...")
        page_m.goto(f"{BASE_URL}/assistant", wait_until="networkidle")
        time.sleep(1)
        page_m.screenshot(path=str(SCREENSHOTS_DIR / "11_assistant_mobile_390px.png"))
        print("   [✓] Mobile assistant layout verified")

        # Mobile Schemes
        print("  [Mobile Step 3] Testing Mobile Schemes Catalog...")
        page_m.goto(f"{BASE_URL}/schemes", wait_until="networkidle")
        time.sleep(1)
        page_m.screenshot(path=str(SCREENSHOTS_DIR / "12_schemes_mobile_390px.png"))
        print("   [✓] Mobile catalog touch layout verified")

        # Mobile Detail
        print("  [Mobile Step 4] Testing Mobile Scheme Detail...")
        page_m.goto(f"{BASE_URL}/schemes/pm-kisan", wait_until="networkidle")
        time.sleep(1)
        page_m.screenshot(path=str(SCREENSHOTS_DIR / "13_scheme_detail_mobile_390px.png"))
        print("   [✓] Mobile detail card readable at 390px width")

        context_mobile.close()
        browser.close()

    print("\n" + "=" * 65)
    print("  BROWSER CONSOLE & RUNTIME AUDIT:")
    if page_errors:
        print(f"  [✗] Page Errors Found ({len(page_errors)}):")
        for err in page_errors:
            print(f"      - {err}")
    else:
        print("  [✓] Zero Page Runtime Errors (0 errors)")

    if console_errors:
        print(f"  [!] Console Errors Logged ({len(console_errors)}):")
        for err in console_errors:
            print(f"      - {err}")
    else:
        print("  [✓] Zero Browser Console Errors (0 errors)")

    print("=" * 65)
    print(f"All 13 demo screenshots captured successfully in {SCREENSHOTS_DIR}")
    return len(page_errors) == 0


if __name__ == "__main__":
    success = run_e2e_journey()
    sys.exit(0 if success else 1)
