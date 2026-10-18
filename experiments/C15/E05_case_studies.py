"""EXP-C15-05: case studies - the fuse magma, Laver tables, GF(4), anchored models of C06, an order-4 band."""

import numpy as np

from lab import oeis
from systems.laver import laver_table
from systems.magma_ca import (FUSE, affine_form, cols_are_permutations, essential_variables, is_associative,
                              is_injective, is_surjective, light_cones, obdd_widths, rows_are_permutations,
                              streaming_width)

META = {
    "id": "EXP-C15-05",
    "cycle": "C15",
    "title": "Case studies: fuse widths to t = 12, Laver tables, GF(4), anchored affine models, an order-4 band",
    "agent": "Formal Verifier",
    "question": "Does the fuse magma's streaming width keep growing linearly beyond t = 9, and does the residual "
                "family of the lower-bound proof really separate? How do the lab's earlier structures (Laver tables, "
                "nimbers on [0,4), anchored models of C06) behave as automata? Is 'surjective iff permutive' special "
                "to orders <= 3?",
    "hypothesis": "The fuse magma has lambda(t) = t + 2 for t = 1..12, and the prefixes 2 (12)^b 2^(m-1-2b) give "
                  "pairwise distinct residuals at level m = t/2; the order-4 rectangular band (b,c)*(b',c') = (b,c') "
                  "is surjective (even injective) without being permutive.",
    "assumptions": ["light cones to t = 12 (fuse), t = 8 (order 4), t = 5 (order 8)"],
    "methodology": "Ordered-BDD widths and essential variables of F_t; explicit residual check for the lower-bound "
                   "family; pair-graph surjectivity/injectivity; OEIS look-ups of the sequences produced.",
    "falsification": "A fuse width differing from t + 2, coinciding residuals in the lower-bound family, or a "
                     "non-surjective or permutive rectangular band.",
}


def profile(T, t_max):
    out = {"essential": [], "width_fw": [], "width_bw": []}
    for t, F in light_cones(T, t_max):
        out["essential"].append(len(essential_variables(F)))
        a, b = streaming_width(F)
        out["width_fw"].append(a)
        out["width_bw"].append(b)
    return out


def fuse_residual_check(t):
    """At level m = t/2, count distinct residual functions among the prefixes 2 (12)^b 2^(m-1-2b)."""
    m = t // 2
    F = None
    for s, G in light_cones(FUSE, t):
        F = G
    flat = F.reshape(3 ** m, 3 ** (t + 1 - m))
    residuals = []
    for b in range(0, (m - 1) // 2 + 1):
        prefix = [2] + [1, 2] * b + [2] * (m - 1 - 2 * b)
        idx = 0
        for v in prefix:
            idx = idx * 3 + v
        residuals.append(flat[idx].tobytes())
    return len(residuals), len(set(residuals))


def run():
    out = {}
    # the fuse magma
    fz = profile(FUSE, 12)
    lam = [min(a, b) for a, b in zip(fz["width_fw"], fz["width_bw"])]
    out["fuse"] = {**fz, "lambda": lam, "lambda_is_t_plus_2": all(lam[t] == t + 2 for t in range(1, 13)),
                   "residual_family": {str(t): fuse_residual_check(t) for t in (6, 8, 10, 12)}}
    # Laver tables
    A2 = laver_table(2).astype(np.int8)
    A3 = laver_table(3).astype(np.int8)
    for name, T, tm in (("Laver A2 (order 4)", A2, 8), ("Laver A3 (order 8)", A3, 5)):
        p = profile(T, tm)
        out[name] = {**p, "associative": is_associative(T), "surjective": is_surjective(T),
                     "injective": is_injective(T)}
    # nimbers on [0,4): GF(4) multiplication and XOR
    gf4 = np.array([[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]], dtype=np.int8)
    xor4 = (np.arange(4)[:, None] ^ np.arange(4)[None, :]).astype(np.int8)
    for name, T in (("GF(4) multiplication", gf4), ("XOR on [0,4)", xor4)):
        p = profile(T, 8)
        out[name] = {**p, "associative": is_associative(T), "surjective": is_surjective(T),
                     "injective": is_injective(T)}
    # anchored models of C06 (affine over Z_N)
    for name, (a, N) in {"golden law N=5 (a=2)": (2, 5), "golden law N=11 (a=3)": (3, 11),
                         "odd law N=5 (a=3)": (3, 5)}.items():
        X, Y = np.arange(N)[:, None], np.arange(N)[None, :]
        T = ((X + 1 + a * Y) % N).astype(np.int8)
        out[name] = {"anchored": bool(all(T[x, 0] == (x + 1) % N for x in range(N))),
                     "row_permutive": rows_are_permutations(T), "col_permutive": cols_are_permutations(T),
                     "surjective": is_surjective(T), "injective": is_injective(T),
                     "affine_detected": affine_form(T) is not None if N <= 7 else "n/a (N > 7)",
                     "lambda_t4": min(streaming_width(list(light_cones(T, 4))[-1][1]))}
    # the order-4 rectangular band
    band = np.array([[2 * (x // 2) + (y % 2) for y in range(4)] for x in range(4)], dtype=np.int8)
    out["rectangular band 2x2 (order 4)"] = {"table": band.tolist(), "associative": is_associative(band),
                                             "row_permutive": rows_are_permutations(band),
                                             "col_permutive": cols_are_permutations(band),
                                             "surjective": is_surjective(band), "injective": is_injective(band)}
    # OEIS
    z3 = ((np.arange(3)[:, None] + np.arange(3)[None, :]) % 3).astype(np.int8)
    ess_z3 = [len(essential_variables(F)) for _, F in light_cones(z3, 12)]
    geo = [3, 3, 6, 9, 19, 42, 88, 183, 355, 649]
    queries = {"surjective tables n=1,2,3": [1, 6, 420], "x+y mod 3: essential cells of F_t": ess_z3,
               "widths of [[0,1,2],[2,0,0],[1,2,0]]": geo}
    out["oeis"] = {}
    for k, q in queries.items():
        r = oeis.novelty_check(q)
        out["oeis"][k] = {"query": q, "status": r["status"], "hits": r.get("hits", [])[:3]}
    out["summary"] = [
        f"fuse: lambda(t) = t + 2 for t = 1..12: {out['fuse']['lambda_is_t_plus_2']}; residual family "
        f"(count, distinct) {out['fuse']['residual_family']}",
        f"Laver A2: widths fw {out['Laver A2 (order 4)']['width_fw']}; A3 fw {out['Laver A3 (order 8)']['width_fw']}",
        f"GF(4) mult lambda bounded: {max(out['GF(4) multiplication']['width_fw'])}; XOR[0,4) widths "
        f"{max(out['XOR on [0,4)']['width_fw'])}",
        f"rectangular band order 4: surjective {out['rectangular band 2x2 (order 4)']['surjective']}, injective "
        f"{out['rectangular band 2x2 (order 4)']['injective']}, permutive "
        f"{out['rectangular band 2x2 (order 4)']['row_permutive'] or out['rectangular band 2x2 (order 4)']['col_permutive']}",
        "OEIS: " + "; ".join(f"{k}: {v['status']} {[h['anumber'] for h in v['hits']]}" for k, v in out["oeis"].items()),
    ]
    return out
