"""EXP-C16-03: Fibonacci pair maps of Laver tables, affine (anchored, odd-law, golden-law) magmas, nimbers, groups."""

import time

import numpy as np

from lab import oeis
from systems.laver import laver_table
from systems.magma_dynamics import (affine_table, analyze, generate_group, group_table, matrix_order_mod, pair_next,
                                    pisano)
from systems.mex import NIM_PRODUCT, table as mex_table

META = {
    "id": "EXP-C16-03",
    "cycle": "C16",
    "title": "Fibonacci dynamics in structured families: Laver tables, affine and anchored magmas, nimbers, groups",
    "agent": "Mathematical Explorer",
    "question": "What do the laws of the lab's structured magmas (left-distributivity, anchored associativity, the odd "
                "and golden laws of C06, nim arithmetic of C07, group laws) do to the cycle structure of the pair "
                "map (a, b) -> (b, b*a)?",
    "hypothesis": "H-C16-4 (bold, Inventor): for every Laver table A_n the maximal period of the pair map is a power "
                  "of 2. H-C16-7 (Formal Verifier): an affine magma x*y = x + beta*y + gamma whose pair map has a "
                  "fixed point has maximal period ord([[0,1],[beta,1]]) mod N; in particular the anchored associative "
                  "magma x + y + 1 has exactly the cycle structure of the Fibonacci numbers mod N (maximum: the "
                  "Pisano period). H-C16-8 (bold, Explorer): for every affine magma x*y = alpha x + beta y + gamma "
                  "with beta a unit the maximal period equals the order of the 3x3 affine matrix. H-C16-9: "
                  "nim-multiplication on [0, 2^(2^k)) has maximal period pi(2^(2^k) - 1) (40 and 360).",
    "assumptions": ["Laver tables A_0..A_10 (N <= 1024)", "anchored associative N <= 60; odd-law magmas "
                    "x + 1 + y/2 for odd N <= 61; golden-law magmas x + 1 + a y (a^2 + a = 1) for every root and "
                    "every N <= 200 in A089270", "300 random affine magmas with N <= 30 (seeded)",
                    "nimbers via the C07 mex tables", "groups S3, D4, Q8, A4, S4 as permutation groups"],
    "methodology": "Exact functional-graph analysis of every pair map; matrix orders computed by repeated "
                   "multiplication; comparisons with Pisano periods (OEIS A001175); OEIS checks of new sequences.",
    "falsification": "H-C16-4: a Laver table whose maximal period is not a power of 2. H-C16-7: a mismatch between "
                     "the period and the matrix order, or between the anchored and Fibonacci cycle structures. "
                     "H-C16-8: any affine magma whose maximal period differs from the 3x3 order. H-C16-9: maximal "
                     "periods other than 40 and 360.",
    "seed": 1616,
}


def order3(alpha, beta, gamma, N, limit=10 ** 6):
    A = np.array([[0, 1, 0], [beta % N, alpha % N, gamma % N], [0, 0, 1]], dtype=np.int64)
    M = A.copy()
    k = 1
    I = np.eye(3, dtype=np.int64) % N
    while not np.array_equal(M % N, I):
        M = (M @ A) % N
        k += 1
        if k > limit:
            return None
    return k


def is_pow2(x):
    return x > 0 and (x & (x - 1)) == 0


def cyclic(n):
    x = np.arange(n)
    return (x[:, None] + x[None, :]) % n


def run():
    rng = np.random.default_rng(META["seed"])
    timings = {}
    # Laver tables
    t0 = time.perf_counter()
    laver = {}
    for n in range(0, 11):
        T = laver_table(n)
        N = 2 ** n
        an = analyze(pair_next(T))
        two_cycles_ok = True
        if N > 1:
            top = N - 1
            for b in range(N):
                if b == top:
                    continue
                if not (T[b, top] == top and T[top, b] == b):
                    two_cycles_ok = False
        # the facts used in the proof of Theorem 11: (N-1)*y = y, x*(N-1) = N-1, x*y > x for x < N-1
        facts_ok = bool(np.array_equal(T[N - 1], np.arange(N)) and (T[:, N - 1] == N - 1).all() and
                        all(T[x].min() > x for x in range(N - 1)))
        laver[str(n)] = {"N": N, **an, "max_period_is_power_of_2": is_pow2(an["max_period"]),
                         "periods": sorted(an["cycle_lengths"]), "top_two_cycles": two_cycles_ok,
                         "laver_facts_hold": facts_ok,
                         "predicted_structure": an["cycle_lengths"] == ({1: 1} if N == 1 else {1: 1, 2: N - 1})}
    timings["laver"] = round(time.perf_counter() - t0, 2)
    laver_max = [laver[str(n)]["max_period"] for n in range(0, 11)]
    h4_counter = [n for n in range(0, 11) if not laver[str(n)]["max_period_is_power_of_2"]]
    # anchored associative vs Fibonacci
    anchored = {}
    for N in range(1, 61):
        a1 = analyze(pair_next(affine_table(N, 1, 1, 1)))
        a2 = analyze(pair_next(cyclic(N)))
        anchored[str(N)] = {"max_period": a1["max_period"], "pisano": pisano(N),
                            "same_cycle_structure_as_fibonacci": a1["cycle_lengths"] == a2["cycle_lengths"]}
    anchored_ok = all(v["max_period"] == v["pisano"] and v["same_cycle_structure_as_fibonacci"]
                      for v in anchored.values())
    # odd law
    odd = {}
    for N in range(3, 62, 2):
        h = (N + 1) // 2
        an = analyze(pair_next(affine_table(N, 1, h, 1)))
        odd[str(N)] = {"max_period": an["max_period"], "order_companion": matrix_order_mod(((0, 1), (h, 1)), N),
                       "n_cycles": an["n_cycles"]}
    odd_ok = all(v["max_period"] == v["order_companion"] for v in odd.values())
    odd_seq = [odd[str(N)]["max_period"] for N in range(3, 62, 2)]
    # golden law
    golden = {}
    for N in range(2, 201):
        roots = [a for a in range(N) if (a * a + a - 1) % N == 0]
        for a in roots:
            an = analyze(pair_next(affine_table(N, 1, a, 1)))
            golden[f"{N}/{a}"] = {"max_period": an["max_period"],
                                  "order_companion": matrix_order_mod(((0, 1), (a, 1)), N),
                                  "pisano": pisano(N)}
    golden_ok = all(v["max_period"] == v["order_companion"] for v in golden.values())
    golden_seq = []
    for N in sorted({int(k.split("/")[0]) for k in golden}):
        golden_seq.append(max(v["max_period"] for k, v in golden.items() if int(k.split("/")[0]) == N))
    # random affine magmas
    t0 = time.perf_counter()
    affine_rows, h8_counter = [], []
    for _ in range(300):
        N = int(rng.integers(2, 31))
        while True:
            beta = int(rng.integers(1, N)) if N > 1 else 0
            if np.gcd(beta, N) == 1:
                break
        alpha, gamma = int(rng.integers(0, N)), int(rng.integers(0, N))
        an = analyze(pair_next(affine_table(N, alpha, beta, gamma)))
        o3 = order3(alpha, beta, gamma, N)
        row = {"N": N, "alpha": alpha, "beta": beta, "gamma": gamma, "max_period": an["max_period"], "order3": o3}
        affine_rows.append(row)
        if an["max_period"] != o3:
            h8_counter.append(row)
    timings["affine"] = round(time.perf_counter() - t0, 2)
    # nimbers
    nim = {}
    for size, q1 in ((16, 15), (256, 255)):
        P = mex_table(NIM_PRODUCT, size)
        X = np.arange(size)[:, None] ^ np.arange(size)[None, :]
        ap, ax = analyze(pair_next(P)), analyze(pair_next(X))
        nim[str(size)] = {"nim_product_max_period": ap["max_period"], "pisano_of_group_order": pisano(q1),
                          "nim_product_periods": sorted(ap["cycle_lengths"]), "xor_periods": sorted(ax["cycle_lengths"])}
    # groups
    groups = {"S3": generate_group([(1, 0, 2), (1, 2, 0)]),
              "D4": generate_group([(1, 2, 3, 0), (0, 3, 2, 1)]),
              "A4": generate_group([(1, 2, 0, 3), (1, 0, 3, 2)]),
              "S4": generate_group([(1, 0, 2, 3), (1, 2, 3, 0)])}
    grp = {}
    for name, els in groups.items():
        T = group_table(els)
        an = analyze(pair_next(T))
        grp[name] = {"order": len(els), "max_period": an["max_period"], "periods": sorted(an["cycle_lengths"]),
                     "n_cycles": an["n_cycles"]}
    from experiments.C16.E02_quasigroups import quaternion_table
    an = analyze(pair_next(quaternion_table()))
    grp["Q8"] = {"order": 8, "max_period": an["max_period"], "periods": sorted(an["cycle_lengths"]),
                 "n_cycles": an["n_cycles"]}
    looks = {}
    for name, seq in (("laver_max_period", laver_max), ("odd_law_max_period_odd_N", odd_seq),
                      ("golden_law_max_period", golden_seq[:30])):
        r = oeis.novelty_check(seq)
        looks[name] = {"terms": seq[:30], "status": r["status"], "hits": r.get("hits", [])[:3]}
    return {
        "laver": laver,
        "H_C16_4_counterexamples": h4_counter,
        "anchored_associative": anchored,
        "anchored_equals_fibonacci": anchored_ok,
        "odd_law": odd,
        "odd_law_period_equals_companion_order": odd_ok,
        "golden_law": golden,
        "golden_law_period_equals_companion_order": golden_ok,
        "affine_random": affine_rows,
        "H_C16_8_counterexamples": h8_counter[:20],
        "H_C16_8_counterexample_count": len(h8_counter),
        "nimbers": nim,
        "groups": grp,
        "oeis": looks,
        "timings": timings,
        "summary": [
            "Laver A_0..A_10 max periods: " + ", ".join(str(x) for x in laver_max) +
            f"; not a power of 2 for n in {h4_counter}; cycle structure = 1 fixed point + N-1 two-cycles and "
            f"Laver's facts hold for all n <= 10: "
            f"{all(v['predicted_structure'] and v['laver_facts_hold'] for v in laver.values())}",
            f"anchored x+y+1 = Fibonacci cycle structure for N <= 60: {anchored_ok}",
            f"odd law: max period = ord([[0,1],[1/2,1]]) for odd N <= 61: {odd_ok}; golden law: max period = "
            f"ord([[0,1],[a,1]]) for all {len(golden)} (N, a) with N <= 200: {golden_ok}",
            f"random affine: max period != order of the 3x3 matrix in {len(h8_counter)} of 300 cases",
            "nim-product max periods: " + ", ".join(f"[0,{k}): {v['nim_product_max_period']} (pi = "
                                                    f"{v['pisano_of_group_order']})" for k, v in nim.items()),
            "groups max period: " + ", ".join(f"{k}: {v['max_period']}" for k, v in grp.items()),
            "OEIS: " + ", ".join(f"{k}: {v['status']}" for k, v in looks.items()),
        ],
    }
