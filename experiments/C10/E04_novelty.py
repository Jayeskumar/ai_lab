"""EXP-C10-04: OEIS checks for the counting-cost sequences (Historian)."""

from lab import oeis
from systems.counting_cost import changes, zeckendorf

META = {
    "id": "EXP-C10-04",
    "cycle": "C10",
    "title": "OEIS look-ups for Zeckendorf counting-cost sequences",
    "agent": "Historian and Novelty Analyst",
    "question": "Are the Zeckendorf counting-cost sequences already catalogued?",
    "hypothesis": "The per-increment change sequence (a 'Zeckendorf ruler function') and the block totals T_m are "
                  "likely known.",
    "assumptions": ["OEIS cache"],
    "methodology": "Query the per-step change counts c(n) = changes(Z(n-1), Z(n)) for n >= 1, the block totals "
                   "T_m and D_m = 2G_m - T_m.",
    "falsification": "n/a (literature check)",
}


def run():
    per_step = [changes(zeckendorf(n - 1), zeckendorf(n)) for n in range(1, 41)]
    G = [1, 2]
    while len(G) < 30:
        G.append(G[-1] + G[-2])
    T = [2 * G[m] - (m + 1) // 2 - 2 for m in range(0, 25)]
    out = {}
    for name, seq in (("per_step_changes", per_step), ("T_m", T[1:]), ("T_m_closed_form_check", T[:12])):
        r = oeis.novelty_check(seq)
        out[name] = {"terms": seq[:24], "status": r["status"], "hits": r.get("hits", [])[:3]}
    return {"checks": out,
            "summary": [f"{k}: {v['status']} {[h['anumber'] + ' ' + h['name'][:50] for h in v['hits'][:2]]}"
                        for k, v in out.items()]}
