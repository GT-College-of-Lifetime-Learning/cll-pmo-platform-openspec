import subprocess
import sys
import time

import httpx

# boot uvicorn
proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "demo.app:app", "--port", "8765"],
    cwd=r"C:\Users\kwong318\GitHub\CLL_project_dashboard",
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

routes = [
    ("Strategy 2035 exec", "/?as=executive"),
    ("Strategy 2035 unit", "/?as=unit:GTPE"),
    ("Overview exec", "/overview?as=executive"),
    ("Overview unit", "/overview?as=unit:GTPE"),
    ("Governance", "/governance?as=executive"),
    ("Unit GTPE", "/unit/GTPE?as=unit:GTPE"),
    ("Unit GTLI", "/unit/GTLI?as=unit:GTLI"),
    ("Priority SP-05", "/priority/SP-05?as=executive"),
    ("Item public", "/item/CLL-26-0002?as=executive"),
    ("Item drill unit", "/item/CLL-26-0002?as=unit:GTPE"),
    ("Confidential own unit", "/item/CLL-26-0024?as=unit:GTPE"),
    ("Confidential other unit", "/item/CLL-26-0024?as=unit:GTLI"),
]

try:
    ok = False
    for _ in range(30):
        try:
            httpx.get("http://127.0.0.1:8765/", timeout=2)
            ok = True
            break
        except Exception:
            time.sleep(0.5)
    if not ok:
        print("server did not start")
        print(proc.stdout.read() if proc.stdout else "")
        sys.exit(1)

    failures = 0
    for name, path in routes:
        try:
            resp = httpx.get(f"http://127.0.0.1:8765{path}", timeout=10, follow_redirects=True)
            expect = 200
            if "other unit" in name:
                expect = 403
            status_ok = resp.status_code == expect
            print(f"{'OK ' if status_ok else 'FAIL'} {name}: {resp.status_code} (expect {expect})")
            if not status_ok:
                failures += 1
        except Exception as e:
            print(f"ERR {name}: {e}")
            failures += 1
    print(f"\n{len(routes) - failures}/{len(routes)} passed")
    sys.exit(1 if failures else 0)
finally:
    proc.terminate()