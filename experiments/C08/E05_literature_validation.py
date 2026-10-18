"""EXP-C08-05: validate the circle-product implementation against the OEIS (Historian)."""

from lab import oeis
from systems.circle import two_term

META = {
    "id": "EXP-C08-05",
    "cycle": "C08",
    "title": "Implementation check: Knuth's product table versus the OEIS",
    "agent": "Historian and Novelty Analyst",
    "question": "Does our circle product with G = 1,2,3,5,... and s = 2 coincide with Knuth's Fibonacci product "
                "as catalogued in the OEIS?",
    "hypothesis": "The antidiagonal reading of the table n o k (n, k >= 1) matches an OEIS entry for Knuth's "
                  "circle product.",
    "assumptions": ["OEIS search API (cached)"],
    "methodology": "Read the table by antidiagonals (n + k constant, n increasing) and search the OEIS; also "
                   "search the first row (1 o k).",
    "falsification": "No match, or a match to an unrelated sequence.",
}


def run():
    F = two_term(1, 1, 2)
    anti = [F.circle(n, d - n, 2) for d in range(2, 10) for n in range(1, d)]
    row1 = [F.circle(1, k, 2) for k in range(1, 25)]
    res_anti = oeis.novelty_check(anti)
    res_row = oeis.novelty_check(row1)
    return {
        "antidiagonals": anti,
        "row_1": row1,
        "oeis_antidiagonals": {"status": res_anti["status"], "hits": res_anti.get("hits", [])[:3]},
        "oeis_row_1": {"status": res_row["status"], "hits": res_row.get("hits", [])[:3]},
        "summary": [f"table by antidiagonals {anti[:12]}...: {res_anti['status']} "
                    f"{[h['anumber'] + ' ' + h['name'][:60] for h in res_anti.get('hits', [])[:2]]}",
                    f"first row 1 o k {row1[:10]}...: {res_row['status']} "
                    f"{[h['anumber'] + ' ' + h['name'][:60] for h in res_row.get('hits', [])[:2]]}"],
    }
