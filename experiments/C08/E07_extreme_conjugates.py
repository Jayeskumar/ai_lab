"""EXP-C08-07: targeted search for non-associativity of circle products at extreme conjugates.

Why. EXP-C08-02..04 tested random triples, EXP-C08-06 all pairs below 300 plus random pairs below 10^6; the
Skeptic's review of C08 (reviews/skeptic_C05_C08_C12.md) found certified failures at shifts both searches had
passed. Failures are rare among random inputs: the identity nu(a o_s b) = x^s nu(a) nu(b) (EXP-C08-06) can only
fail when the conjugate coordinates of a and b are large, so that beta^s c(a) c(b) leaves the window of conjugates
of greedy expansions.

Method. For every non-dominant root beta of the characteristic polynomial, c_beta(n) = sum_i d_i beta^i over the
greedy digits of n (n <= N). Candidates: 1..30 and the K most extreme n in each direction (min and max for real
beta, 8 directions in the plane for complex beta). Every pair of candidates is tested with the exact embedding
identity in Z[x]/(char poly); a failing pair is certified by an explicit triple (a o b) o c != a o (b o c) with c
from 1..60 or the candidates. Certified failures are proofs of non-associativity; "no failure found" is only
computational support.
"""

import cmath
import time

import numpy as np

from lab.seqtools import berlekamp_massey
from systems.circle import BaseSequence

from experiments.C08.E01_associativity_atlas import families

META = {
    "id": "EXP-C08-07",
    "cycle": "C08",
    "title": "Extreme-conjugate search: certified non-associativity for the named sequences, the 45-sequence atlas "
             "and the 90 quadratic rows",
    "agent": "Mathematical Explorer",
    "question": "Do the associativity thresholds and the shift sets of EXP-C08-02, -04 and -06 survive a search that "
                "targets inputs with extreme conjugate coordinates?",
    "hypothesis": "H-C08-7: targeted inputs find certified failures at shifts that random and small-input searches "
                  "passed (as the Skeptic reports for (2,2;1,2) at s = 6 and (3,3;1,5) at s = 10); after the "
                  "targeted search, no Pisot sequence with a positive conjugate root has a non-monotone shift set "
                  "(CLM-C08-04) and no non-Pisot sequence has a shift without failure (CLM-C08-02).",
    "assumptions": ["named sequences - N = 200000, K = 25, pool 1..1500 plus 1500 random n <= N plus the "
                    "candidates, the known failing pairs as seeds, shifts 0..16",
                    "atlas (the 45 base sequences of EXP-C08-02) and the 90 quadratic rows of EXP-C08-04 - "
                    "N = 50000, K = 12, pool 1..800 plus 800 random, shifts 0..12",
                    "window filter - occupancy grid of {c(n) : n <= N}, dilated by one cell; it cannot see "
                    "failures whose product conjugate lies within one cell of the window (fractal boundaries), "
                    "which is why the known pairs are added as seeds",
                    "a failing pair is certified only by an explicit triple"],
    "methodology": "Candidate inputs with extreme conjugates; exact embedding test on all candidate pairs and on the "
                   "pool pairs whose product conjugate falls outside the occupancy grid of the window; explicit "
                   "triples for failing pairs; per sequence, the shifts with a certified failure and the shifts "
                   "without any failure found.",
    "falsification": "A certified failure for Fibonacci at s >= 2 (would contradict the Lean theorem CLM-C08-01); a "
                     "certified failure at a shift listed as associative by EXP-C08-06 (refutes that row); a "
                     "positive-beta quadratic row whose no-failure set is not upward closed (refutes CLM-C08-04).",
    "seed": 807,
}

# Known failing pairs, tested at every shift of every named sequence (their triples are re-certified here):
# the tribonacci example of Ambroz-Frougny-Masakova-Pelantova (2003), the Historian's pairs (EXP-C08-06).
SEEDS = [(10016, 10016), (78, 248), (50, 96), (41, 280)]
RES = {1: 4000, 2: 300, 3: 48}           # grid resolution by window dimension (atlas, quadratic rows)
RES_NAMED = {1: 4000, 2: 600, 3: 64}

NAMED = [
    ("Fibonacci 1,2", [1, 2], (1, 1)),
    ("Pell 1,2,5", [1, 2], (2, 1)),
    ("(2,2) 1,2", [1, 2], (2, 2)),
    ("(3,3) 1,5", [1, 5], (3, 3)),
    ("tribonacci 1,2,4", [1, 2, 4], (1, 1, 1)),
    ("4-bonacci 1,2,4,8", [1, 2, 4, 8], (1, 1, 1, 1)),
    ("G(k+1)=G(k)+G(k-2) 1,2,3", [1, 2, 3], (1, 0, 1)),
    ("G(k+1)=G(k)+G(k-3) 1,2,3,4", [1, 2, 3, 4], (1, 0, 0, 1)),
]


def minimal_coeffs(S: BaseSequence):
    """Coefficients of the minimal recurrence (Berlekamp-Massey on 30 terms, verified on 60), as in EXP-C08-02.

    A sequence can satisfy a shorter recurrence than the one defining it (G(k+1) = G(k) + 2G(k-1) with G_1 = 2
    gives the powers of 2); the embedding must use the minimal one, or it is not faithful.
    """
    S.extend(60)
    c = berlekamp_massey(S.G[:30])
    if all(x.denominator == 1 for x in c) and \
            all(sum(int(c[i]) * S.G[n - 1 - i] for i in range(len(c))) == S.G[n] for n in range(len(c), 61)):
        return tuple(int(x) for x in c)
    return S.coeffs


class Embedding:
    """nu(n) = sum_i d_i x^i in Z[x]/(x^d - a_1 x^(d-1) - ... - a_d), on greedy digits."""

    def __init__(self, S: BaseSequence, coeffs, top: int = 600):
        self.S, self.coeffs, self.d = S, tuple(coeffs), len(coeffs)
        d = self.d
        x = tuple([0, 1] + [0] * (d - 2)) if d > 1 else (self.coeffs[0],)
        self.pw = [tuple([1] + [0] * (d - 1))]
        for _ in range(top):
            self.pw.append(self.mul(self.pw[-1], x))
        self.cache = {}

    def mul(self, u, v):
        d, coeffs = self.d, self.coeffs
        p = [0] * (2 * d - 1)
        for i, a in enumerate(u):
            if a:
                for j, b in enumerate(v):
                    p[i + j] += a * b
        for k in range(2 * d - 2, d - 1, -1):
            c, p[k] = p[k], 0
            if c:
                for t, a in enumerate(coeffs, start=1):
                    p[k - t] += a * c
        return tuple(p[:d])

    def nu(self, n):
        if n not in self.cache:
            u = [0] * self.d
            for i, dg in self.S.greedy(n).items():
                for t, y in enumerate(self.pw[i]):
                    u[t] += dg * y
            self.cache[n] = tuple(u)
        return self.cache[n]

    def ok(self, a, b, s):
        return self.nu(self.S.circle(a, b, s)) == self.mul(self.pw[s], self.mul(self.nu(a), self.nu(b)))


def conjugate_roots(coeffs):
    roots = np.roots([1] + [-a for a in coeffs])
    dom = max(roots, key=abs)
    out = []
    for z in roots:
        if abs(z - dom) < 1e-9:
            continue
        if abs(z.imag) < 1e-12:
            out.append(complex(z.real, 0.0))
        elif z.imag > 0:
            out.append(complex(z))
    others = sorted(abs(z) for z in roots if abs(z - dom) >= 1e-9)
    if len(coeffs) == 1:
        kind = "geometric"
    elif all(m < 1 - 1e-9 for m in others):
        kind = "Pisot"
    else:
        kind = "non-Pisot"
    return float(abs(dom)), out, kind


def conjugate_values(S: BaseSequence, N: int, beta: complex):
    while S.G[-1] <= N:
        S.extend(len(S.G))
    G = S.G
    pw = [beta ** i for i in range(len(G))]
    c = np.zeros(N + 1, dtype=complex)
    k = 0
    for n in range(1, N + 1):
        while k + 1 < len(G) and G[k + 1] <= n:
            k += 1
        g = G[k]
        dg = n // g
        c[n] = dg * pw[k] + c[n - dg * g]
    return c


def candidates(S, N, roots, K, directions=8):
    cand = set(range(1, 31))
    for beta in roots:
        c = conjugate_values(S, N, beta)[1:]
        if beta.imag == 0:
            idx = np.argsort(c.real, kind="stable")
            cand.update(int(i) + 1 for i in idx[:K])
            cand.update(int(i) + 1 for i in idx[-K:])
        else:
            for t in range(directions):
                w = cmath.exp(-2j * cmath.pi * t / directions)
                idx = np.argsort((c * w).real, kind="stable")[-K:]
                cand.update(int(i) + 1 for i in idx)
    return sorted(cand)


def conjugate_coords(S, N, roots):
    """Real coordinates of the conjugate embedding (Re for real roots, Re and Im for complex ones)."""
    cols, parts = [], []
    for beta in roots:
        c = conjugate_values(S, N, beta)
        cols.append(c)
        parts.append(1 if beta.imag == 0 else 2)
    return cols, parts


class Window:
    """Occupancy grid of the conjugate point cloud {c(n) : n <= N}, dilated by one and by two cells."""

    def __init__(self, cols, parts, res):
        pts = np.stack([x for c, k in zip(cols, parts) for x in ((c.real,) if k == 1 else (c.real, c.imag))], 1)
        self.lo = pts.min(0)
        self.span = np.maximum(pts.max(0) - self.lo, 1e-12)
        self.res, self.dim = res, pts.shape[1]
        occ = np.zeros((res,) * self.dim, dtype=bool)
        occ[tuple(self.cell(pts).T)] = True
        self.mask1 = self.dilate(occ)
        self.mask2 = self.dilate(self.mask1)

    def cell(self, pts):
        return np.clip(np.floor((pts - self.lo) / self.span * self.res).astype(np.int64), 0, self.res - 1)

    def dilate(self, m):
        out = m.copy()
        for ax in range(self.dim):
            out = out | np.roll(out, 1, ax) | np.roll(out, -1, ax)
        return out

    def depth(self, pts):
        """0 inside the dilated cloud, 1 just outside, 2 well outside, 3 outside the bounding box."""
        rel = (pts - self.lo) / self.span
        outside_box = np.any((rel < -0.01) | (rel > 1.01), axis=1)
        idx = tuple(self.cell(pts).T)
        d = np.where(~self.mask1[idx], 1, 0) + np.where(~self.mask2[idx], 1, 0)
        return np.where(outside_box, 3, d)


def window_pairs(cols, parts, roots, window, pool, s, top):
    """Pairs (a, b) of the pool whose product conjugate beta^s c(a) c(b) falls outside the window, most outside first."""
    pool = np.asarray(pool)
    vals = [c[pool] for c in cols]
    found = []
    for i in range(len(pool)):
        comp = []
        for v, k, beta in zip(vals, parts, roots):
            z = (beta ** s) * v[i] * v[i:]
            comp.extend((z.real,) if k == 1 else (z.real, z.imag))
        dep = window.depth(np.stack(comp, 1))
        hit = np.nonzero(dep)[0]
        if len(hit):                                   # at most 3 partners per a, deepest first
            best = hit[np.argsort(-dep[hit], kind="stable")[:3]]
            found.extend((-int(dep[j]), int(pool[i]), int(pool[i + j])) for j in best)
    found.sort()
    return [(a, b) for _, a, b in found[:top]]


def certify(S, a, b, s, cs):
    ab = S.circle(a, b, s)
    for c in cs:
        lhs = S.circle(ab, c, s)
        rhs = S.circle(a, S.circle(b, c, s), s)
        if lhs != rhs:
            return [a, b, c], lhs, rhs
    return None


def scan(S, N, K, shifts, res, pool_small=1500, pool_random=1500, top=150, seeds=(), max_pairs_to_certify=25):
    coeffs = minimal_coeffs(S)
    dom, roots, kind = conjugate_roots(coeffs)
    cand = candidates(S, N, roots, K)
    E = Embedding(S, coeffs)
    pairs = [(a, b) for i, a in enumerate(cand) for b in cand[i:]]
    cs = list(range(1, 61)) + cand
    window, pool = None, None
    if roots and kind == "Pisot":                     # the window is bounded only for Pisot sequences
        cols, parts = conjugate_coords(S, N, roots)
        window = Window([c[1:] for c in cols], parts, res)
        rng = np.random.default_rng(META["seed"])
        big = rng.choice(np.arange(pool_small + 1, N + 1), size=min(pool_random, N - pool_small), replace=False)
        pool = sorted(set(range(1, pool_small + 1)) | set(int(x) for x in big) | set(cand))
    by_shift = {}
    for s in shifts:
        status, tried = {"status": "no failure found"}, 0
        extra = window_pairs(cols, parts, roots, window, pool, s, top) if window is not None else []
        for a, b in list(seeds) + pairs + extra:
            if E.ok(a, b, s):
                continue
            tried += 1
            cert = certify(S, a, b, s, cs)
            if cert:
                triple, lhs, rhs = cert
                status = {"status": "NOT ASSOCIATIVE", "triple": triple, "lhs_minus_rhs": lhs - rhs}
                break
            status = {"status": "embedding fails, no triple found", "pair": [a, b]}
            if tried >= max_pairs_to_certify:
                break
        by_shift[s] = status
    fails = [s for s, r in by_shift.items() if r["status"] == "NOT ASSOCIATIVE"]
    clean = [s for s, r in by_shift.items() if r["status"] == "no failure found"]
    upward = all(not (s1 < s2 and s1 in clean and s2 in fails) for s1 in shifts for s2 in shifts)
    return {"kind": kind, "minimal_recurrence": list(coeffs), "dominant_root": round(dom, 6),
            "conjugates": [[round(z.real, 6), round(z.imag, 6)] for z in roots],
            "candidates": len(cand), "pool": len(pool) if pool else 0,
            "certified_failures": fails, "no_failure_shifts": clean,
            "uncertified": [s for s, r in by_shift.items() if r["status"].startswith("embedding")],
            "upward_closed": upward,
            "largest_certified_failure": max(fails) if fails else None,
            "examples": {str(s): by_shift[s].get("triple") for s in fails}}


def quadratic_rows():
    """The same 90 rows as EXP-C08-04 / EXP-C08-06."""
    rows = []
    for p in range(1, 6):
        for q in (-3, -2, -1, 1, 2, 3):
            r = np.roots([1, -p, -q])
            if np.iscomplexobj(r) and np.max(np.abs(np.imag(r))) > 1e-12:
                continue
            r = sorted(np.real(r), key=abs)
            beta, alpha = float(r[0]), float(r[1])
            if not (alpha > 1 and abs(beta) < 1 - 1e-9) or abs(beta) < 1e-12:
                continue
            for g1 in range(2, 7):
                try:
                    S = BaseSequence(f"G(k+1)={p}G(k)+({q})G(k-1); 1,{g1}", [1, g1], (p, q))
                    S.extend(60)
                except (ValueError, AssertionError):
                    continue
                if any(S.G[i] * S.G[i] == S.G[i - 1] * S.G[i + 1] for i in range(1, 6)):
                    continue
                rows.append((p, q, g1, beta, S))
    return rows


def atlas():
    """The 45 base sequences of EXP-C08-02."""
    return families() + [
        BaseSequence("Pell 1,2,5 (2,1)", [1, 2, 5], (2, 1)),
        BaseSequence("G(k+1)=G(k)+G(k-3); 1,2,3,4", [1, 2, 3, 4], (1, 0, 0, 1)),
        BaseSequence("G(k+1)=2G(k)-G(k-1)+G(k-2) (non-Pisot?); 1,2,4", [1, 2, 4], (2, -1, 1)),
        BaseSequence("G(k+1)=G(k)+G(k-1)+2G(k-2); 1,2,4", [1, 2, 4], (1, 1, 2)),
    ]


def run():
    t0 = time.time()
    named = {}
    for name, init, coeffs in NAMED:
        named[name] = scan(BaseSequence(name, init, coeffs), 200_000, 25, range(0, 17),
                           res=RES_NAMED[len(coeffs) - 1], seeds=SEEDS)
    t1 = time.time()
    atlas_rows = []
    for S in atlas():
        try:
            S.extend(60)
        except ValueError:
            continue
        res = scan(S, 50_000, 12, range(0, 13), res=RES[len(S.coeffs) - 1] if len(S.coeffs) > 1 else 1,
                   pool_small=800, pool_random=800, top=100)
        atlas_rows.append({"G": S.name, **res})
    t2 = time.time()
    quad = []
    for p, q, g1, beta, S in quadratic_rows():
        res = scan(S, 50_000, 12, range(0, 13), res=RES[1], pool_small=800, pool_random=800, top=100)
        quad.append({"p": p, "q": q, "g1": g1, "beta": round(beta, 6), "canonical": g1 in (p, p + 1), **res})
    t3 = time.time()

    prev = {}
    import json
    from pathlib import Path
    for row in json.loads(Path("results/EXP-C08-06.json").read_text())["results"]["quadratic_rows"]:
        prev[(row["p"], row["q"], row["g1"])] = row["no_failure_shifts"]
    newly_failing = [{"p": r["p"], "q": r["q"], "g1": r["g1"],
                      "shifts": sorted(set(prev.get((r["p"], r["q"], r["g1"]), [])) & set(r["certified_failures"]))}
                     for r in quad]
    newly_failing = [x for x in newly_failing if x["shifts"]]
    non_monotone = [r for r in quad if not r["upward_closed"]]
    pos = [r for r in quad if r["beta"] > 0]
    non_pisot_clean = [r["G"] for r in atlas_rows if r["kind"] == "non-Pisot" and r["no_failure_shifts"]]
    pisot_never_clean = [r["G"] for r in atlas_rows if r["kind"] == "Pisot" and not r["no_failure_shifts"]]
    return {
        "named": named,
        "atlas": atlas_rows,
        "quadratic_rows": quad,
        "quadratic_rows_with_new_certified_failures_vs_EXP_C08_06": newly_failing,
        "non_monotone_quadratic_rows": [{"p": r["p"], "q": r["q"], "g1": r["g1"], "beta": r["beta"],
                                         "canonical": r["canonical"], "no_failure_shifts": r["no_failure_shifts"]}
                                        for r in non_monotone],
        "summary": [
            "named sequences (largest certified failing shift / shifts 0..16 without a failure found): " +
            "; ".join(f"{k}: {v['largest_certified_failure']} / {v['no_failure_shifts']}" for k, v in named.items()),
            f"atlas: {len(atlas_rows)} sequences; non-Pisot with a shift without failure: {len(non_pisot_clean)} "
            f"{non_pisot_clean}; Pisot with no shift without failure in 0..12: {len(pisot_never_clean)} "
            f"{pisot_never_clean}",
            f"quadratic rows: {len(quad)}; rows with a newly certified failure at a shift EXP-C08-06 passed: "
            f"{len(newly_failing)}; non-monotone on 0..12: {len(non_monotone)} (beta > 0: "
            f"{sum(1 for r in non_monotone if r['beta'] > 0)} of {len(pos)} rows; canonical: "
            f"{sum(1 for r in non_monotone if r['canonical'])})",
            "uncertified embedding failures (no triple found): " +
            str(sum(len(v["uncertified"]) for v in named.values()) +
                sum(len(r["uncertified"]) for r in atlas_rows) + sum(len(r["uncertified"]) for r in quad)),
        ],
        "timings": {"named_s": round(t1 - t0, 1), "atlas_s": round(t2 - t1, 1), "quadratic_s": round(t3 - t2, 1)},
    }
