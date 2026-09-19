# Flow-engine scenario tests: F1 intake, F2 decisions + call-up (D11),
# F4 Red validation, activation gates, closeout gate. Uses TestClient so
# no manual server is needed; exercises exactly the spec scenarios.

import sys

sys.path.insert(0, r"C:\Users\kwong318\GitHub\CLL_project_dashboard")

from fastapi.testclient import TestClient

from demo.app import app

client = TestClient(app, raise_server_exceptions=False, follow_redirects=False)
AS = "?as=executive"
passed = failed = 0

def check(name, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
        print(f"OK   {name}")
    else:
        failed += 1
        print(f"FAIL {name} {detail}")

# ---- F1: request submitted -> REQ id assigned, notified record exists ----
r = client.post("/intake/submit" + AS, data={
    "title": "Flow Test: cross-unit pilot", "requester": "Test User", "unit": "GTPE",
    "contributing": "GTLI", "problem": "Testing intake",
    "priority": "SP-03", "effort": "100", "cost": "0", "external": "", "new_launch": ""})
check("F1 submit redirects (303)", r.status_code == 303, r.status_code)
req_path = r.headers["location"]
req_id = req_path.split("/requests/")[1].split("?")[0]
html = client.get(req_path).text
check("F1 request record created with ID", f"{req_id} —" in html, req_id)
check("F1 multi-unit stamped Tier 1 (D14)", "classified Tier 1 at submission" in html)

# ---- F1: single-unit small request -> below Tier 2 ----
r = client.post("/intake/submit" + AS, data={
    "title": "Flow Test: tiny ops task", "requester": "Test User", "unit": "GTLI",
    "contributing": "", "problem": "small", "priority": "", "effort": "10", "cost": "0",
    "external": "", "new_launch": ""})
req2 = r.headers["location"].split("/requests/")[1].split("?")[0]
import sqlite3
con = sqlite3.connect(r"C:\Users\kwong318\GitHub\CLL_project_dashboard\demo\cll_spm.db")
tier2 = con.execute("SELECT Tier FROM IntakeRequests WHERE RequestId=?", (req2,)).fetchone()[0]
check("F1 small request classified below Tier 2 (None)", tier2 is None, tier2)

# ---- Triage: complete -> Ready for Review ----
r = client.post(f"/requests/{req_id}/triage" + AS, data={
    "action": "complete", "tier": "1", "triage_owner": "K. Osei", "priority": "SP-03"})
html = client.get(f"/requests/{req_id}" + AS).text
check("Triage completes to Ready for Review", "Ready for Review" in html)

# ---- F2: TCC approves -> DEC recorded + WorkItem created, linked both ways ----
r = client.post(f"/requests/{req_id}/decide" + AS, data={
    "decision": "approve", "rationale": "test approve", "conditions": "", "decides_as": "TCC"})
html = client.get(f"/requests/{req_id}" + AS).text
check("F2 approval recorded in Decisions", "Approved" in html)
import re
m = re.search(r"CLL-26-\d{4}", html)
item_id = m.group(0) if m else None
check("F2 approval creates registry item", item_id is not None)
row = con.execute("SELECT Stage, RequestId FROM WorkItems WHERE ItemId=?", (item_id,)).fetchone()
check("F2 item created in Approved stage, linked", row and row[0] == "Approved" and row[1] == req_id)

# ---- Tier 2 call-up (D11) ----
r = client.post("/intake/submit" + AS, data={
    "title": "Flow Test: unit T2", "requester": "T", "unit": "GTPE",
    "contributing": "", "problem": "t2", "priority": "SP-05",
    "effort": "120", "cost": "0", "external": "", "new_launch": ""})
req3 = r.headers["location"].split("/requests/")[1].split("?")[0]
con.execute("UPDATE IntakeRequests SET Tier='2', Status='Ready for Review' WHERE RequestId=?", (req3,))
con.commit()
client.post(f"/requests/{req3}/decide" + AS, data={
    "decision": "approve", "rationale": "unit head approves"})
html = client.get(f"/requests/{req3}" + AS).text
check("D11 Tier 2 approval opens call-up window", "open for TCC call-up" in html)
r = client.post(f"/requests/{req3}/callup" + AS, data={"member": "TCC member"})
html = client.get(f"/requests/{req3}" + AS).text
check("D11 call-up: stays Approved, blocked from Active", "cannot become Active" in html)
# activation gate: called-up item cannot go Active (read linked item from DB, not regex)
item3 = con.execute("SELECT LinkedItemId FROM IntakeRequests WHERE RequestId=?", (req3,)).fetchone()[0]
r = client.post(f"/items/{item3}/stage" + AS, data={"stage": "Active"})
check("D11 called-up item blocked from Active", r.status_code == 422 and "call-up" in r.text,
      f"got {r.status_code}: {r.text[:120]}")

# ---- F4: Red without path/ask rejected ----
r = client.post(f"/update/{item_id}/submit" + AS, data={
    "overall": "Red", "summary": "bad", "pct": "10"})
check("F4 Red without path/ask rejected (422)", r.status_code == 422 and "not saved" in r.text)
r = client.post(f"/update/{item_id}/submit" + AS, data={
    "overall": "Red", "summary": "off track", "path_to_green": "re-sequence launch",
    "decision_ask": "", "pct": "30"})
check("F4 Red with path accepted", r.status_code == 303)
hist = con.execute("SELECT COUNT(*) FROM StatusUpdates WHERE ItemId=? AND OverallRAG='Red'",
                   (item_id,)).fetchone()[0]
check("F4 Red appended to StatusUpdates", hist >= 1)

# ---- Activation gates (registry spec) ----
row = con.execute("SELECT Sponsor, StartDate, TargetEndDate, CharterUrl FROM WorkItems WHERE ItemId=?",
                  (item_id,)).fetchone()
con.execute("UPDATE WorkItems SET Sponsor=NULL, CharterUrl=NULL WHERE ItemId=?", (item_id,))
con.commit()
r = client.post(f"/items/{item_id}/stage" + AS, data={"stage": "Active"})
check("Activation blocked: missing sponsor + Tier 1 charter", r.status_code == 422 and "sponsor" in r.text and "charter" in r.text)
con.execute("UPDATE WorkItems SET Sponsor='Bill', StartDate='2026-10-01', TargetEndDate='2027-03-31', CharterUrl='x' WHERE ItemId=?", (item_id,))
con.commit()
r = client.post(f"/items/{item_id}/stage" + AS, data={"stage": "Active"})
check("Activation passes once required data present", r.status_code == 303)

# ---- Closeout gate: Tier 1 Closed requires summary ----
r = client.post(f"/items/{item_id}/stage" + AS, data={"stage": "Closed", "closeout": ""})
check("Closeout blocked without summary (Tier 1)", r.status_code == 422 and "closeout" in r.text)
r = client.post(f"/items/{item_id}/stage" + AS, data={"stage": "Closed", "closeout": "Outcomes delivered"})
check("Closeout accepted with summary", r.status_code == 303)

con.close()
print(f"\n{passed}/{passed + failed} flow scenario checks passed")
sys.exit(1 if failed else 0)