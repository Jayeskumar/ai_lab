"""Plain-Python big-integer verification of the remaining triples quoted in Appendix C.1.  -> out/c08_verify_extra.json"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
exec((HERE / "c08_verify_triples.py").read_text().split("CASES = [")[0])
CASES = [("4-bonacci", (1, 1, 1, 1), (1, 2, 4, 8), 7, (348872, 348872, 1)),
         ("G(k+1)=G(k)+G(k-2)", (1, 0, 1), (1, 2, 3), 10, (164049, 164049, 1)),
         ("Pell 1,2", (2, 1), (1, 2), 0, (275806, 275806, 2)),
         ("G(k+1)=G(k)+G(k-3)", (1, 0, 0, 1), (1, 2, 3, 4), 24, (1, 6, 6)),
         ("1,3,4,7,11", (1, 1), (1, 3), 3, (1, 2, 6)),
         ("1,4,5,9,14", (1, 1), (1, 4), 5, (1, 8, 8)),
         ("Fibonacci", (1, 1), (1, 2), 1, (1, 4, 4))]
out = {}
for name, c, g, s, (a, b, cc) in CASES:
    l = circ(circ(a, b, s, c, g), cc, s, c, g)
    r = circ(a, circ(b, cc, s, c, g), s, c, g)
    out[f"{name} s={s}"] = {"triple": [a, b, cc], "(ab)c": str(l), "a(bc)": str(r), "non_associative": l != r}
    print(name, s, (a, b, cc), "NOT assoc" if l != r else "assoc")
(HERE / "out/c08_verify_extra.json").write_text(json.dumps(out, indent=1))
