"""EXP-C16-04: are Fibonacci recurrences in invented magmas usable as pseudo-random generators? (honest baselines)"""

import time

import numpy as np
from scipy import stats

META = {
    "id": "EXP-C16-04",
    "cycle": "C16",
    "title": "Magma Fibonacci generators versus PCG64 and an LCG on simple statistical tests",
    "agent": "Application Researcher",
    "question": "The longest pair-map periods found are n^2 (de Bruijn tables) and, for affine magmas on Z/2^32, the "
                "order of a matrix. Do such generators give usable pseudo-random numbers compared with standard "
                "generators?",
    "hypothesis": "H-C16-10 (Application Researcher): none of the magma generators passes the simple test battery "
                  "as well as PCG64; the anchored Fibonacci generator fails low-bit tests (Fibonacci numbers are not "
                  "uniformly distributed modulo 2^k) and the de Bruijn byte generator is too regular.",
    "assumptions": ["2^20 outputs per generator", "tests: chi-square of the top byte and of the low byte, serial "
                    "chi-square of consecutive top-byte pairs, lowest-bit period (searched up to 2^16), lag-1 "
                    "correlation; p-values from scipy.stats", "this is a sanity battery, not TestU01/PractRand"],
    "methodology": "Generators: G1 anchored associative magma on Z/2^32, x_{k+1} = x_k + x_{k-1} + 1; G2 affine magma "
                   "x_{k+1} = x_k + beta x_{k-1} + 1 (beta = 0x9E3779B9); G3 the de Bruijn byte magma (full period "
                   "65536 = the maximum for an order-2 byte recurrence; FKM construction); baselines PCG64 and the "
                   "LCG 1664525 x + 1013904223 mod 2^32.",
    "falsification": "A magma generator passing every test at the 1% level with a period comparable to the baselines.",
    "seed": 160416,
}

M32 = (1 << 32) - 1
N_OUT = 1 << 20


def fib_anchored(n, x0=12345, x1=67890):
    out = np.empty(n, dtype=np.uint64)
    a, b = x0, x1
    for i in range(n):
        a, b = b, (b + a + 1) & M32
        out[i] = b
    return out


def affine_mrg(n, beta=0x9E3779B9, gamma=1, x0=12345, x1=67890):
    out = np.empty(n, dtype=np.uint64)
    a, b = x0, x1
    for i in range(n):
        a, b = b, (b + beta * a + gamma) & M32
        out[i] = b
    return out


def lcg(n, seed=12345):
    out = np.empty(n, dtype=np.uint64)
    x = seed
    for i in range(n):
        x = (1664525 * x + 1013904223) & M32
        out[i] = x
    return out


def de_bruijn_bytes():
    """FKM: concatenation of the Lyndon words of length 1 and 2 over 0..255 in lexicographic order."""
    seq = []
    for a in range(256):
        seq.append(a)
        for b in range(a + 1, 256):
            seq.extend([a, b])
    return np.array(seq, dtype=np.uint64)


def chi2_bytes(x):
    obs = np.bincount(x.astype(np.int64), minlength=256)
    chi = float(((obs - obs.mean()) ** 2 / obs.mean()).sum())
    return chi, float(stats.chi2.sf(chi, 255)), float(stats.chi2.cdf(chi, 255))


def serial_pairs(x):
    pairs = x[:-1].astype(np.int64) * 256 + x[1:].astype(np.int64)
    obs = np.bincount(pairs, minlength=65536)
    e = obs.mean()
    chi = float(((obs - e) ** 2 / e).sum())
    return chi, float(stats.chi2.sf(chi, 65535)), float(stats.chi2.cdf(chi, 65535))


def bit_period(bits, limit=1 << 16):
    n = bits.size
    for p in range(1, min(limit, n // 4) + 1):
        if np.array_equal(bits[p:], bits[:-p]):
            return p
    return None


def battery(name, words, top_shift=24, is_bytes=False):
    if is_bytes:
        top = words
        low = words
    else:
        top = (words >> np.uint64(top_shift)) & np.uint64(255)
        low = words & np.uint64(255)
    c_top = chi2_bytes(top)
    c_low = chi2_bytes(low)
    ser = serial_pairs(top)
    u = words.astype(np.float64) / (256.0 if is_bytes else 2.0 ** 32)
    corr = float(np.corrcoef(u[:-1], u[1:])[0, 1])
    bp = bit_period((words & np.uint64(1)).astype(np.int8))
    # a two-sided criterion: a test fails if p < 0.01 (too irregular) or p > 0.99 (too regular)
    fails = []
    for label, (_, p_hi, p_lo) in (("top byte", c_top), ("low byte", c_low), ("serial pairs", ser)):
        if p_hi < 0.01:
            fails.append(f"{label}: non-uniform (p = {p_hi:.2g})")
        elif p_lo < 0.01:
            fails.append(f"{label}: too regular (p_lower = {p_lo:.2g})")
    if abs(corr) > 4 / np.sqrt(len(u)):
        fails.append(f"lag-1 correlation {corr:.4f}")
    if bp is not None:
        fails.append(f"lowest bit periodic with period {bp}")
    return {"name": name, "chi2_top": c_top[0], "p_top": c_top[1], "chi2_low": c_low[0], "p_low": c_low[1],
            "chi2_serial": ser[0], "p_serial": ser[1], "p_serial_lower": ser[2], "lag1_corr": corr,
            "lowest_bit_period": bp, "failures": fails, "passes_all": not fails}


def run():
    rng = np.random.default_rng(META["seed"])
    t0 = time.perf_counter()
    gens = {
        "G1 anchored Fibonacci x+y+1 on Z/2^32": fib_anchored(N_OUT),
        "G2 affine magma x + beta y + 1 on Z/2^32": affine_mrg(N_OUT),
        "B1 PCG64 (numpy)": rng.integers(0, 1 << 32, N_OUT, dtype=np.uint64),
        "B2 LCG 1664525x + 1013904223": lcg(N_OUT),
    }
    rows = [battery(k, v) for k, v in gens.items()]
    db = de_bruijn_bytes()
    reps = N_OUT // db.size
    rows.append(battery("G3 de Bruijn byte magma (period 65536)", np.tile(db, reps), is_bytes=True))
    gen_time = round(time.perf_counter() - t0, 2)
    return {
        "rows": rows,
        "pisano_period_2_32": 3 * (1 << 31),
        "timings": {"total": gen_time},
        "summary": [f"{r['name']}: " + ("passes all" if r["passes_all"] else "; ".join(r["failures"]))
                    for r in rows],
    }
