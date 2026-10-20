"""EXP-C05-12: every order n <= 7 of the 13 open ETP laws x = y*T, decided again with certificates.

EXP-C05-03 decided these orders with a plain SAT search; EXP-C05-06 certified only the gaps that the ETP notes do
not state. Running the case split of systems/magma_split.py on all of them gives every gap n <= 7 its own DRAT
certificate (verified by drat-trim) and every member an explicit, re-checked table, so that the complete spectra
up to order 10 of CLM-C05-17 rest on the lab's own certificates and models, not on the notes.
"""

from experiments.C05.E03_frontier_push import LAWS
from systems.magma_split import decide, drat_path, inner_term

META = {
    "id": "EXP-C05-12",
    "cycle": "C05",
    "title": "Certified decisions for every order n <= 7 of the 13 open ETP laws x = y*T",
    "agent": "Formal Verifier",
    "question": "Do the certified case split and EXP-C05-03 agree on every order 2..7 of the 13 laws, and can every "
                "gap be given a DRAT certificate?",
    "hypothesis": "Yes: the same orders are found, with every gap certified.",
    "assumptions": ["as EXP-C05-09", "conflict budget 200,000 per case (EXP-C05-03 decided all these orders)"],
    "methodology": "decide(law, n) for n = 2..7 and every law x = y*T of EXP-C05-03; compare with its statuses.",
    "falsification": "A disagreement with EXP-C05-03, a rejected proof or an UNKNOWN case.",
}

ORDERS = range(2, 8)
BUDGET = 200_000


def run():
    import json
    from lab.paths import RESULTS
    e03 = {r["etp_number"]: r["status_n_2_10"] for r in json.load(open(RESULTS / "EXP-C05-03.json"))["results"]["rows"]}
    out, disagreements, timings = {}, [], {}
    checker = drat_path()
    for num, (t, *_rest) in LAWS.items():
        if inner_term(t) is None:
            continue
        for n in ORDERS:
            summary, records, times = decide(t, n, BUDGET, checker, label=f"{num}/{n}")
            key = f"{num}/{n}"
            mine = "SAT" if summary["verdict"] == "model found" else (
                "UNSAT" if summary["verdict"] == "no model (every case certified)" else "UNDECIDED")
            out[key] = {"verdict": summary["verdict"], "cases_run": summary["cases_run"],
                        "model": next((r["model"] for r in records if r["status"] == "SAT"), None),
                        "proof_lines": summary["proof_lines"],
                        "records": [{k: r.get(k) for k in ("index", "case", "lam", "ell", "cnf_sha256", "status",
                                                          "conflicts", "proof_lines", "drat_trim")} for r in records]}
            timings[key] = sum(x.get("solve_s", 0) + x.get("check_s", 0) for x in times)
            if mine != e03[num][str(n)]:
                disagreements.append((key, mine, e03[num][str(n)]))
    gaps = sorted(k for k, v in out.items() if v["verdict"].startswith("no model"))
    return {
        "pairs": out,
        "disagreements_with_EXP_C05_03": disagreements,
        "timings": {"seconds_per_pair": timings},
        "summary": [
            f"{len(out)} pairs (13 laws, n = 2..7): {len(gaps)} gaps, every one certified by drat-trim: "
            f"{all(out[k]['verdict'] == 'no model (every case certified)' for k in gaps)}; "
            f"{sum(v['verdict'] == 'model found' for v in out.values())} members with a re-checked model",
            f"disagreements with EXP-C05-03: {len(disagreements)}",
        ],
    }
