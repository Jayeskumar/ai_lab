"""EXP-C11-04: code lengths on data computed in-repo (prime gaps, posting-list gaps)."""

import numpy as np

from systems.code_bench import Empirical, expected_length, tuned_golomb
from systems.codes import ExpGolomb, PatternCode, baseline_codes

from experiments.C11.E03_synthetic_benchmarks import FIXED_PATTERNS

META = {
    "id": "EXP-C11-04",
    "cycle": "C11",
    "title": "Benchmark on in-repo data: prime gaps up to 1e7 and simulated posting lists",
    "agent": "Application Researcher",
    "question": "Do the synthetic conclusions survive on concrete integer sequences?",
    "hypothesis": "On prime gaps (light tail, mean ~15) gamma-like codes or Fibonacci win; on bursty posting-list "
                  "gaps (heavy-tailed mixture) pattern codes beat both classical universal codes and a tuned Golomb "
                  "code; on homogeneous posting lists (geometric gaps) tuned Golomb wins.",
    "assumptions": ["primes <= 1e7 by sieve (664579 primes); gaps coded raw and halved (gap/2, first gap dropped)",
                    "posting lists: 1e5 geometric(0.001) gaps; bursty: 100 segments x 1000 gaps with p drawn from "
                    "{0.1, 0.01, 0.001, 0.0001}", "seeded numpy generator", "zeroth-order empirical entropy as "
                    "reference (codes are memoryless)"],
    "methodology": "Average bits per value for every code (exact, from the empirical distribution); tuned codes are "
                   "tuned on the same data (optimistic for them).",
    "falsification": "Pattern codes never best among universal codes on these data.",
    "seed": 1107,
}


def primes_upto(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0]


def datasets(seed=META["seed"]):
    rng = np.random.default_rng(seed)
    P = primes_upto(10 ** 7)
    gaps = np.diff(P)
    halved = gaps[1:] // 2
    post = rng.geometric(0.001, size=100_000)
    ps = rng.choice([0.1, 0.01, 0.001, 0.0001], size=100)
    bursty = np.concatenate([rng.geometric(p, size=1000) for p in ps])
    return [Empirical("prime gaps <= 1e7 (raw)", gaps), Empirical("prime gaps <= 1e7 (halved)", halved),
            Empirical("posting list geometric(0.001)", post), Empirical("bursty posting list (mixture)", bursty)]


def run():
    data = datasets()
    universal = baseline_codes() + [PatternCode(p) for p in FIXED_PATTERNS]
    table = {}
    for d in data:
        row = {c.name: round(expected_length(c, d), 4) for c in universal}
        tg = tuned_golomb(d)
        best_eg = min((expected_length(ExpGolomb(k), d), k) for k in range(0, 31))
        row[f"tuned Golomb(M={tg['golomb_M']})"] = round(tg["golomb_E"], 4)
        row[f"tuned Exp-Golomb(k={best_eg[1]})"] = round(best_eg[0], 4)
        fixed = {k: v for k, v in row.items() if not k.startswith("tuned")}
        classical = {k: v for k, v in fixed.items() if not k.startswith("T_")}
        bf, bc, ba = min(fixed, key=fixed.get), min(classical, key=classical.get), min(row, key=row.get)
        table[d.name] = {"count": d.size, "max": d.nmax, "entropy_bits": round(d.entropy, 4), "bits_per_value": row,
                         "best_fixed_universal": [bf, row[bf]], "best_classical": [bc, row[bc]], "best_overall": [ba, row[ba]]}
    return {
        "table": table,
        "summary": [f"{k} (n={v['count']}, H0={v['entropy_bits']}): best classical {v['best_classical']}, best fixed "
                    f"{v['best_fixed_universal']}, best overall {v['best_overall']}" for k, v in table.items()],
    }
