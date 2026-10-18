"""EXP-C04-03: derivational complexity of the 162 terminating one-rule systems with |l|,|r| <= 3."""

from collections import Counter

import sympy as sp

from lab.seqtools import guess_recurrence
from systems.derivations import (GraphLimit, all_rules, classify_termination, derivation_graph, graph_values)
from systems.rewriting import words

META = {
    "id": "EXP-C04-03",
    "cycle": "C04",
    "title": "Derivational complexity of terminating one-rule systems (|l|, |r| <= 3)",
    "agent": "Mathematical Explorer",
    "question": "How long can derivations of a terminating one-rule system be, as a function of the length of the "
                "start word, and which growth classes occur?",
    "hypothesis": "H-C04-G: every terminating rule in the family has derivational complexity D(n) = max over words "
                  "of length n of the longest derivation that is linear, quadratic or exponential, and D(n) is "
                  "given by a linear recurrence (rational generating function).",
    "assumptions": ["the 162 rules proved terminating in EXP-C04-01", "exhaustive derivation graphs from all words "
                    "of length <= 12 (<= 8 for four exponential rules, extended to 20 by a verified formula)"],
    "methodology": "Exact min/max derivation lengths per word from the acyclic derivation graph; D_max(n), D_min(n); "
                   "minimal linear recurrence (Berlekamp-Massey, over-determined) and the moduli/multiplicities "
                   "of its characteristic roots give the growth class. Rules are grouped by the symmetries "
                   "reversal and letter exchange.",
    "falsification": "A rule whose D_max admits no over-determined recurrence, or a growth class other than "
                     "linear/quadratic/exponential.",
}

N_DEFAULT = 12
N_LONG = 17


def canonical(rule):
    """Representative of the orbit under reversal and a<->b exchange."""
    swap = str.maketrans("ab", "ba")
    l, r = rule
    orbit = [(l, r), (l[::-1], r[::-1]), (l.translate(swap), r.translate(swap)),
             (l[::-1].translate(swap), r[::-1].translate(swap))]
    return min(orbit)


def fast_length(word, rule):
    """Derivation length for the four doubling rules (all derivations have equal length, lhs unbordered).

    ab -> bba: scanning right to left, an 'a' crossing B b's costs B steps and doubles them.
    ab -> baa: scanning left to right, a 'b' crossing A a's costs A steps and doubles them.
    The mirrored rules are reduced by reversing the word.
    """
    l, r = rule
    if (l, r) == ("ba", "abb"):
        return fast_length(word[::-1], ("ab", "bba"))
    if (l, r) == ("ba", "aab"):
        return fast_length(word[::-1], ("ab", "baa"))
    steps = 0
    if (l, r) == ("ab", "bba"):
        B = 0
        for ch in reversed(word):
            if ch == "b":
                B += 1
            else:
                steps += B
                B *= 2
        return steps
    if (l, r) == ("ab", "baa"):
        A = 0
        for ch in word:
            if ch == "a":
                A += 1
            else:
                steps += A
                A *= 2
        return steps
    raise ValueError(rule)


def growth_class(seq):
    rec = guess_recurrence(seq)
    if rec is None:
        return {"class": "no recurrence found", "recurrence": None}
    c = rec[0]
    if not c:
        return {"class": "eventually zero", "recurrence": []}
    x = sp.Symbol("x")
    poly = sp.Poly(x ** len(c) - sum(sp.Rational(ci) * x ** (len(c) - 1 - i) for i, ci in enumerate(c)), x)
    roots = sp.roots(poly, multiple=False)
    if sum(roots.values()) != len(c):           # not all roots found symbolically: numeric fallback
        num = [complex(z) for z in sp.Poly(poly).nroots()]
        rho = max(abs(z) for z in num)
        mult_unit = 1
    else:
        rho = max(abs(complex(z)) for z in roots)
        mult_unit = max((m for z, m in roots.items() if abs(abs(complex(z)) - 1) < 1e-12), default=0)
    if rho > 1 + 1e-9:
        cls = f"exponential (base {rho:.6f})"
    elif mult_unit <= 1:
        cls = "bounded"
    else:
        cls = {2: "linear", 3: "quadratic", 4: "cubic"}.get(mult_unit, f"polynomial degree {mult_unit - 1}")
    return {"class": cls, "recurrence": [str(ci) for ci in c]}


def closed_form(seq, start=2):
    """Simplest floor((a n^2 + b n + c)/d) (a <= 2) matching seq[n] for all n >= start, or 2^(n-1) - 1."""
    ns = range(start, len(seq))
    if all(seq[n] == 2 ** (n - 1) - 1 for n in ns):
        return "2^(n-1) - 1"
    for d in range(1, 13):
        for a in (0, 1, 2):
            for b in sorted(range(-6, 7), key=abs):
                for c in sorted(range(-12, 13), key=abs):
                    if all((a * n * n + b * n + c) // d == seq[n] for n in ns):
                        return f"floor(({a} n^2 + {b} n + {c})/{d})"
    return None


def run():
    term = [r for r in all_rules() if classify_termination(r)["status"] == "TERMINATING"]
    per_rule = {}
    formula_checks = 0
    for rule in term:
        N = N_DEFAULT
        while True:
            starts = [w for L in range(0, N + 1) for w in words("ab", L)]
            try:
                vals = graph_values(derivation_graph(starts, rule, limit=400_000))
                break
            except GraphLimit:
                N -= 1
        dmax = [max(vals[w][1] for w in starts if len(w) == n) for n in range(N + 1)]
        dmin = [max(vals[w][0] for w in starts if len(w) == n) for n in range(N + 1)]
        if N < N_DEFAULT:                       # the doubling rules: extend with the verified formula
            for w in starts:
                assert fast_length(w, rule) == vals[w][0] == vals[w][1]
                formula_checks += 1
            for n in range(N + 1, 21):
                ws = list(words("ab", n))
                dmax.append(max(fast_length(w, rule) for w in ws))
                dmin.append(dmax[-1])
        gc = growth_class(dmax)
        if gc["class"] == "no recurrence found" and len(rule[1]) <= len(rule[0]):
            # quasi-polynomials with longer periods need more terms: extend (graphs stay small)
            N = N_LONG
            starts = [w for L in range(0, N + 1) for w in words("ab", L)]
            vals = graph_values(derivation_graph(starts, rule, limit=2_000_000))
            dmax = [max(vals[w][1] for w in starts if len(w) == n) for n in range(N + 1)]
            dmin = [max(vals[w][0] for w in starts if len(w) == n) for n in range(N + 1)]
            gc = growth_class(dmax)
        gc_min = growth_class(dmin)
        per_rule["->".join(rule)] = {"N_graph": N, "D_max": dmax, "D_min": dmin, **gc,
                                     "D_min_class": gc_min["class"]}
    classes = {}
    for key, info in per_rule.items():
        l, r = key.split("->")
        classes.setdefault("->".join(canonical((l, r))), []).append(key)
    reps = {}
    for rep, members in sorted(classes.items()):
        info = per_rule[rep]
        reps[rep] = {"members": members, "class": info["class"], "D_max": info["D_max"],
                     "D_max_closed_form_n_ge_2": closed_form(info["D_max"]),
                     "D_min_closed_form_n_ge_2": closed_form(info["D_min"]),
                     "D_min": info["D_min"], "recurrence": info["recurrence"], "D_min_class": info["D_min_class"]}
    cls_count = Counter(per_rule[k]["class"].split(" (")[0] for k in per_rule)
    no_form = [k for k, v in reps.items() if v["D_max_closed_form_n_ge_2"] is None]
    return {
        "per_rule": per_rule,
        "symmetry_classes": reps,
        "class_counts_rules": dict(cls_count),
        "class_counts_symmetry_classes": dict(Counter(v["class"].split(" (")[0] for v in reps.values())),
        "doubling_formula_checks": formula_checks,
        "classes_without_simple_closed_form": no_form,
        "highlights": {k: per_rule[k] for k in ("ab->ba", "ab->bba", "ab->baa", "ab->", "aa->a", "aa->b",
                                                  "aa->aba", "aab->baa", "aba->aab") if k in per_rule},
        "summary": [
            f"{len(per_rule)} terminating rules in {len(reps)} symmetry classes; growth classes (rules): {dict(cls_count)}",
            f"doubling-rule formula verified against exhaustive graphs on {formula_checks} words",
            f"symmetry classes without a floor((a n^2+b n+c)/d) or 2^(n-1)-1 closed form: {no_form}",
            f"ab->ba D_max: {per_rule['ab->ba']['D_max']}; ab->bba D_max: {per_rule['ab->bba']['D_max'][:14]}",
        ],
    }
