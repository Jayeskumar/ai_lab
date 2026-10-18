"""EXP-C15-01: the 16 two-element magma automata are the elementary CA rules 17m (calibration)."""

import numpy as np

from systems.magma_ca import (affine_form, all_tables, cols_are_permutations, cyclic_map, essential_variables,
                              functional_graph_stats, is_associative, is_commutative, is_constant, is_injective,
                              is_medial, is_surjective, light_cones, rows_are_permutations, streaming_width,
                              wolfram_rule)

META = {
    "id": "EXP-C15-01",
    "cycle": "C15",
    "title": "Two-element magma automata: elementary rules 17m, light cones, surjectivity and cyclic dynamics",
    "agent": "Mathematical Explorer",
    "question": "Which elementary CA rules are the automata c'_i = c_i * c_{i+1} of the 16 two-element magmas, and "
                "how do their light cones, streaming widths, surjectivity and cyclic dynamics look?",
    "hypothesis": "H-C15-0 (calibration): the 16 automata are exactly the elementary rules that ignore the left "
                  "neighbour, i.e. the multiples of 17; XOR (rule 102) has 2^popcount(t) essential cells "
                  "(Gould's sequence A001316) and bounded streaming width.",
    "assumptions": ["light cones to t = 18 (tables of 2^19 entries)", "cyclic rows of length L = 1..16",
                    "surjectivity and injectivity on bi-infinite rows by the pair-graph (Garden of Eden) criterion"],
    "methodology": "Compute the Wolfram number of each table, the essential variables and the forward/backward "
                   "ordered-BDD widths of F_t, nilpotency (F_t constant), pair-graph surjectivity/injectivity and "
                   "the functional graph of the global map on all cyclic rows of each length.",
    "falsification": "A rule number that is not a multiple of 17, or an XOR light cone that is not 2^popcount(t).",
}

T_MAX = 18


def run():
    rows = []
    for T in all_tables(2):
        e, fw, bw, nil = [], [], [], None
        for t, F in light_cones(T, T_MAX):
            e.append(len(essential_variables(F)))
            a, b = streaming_width(F)
            fw.append(a)
            bw.append(b)
            if nil is None and is_constant(F):
                nil = t
        cyc = {}
        for L in range(1, 17):
            st = functional_graph_stats(cyclic_map(T, L))
            cyc[str(L)] = [st["max_cycle"], st["max_transient"], st["bijective"]]
        rows.append({"table": T.tolist(), "rule": wolfram_rule(T), "associative": is_associative(T),
                     "commutative": is_commutative(T), "medial": is_medial(T), "affine": affine_form(T),
                     "row_permutive": rows_are_permutations(T), "col_permutive": cols_are_permutations(T),
                     "surjective": is_surjective(T), "injective": is_injective(T), "nilpotent_at": nil,
                     "essential": e, "width_fw": fw, "width_bw": bw, "cyclic": cyc})
    rules = sorted(r["rule"] for r in rows)
    xor = next(r for r in rows if r["rule"] == 102)
    gould = [2 ** bin(t).count("1") for t in range(T_MAX + 1)]
    surj = sorted(r["rule"] for r in rows if r["surjective"])
    inj = sorted(r["rule"] for r in rows if r["injective"])
    unbounded = sorted(r["rule"] for r in rows if min(r["width_fw"][-1], r["width_bw"][-1]) > 4)
    return {
        "rows": rows,
        "rules": rules,
        "all_multiples_of_17": all(x % 17 == 0 for x in rules),
        "xor_essential_is_gould": xor["essential"] == gould,
        "surjective_rules": surj,
        "injective_rules": inj,
        "rules_with_streaming_width_above_4_at_t18": unbounded,
        "summary": [f"rules: {rules} (all multiples of 17: {all(x % 17 == 0 for x in rules)})",
                    f"XOR (rule 102) essential cells = 2^popcount(t): {xor['essential'] == gould}",
                    f"surjective: {surj}; injective: {inj}",
                    f"streaming width > 4 at t = {T_MAX}: {unbounded}"],
    }
