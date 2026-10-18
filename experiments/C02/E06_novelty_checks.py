"""EXP-C02-06: OEIS look-ups for the integer sequences produced in cycle C02 (Historian)."""

import json

from lab import oeis
from lab.paths import RESULTS
from systems.exchange import stabilize_carry

META = {
    "id": "EXP-C02-06",
    "cycle": "C02",
    "title": "Novelty checks of C02 sequences against the OEIS",
    "agent": "Historian and Novelty Analyst",
    "question": "Are the sequences produced by exchange systems already catalogued?",
    "hypothesis": "Integer-base and rational-base sequences are known; the Fibonacci exchange derivation lengths "
                  "and representations in the emergent base r = 1.3028 (3[k] -> [k+1]+[k+2]) may not be.",
    "assumptions": ["OEIS search API (responses cached in cache/oeis for reproducibility)",
                    "absence of a match is weak evidence of novelty only"],
    "methodology": "Query the first terms of each sequence; if there is no hit, query a shifted window.",
    "falsification": "An OEIS entry matching a sequence labelled potentially novel.",
}


def rep_as_int(n, m, b):
    c = stabilize_carry((n,), m, b)[0]
    return int("".join(str(x) for x in reversed(c)) or "0")


def run():
    fib = json.load(open(RESULTS / "EXP-C02-02.json"))["results"]
    seqs = {
        "fibonacci_exchange_max_derivation_length": fib["max_len_seq"][1:],
        "fibonacci_exchange_min_derivation_length": fib["min_len_seq"][1:],
        "base_3/2_representations (rule 3[k]->2[k+1])": [rep_as_int(n, 3, (2,)) for n in range(1, 25)],
        "base_1.3028_representations (rule 3[k]->[k+1]+[k+2])": [rep_as_int(n, 3, (1, 1)) for n in range(1, 25)],
        "base_1.3028_digit_sums": [sum(stabilize_carry((n,), 3, (1, 1))[0]) for n in range(1, 41)],
        "base_1.3028_lengths": [len(stabilize_carry((n,), 3, (1, 1))[0]) for n in range(1, 41)],
        "base_sqrt(3)/rule 3[k]->[k+2] digit sums": [sum(stabilize_carry((n,), 3, (0, 1))[0]) for n in range(1, 41)],
        "rule 4[k]->[k+1]+2[k+2] representations": [rep_as_int(n, 4, (1, 2)) for n in range(1, 25)],
        "rule 4[k]->[k+1]+[k+2]+[k+3] representations": [rep_as_int(n, 4, (1, 1, 1)) for n in range(1, 25)],
    }
    out = {}
    for name, terms in seqs.items():
        res = oeis.novelty_check(terms)
        out[name] = {"terms": terms[:30], "status": res["status"], "hits": res.get("hits", [])[:3],
                     "query": res.get("query")}
    novel = [k for k, v in out.items() if v["status"] == "NO MATCH"]
    return {
        "checks": out,
        "no_match": novel,
        "summary": [f"{len(seqs)} sequences checked; no OEIS match for: {novel}"] +
                   [f"{k}: {v['status']} {[h['anumber'] for h in v['hits']]}" for k, v in out.items()],
    }
