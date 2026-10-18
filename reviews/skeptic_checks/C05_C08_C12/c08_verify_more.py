"""Re-derive and independently verify (plain Python big integers) certified failures from the targeted search
for rows where EXP-C08-04 / EXP-C08-06 listed the shift as associative.  -> out/c08_verify_more.json"""
import json, subprocess
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
src = (HERE / "c08_verify_triples.py").read_text().split("CASES = [")[0]
exec(src)          # defines seq, greedy, circ (own Python implementation)
CASES = [((4, -2), 2, 3), ((4, -2), 3, 3), ((4, -2), 6, 4), ((5, -3), 2, 5), ((5, -3), 3, 7), ((2, 2), 5, 6),
         ((2, 2), 6, 9), ((3, 2), 6, 4), ((3, 2), 5, 5), ((3, 3), 2, 9), ((3, 3), 2, 10), ((4, 2), 5, 3), ((4, 3), 6, 7)]
out = []
for (p, q), g1, s in CASES:
    beta = sorted(np.roots([1, -p, -q]).real, key=abs)[0]
    line = subprocess.run([str(HERE / "c08_extreme"), "2", str(p), str(q), "1", str(g1), repr(float(beta)), "0",
                           str(s), str(s), "100000", "100", "2", "300"], capture_output=True, text=True).stdout.split()
    rec = {"p": p, "q": q, "g1": g1, "s": s, "beta": round(float(beta), 6), "search": " ".join(line)}
    if line[1] == "CERT":
        a, b, c = map(int, line[2:5])
        l = circ(circ(a, b, s, (p, q), (1, g1)), c, s, (p, q), (1, g1))
        r = circ(a, circ(b, c, s, (p, q), (1, g1)), s, (p, q), (1, g1))
        rec.update({"triple": [a, b, c], "(ab)c": str(l), "a(bc)": str(r), "python_confirms_non_assoc": l != r})
    out.append(rec)
    print(rec)
(HERE / "out/c08_verify_more.json").write_text(json.dumps(out, indent=1))
