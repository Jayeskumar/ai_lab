"""EXP-C04-09: OEIS look-ups for the sequences of cycle C04 (Historian)."""

import json

from lab import oeis
from lab.paths import RESULTS

META = {
    "id": "EXP-C04-09",
    "cycle": "C04",
    "title": "Novelty checks of C04 sequences against the OEIS",
    "agent": "Historian and Novelty Analyst",
    "question": "Which derivation-length and game sequences of cycle C04 are already catalogued?",
    "hypothesis": "Quadratic/exponential complexity sequences and the octal-game Grundy sequences are known; the "
                  "derivational complexity of aab -> ba may not be.",
    "assumptions": ["OEIS search API, cached in cache/oeis", "a match must be read: equal terms need not mean the "
                    "same definition"],
    "methodology": "Query the first terms (skipping leading zeros where they make the query trivial); record hits.",
    "falsification": "A catalogued sequence for something labelled potentially novel.",
}


def run():
    e3 = json.load(open(RESULTS / "EXP-C04-03.json"))["results"]["per_rule"]
    e4 = json.load(open(RESULTS / "EXP-C04-04.json"))["results"]
    e8 = {"->".join(r["rule"]): r for r in json.load(open(RESULTS / "EXP-C04-08.json"))["results"]["rows"]}
    seqs = {
        "D_max aab->ba (n - 1 - kappa(n))": e4["D_simulated_n0_21"][3:],
        "n - D(n) for aab->ba (1 + kappa(n))": e4["n_minus_D_formula_up_to_64"][1:40],
        "D_max aab->aba (floor(n(n-1)/6))": e3["aab->aba"]["D_max"][3:],
        "D_max aab->baa (floor(n^2/8))": e3["aab->baa"]["D_max"][3:],
        "D_max ab->ba (floor(n^2/4))": e3["ab->ba"]["D_max"][2:],
        "D_max ab->bba (2^(n-1)-1)": e3["ab->bba"]["D_max"][2:],
        "Grundy aa->b on a^n (Dawson's Kayles 0.07)": e8["aa->b"]["first_40"],
        "Grundy aa->ab on a^n (Officers 0.6)": e8["aa->ab"]["first_40"],
        "Grundy aaa->b on a^n (octal 0.007)": e8["aaa->b"]["first_40"],
        "Grundy aaa->ab on a^n (octal 0.06)": e8["aaa->ab"]["first_40"],
        "Grundy aaa->aba on a^n (octal 0.4)": e8["aaa->aba"]["first_40"],
    }
    out = {}
    for name, terms in seqs.items():
        res = oeis.novelty_check(terms)
        out[name] = {"terms": terms[:30], "status": res["status"], "hits": res.get("hits", [])[:3]}
    nomatch = [k for k, v in out.items() if v["status"] == "NO MATCH"]
    errors = [k for k, v in out.items() if v["status"] == "ERROR"]
    return {
        "checks": out,
        "no_match": nomatch,
        "errors": errors,
        "summary": [f"{len(seqs)} sequences checked; no OEIS match: {nomatch}; errors: {errors}"] +
                   [f"{k}: {v['status']} {[h['anumber'] + ' ' + h['name'][:60] for h in v['hits'][:1]]}"
                    for k, v in out.items()],
    }
