"""EXP-C05-03: pushing the known spectra of open order-4 laws (ETP numbering) to n <= 12."""

import time

from pysat.card import CardEnc, EncType

from systems.magma import MagmaSAT, parse, satisfies, to_str

META = {
    "id": "EXP-C05-03",
    "cycle": "C05",
    "title": "Frontier push: spectra of open order-4 laws for n = 2..10 (SAT with sound Latin-row constraints)",
    "agent": "Formal Verifier",
    "question": "For the order-4 laws x = t whose spectrum is listed as unknown in the Equational Theories Project "
                "notes, which sizes n <= 12 admit models?",
    "hypothesis": "Several open laws have unresolved small sizes that SAT can decide; our results must agree with "
                  "every membership/non-membership already stated in the notes.",
    "assumptions": ["laws and partial knowledge taken from B. Le Floch's ETP notes 'spectrum.pdf' (Lean Zulip)",
                    "for laws of the form x = y*(...), every left translation is onto, hence a bijection in a finite "
                    "magma, so 'every row is a permutation' is added as a sound implied constraint",
                    "symmetry breaking 0*0 in {0,1} (any magma can be relabelled so)",
                    "CaDiCaL conflict budget 1e6 per instance; UNKNOWN is reported as such"],
    "methodology": "SAT model search for each law and n = 2..10; every SAT answer is re-verified by evaluating the "
                   "law on the returned table; results are compared with the sizes stated in the notes.",
    "falsification": "A disagreement with a size stated in the notes would indicate a bug (ours or theirs).",
}

# ETP number -> (law t as in 'x = t', sizes stated IN the notes, sizes stated NOT in the notes, notes' phrase)
LAWS = {
    467: ("y(x(x(yy)))", [1, 5, 7, 8], [], "unknown spectrum starting with 1,5,7,8"),
    501: ("y(y(x(xy)))", [1, 4, 5, 8, 9], [], "unknown spectrum containing 1,4,5,8,9"),
    670: ("y(x((xy)y))", [1, 4, 5], [6, 7], "unknown spectrum starting with 1,4,5, not 6 nor 7"),
    677: ("y(x((yx)y))", [], [], "unknown spectrum (no sizes stated)"),
    704: ("y(y((xx)y))", [1, 5, 7, 8], [9], "unknown spectrum starting with 1,5,7,8 and no 9"),
    883: ("y((xy)(yy))", [1, 2, 4, 5, 7, 8], [], "unknown spectrum containing {1,2 mod 3}"),
    907: ("y((yx)(xy))", [1, 3, 7, 9, 13], [2, 4, 5, 6], "unknown spectrum containing 1,3,7,9,13, not 2,4,5,6"),
    1076: ("y((x(xy))y)", [1, 5], [6, 7], "unknown spectrum starting with 1,5, not 6 nor 7"),
    1083: ("y((x(yx))y)", [1, 3, 4, 7, 8, 9], [], "unknown spectrum containing 1,3,4,7,8,9"),
    1110: ("y((y(xx))y)", [1, 4, 5, 7, 8, 9], [], "unknown spectrum starting with 1,4,5,7,8,9"),
    1279: ("y(((xx)y)y)", [1, 5, 7, 8], [9], "unknown spectrum starting with 1,5,7,8 and no 9"),
    1286: ("y(((xy)x)y)", [1, 7], [], "unknown spectrum starting with 1,7"),
    1313: ("y(((yx)x)y)", [1, 5, 7], [], "unknown spectrum starting with 1,5,7"),
    1516: ("(yy)(x(xy))", [1, 5, 7, 8], [], "unknown spectrum starting with 1,5,7,8"),
    1719: ("(yy)((xx)y)", [1, 3, 4, 5, 6, 7, 8, 9], [], "unknown spectrum containing {0,1 mod 3} and 5, 8"),
}
SIZES = range(2, 11)
BUDGET = 1_000_000


def latin_rows(sat: MagmaSAT):
    n = sat.n
    cls = []
    for a in range(n):
        for c in range(n):
            cls += CardEnc.equals([sat.v[a, b, c] for b in range(n)], 1, vpool=sat.pool,
                                  encoding=EncType.pairwise).clauses
    return cls


def run():
    t0 = time.time()
    rows = []
    disagreements = []
    for num, (t, known_in, known_out, phrase) in LAWS.items():
        law = (parse(t), "x")
        rows_latin = t.startswith("y(")
        res = {}
        for n in SIZES:
            extra = []
            sat = MagmaSAT(n, [law])
            if rows_latin:
                sat.clauses += latin_rows(sat)
            sat.clauses.append([sat.v[0, 0, 0], sat.v[0, 0, 1]] if n > 1 else [sat.v[0, 0, 0]])
            status, T = sat.solve(conf_budget=BUDGET)
            if status == "SAT":
                assert satisfies(T, law), "SAT model fails the law"
            res[n] = status
            if n in known_in and status == "UNSAT":
                disagreements.append((num, n, "notes say IN, SAT says UNSAT"))
            if n in known_out and status == "SAT":
                disagreements.append((num, n, "notes say OUT, SAT found a model"))
        decided_new = [n for n in SIZES if res[n] != "UNKNOWN" and n not in known_in and n not in known_out]
        rows.append({"etp_number": num, "law": "x = " + to_str(law[0]), "notes": phrase,
                     "status_n_2_10": {str(n): res[n] for n in SIZES},
                     "in_spectrum": [n for n in SIZES if res[n] == "SAT"],
                     "not_in_spectrum": [n for n in SIZES if res[n] == "UNSAT"],
                     "unknown": [n for n in SIZES if res[n] == "UNKNOWN"],
                     "decided_beyond_notes": decided_new,
                     "latin_row_constraints": rows_latin})
    return {
        "rows": rows,
        "disagreements_with_notes": disagreements,
        "timings": {"seconds": round(time.time() - t0, 1)},
        "summary": [f"{r['etp_number']}: in {r['in_spectrum']}, out {r['not_in_spectrum']}, unknown {r['unknown']}"
                    for r in rows] + [f"disagreements with the notes: {len(disagreements)}"],
    }
