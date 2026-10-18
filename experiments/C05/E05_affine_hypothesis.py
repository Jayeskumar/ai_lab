"""EXP-C05-05: are full spectra always explained by affine models over Z_n?"""

import json

from lab.paths import RESULTS
from systems.magma import affine_models, parse

META = {
    "id": "EXP-C05-05",
    "cycle": "C05",
    "title": "Bold hypothesis H-C05-A: full spectrum iff affine models over every Z_n",
    "agent": "Mathematical Inventor",
    "question": "Is having models of every order the same as having affine models x*y = a x + b y + c (mod n) "
                "for every n?",
    "hypothesis": "H-C05-A (bold): a nontrivial identity t = x has models of all orders 1..6 iff for every n <= 6 "
                  "it has an affine model over Z_n; restricted spectra are exactly the affine obstructions.",
    "assumptions": ["identities and spectra from EXP-C05-01 (n <= 6)", "exhaustive search over (a, b, c) in Z_n^3"],
    "methodology": "For every identity, list the orders n <= 6 having an affine model over Z_n; compare with the "
                   "SAT spectrum.",
    "falsification": "A full-spectrum identity without an affine model for some n (refutes 'only if'), or an "
                     "affine model of an order outside the SAT spectrum (would indicate a bug).",
}


def run():
    e01 = json.load(open(RESULTS / "EXP-C05-01.json"))["results"]
    rows, refuting, bugs = [], [], []
    for r in e01["rows"]:
        law = (parse(r["identity"].split(" = ")[0]), "x")
        aff_orders = [n for n in range(1, 7) if affine_models(law, n)]
        sat_orders = [n for n in range(1, 7) if r["spectrum_1_6"][n - 1] == "1"]
        rows.append({"identity": r["identity"], "spectrum_1_6": r["spectrum_1_6"], "affine_orders": aff_orders})
        if any(n not in sat_orders for n in aff_orders):
            bugs.append(r["identity"])
        if r["spectrum_1_6"] == "111111" and aff_orders != list(range(1, 7)):
            refuting.append({"identity": r["identity"], "affine_orders": aff_orders})
    full = [r for r in rows if r["spectrum_1_6"] == "111111"]
    restricted_with_affine_gap = [r for r in rows if r["spectrum_1_6"] not in ("111111",)
                                  and set(r["affine_orders"]) != {n for n in range(1, 7) if r["spectrum_1_6"][n - 1] == "1"}]
    return {
        "rows": rows,
        "full_spectrum_without_affine_models": refuting,
        "restricted_where_affine_models_miss_some_orders": [(r["identity"], r["spectrum_1_6"], r["affine_orders"])
                                                           for r in restricted_with_affine_gap],
        "bugs": bugs,
        "summary": [
            f"{len(full)} identities with spectrum 1..6 full; {len(refuting)} of them lack an affine model for some "
            f"order <= 6 (each refutes H-C05-A)",
            f"restricted identities whose SAT spectrum contains orders without affine models: "
            f"{len(restricted_with_affine_gap)}; consistency bugs: {len(bugs)}",
        ],
    }
