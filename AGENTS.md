# AGENTS.md - CitizenAssist AI: Persistent Agent Rules

## Section 1: HOW TO WORK (rules for the agent)

1. FIRST inspect the environment: OS, Python version, Node version, npm, git. Generate setup/start scripts for the detected OS.
2. Work only inside the current workspace folder. Run git init if needed and commit after every phase.
3. Create AGENTS.md in the project root containing sections 1 and 3 of this brief.
4. Keep docs/PROGRESS.md as a live checklist of milestones and phases. Update it after each phase.
5. Keep the website runnable after every phase. Run tests after every phase. Never continue on top of failing tests or a failing build.
6. NEVER write package APIs from memory. Check installed versions before using them.
7. Use the current official Google Gen AI SDK (Python package google-genai, import: from google import genai). Do NOT use the deprecated google-generativeai package.
8. Prefer packages with prebuilt wheels that need no C++ build tools.
9. Do not claim anything works unless you ran it. Final reporting must be honest.
10. TIME MATTERS. Reach Milestone 1 as fast as possible.

## Section 3: GOVERNMENT DATA INTEGRITY (highest priority)

- NEVER invent schemes, services, eligibility, benefits, deadlines, documents or URLs.
- Records have record_type: "scheme" or "service".
- Seed 8-10 real schemes AND 3-4 real citizen services, but ONLY verified ones.
- For every fact store: value, source_url, a short source excerpt, and fetched_at.
- If the source does not state a field, store null and display "Not stated in source - confirm on the official portal."
- verification_status: "verified", "draft", or "demo" (shown with a visible DEMO DATA badge).
- Citizens see only verified (and clearly labelled demo) records.
- Application URLs only from pages you visited.
- Do NOT use the Government of India emblem, Ashoka symbol or any government logo.
- Footer and About page must say: independent hackathon project, not affiliated with or endorsed by the Government of India.
