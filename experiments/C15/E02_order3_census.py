"""EXP-C15-02: census of the 1734 magmas of order 3 (up to isomorphism and anti-isomorphism) as automata."""

import time

import numpy as np

from systems.magma_ca import (affine_form, classes, cols_are_permutations, cyclic_map, essential_variables,
                              functional_graph_stats, is_associative, is_commutative, is_constant, is_injective,
                              is_medial, is_surjective, light_cones, rows_are_permutations, streaming_width)

META = {
    "id": "EXP-C15-02",
    "cycle": "C15",
    "title": "Order-3 magma automata: light cones, streaming widths, surjectivity and cyclic dynamics",
    "agent": "Mathematical Explorer",
    "question": "For all 1734 magmas of order 3 up to isomorphism and anti-isomorphism: how complex are the t-step "
                "local maps of c'_i = c_i * c_{i+1}, which automata are surjective, and how do they behave on "
                "cyclic rows?",
    "hypothesis": "H-C15-1 (bold, inventor): no intermediate growth - the streaming width lambda(t) (the smaller of "
                  "the forward and backward ordered-BDD widths of F_t) is either bounded or grows geometrically. "
                  "H-C15-2 (bold, inventor): bounded streaming width holds exactly for semigroups, affine magmas "
                  "x*y = ax + by + c over Z_3, and magmas whose light cone depends on at most two cells. "
                  "H-C15-3 (explorer): the automaton is surjective on bi-infinite rows iff the table has all rows or "
                  "all columns permutations (permutive).",
    "assumptions": ["light cones to t = 9 (tables of 3^10 entries)", "cyclic rows of length L = 1..7",
                    "growth classes judged on t <= 9 only: bounded = eventually 2-periodic from t = 5; linear = "
                    "lambda(t+2) - lambda(t) positive and constant on each parity for t = 4..7; geometric = "
                    "lambda(t+2) >= 1.8 lambda(t) for t = 5, 6, 7; other = the rest",
                    "statistics are invariant under anti-isomorphism (mirror)"],
    "methodology": "Canonical representatives by minimum code over the 12 (anti-)relabellings; for each: algebraic "
                   "properties, essential variables and widths of F_t (t <= 9), nilpotency, pair-graph surjectivity "
                   "and injectivity, functional-graph statistics of the global map on cyclic rows.",
    "falsification": "H-C15-1: a magma with growing but sub-geometric width. H-C15-2: a bounded-width magma outside "
                     "the three classes or a semigroup/affine magma with unbounded width. H-C15-3: a surjective "
                     "non-permutive table or a non-surjective permutive one.",
}

T_MAX = 9


def width_class(lam):
    if lam[5] == lam[7] == lam[9] and lam[6] == lam[8]:
        return "bounded"
    d = {t: lam[t + 2] - lam[t] for t in range(4, 8)}
    if all(v > 0 for v in d.values()) and d[4] == d[6] and d[5] == d[7]:
        return "linear"
    if all(lam[t + 2] >= 1.8 * lam[t] for t in (5, 6, 7)):
        return "geometric"
    return "other"


def restricted(T, S):
    """The sub-table on the set S if S is closed under *, else None."""
    S = sorted(S)
    if any(int(T[a, b]) not in S for a in S for b in S):
        return None
    idx = {v: i for i, v in enumerate(S)}
    return np.array([[idx[int(T[a, b])] for b in S] for a in S], dtype=np.int8)


def run():
    t0 = time.perf_counter()
    reps, sizes, _ = classes(3)
    rows = []
    for T, size in zip(reps, sizes):
        ess, lam, fwbw, nil = [], [], [], None
        image9 = None
        for t, F in light_cones(T, T_MAX):
            if t == T_MAX:
                image9 = sorted(int(v) for v in np.unique(F))
            E = essential_variables(F)
            ess.append(len(E))
            a, b = streaming_width(F)
            fwbw.append([a, b])
            lam.append(min(a, b))
            if nil is None and is_constant(F):
                nil = t
        cyc = {}
        for L in range(1, 8):
            st = functional_graph_stats(cyclic_map(T, L))
            cyc[str(L)] = [st["max_cycle"], st["max_transient"], st["bijective"]]
        aff = affine_form(T)
        assoc = is_associative(T)
        rp, cp = rows_are_permutations(T), cols_are_permutations(T)
        bounded_dep = nil is not None or max(ess) <= 2
        sub = restricted(T, image9)
        ev_assoc = sub is not None and is_associative(sub)
        ev_affine = sub is not None and (len(image9) == 1 or affine_form(sub) is not None)
        rows.append({"image_t9": image9, "eventually_associative": bool(ev_assoc), "eventually_affine": bool(ev_affine),"table": T.tolist(), "class_size": int(size), "associative": assoc,
                     "commutative": is_commutative(T), "medial": is_medial(T), "affine": aff is not None,
                     "affine_form": aff, "row_permutive": rp, "col_permutive": cp,
                     "surjective": is_surjective(T), "injective": is_injective(T), "nilpotent_at": nil,
                     "essential": ess, "widths": fwbw, "lambda": lam, "width_class": width_class(lam),
                     "bounded_dependence": bool(bounded_dep), "cyclic": cyc})
    # hypothesis checks
    inter = [r["table"] for r in rows if r["width_class"] in ("linear", "other")]
    linear = [r["table"] for r in rows if r["width_class"] == "linear"]
    bounded = [r for r in rows if r["width_class"] == "bounded"]
    h2_outside = [r["table"] for r in bounded if not (r["associative"] or r["affine"] or r["bounded_dependence"])]
    h2_unbounded_special = [r["table"] for r in rows if r["width_class"] != "bounded"
                            and (r["associative"] or r["affine"])]
    h3_bad = [r["table"] for r in rows if r["surjective"] != (r["row_permutive"] or r["col_permutive"])]
    explained = [r for r in bounded if r["associative"] or r["affine"] or r["bounded_dependence"]
                 or r["eventually_associative"] or r["eventually_affine"]]
    injective = [r["table"] for r in rows if r["injective"]]
    counts = {}
    for r in rows:
        counts[r["width_class"]] = counts.get(r["width_class"], 0) + 1
    tally = lambda key: sum(1 for r in rows if r[key])
    nilp = sum(1 for r in rows if r["nilpotent_at"] is not None)
    return {
        "n_classes": len(rows),
        "width_classes": counts,
        "n_associative": tally("associative"), "n_commutative": tally("commutative"), "n_medial": tally("medial"),
        "n_affine": tally("affine"), "n_surjective": tally("surjective"), "n_injective": tally("injective"),
        "n_nilpotent_t9": nilp, "n_bounded_dependence": tally("bounded_dependence"),
        "h1_intermediate": inter[:20], "h1_n_intermediate": len(inter), "linear_examples": linear[:20],
        "n_linear": len(linear), "bounded_explained_by_eventual_image": len(explained),
        "injective_tables": injective,
        "h2_bounded_outside_classes": h2_outside[:20], "h2_n_bounded_outside": len(h2_outside),
        "h2_semigroup_or_affine_unbounded": h2_unbounded_special[:20], "h2_n_special_unbounded": len(h2_unbounded_special),
        "h3_counterexamples": h3_bad[:20], "h3_n_counterexamples": len(h3_bad),
        "rows": rows,
        "timings": {"total_s": round(time.perf_counter() - t0, 1)},
        "summary": [f"{len(rows)} classes; width classes {counts}; nilpotent by t=9: {nilp}",
                    f"associative {tally('associative')}, commutative {tally('commutative')}, medial "
                    f"{tally('medial')}, affine {tally('affine')}, surjective {tally('surjective')}, injective "
                    f"{tally('injective')}, bounded dependence {tally('bounded_dependence')}",
                    f"H-C15-1 non-bounded, non-geometric magmas: {len(inter)} (linear: {len(linear)})",
                    f"bounded-width magmas explained by semigroup/affine/bounded dependence/eventual image: "
                    f"{len(explained)} of {len(bounded)}",
                    f"H-C15-2: bounded outside the three classes {len(h2_outside)}; semigroup/affine not bounded "
                    f"{len(h2_unbounded_special)}",
                    f"H-C15-3 counterexamples (surjective != permutive): {len(h3_bad)}"],
    }
