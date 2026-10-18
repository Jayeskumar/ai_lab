"""EXP-C02-07: critical carry rules (sum b = m) fail to terminate from EVERY sufficiently large unary start."""

import itertools
from math import gcd

import numpy as np

from experiments.C02.E03_carry_rule_survey import sweep

META = {
    "id": "EXP-C02-07",
    "cycle": "C02",
    "title": "Critical rules: non-termination from all large unary starts and the spectral gap",
    "agent": "Formal Verifier",
    "question": "Is non-termination of critical rules (sum b = m) a property of all large starts, as a spectral "
                "argument predicts?",
    "hypothesis": "T-C02-12: if sum b = m and gcd{j : b_j > 0} = 1, the window map's linearisation has the simple "
                  "eigenvalue 1 (eigenvector T = tail sums) and all other eigenvalues of modulus < 1; consequently "
                  "every unary start n >= n0 reaches a window dominating T and never terminates.",
    "assumptions": ["all critical rules with m <= 5, J <= 4, b_j <= 4 and gcd of support 1 (b_J > 0)",
                    "starts n = 1..2000"],
    "methodology": "For each rule: eigenvalues of the J x J linear map (A x)_i = x_(i+1) + (b_i/m) x_1; sweep every "
                   "start up to 2000 with periodic/pumping certificates; record the largest terminating start n0 - 1 "
                   "and check that every larger start has a certificate.",
    "falsification": "A rule with an eigenvalue of modulus >= 1 other than the simple eigenvalue 1, or a terminating "
                     "start after the first certified one beyond a stable tail.",
}


def linear_map(m, b):
    J = len(b)
    A = np.zeros((J, J))
    for i in range(J - 1):
        A[i, i + 1] = 1.0
    for i in range(J):
        A[i, 0] += b[i] / m
    return A


def run():
    rows, spectral_viol, tail_viol = [], [], []
    for m in range(2, 6):
        for J in range(1, 5):
            for b in itertools.product(range(5), repeat=J):
                if b[-1] == 0 or sum(b) != m:
                    continue
                g = 0
                for j, bj in enumerate(b, start=1):
                    if bj:
                        g = gcd(g, j)
                if g != 1:
                    continue
                ev = np.linalg.eigvals(linear_map(m, b))
                mods = sorted(abs(ev), reverse=True)
                one = min(abs(ev - 1))
                rho = mods[1] if len(mods) > 1 else 0.0
                if one > 1e-9 or (len(mods) > 1 and rho >= 1 - 1e-9) or (len(mods) > 1 and abs(mods[0] - 1) > 1e-9):
                    spectral_viol.append([m, list(b)])
                kinds = [sweep(n, m, b)[0] for n in range(1, 2001)]
                terminating = [n for n, k in zip(range(1, 2001), kinds) if k == "stable"]
                unknown = [n for n, k in zip(range(1, 2001), kinds) if k == "unknown"]
                last_term = max(terminating) if terminating else 0
                # every start after the last terminating one must be certified (no 'unknown')
                tail_ok = all(k == "glider" for k in kinds[last_term:])
                if not tail_ok:
                    tail_viol.append([m, list(b)])
                rows.append({"m": m, "b": list(b), "rho_second_eigenvalue": round(float(rho), 6),
                             "largest_terminating_start": last_term, "n_terminating_starts": len(terminating),
                             "unknown": len(unknown), "tail_all_certified": tail_ok})
    return {
        "n_rules": len(rows),
        "rows": rows,
        "spectral_violations": spectral_viol,
        "tail_violations": tail_viol,
        "max_largest_terminating_start": max(r["largest_terminating_start"] for r in rows),
        "summary": [
            f"{len(rows)} critical rules with gcd-1 support (m <= 5, J <= 4): spectral violations {len(spectral_viol)}",
            f"every start beyond the largest terminating one is certified non-terminating: "
            f"{len(tail_viol) == 0} (largest terminating start over all rules: "
            f"{max(r['largest_terminating_start'] for r in rows)})",
            f"max second-eigenvalue modulus: {max(r['rho_second_eigenvalue'] for r in rows)}",
        ],
    }
