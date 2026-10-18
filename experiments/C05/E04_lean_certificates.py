"""EXP-C05-04: Lean certificates for the models behind new spectrum memberships (from EXP-C05-03)."""

import json

from lab.paths import RESULTS
from lab.runner import save_artifact
from systems.magma import MagmaSAT, is_quasigroup, parse, satisfies

from experiments.C05.E03_frontier_push import LAWS, latin_rows

META = {
    "id": "EXP-C05-04",
    "cycle": "C05",
    "title": "Lean decide-certificates for models establishing new spectrum memberships",
    "agent": "Formal Verifier",
    "question": "Can every spectrum membership found by SAT beyond the ETP notes be machine-checked independently "
                "of the SAT solver?",
    "hypothesis": "Each such membership is witnessed by an explicit Cayley table whose law can be checked by Lean's "
                  "kernel with `decide`.",
    "assumptions": ["memberships taken from results/EXP-C05-03.json ('decided_beyond_notes' with status SAT)"],
    "methodology": "Re-solve each (law, n) instance with the same encoding, re-verify the table in Python, and emit "
                   "a Lean theorem `forall x y : Fin n, x = t(x, y)` proved by `decide` (the Lean file is "
                   "compiled separately; see proofs/lean/Infinity/C05_Magmas.lean).",
    "falsification": "A table that fails the Python re-check or the Lean kernel check.",
}


def lean_term(t, op="T"):
    if isinstance(t, str):
        return t
    return f"({op} {lean_term(t[0], op)} {lean_term(t[1], op)})"


def run():
    e03 = json.load(open(RESULTS / "EXP-C05-03.json"))["results"]
    blocks, items = [], []
    for row in e03["rows"]:
        num = row["etp_number"]
        t = LAWS[num][0]
        law = (parse(t), "x")
        for n in row["decided_beyond_notes"]:
            if row["status_n_2_10"][str(n)] != "SAT":
                continue
            sat = MagmaSAT(n, [law])
            if t.startswith("y("):
                sat.clauses += latin_rows(sat)
            sat.clauses.append([sat.v[0, 0, 0], sat.v[0, 0, 1]])
            status, T = sat.solve()
            assert status == "SAT" and satisfies(T, law)
            name = f"E{num}_order{n}"
            rows = ", ".join("![" + ", ".join(str(int(v)) for v in r) + "]" for r in T)
            blocks.append(
                f"/-- A model of ETP law {num}, `x = {t}`, of order {n} (SAT, EXP-C05-03/04). -/\n"
                f"def {name} : Fin {n} → Fin {n} → Fin {n} := fun a b => ![{rows}] a b\n\n"
                f"theorem {name}_law : ∀ x y : Fin {n}, {lean_term(law[0], name)} = x := by decide\n")
            items.append({"law": num, "n": n, "table": T.tolist(), "quasigroup": is_quasigroup(T), "lean_name": name})
    text = "\n".join(blocks)
    ref = save_artifact(META["id"], "certificates_lean.json", {"lean": text, "items": items})
    return {
        "n_certificates": len(items),
        "items": [{k: v for k, v in it.items() if k != "table"} for it in items],
        "lean_artifact": ref,
        "summary": [f"{len(items)} models re-solved, re-verified and emitted as Lean decide-certificates: "
                    f"{[(it['law'], it['n']) for it in items]}"],
    }
