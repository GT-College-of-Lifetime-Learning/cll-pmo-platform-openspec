import subprocess
import sys
import time

import httpx

proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "demo.app:app", "--port", "8767"],
    cwd=r"C:\Users\kwong318\GitHub\CLL_project_dashboard",
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
try:
    for _ in range(30):
        try:
            httpx.get("http://127.0.0.1:8767/", timeout=2)
            break
        except Exception:
            time.sleep(0.5)
    html = httpx.get("http://127.0.0.1:8767/?as=executive", timeout=15).text
    checks = {
        "progress ring": 'class="ring"' in html and 'stroke-dasharray' in html,
        "term trend bars": 'aria-label="Trend by period' in html,
        "hub timeline badges": 'Hub/start-up milestones by year' in html,
        "credential trend": 'aria-label="Credential trend' in html,
        "expenditure gauge": 'aria-label="Research expenditures' in html and '$' in html,
        "maturity ladder": 'maturity-ladder' in html,
        "capability heatmap": 'Area' in html and '<strong>1</strong>' in html,
        "five goal cards": html.count('class="card goal-card"') == 5,
        "timeline strip": 'Business days remaining' in html,
        "pace labels": 'Linear pace (unapproved)' in html,
        "recent lists": 'class="recent-list"' in html,
        "drill-throughs": html.count('Drill through to objectives') == 5,
    }
    for name, ok in checks.items():
        print(('OK  ' if ok else 'MISS'), name)
    print(f"\n{sum(checks.values())}/{len(checks)} visuals verified")
    sys.exit(0 if all(checks.values()) else 1)
finally:
    proc.terminate()