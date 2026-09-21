import sys

sys.path.insert(0, r"C:\Users\kwong318\GitHub\CLL_project_dashboard")

from fastapi.testclient import TestClient

from demo.app import app

client = TestClient(app, follow_redirects=True)
html = client.get("/?as=executive").text

checks = {
    "diagnostics dropdown present": 'details class="nav-more"' in html and "Diagnostics" in html,
    "dropdown carries readiness + coverage": "Cycle readiness" in html and "Data coverage" in html,
    "admin link present": 'class="admin-link"' in html,
    "primary nav cleaned (Overview label)": ">Overview</a>" in html,
    "F7 button REMOVED from header": "Run F7 hygiene" not in html.split("</header>")[0],
    "Run sync button REMOVED from header": "Run sync" not in html.split("</header>")[0],
}
admin = client.get("/admin?as=executive").text
checks["admin panel renders readiness state"] = "Readiness gates" in admin
checks["admin panel shows run actions"] = admin.count("<form method") >= 5
checks["admin panel shows build counts"] = "Current build" in admin

# actions work
r = client.post("/admin/export-feed")
checks["export-feed action works"] = r.status_code == 200 and "feed_version" in r.text
r = client.post("/admin/matrix")
checks["matrix action works"] = r.status_code == 200 and "matrix" in r.text.lower()
r = client.post("/admin/hygiene")
checks["hygiene action works (from panel now)"] = r.status_code == 200
r = client.post("/admin/sync")
checks["sync action works (from panel now)"] = r.status_code == 200

passed = sum(checks.values())
for name, ok in checks.items():
    print(("OK  " if ok else "MISS"), name)
print(f"\n{passed}/{len(checks)} nav/admin checks passed")
sys.exit(0 if passed == len(checks) else 1)