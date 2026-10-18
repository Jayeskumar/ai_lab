"""EXP-C12-04: OEIS checks for every Grundy sequence and P-position sequence (Historian)."""

import json

from lab import oeis
from lab.paths import RESULTS

META = {
    "id": "EXP-C12-04",
    "cycle": "C12",
    "title": "OEIS look-ups for the Grundy and P-position sequences of the 19 games",
    "agent": "Historian and Novelty Analyst",
    "question": "Which of the 19 Grundy sequences and P-position sets are already catalogued?",
    "hypothesis": "Classical closed forms (v2, Omega, popcount, n mod 3, Grundy's game) are catalogued; some "
                  "relational games may not be.",
    "assumptions": ["OEIS search API with on-disk cache", "Grundy sequences queried from n = 1 (n = 0 is not a "
                    "position for several games); P-position sequences from the first positive P-position"],
    "methodology": "novelty_check on the first 40 terms; the matched entries' names are recorded for manual "
                   "reading (a shifted-window hit is not accepted as a match without inspection).",
    "falsification": "n/a (literature check)",
}


def run():
    seqs = json.load(open(RESULTS / "artifacts" / "EXP-C12-01" / "grundy_sequences.json"))
    out = {}
    for name, g in seqs.items():
        r = oeis.novelty_check(g[1:41])
        P = [n for n in range(1, len(g)) if g[n] == 0][:40]
        rp = oeis.novelty_check(P) if len(P) >= 8 else {"status": "TOO FEW P-POSITIONS", "hits": []}
        out[name] = {"grundy": {"status": r["status"], "hits": r.get("hits", [])[:3], "query": r.get("query")},
                     "P_positions": {"status": rp["status"], "hits": rp.get("hits", [])[:3], "terms": P[:20]}}
    no_g = [k for k, v in out.items() if v["grundy"]["status"] == "NO MATCH"]
    no_p = [k for k, v in out.items() if v["P_positions"]["status"] == "NO MATCH"]
    return {"checks": out, "grundy_no_match": no_g, "P_no_match": no_p,
            "summary": [f"Grundy sequences without OEIS match: {no_g}", f"P-position sets without match: {no_p}"] +
                       [f"{k}: G {v['grundy']['status']} {[h['anumber'] for h in v['grundy']['hits'][:2]]} | P "
                        f"{v['P_positions']['status']} {[h['anumber'] for h in v['P_positions']['hits'][:2]]}"
                        for k, v in out.items()]}
