"""Check the ETP equation numbers used in C05 against the ETP list (data/equations.txt of
github.com/teorth/equational_theories, downloaded to the scratchpad; path given as argument).
Equation k is line k of that file.  -> out/c05_etp_numbers.json"""
import json, sys
from pathlib import Path
import c05_checks as C

lines = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()

def parse_etp(s):
    s = s.replace(" ", "").replace("◇", "")
    return C.parse(s)

USED = {63: "y(x(xy))", 66: "y(x(yy))", 115: "y((xx)y)", 167: "(yx)(xy)", 467: "y(x(x(yy)))", 474: "y(x(y(xy)))",
        501: "y(y(x(xy)))", 670: "y(x((xy)y))", 677: "y(x((yx)y))", 704: "y(y((xx)y))", 883: "y((xy)(yy))",
        907: "y((yx)(xy))", 1076: "y((x(xy))y)", 1083: "y((x(yx))y)", 1110: "y((y(xx))y)", 1279: "y(((xx)y)y)",
        1286: "y(((xy)x)y)", 1313: "y(((yx)x)y)", 1516: "(yy)(x(xy))", 1685: "(yx)((xy)y)", 1719: "(yy)((xx)y)"}
out = {}
for num, t in USED.items():
    lhs, rhs = lines[num - 1].split("=")
    L, R = parse_etp(lhs), parse_etp(rhs)
    ours = C.parse(t)
    # ETP writes "x = t"; compare up to the renaming x<->y is NOT allowed (x is the lhs variable)
    out[num] = {"etp_line": lines[num - 1], "ours": "x = " + t, "match": L == "x" and R == ours}
    print(num, out[num])
out["168"] = lines[167]
(Path(__file__).resolve().parent / "out/c05_etp_numbers.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
