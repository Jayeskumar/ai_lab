"""Compare results_sha256 and code sha256 of the re-run lab experiments with the pre-run copies.
-> out/lab_rerun_compare.json"""
import hashlib, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
rows = []
for f in sorted((HERE / "out/lab_rerun_before").glob("EXP-*.json")):
    before = json.loads(f.read_text())
    after = json.loads((ROOT / "results" / f.name).read_text())
    script = ROOT / before["code"]["file"]
    rows.append({"id": before["id"],
                 "code_sha256_before_eq_script": before["code"]["sha256"] == hashlib.sha256(script.read_bytes()).hexdigest(),
                 "rerun_started": after["started"], "same_results_sha256": before["results_sha256"] == after["results_sha256"],
                 "differing_top_level_keys": sorted(k for k in set(before["results"]) | set(after["results"])
                                                    if before["results"].get(k) != after["results"].get(k)),
                 "runtime_before_after": [before["runtime_s"], after["runtime_s"]]})
(HERE / "out/lab_rerun_compare.json").write_text(json.dumps(rows, indent=1))
for r in rows:
    print(r)
