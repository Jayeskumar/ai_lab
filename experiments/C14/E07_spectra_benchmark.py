"""EXP-C14-07: computing spectra of product graphs from their factors (characters) vs. direct diagonalisation."""

import random
import time

import numpy as np

from systems.graph_products import NAMED_CODES, product, seidel

META = {
    "id": "EXP-C14-07",
    "cycle": "C14",
    "title": "Spectra of symmetric-difference, strong, co-normal and Cartesian products from the factors",
    "agent": "Application Researcher",
    "question": "How much faster and how accurate is it to obtain the spectrum of a product graph from its factors "
                "via the Kronecker characters (Theorems 4-6) instead of diagonalising the product matrix?",
    "hypothesis": "The factor route is exact up to rounding (max error < 1e-8 relative to the spectral norm) and "
                  "asymptotically faster (O(n^3 + m^3 + nm log nm) vs O((nm)^3)); this is the standard Kronecker "
                  "eigenvalue speed-up, newly applicable to the symmetric-difference product via Seidel matrices.",
    "assumptions": ["Erdos-Renyi G(n, 1/2) factors with n = m in {10, 20, 30, 40} (seeded)",
                    "baseline: numpy.linalg.eigvalsh on the full (nm x nm) matrix",
                    "timings are machine-dependent and stored under 'timings' (excluded from the result hash)"],
    "methodology": "XOR: Seidel spectrum = {(s+1)(t+1) - 1}; strong: adjacency spectrum = {(a+1)(b+1) - 1}; "
                   "co-normal: spectrum of J - A multiplies; Cartesian: adjacency spectrum = {a + b}. Compare sorted "
                   "spectra and wall-clock times (median of 3).",
    "falsification": "Max deviation above 1e-8 * spectral norm, or no speed-up at nm = 1600.",
    "seed": 1407,
}


def rand_graph(rng, n):
    G = np.zeros((n, n), dtype=np.int8)
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < 0.5:
                G[i, j] = G[j, i] = 1
    return G


def med(f, k=3):
    ts, out = [], None
    for _ in range(k):
        t0 = time.perf_counter()
        out = f()
        ts.append(time.perf_counter() - t0)
    return out, sorted(ts)[k // 2]


def run():
    rng = random.Random(META["seed"])
    eig = lambda M: np.linalg.eigvalsh(np.asarray(M, dtype=float))
    J = lambda n: np.ones((n, n))
    cases = {
        "symmetric difference": (NAMED_CODES["symmetric difference"], lambda G: seidel(G) + np.eye(len(G)),
                                 "mult", lambda P: seidel(P) + np.eye(len(P))),
        "strong": (NAMED_CODES["strong"], lambda G: G + np.eye(len(G)), "mult", lambda P: P + np.eye(len(P))),
        "co-normal": (NAMED_CODES["co-normal"], lambda G: J(len(G)) - G, "mult", lambda P: J(len(P)) - P),
        "cartesian": (NAMED_CODES["cartesian"], lambda G: G, "add", lambda P: P),
    }
    acc, timings = {}, {}
    for n in (10, 20, 30, 40):
        G, H = rand_graph(rng, n), rand_graph(rng, n)
        for name, (code, M, kind, Mprod) in cases.items():
            P = product(code, G, H)
            direct, t_direct = med(lambda: np.sort(eig(Mprod(P))))

            def factored():
                a, b = eig(M(G)), eig(M(H))
                v = np.outer(a, b).ravel() if kind == "mult" else np.add.outer(a, b).ravel()
                return np.sort(v)
            fact, t_fact = med(factored)
            err = float(np.max(np.abs(direct - fact)) / max(1.0, np.max(np.abs(direct))))
            acc[f"{name} n=m={n}"] = err
            timings[f"{name} n=m={n}"] = {"direct_s": round(t_direct, 5), "factored_s": round(t_fact, 6),
                                          "speedup": round(t_direct / max(t_fact, 1e-9), 1)}
    worst = max(acc.values())
    return {
        "relative_errors": acc,
        "max_relative_error_below_1e-8": worst < 1e-8,
        "timings": timings,
        "summary": [f"max relative spectral error over 16 cases: {worst:.1e} (< 1e-8: {worst < 1e-8})",
                    "timings (machine-dependent) are under 'timings'"],
    }
