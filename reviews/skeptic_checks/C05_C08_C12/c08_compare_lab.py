"""Compare the lab's EXP-C08-04 associative-shift sets with the targeted search (out/c08_targeted_quadratic.json).
-> out/c08_compare_lab.json"""
import json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
mine = json.loads((HERE / "out/c08_targeted_quadratic.json").read_text())["result"]["rows"]
lab = json.loads((ROOT / "results/EXP-C08-04.json").read_text())["results"]["rows"]
key = lambda p, q, g: (p, q, g)
labmap = {}
for x in lab:
    m = re.match(r"G\(k\+1\)=(\d+)G\(k\)\+\((-?\d+)\)G\(k-1\); 1,(\d+)", x["G"])
    labmap[key(int(m.group(1)), int(m.group(2)), int(m.group(3)))] = (x["associative_shifts"], x["upward_closed"], x["beta"])
out = {"false_positives_in_EXP-C08-04": [], "lab_non_monotone": [], "n_lab_rows": len(labmap)}
for r in mine:
    k = key(r["p"], r["q"], r["g1"])
    if k not in labmap:
        continue
    shifts, up, beta = labmap[k]
    fp = sorted(s for s in shifts if s in r["certified_failures"])
    if fp:
        out["false_positives_in_EXP-C08-04"].append({"p": k[0], "q": k[1], "g1": k[2], "lab_shifts": shifts,
                                                      "certified_failing": fp})
    if shifts and not up:
        out["lab_non_monotone"].append({"p": k[0], "q": k[1], "g1": k[2], "lab_shifts": shifts,
                                        "targeted_no_failure": [s for s in r["no_failure_found"] if s <= 10],
                                        "targeted_certified_failures": [s for s in r["certified_failures"] if s <= 10],
                                        "still_non_monotone_on_0_10": any(s1 < s2 for s1 in r["no_failure_found"] if s1 <= 10 for s2 in r["certified_failures"] if s2 <= 10)})
(HERE / "out/c08_compare_lab.json").write_text(json.dumps(out, indent=1))
print("false positives:", len(out["false_positives_in_EXP-C08-04"]))
for x in out["false_positives_in_EXP-C08-04"]: print("  ", x)
print("lab non-monotone rows:", len(out["lab_non_monotone"]))
for x in out["lab_non_monotone"]: print("  ", x)
