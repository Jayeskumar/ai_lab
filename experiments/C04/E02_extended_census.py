"""EXP-C04-02: does a one-rule system with |l| <= 3 terminate iff l is not a factor of r?"""

from collections import Counter

from systems.derivations import (check_self_embedding, classify_termination, derivation_graph, graph_values,
                                 GraphLimit, linear_interpretation, self_embedding,
                                 weighted_factor_certificate)
from systems.rewriting import words

META = {
    "id": "EXP-C04-02",
    "cycle": "C04",
    "title": "Extended termination census (|l| <= 3, |r| <= 5) and the factor hypothesis",
    "agent": "Mathematical Inventor",
    "question": "In EXP-C04-01 every non-terminating rule had l as a factor of r. Is that a law?",
    "hypothesis": "H-C04-0 (bold): a one-rule system l -> r with |l| <= 3 terminates iff l is not a factor of r.",
    "assumptions": ["System A over {a,b}", "1 <= |l| <= 3, 0 <= |r| <= 5, l != r: 868 rules"],
    "methodology": "Certificate cascade of EXP-C04-01, then linear interpretations with coefficients <= 7, "
                   "integer weighted factor counts (|f| <= 4) found by LP and re-verified exactly, and a deeper "
                   "self-embedding search (seeds up to length 10). Undecided rules get bounded evidence.",
    "falsification": "A non-terminating rule whose lhs is not a factor of its rhs refutes H-C04-0.",
}


def run():
    lhs = [w for L in (1, 2, 3) for w in words("ab", L)]
    rhs = [""] + [w for L in range(1, 6) for w in words("ab", L)]
    rules = [(l, r) for l in lhs for r in rhs if l != r]
    seeds = [w for L in range(1, 11) for w in words("ab", L)]
    rows = []
    for rule in rules:
        c = classify_termination(rule)
        if c["status"] == "UNKNOWN":
            li = linear_interpretation(rule, max_coef=7, max_const=7)
            if li:
                c = {"status": "TERMINATING", "proof": "linear interpretation (coef <= 7)", "certificate": li}
        if c["status"] == "UNKNOWN":
            wf = weighted_factor_certificate(rule)
            if wf:
                c = {"status": "TERMINATING", "proof": "weighted factor count (LP, exact check)", "certificate": wf}
        if c["status"] == "UNKNOWN":
            path = self_embedding(rule, seeds, max_depth=30, max_len=70, max_states=40000)
            if path:
                c = {"status": "NON-TERMINATING", "proof": "self-embedding (deep)", "certificate": path}
        row = {"rule": list(rule), "status": c["status"], "proof": c.get("proof"),
               "lhs_factor_of_rhs": rule[0] in rule[1]}
        if c["status"] == "NON-TERMINATING":
            row["certificate"] = c["certificate"]
            row["certificate_ok"] = check_self_embedding(rule, c["certificate"])
        elif "certificate" in c:
            row["certificate"] = c["certificate"]
        rows.append(row)
    unknown = [r for r in rows if r["status"] == "UNKNOWN"]
    evidence = {}
    for r in unknown:
        rule = tuple(r["rule"])
        best = None
        for N in range(4, 13):
            starts = [w for L in range(0, N + 1) for w in words("ab", L)]
            try:
                g = derivation_graph(starts, rule, limit=200_000)
                v = graph_values(g)
                best = {"all_words_up_to_length": N, "max_derivation": max(v[w][1] for w in starts),
                        "max_derivation_by_length": [max(v[w][1] for w in starts if len(w) == L) for L in range(N + 1)]}
            except (GraphLimit, ValueError):
                break
        evidence["->".join(rule)] = best
    counter_examples = [r for r in rows if r["status"] == "NON-TERMINATING" and not r["lhs_factor_of_rhs"]]
    return {
        "n_rules": len(rows),
        "by_status": dict(Counter(r["status"] for r in rows)),
        "by_proof": dict(Counter(str(r["proof"]) for r in rows)),
        "bad_certificates": [r["rule"] for r in rows if r.get("certificate_ok") is False],
        "h0_counterexamples": [{"rule": r["rule"], "certificate": r["certificate"]} for r in counter_examples],
        "unknown": [r["rule"] for r in unknown],
        "unknown_evidence": evidence,
        "rows": rows,
        "summary": [
            f"{len(rows)} rules: {dict(Counter(r['status'] for r in rows))}",
            f"H-C04-0 counterexamples (non-terminating, l not a factor of r): {len(counter_examples)}, e.g. "
            f"{counter_examples[0]['rule'] if counter_examples else None} via {counter_examples[0]['certificate'] if counter_examples else None}",
            f"undecided rules: {len(unknown)} {[ '->'.join(r['rule']) for r in unknown]}",
        ],
    }
