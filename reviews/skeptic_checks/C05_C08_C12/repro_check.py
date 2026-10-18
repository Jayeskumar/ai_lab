"""Compare the code sha256 stored in results/EXP-Cnn-*.json with the current experiment scripts
(cycles C05, C08, C09, C10, C11, C12).  Read-only.  -> out/repro_sha.json"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
rows = []
for cyc in ("C05", "C08", "C09", "C10", "C11", "C12"):
    for f in sorted((ROOT / "results").glob(f"EXP-{cyc}-*.json")):
        d = json.loads(f.read_text())
        code = d.get("code", {})
        script = ROOT / code.get("file", "")
        cur = hashlib.sha256(script.read_bytes()).hexdigest() if script.is_file() else None
        rows.append({"id": d["id"], "script": code.get("file"), "stored_sha256": code.get("sha256"),
                     "current_sha256": cur, "match": cur == code.get("sha256"),
                     "started": d.get("started"), "runtime_s": d.get("runtime_s"), "error": d.get("error") is not None,
                     "volatile_keys_in_results": [k for k in d.get("results", {}) if "time" in k.lower() or "second" in k.lower()]})
out = {"rows": rows, "n": len(rows), "mismatches": [r["id"] for r in rows if not r["match"]]}
(Path(__file__).resolve().parent / "out" / "repro_sha.json").write_text(json.dumps(out, indent=1))
for r in rows:
    print(r["id"], "match" if r["match"] else "MISMATCH", r["started"], r["runtime_s"], r["volatile_keys_in_results"])
