"""Skeptic checks for cycle C11 (pattern-terminated codes), independent of systems/codes.py.

Usage: python3 c11_checks.py <part>   parts: theory | codes | compare | oscillation | bench
Writes out/c11_<part>.json.
"""
import itertools
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent / "out"


# ---------------------------------------------------------------- basic objects (own implementation)
def first_occurrence_at_end(w, p):
    """True iff p occurs in w for the first time exactly at the end."""
    k = len(p)
    if len(w) < k or w[-k:] != p:
        return False
    return p not in w[:-1]


def periods(p):
    k = len(p)
    return [j for j in range(k) if p[j:] == p[:k - j]]


def counts_bruteforce(p, Lmax):
    return [sum(first_occurrence_at_end("".join(w), p) for w in itertools.product("01", repeat=L))
            for L in range(Lmax + 1)]


def counts_gf(p, Lmax):
    """Coefficients of x^k / (x^k + (1 - 2x) c_p(x)) by power-series division (exact integers)."""
    k = len(p)
    D = [0] * (Lmax + k + 2)
    for j in periods(p):
        D[j] += 1
        D[j + 1] -= 2
    D[k] += 1
    assert D[0] == 1
    f = [0] * (Lmax + 1)
    num = [0] * (Lmax + 1)
    if k <= Lmax:
        num[k] = 1
    for n in range(Lmax + 1):
        f[n] = num[n] - sum(D[i] * f[n - i] for i in range(1, n + 1) if i < len(D))
    return f


def counts_automaton(p, Lmax):
    """Number of words of length L whose first occurrence of p is at the end (KMP-free: suffix states)."""
    k = len(p)

    def step(s, ch):            # s = length of the longest suffix of the read word that is a prefix of p
        t = p[:s] + ch
        for l in range(min(len(t), k), -1, -1):
            if t.endswith(p[:l]):
                return l
        return 0

    trans = [[step(s, ch) for ch in "01"] for s in range(k)]
    vec = [0] * (k + 1)
    vec[0] = 1
    out = [0] * (Lmax + 1)
    for L in range(1, Lmax + 1):
        nv = [0] * (k + 1)
        for s in range(k):
            if vec[s]:
                for t in trans[s]:
                    nv[t] += vec[s]
        out[L] = nv[k]
        nv[k] = 0
        vec = nv
    return out


def growth(p):
    k = len(p)
    D = np.zeros(k + 1)
    for j in periods(p):
        D[j] += 1
        D[j + 1] -= 2
    D[k] += 1
    # smallest positive root of D (increasing powers) by bisection on (1/2, 1]
    def Dv(x):
        return float(np.polyval(D[::-1], x))
    # scan for first sign change (D > 0 on (0, 1/2], see Theorem 2)
    xs = np.linspace(0.5, 1.0, 20001)
    vals = np.polyval(D[::-1], xs)
    for i in range(1, len(xs)):
        if vals[i] <= 0:
            lo, hi = xs[i - 1], xs[i]
            for _ in range(80):
                mid = (lo + hi) / 2
                if Dv(mid) > 0:
                    lo = mid
                else:
                    hi = mid
            return 1 / hi
    return 1.0


def cum(c):
    out, acc = [], 0
    for x in c:
        acc += x
        out.append(acc)
    return out


# ---------------------------------------------------------------- part: theory (Theorems 1-3, H-C11-2)
def part_theory():
    res = {}
    # Theorem 1(c): GF = brute force for all patterns of length 1..6, L <= 16; automaton too
    bad = []
    for k in range(1, 7):
        for p in ("".join(t) for t in itertools.product("01", repeat=k)):
            bf = counts_bruteforce(p, 16)
            if bf != counts_gf(p, 16) or bf != counts_automaton(p, 16):
                bad.append(p)
    res["thm1_gf_vs_bruteforce_bad"] = bad
    # Theorem 1(d): T_11 codeword set = Fibonacci C1 codeword set (Zeckendorf lsb-first + '1'), lengths <= 18
    F = [1, 2]
    while len(F) < 40:
        F.append(F[-1] + F[-2])

    def c1(n):
        k = max(i for i in range(len(F)) if F[i] <= n)
        d = ["0"] * (k + 1)
        m = n
        for i in range(k, -1, -1):
            if F[i] <= m:
                d[i] = "1"
                m -= F[i]
        return "".join(d) + "1"

    C1set = {c1(n) for n in range(1, F[17])}
    T11set = {"".join(w) for L in range(2, 19) for w in itertools.product("01", repeat=L)
              if first_occurrence_at_end("".join(w), "11")}
    res["thm1d_T11_equals_C1_up_to_length_18"] = ({w for w in C1set if len(w) <= 18} == T11set)
    # Kraft partial sums
    res["kraft_partial_sum_T011_L60"] = float(sum(Fraction(c, 2 ** L) for L, c in enumerate(counts_automaton("011", 60))))
    # Theorem 2: growth rates, all patterns of length 2..10
    viol = []
    lam_examples = {}
    for k in range(2, 11):
        lams = {p: growth(p) for p in ("".join(t) for t in itertools.product("01", repeat=k))}
        top = lams["1" * k]
        for p, l in lams.items():
            if p not in ("1" * k, "0" * k) and not l < top - 1e-9:
                viol.append(p)
        if k <= 5:
            lam_examples.update({p: round(lams[p], 6) for p in lams if p[0] == "1"})
    res["thm2_violations"] = viol
    res["growth_rates_k_le_5"] = {p: lam_examples[p] for p in ("11", "101", "111", "1011", "0110", "0101", "1111", "11111") if p in lam_examples} | \
        {"0110": round(growth("0110"), 6), "0101": round(growth("0101"), 6)}
    # Theorem 3: f_u(L) = cum_{1^k}(L-1) for unbordered u of length k+1, k = 2..8, L <= 80
    bad3 = []
    nunb = 0
    for k in range(2, 9):
        ones = cum(counts_automaton("1" * k, 80))
        for u in ("".join(t) for t in itertools.product("01", repeat=k + 1)):
            if periods(u) != [0]:
                continue
            nunb += 1
            fu = counts_automaton(u, 80)
            if any(fu[L] != ones[L - 1] for L in range(1, 81)):
                bad3.append(u)
    res["thm3_unbordered_patterns_checked"] = nunb
    res["thm3_bad"] = bad3
    # H-C11-2 counterexample: k = 4, n = 1000
    def Lp(p, n, cache={}):
        if p not in cache:
            cache[p] = cum(counts_automaton(p, 400))
        c = cache[p]
        return next(L for L, x in enumerate(c) if x >= n)
    res["H_C11_2_n1000_lengths"] = {p: Lp(p, 1000) for p in ("1111", "1000", "1001", "1010", "0111", "1110")}
    # rivals beating 1^k at large n (spot values quoted in CLM-C11-05)
    for k, n in ((4, 311743), (5, 2 ** 45), (6, 13 * 10 ** 18)):
        best = Lp("1" * k, n)
        rivals = sorted(p for p in ("".join(t) for t in itertools.product("01", repeat=k)) if Lp(p, n) < best)
        res[f"rivals_beating_1^{k}_at_n={n}"] = rivals
    return res


# ---------------------------------------------------------------- part: codes (own encoders, prefix-freeness)
class Tp:
    def __init__(self, p, Lmax=200):
        self.p = p
        self.k = len(p)
        self.c = counts_automaton(p, Lmax)
        self.cum = cum(self.c)
        # completions: number of ways to finish from a given prefix (state) in exactly r more letters
        k = self.k

        def step(s, ch):
            t = p[:s] + ch
            for l in range(min(len(t), k), -1, -1):
                if t.endswith(p[:l]):
                    return l
            return 0
        self.trans = [[step(s, ch) for ch in "01"] for s in range(k)]
        W = [[0] * (k + 1) for _ in range(Lmax + 1)]
        W[0][k] = 1
        for r in range(1, Lmax + 1):
            for s in range(k):
                W[r][s] = W[r - 1][self.trans[s][0]] + W[r - 1][self.trans[s][1]]
        self.W = W

    def length(self, n):
        return next(L for L, x in enumerate(self.cum) if x >= n)

    def encode(self, n):
        L = self.length(n)
        rank = n - self.cum[L - 1] - 1
        s, out = 0, []
        for i in range(L):
            r = L - i - 1
            for b in (0, 1):
                t = self.trans[s][b]
                if t == self.k and r > 0:
                    continue
                cnt = self.W[r][t] if t < self.k else (1 if r == 0 else 0)
                if rank < cnt:
                    out.append(str(b))
                    s = t
                    break
                rank -= cnt
        return "".join(out)


def is_prefix_free(words):
    ws = sorted(words)
    return all(not ws[i + 1].startswith(ws[i]) for i in range(len(ws) - 1))


def part_codes():
    res = {}
    for p in ("011", "101", "0111", "00111", "11", "111"):
        T = Tp(p)
        n = 30000 if len(p) < 5 else 20000
        cw = [T.encode(i) for i in range(1, n + 1)]
        ok_set = all(first_occurrence_at_end(w, p) for w in cw)
        ok_len = all(len(w) == T.length(i) for i, w in enumerate(cw, start=1))
        distinct = len(set(cw)) == len(cw)
        order = all((len(a), a) < (len(b), b) for a, b in zip(cw, cw[1:]))
        res[p] = {"n": n, "codewords_in_T_p": ok_set, "lengths_match_counts": ok_len, "distinct": distinct,
                  "length_then_lex_order": order, "prefix_free": is_prefix_free(cw),
                  "first": cw[:6]}
    return res


# ---------------------------------------------------------------- part: compare (Cor. 4, Cor. 6)
def fib_list(m):
    F = [0, 1]
    while len(F) < m:
        F.append(F[-1] + F[-2])
    return F


def part_compare(NMAX=2_000_000):
    F = fib_list(400)
    cum11 = cum(counts_automaton("11", 120))
    cum011 = cum(counts_automaton("011", 120))
    # closed forms of Corollary 4
    res = {"cum11_closed_form_ok": all(cum11[L] == F[L + 1] - 1 for L in range(1, 120)),
           "cum011_closed_form_ok": all(cum011[L] == F[L + 2] - L - 1 for L in range(1, 120))}

    def L_from_cum(c, n):
        lo, hi = 0, len(c) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if c[mid] >= n:
                hi = mid
            else:
                lo = mid + 1
        return lo

    # C1 length from Zeckendorf directly (independent of cum11): index of largest Fibonacci <= n, + 1
    G = [1, 2]
    while G[-1] <= 10 ** 7:
        G.append(G[-1] + G[-2])

    def L_C1(n):
        k = max(i for i in range(len(G)) if G[i] <= n)
        return k + 2

    # C3 counts from the construction: C1 codewords of length l, minus final bit, prefixed by 10 / 11 -> length l + 1
    cnt_c1 = counts_automaton("11", 120)
    cnt_c3 = [0] * 121
    for l in range(2, 120):
        cnt_c3[l + 1] = 2 * cnt_c1[l]
    cum3 = cum(cnt_c3)
    res["cumC3_closed_form_2F_L_minus_2_ok"] = all(cum3[L] == 2 * F[L] - 2 for L in range(1, 120))
    diff011_c1 = {-1: 0, 0: 0, 1: 0}
    longer011_c1, c3_longer_c1, longer011_c3 = [], [], []
    k = 0
    for n in range(1, NMAX + 1):
        while G[k + 1] <= n:
            k += 1
        l1 = k + 2
        l011 = L_from_cum(cum011, n)
        l3 = L_from_cum(cum3, n)
        dd = l1 - l011
        diff011_c1[max(-1, min(1, dd))] += 1
        if l011 > l1:
            longer011_c1.append(n)
        if l3 > l1:
            c3_longer_c1.append(n)
        if l011 > l3:
            longer011_c3.append(n)
    res["n_max"] = NMAX
    res["C1_minus_T011_counts(-1,0,+1)"] = diff011_c1
    res["T011_longer_than_C1_at"] = longer011_c1[:20]
    res["C3_longer_than_C1_at"] = c3_longer_c1[:20]
    res["T011_longer_than_C3_at"] = longer011_c3[:20]
    # count inequalities for all L < 300 (exact)
    cum011b = [F[L + 2] - L - 1 for L in range(300)]
    cum3b = [max(2 * F[L] - 2, 0) for L in range(300)]
    cum1b = [F[L + 1] - 1 for L in range(300)]
    res["L_with_cum011_lt_cumC3"] = [L for L in range(1, 300) if cum011b[L] < cum3b[L]]
    res["L_with_cumC3_lt_cumC1"] = [L for L in range(1, 300) if cum3b[L] < cum1b[L]]
    res["ratio_cum011_cumC3_L299"] = cum011b[299] / cum3b[299]
    res["phi2_over_2"] = ((1 + 5 ** 0.5) / 2) ** 2 / 2
    res["ratio_cumC3_cumC1_L299"] = cum3b[299] / cum1b[299]
    # Fraenkel-Klein C3 is not prefix-free: 101 and 10101 are both codewords
    res["C3_codewords_len3_5_from_construction"] = None
    return res


# ---------------------------------------------------------------- part: oscillation (Prop. 5, H refutations)
def k_bonacci(k):
    # largest real root of x^k - x^{k-1} - ... - 1
    lo, hi = 1.0, 2.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if mid ** k - sum(mid ** i for i in range(k)) > 0:
            hi = mid
        else:
            lo = mid
    return lo


def part_oscillation():
    res = {}
    for k in range(2, 7):
        Lmax = 420
        a = cum(counts_automaton("1" * k, Lmax))          # cum_O
        u = "0" + "1" * k                                  # unbordered, length k + 1
        assert periods(u) == [0]
        b = cum(counts_automaton(u, Lmax))                 # cum_U

        def S(N):
            """sum_{n <= N} (L_O(n) - L_U(n)) exactly: sum over n of #{L : cum_U(L) < n} - #{L : cum_O(L) < n}."""
            # sum_{n<=N} L_X(n) = sum_{L>=0} #{n <= N : n > cum_X(L)} = sum_L max(0, N - cum_X(L))
            sO = sum(max(0, N - x) for x in a)
            sU = sum(max(0, N - x) for x in b)
            return sO - sU

        lam = k_bonacci(k)
        lo_c = (2 - lam) / (lam - 1) ** 2
        hi_c = lam * (2 - lam) / (lam - 1)
        vals = {}
        for L in (100, 200, 400):
            vals[L] = {"G(cum_O(L))": float(Fraction(S(a[L]), a[L])), "G(cum_U(L-1))": float(Fraction(S(b[L - 1]), b[L - 1]))}
        # structural inequalities used in the proof (k >= 3): b_{L-2} <= a_{L-1} < b_{L-1} <= a_L
        first_ok = None
        for L in range(3, Lmax):
            ok = b[L - 2] <= a[L - 1] < b[L - 1] <= a[L]
            if ok and first_ok is None:
                first_ok = L
            if not ok:
                first_ok = None
        G_at = {}
        for e in (40, 80, 120):
            N = 2 ** e
            G_at[f"2^{e}"] = float(Fraction(S(N), N))
        res[f"k={k}"] = {"lambda": lam, "liminf_pred": lo_c, "limsup_pred": hi_c,
                         "log_prediction_(a)": math.log(1 / (lam - 1)) / math.log(lam),
                         "values": vals, "structure_holds_for_all_L_from": first_ok, "G_at_powers_of_2": G_at}
    return res


# ---------------------------------------------------------------- part: bench (a few exact expectations)
def part_bench():
    F = fib_list(400)
    T = {p: cum(counts_automaton(p, 400)) for p in ("101", "0111", "00111", "011", "111")}
    cumC1 = [F[L + 1] - 1 for L in range(200)]
    cumC3 = [max(2 * F[L] - 2, 0) for L in range(200)]

    def bp_from_cum(c, nmax):
        out, prev = [], 0
        for L, x in enumerate(c):
            if x > prev:
                out.append((prev + 1, min(x, nmax), L))
                if x >= nmax:
                    return out
            prev = x
        raise ValueError

    def bp_func(lenf, nmax):
        out, n = [], 1
        while n <= nmax:
            L = lenf(n)
            lo, hi = n, nmax
            while lo < hi:                                     # last m with lenf(m) == L (monotone)
                mid = (lo + hi + 1) // 2
                if lenf(mid) == L:
                    lo = mid
                else:
                    hi = mid - 1
            out.append((n, lo, L))
            n = lo + 1
        return out

    def delta_len(n):
        L = n.bit_length()
        return 2 * L.bit_length() - 1 + L - 1

    def leb_len(n):
        x = n - 1
        return 8 * max(1, -(-x.bit_length() // 7))

    def expect(bps, cdf):
        return sum((cdf(hi) - cdf(lo - 1)) * L for lo, hi, L in bps)

    out = {}
    # Zipf s = 1.1 on [1, 1e6]
    N = 10 ** 6
    w = np.arange(1, N + 1, dtype=np.float64) ** -1.1
    pz = w / w.sum()
    cz = np.concatenate([[0.0], np.cumsum(pz)])
    Hz = float(-(pz * np.log2(pz)).sum())
    cdfz = lambda n: cz[min(n, N)]
    codes = {"T_101": bp_from_cum(T["101"], N), "T_0111": bp_from_cum(T["0111"], N),
             "C3": bp_from_cum(cumC3, N), "Fibonacci": bp_from_cum(cumC1, N), "delta": bp_func(delta_len, N)}
    out["Zipf1.1"] = {k: round(expect(v, cdfz) - Hz, 4) for k, v in codes.items()} | {"H": round(Hz, 4)}
    # log-uniform on [1, 1e6]
    w = 1.0 / np.arange(1, N + 1, dtype=np.float64)
    pl = w / w.sum()
    cl = np.concatenate([[0.0], np.cumsum(pl)])
    Hl = float(-(pl * np.log2(pl)).sum())
    cdfl = lambda n: cl[min(n, N)]
    out["log-uniform"] = {k: round(expect(v, cdfl) - Hl, 4) for k, v in codes.items()} | {"H": round(Hl, 4)}
    # uniform 2^32
    N2 = 2 ** 32
    cdfu = lambda n: min(n, N2) / N2
    codes2 = {"T_00111": bp_from_cum(T["00111"], N2), "T_0111": bp_from_cum(T["0111"], N2),
              "LEB128": bp_func(leb_len, N2), "delta": bp_func(delta_len, N2), "C3": bp_from_cum(cumC3, N2)}
    out["uniform2^32"] = {k: round(expect(v, cdfu) - 32, 4) for k, v in codes2.items()}
    # geometric p = 0.001 (support n >= 1, P(n) = p q^(n-1))
    p = 0.001
    nmax = int(math.ceil(math.log(1e-18) / math.log1p(-p))) + 1
    cdfg = lambda n: -math.expm1(n * math.log1p(-p))
    Hg = (-p * math.log2(p) - (1 - p) * math.log2(1 - p)) / p
    codes3 = {"T_0111": bp_from_cum(T["0111"], nmax), "T_111": bp_from_cum(T["111"], nmax),
              "C3": bp_from_cum(cumC3, nmax), "Fibonacci": bp_from_cum(cumC1, nmax), "delta": bp_func(delta_len, nmax)}
    out["geometric0.001"] = {k: round(expect(v, cdfg) - Hg, 4) for k, v in codes3.items()}
    return out


PARTS = {"theory": part_theory, "codes": part_codes, "compare": part_compare, "oscillation": part_oscillation,
         "bench": part_bench}

if __name__ == "__main__":
    part = sys.argv[1]
    t0 = time.time()
    res = PARTS[part]()
    res = {"part": part, "result": res, "wall_seconds": round(time.time() - t0, 1)}
    (OUT / f"c11_{part}.json").write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps(res, default=str)[:5000])
