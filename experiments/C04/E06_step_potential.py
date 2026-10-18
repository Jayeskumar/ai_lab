"""EXP-C04-06: every one-rule system has a potential that changes by the same constant at every step."""

from systems.derivations import borders, derivation_graph, graph_values
from systems.rewriting import one_step, words

from experiments.C04.E05_random_descent import normal_form_counts

META = {
    "id": "EXP-C04-06",
    "cycle": "C04",
    "title": "Constant-step potentials for one-rule systems; confluence versus random descent",
    "agent": "Formal Verifier",
    "question": "Why did no terminating one-rule system turn out confluent without random descent?",
    "hypothesis": "H-C04-3: for every rule l -> r (l != r) there are a letter c, an exponent K and delta != 0 such "
                  "that Phi(w) = sum over positions i with w_i = c of i^K (or Phi = |w| if |l| != |r|) satisfies "
                  "Phi(v) = Phi(u) + delta for every step u -> v. Hence all derivations between two words have equal "
                  "length, and a terminating one-rule system is confluent iff it has random descent.",
    "assumptions": ["binary rules with |l|, |r| <= 5 and ternary rules with |l|, |r| <= 3 for the potential",
                    "length-preserving binary rules with bordered lhs, |l| = 4, 5, words <= 10 for confluence/RD"],
    "methodology": "Construct (c, K, delta) as in the proof (first letter whose position power sums differ, least K); "
                   "check Phi(v) - Phi(u) = delta on every one-step pair from every word up to length 7. Separately "
                   "compare confluence and random descent on exhaustive derivation graphs.",
    "falsification": "A rule with no admissible (c, K), a step violating the constant change, or a confluent "
                     "length-preserving rule without random descent.",
}


def potential_spec(l, r, alphabet):
    if len(l) != len(r):
        return {"kind": "length", "delta": len(r) - len(l)}
    for c in alphabet:
        P = [j for j, x in enumerate(l) if x == c]
        Q = [j for j, x in enumerate(r) if x == c]
        for K in range(0, len(l) + 1):
            d = sum(j ** K for j in Q) - sum(j ** K for j in P)
            if d != 0:
                return {"kind": "moment", "letter": c, "K": K, "delta": d}
    return None


def phi(w, spec):
    if spec["kind"] == "length":
        return len(w)
    return sum(i ** spec["K"] for i, x in enumerate(w) if x == spec["letter"])


def run():
    checked_rules, steps_checked, bad = 0, 0, []
    max_K = 0
    for alphabet, maxlen in (("ab", 5), ("abc", 3)):
        ws = [w for L in range(1, maxlen + 1) for w in words(alphabet, L)]
        rhs = [""] + ws
        test_words = [w for L in range(0, 8 if alphabet == "ab" else 6) for w in words(alphabet, L)]
        for l in ws:
            for r in rhs:
                if l == r:
                    continue
                spec = potential_spec(l, r, alphabet)
                checked_rules += 1
                if spec is None:
                    bad.append({"rule": [l, r], "why": "no potential"})
                    continue
                max_K = max(max_K, spec.get("K", 0))
                for u in test_words:
                    for v in one_step(u, [(l, r)]):
                        steps_checked += 1
                        if phi(v, spec) - phi(u, spec) != spec["delta"]:
                            bad.append({"rule": [l, r], "u": u, "v": v})
                            break
    conf_vs_rd = {"tested": 0, "confluent": 0, "length_uniform": 0, "confluent_not_length_uniform": [],
                  "length_uniform_not_confluent_examples": [], "length_uniform_not_confluent": 0}
    for k in (4, 5):
        ws = list(words("ab", k))
        for l in ws:
            if not borders(l):
                continue
            for r in ws:
                if r == l:
                    continue
                starts = [w for L in range(0, 11) for w in words("ab", L)]
                succ = derivation_graph(starts, (l, r), limit=2_000_000)
                vals = graph_values(succ)
                nfc = normal_form_counts(succ)
                conf = all(nfc[w] == 1 for w in starts)
                rd = all(vals[w][0] == vals[w][1] for w in starts)
                conf_vs_rd["tested"] += 1
                conf_vs_rd["confluent"] += conf
                conf_vs_rd["length_uniform"] += rd
                if conf and not rd:
                    conf_vs_rd["confluent_not_length_uniform"].append([l, r])
                if rd and not conf:
                    conf_vs_rd["length_uniform_not_confluent"] += 1
                    if len(conf_vs_rd["length_uniform_not_confluent_examples"]) < 5:
                        w = next(x for x in starts if nfc[x] > 1)
                        conf_vs_rd["length_uniform_not_confluent_examples"].append(
                            {"rule": [l, r], "word": w, "derivation_length": vals[w][0]})
    return {
        "rules_checked": checked_rules,
        "one_step_pairs_checked": steps_checked,
        "violations": bad[:20],
        "n_violations": len(bad),
        "max_exponent_K_needed": max_K,
        "confluence_vs_random_descent_length_preserving": conf_vs_rd,
        "summary": [
            f"constant-step potential verified for {checked_rules} rules on {steps_checked} one-step pairs: "
            f"{len(bad)} violations (largest exponent K needed: {max_K})",
            f"length-preserving bordered rules |l| = 4, 5: {conf_vs_rd['tested']} tested, {conf_vs_rd['confluent']} "
            f"confluent (all of them length-uniform: {not conf_vs_rd['confluent_not_length_uniform']}), "
            f"{conf_vs_rd['length_uniform']} length-uniform, of which {conf_vs_rd['length_uniform_not_confluent']} "
            f"are not confluent",
        ],
    }
