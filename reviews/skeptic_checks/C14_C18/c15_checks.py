"""Skeptic checks for cycle C15 (magma cellular automata). Own code only (numpy).

usage: python3 c15_checks.py fuse|census3|cycledet|semigroups|fastforward|misc
"""
import itertools
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
FUSE = np.array([[0, 0, 0], [0, 0, 1], [1, 2, 2]], dtype=np.int8)


# ------------------------------------------------------------------ basic tools (own)
def step(T, row):
    return T[row, np.roll(row, -1)]


def simulate(T, row, t):
    for _ in range(t):
        row = step(T, row)
    return row


def cone(T, t):
    """F_t as an array with t+1 axes: F_t[x0..xt] = F_{t-1}[x0..x_{t-1}] * F_{t-1}[x1..xt]."""
    n = T.shape[0]
    F = np.arange(n, dtype=np.int8)
    for _ in range(t):
        F = T[F[..., None], F[None, ...]]
    return F


_W = {}


def _weights(length):
    if length not in _W:
        r = np.random.default_rng(12345 + length)
        _W[length] = r.integers(0, 2 ** 63, length, dtype=np.uint64) * np.uint64(2) + np.uint64(1)
    return _W[length]


def level_widths(F):
    """number of distinct residual functions after the first k inputs (k = 0..m); own implementation:
    every residual (a row of the reshaped table) is hashed by a random odd-weighted linear form mod 2^64
    (distinct rows collide with probability ~2^-63 per pair), and distinct hashes are counted."""
    n = F.shape[0] if F.ndim else 1
    m = F.ndim
    flat = np.ascontiguousarray(F.reshape(-1)).astype(np.uint64)
    out = []
    for k in range(m + 1):
        width = n ** (m - k)
        rows = flat.reshape(n ** k, width)
        w = _weights(width)
        with np.errstate(over='ignore'):
            h = (rows * w[None, :]).sum(axis=1, dtype=np.uint64) if width > 1 else rows[:, 0] * w[0]
        out.append(int(np.unique(h).size))
    return out


def widths(F):
    fw = max(level_widths(F))
    bw = max(level_widths(np.transpose(F, tuple(range(F.ndim - 1, -1, -1)))))
    return fw, bw


def essential(F):
    return [k for k in range(F.ndim) if not (F == np.take(F, [0], axis=k)).all()]


# ------------------------------------------------------------------ pair graph (own)
def pair_graph(T):
    n = T.shape[0]
    V = [(u, v) for u in range(n) for v in range(n)]
    succ = {x: [(a, b) for a in range(n) for b in range(n) if T[x[0], a] == T[x[1], b]] for x in V}
    return V, succ


def surjective(T):
    V, succ = pair_graph(T)
    # diamond: diag -> off-diag -> ... -> diag
    start = [y for x in V if x[0] == x[1] for y in succ[x] if y[0] != y[1]]
    seen = set(start)
    q = list(start)
    while q:
        x = q.pop()
        for y in succ[x]:
            if y[0] == y[1]:
                return False
            if y not in seen:
                seen.add(y)
                q.append(y)
    return True


def _reach_cycle(V, succ):
    """vertices from which an infinite forward path starts (= can reach a cycle), via Tarjan SCCs."""
    index, low, onst, st, comp = {}, {}, set(), [], {}
    cnt = [0]
    sccs = []

    def strong(v):
        index[v] = low[v] = cnt[0]
        cnt[0] += 1
        st.append(v)
        onst.add(v)
        for w in succ[v]:
            if w not in index:
                strong(w)
                low[v] = min(low[v], low[w])
            elif w in onst:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            c = []
            while True:
                w = st.pop()
                onst.discard(w)
                c.append(w)
                if w == v:
                    break
            sccs.append(c)
    sys.setrecursionlimit(10000)
    for v in V:
        if v not in index:
            strong(v)
    cyclic = set()
    for c in sccs:
        if len(c) > 1 or c[0] in succ[c[0]]:
            cyclic |= set(c)
    # backward closure from cyclic vertices
    pred = {v: [] for v in V}
    for v in V:
        for w in succ[v]:
            pred[w].append(v)
    good = set(cyclic)
    q = list(cyclic)
    while q:
        v = q.pop()
        for u in pred[v]:
            if u not in good:
                good.add(u)
                q.append(u)
    return good


def injective(T):
    V, succ = pair_graph(T)
    fwd = _reach_cycle(V, succ)
    pred = {v: [] for v in V}
    for v in V:
        for w in succ[v]:
            pred[w].append(v)
    bwd = _reach_cycle(V, pred)
    return not any(x[0] != x[1] and x in fwd and x in bwd for x in V)


def cyclic_bijective(T, L):
    n = T.shape[0]
    codes = np.arange(n ** L)
    d = (codes[:, None] // n ** np.arange(L)) % n
    img = T[d, np.roll(d, -1, axis=1)]
    c2 = (img * n ** np.arange(L)).sum(axis=1)
    return np.unique(c2).size == codes.size


# ------------------------------------------------------------------ order-3 classes (own)
def all_tables3():
    return np.array(list(itertools.product(range(3), repeat=9)), dtype=np.int8).reshape(-1, 3, 3)


def classes3():
    tabs = all_tables3()
    w = 3 ** np.arange(8, -1, -1)
    own = tabs.reshape(-1, 9).astype(np.int64) @ w
    best = own.copy()
    for p in itertools.permutations(range(3)):
        p = np.array(p)
        inv = np.argsort(p)
        U = p[tabs[:, inv][:, :, inv]]
        for V in (U, np.transpose(U, (0, 2, 1))):
            best = np.minimum(best, V.reshape(-1, 9).astype(np.int64) @ w)
    uniq, counts = np.unique(best, return_counts=True)
    reps = tabs[np.searchsorted(own, uniq)]           # own codes are sorted (lexicographic enumeration)
    return reps, counts


def width_class(lam):
    if lam[5] == lam[7] == lam[9] and lam[6] == lam[8]:
        return 'bounded'
    d = {t: lam[t + 2] - lam[t] for t in range(4, 8)}
    if all(v > 0 for v in d.values()) and d[4] == d[6] and d[5] == d[7]:
        return 'linear'
    if all(lam[t + 2] >= 1.8 * lam[t] for t in (5, 6, 7)):
        return 'geometric'
    return 'other'


def is_assoc(T):
    n = T.shape[0]
    a, b, c = np.ix_(range(n), range(n), range(n))
    return bool((T[T[a, b], c] == T[a, T[b, c]]).all())


def permutive(T):
    n = T.shape[0]
    rows = all(len(set(T[a].tolist())) == n for a in range(n))
    cols = all(len(set(T[:, b].tolist())) == n for b in range(n))
    return rows or cols


def part_census3():
    t0 = time.time()
    reps, sizes = classes3()
    rows = []
    for T in reps:
        lam, nil, ess_max = [], None, 0
        for t in range(10):
            F = cone(T, t)
            fw, bw = widths(F)
            lam.append(min(fw, bw))
            ess_max = max(ess_max, len(essential(F)))
            if nil is None and (F == F.flat[0]).all():
                nil = t
        rows.append({'table': T.tolist(), 'lam': lam, 'wc': width_class(lam), 'nil': nil, 'ess_max': ess_max,
                     'surj': surjective(T), 'inj': injective(T), 'perm': permutive(T), 'assoc': is_assoc(T)})
    counts = {}
    for r in rows:
        counts[r['wc']] = counts.get(r['wc'], 0) + 1
    surj_tables = sum(int(s) for r, s in zip(rows, sizes) if r['surj'])
    perm_tables = 0
    for T in all_tables3():
        perm_tables += permutive(T)
    inj_classes = [r['table'] for r in rows if r['inj']]
    # periodic-configuration cross-check of injectivity and surjectivity
    cross = []
    for r in rows:
        T = np.array(r['table'], dtype=np.int8)
        bij = all(cyclic_bijective(T, L) for L in range(1, 9))
        if r['inj'] and not bij:
            cross.append(('injective but cyclic map not bijective', r['table']))
        if (not r['surj']) and bij:
            cross.append(('non-surjective but all cyclic maps L<=8 bijective', r['table']))
    lab = json.load(open(os.path.join(ROOT, 'results', 'EXP-C15-02.json')))['results']['rows']
    same_order = [r['table'] for r in rows] == [r['table'] for r in lab]
    same_lambda = all(a['lam'] == b['lambda'] for a, b in zip(rows, lab)) if same_order else None
    special = [[0, 0, 2], [2, 2, 0], [1, 1, 1]]
    sp = next((r for r in rows if r['table'] == special), None)
    if sp is None:   # the special table may not be the class representative: find its class
        Ts = np.array(special, dtype=np.int8)
        sp = {'lam': [min(widths(cone(Ts, t))) for t in range(10)], 'ess': [len(essential(cone(Ts, t))) for t in range(10)],
              'inj': injective(Ts), 'surj': surjective(Ts)}
    else:
        Ts = np.array(special, dtype=np.int8)
        sp = dict(sp)
        sp['ess'] = [len(essential(cone(Ts, t))) for t in range(10)]
    semis = [r for r in rows if r['assoc']]
    return {'n_classes': len(rows), 'class_sizes_sum': int(sizes.sum()), 'width_classes': counts,
            'max_lambda9': max(r['lam'][9] for r in rows),
            'surjective_classes': sum(r['surj'] for r in rows), 'surjective_tables': surj_tables,
            'permutive_tables': perm_tables, 'surjective_iff_permutive': all(r['surj'] == r['perm'] for r in rows),
            'injective_classes': len(inj_classes), 'injective_tables_list': inj_classes,
            'nilpotent_by_t9': sum(r['nil'] is not None for r in rows),
            'semigroup_classes': len(semis), 'semigroup_max_lambda': max(max(r['lam']) for r in semis),
            'semigroup_width_classes': sorted(set(r['wc'] for r in semis)),
            'periodic_cross_check_conflicts': cross,
            'same_class_order_as_lab': same_order, 'same_lambda_as_lab': same_lambda,
            'reversible_example': sp, 'runtime_s': round(time.time() - t0, 1),
            '_rows': [{'table': r['table'], 'wc': r['wc'], 'lam9': r['lam'][9]} for r in rows]}


# ------------------------------------------------------------------ fuse
def burn_times_own(x):
    """own implementation of the burn-time recursion on a cyclic row, by fixed-point iteration from the right."""
    L = len(x)
    INF = 1 << 60
    tau = [INF] * L
    for i in range(L):
        if x[i] == 0:
            tau[i] = 0
        elif x[i] == 1 and x[(i + 1) % L] != 2:
            tau[i] = 1
    changed = True
    while changed:
        changed = False
        for i in range(L - 1, -1, -1):
            j = (i + 1) % L
            if x[i] == 2 and tau[j] < INF and tau[i] != tau[j] + 2:
                tau[i] = tau[j] + 2
                changed = True
            elif x[i] == 1 and x[j] == 2 and tau[j] < INF and tau[i] != tau[j]:
                tau[i] = tau[j]
                changed = True
    return tau


def fuse_row_at(x, t):
    L = len(x)
    tau = burn_times_own(x)
    INF = 1 << 60
    out = []
    for i in range(L):
        j, k = (i + 1) % L, (i + 2) % L
        if t == 0:
            out.append(int(x[i]))
        elif x[i] == 0:
            out.append(0)
        elif x[i] == 2:
            out.append(2 if t <= tau[j] else (1 if t == tau[j] + 1 else 0))
        else:
            out.append(1 if (x[j] == 2 and (tau[k] >= INF or t <= tau[k] + 1)) else 0)
    return out


def part_fuse(tmax):
    t0 = time.time()
    lam, fwbw = [], []
    for t in range(0, tmax + 1):
        F = cone(FUSE, t)
        fw, bw = widths(F)
        fwbw.append((fw, bw))
        lam.append(min(fw, bw))
        print('t', t, fw, bw, round(time.time() - t0, 1), flush=True)
    bounds_ok = all(((t // 2 + 1) // 2) <= lam[t] <= 3 * t + 3 for t in range(2, tmax + 1))
    # burn-time theorem: exhaustive cyclic rows L <= 9, t <= 3L+3, plus random rows
    mism = 0
    tested = 0
    for L in range(1, 10):
        for x in itertools.product(range(3), repeat=L):
            x = np.array(x, dtype=np.int8)
            row = x.copy()
            for t in range(0, 3 * L + 4):
                if t > 0:
                    row = step(FUSE, row)
                tested += 1
                if list(row) != fuse_row_at(x, t):
                    mism += 1
    rng = np.random.default_rng(7)
    mism_r = 0
    for _ in range(200):
        L = int(rng.integers(10, 200))
        x = rng.integers(0, 3, L).astype(np.int8)
        row = x.copy()
        for t in range(0, 2 * L + 5):
            if t:
                row = step(FUSE, row)
            if t % 7 == 0 and list(row) != fuse_row_at(x, t):
                mism_r += 1
    # lower-bound family distinctness at level m = floor(t/2)
    fam = {}
    for t in range(2, min(tmax, 12) + 1):
        m = t // 2
        F = cone(FUSE, t).reshape(3 ** m, -1)
        res = []
        for b in range((m - 1) // 2 + 1):
            pre = [2] + [1, 2] * b + [2] * (m - 1 - 2 * b)
            idx = 0
            for v in pre:
                idx = idx * 3 + v
            res.append(F[idx].tobytes())
        fam[t] = (len(res), len(set(res)))
    return {'lambda': lam, 'fw_bw': fwbw, 'lambda_eq_t_plus_2_for_t_ge_1': all(lam[t] == t + 2 for t in range(1, tmax + 1)),
            'bounds_hold': bounds_ok, 'burn_time_exhaustive_cases': tested, 'burn_time_mismatches': mism,
            'burn_time_random_mismatches': mism_r, 'lower_bound_family_count_distinct': fam,
            'runtime_s': round(time.time() - t0, 1)}


# ------------------------------------------------------------------ cycle detection (reproduce EXP-C15-04 rows)
def part_cycledet():
    t0 = time.time()
    lab = json.load(open(os.path.join(ROOT, 'results', 'EXP-C15-02.json')))['results']['rows']
    mine = json.load(open(os.path.join(OUT, 'c15_census3.json')))['_rows']
    assert [r['table'] for r in lab] == [r['table'] for r in mine]
    wc = [r['wc'] for r in mine]
    rng = np.random.default_rng(1515)
    out = {}
    for L in (16, 32, 64):
        found, mus, lams, notfound_by = 0, [], [], {}
        aff_q = []
        for r, c in zip(mine, wc):
            T = np.array(r['table'], dtype=np.int8)
            row = rng.integers(0, 3, L).astype(np.int8)
            seen = {row.tobytes(): 0}
            ok = False
            for s in range(1, 5001):
                row = step(T, row)
                k = row.tobytes()
                if k in seen:
                    mus.append(seen[k])
                    lams.append(s - seen[k])
                    ok = True
                    break
                seen[k] = s
            if ok:
                found += 1
            else:
                notfound_by[c] = notfound_by.get(c, 0) + 1
        out[L] = {'found': found, 'median_mu': float(np.median(mus)), 'median_lambda': float(np.median(lams)),
                  'not_found_by_width_class': notfound_by}
        print(L, out[L], round(time.time() - t0, 1), flush=True)
    # exact cycle lengths of the affine quasigroups at L = 32, 64 for a random row (own simulation, cap 200000)
    aff = {}
    for name, (a, b, c) in {'x+y': (1, 1, 0), '2x+y': (2, 1, 0), '2x+2y': (2, 2, 0), '2x+2y+1': (2, 2, 1)}.items():
        X, Y = np.arange(3)[:, None], np.arange(3)[None, :]
        T = ((a * X + b * Y + c) % 3).astype(np.int8)
        for L in (32, 64):
            row = np.random.default_rng(99).integers(0, 3, L).astype(np.int8)
            seen = {row.tobytes(): 0}
            res = None
            for s in range(1, 200001):
                row = step(T, row)
                k = row.tobytes()
                if k in seen:
                    res = (seen[k], s - seen[k])
                    break
                seen[k] = s
            aff[f'{name} L={L}'] = res
    out['affine_quasigroup_mu_lambda'] = aff
    out['runtime_s'] = round(time.time() - t0, 1)
    return out


# ------------------------------------------------------------------ semigroups: popcount word, widths of non-commutative groups
def s3_table():
    perms = list(itertools.permutations(range(3)))
    idx = {p: i for i, p in enumerate(perms)}
    T = np.zeros((6, 6), dtype=np.int8)
    for i, g in enumerate(perms):
        for j, h in enumerate(perms):
            T[i, j] = idx[tuple(g[h[x]] for x in range(3))]
    return T


def part_semigroups():
    T = s3_table()
    rng = np.random.default_rng(3)
    # Theorem 1(a): popcount word
    bad = 0
    for _ in range(300):
        t = int(rng.integers(0, 9))
        x = rng.integers(0, 6, t + 1)
        row = x.copy()
        val = x[0]
        # F_t(x0..xt) by recursion on the light cone
        cur = list(x)
        for _ in range(t):
            cur = [int(T[cur[i], cur[i + 1]]) for i in range(len(cur) - 1)]
        word = [x[bin(j).count('1')] for j in range(2 ** t)]
        p = word[0]
        for w in word[1:]:
            p = T[p, w]
        bad += int(p != cur[0])
    lam = []
    for t in range(0, 7):
        F = cone(T, t)
        lam.append(widths(F))
    # commutative / abelian comparison: Z6
    Z6 = ((np.arange(6)[:, None] + np.arange(6)[None, :]) % 6).astype(np.int8)
    lamz = [widths(cone(Z6, t)) for t in range(0, 7)]
    return {'popcount_word_mismatches': bad, 'S3_widths_fw_bw_t0_6': lam, 'Z6_widths_fw_bw_t0_6': lamz,
            'S3_order': 6}


# ------------------------------------------------------------------ fast-forward formulas (Theorems 2, 3)
def poly_pow_cyclic(coeffs, t, n):
    L = len(coeffs)
    res = np.zeros(L, dtype=np.int64)
    res[0] = 1 % n
    base = np.array(coeffs, dtype=np.int64) % n

    def mul(p, q):
        full = np.convolve(p, q)          # exact integer convolution (values < n^2 L)
        out = full[:L].copy()
        out[:len(full) - L] += full[L:]
        return out % n
    while t:
        if t & 1:
            res = mul(res, base)
        base = mul(base, base)
        t >>= 1
    return res


def affine_ff(a, b, c, n, row, t):
    L = len(row)
    co = np.zeros(L, dtype=np.int64)
    co[0] = a % n
    co[1 % L] = (co[1 % L] + b) % n
    P = poly_pow_cyclic(co, t, n)
    # (P r)_i = sum_j P_j r_{i+j}
    lin = np.array([int(sum(int(P[j]) * int(row[(i + j) % L]) for j in range(L)) % n) for i in range(L)])
    q = (a + b) % n
    g = 0
    for _ in range(min(t, 10 ** 6)):
        g = (g * q + 1) % n            # sum_{s<t} q^s, by Horner (t small here)
    return (lin + c * g) % n


def part_fastforward():
    rng = np.random.default_rng(15)
    res = {}
    mism = 0
    for (a, b, c, n) in [(1, 1, 0, 2), (1, 1, 0, 3), (1, 2, 1, 3), (2, 2, 0, 3), (1, 2, 1, 5), (3, 5, 2, 7)]:
        X, Y = np.arange(n)[:, None], np.arange(n)[None, :]
        T = ((a * X + b * Y + c) % n).astype(np.int64)
        for _ in range(6):
            L = int(rng.integers(5, 60))
            row = rng.integers(0, n, L)
            for t in (0, 1, 2, 7, 50, 333, 1000):
                if not np.array_equal(affine_ff(a, b, c, n, row, t), simulate(T, row, t)):
                    mism += 1
    res['affine_mismatches'] = mism
    # Theorem 3: all commutative semigroups of order 3 (from the 19683 tables), exponent arithmetic vs simulation
    tabs = all_tables3()
    comm_semis = [T for T in tabs if is_assoc(T) and (T == T.T).all()]
    bad3 = 0
    checked = 0
    for T in comm_semis:
        ip = []
        for x in range(3):
            seen, v, m = {}, x, 1
            while v not in seen:
                seen[v] = m
                v = int(T[v, x])
                m += 1
            ip.append((seen[v], m - seen[v]))
        iota = max(i for i, _ in ip)
        lcm = 1
        for _, p in ip:
            lcm = lcm * p // math.gcd(lcm, p)
        for _ in range(3):
            L = int(rng.integers(2, 12))
            row = rng.integers(0, 3, L)
            for t in (2 * L + iota + 1, 2 * L + iota + 7, 3 * L + 11, 200):
                if t < 2 * L + iota + 1:
                    continue
                # exponents N_j = sum_{k = j mod L} C(t, k) exactly (python ints), reduced via index/period
                N = [0] * L
                for k in range(t + 1):
                    N[k % L] += math.comb(t, k)
                out = []
                for i in range(L):
                    acc = None
                    for j in range(L):
                        x = int(row[(i + j) % L])
                        e = N[j]
                        i_x, p_x = ip[x]
                        e_red = i_x + ((e - i_x) % p_x) if e >= i_x else e
                        val = x
                        for _ in range(e_red - 1):
                            val = int(T[val, x])
                        acc = val if acc is None else int(T[acc, val])
                    out.append(acc)
                checked += 1
                bad3 += int(out != list(simulate(T, row, t)))
    res['commutative_semigroups_order3'] = len(comm_semis)
    res['thm3_cases'] = checked
    res['thm3_mismatches'] = bad3
    return res


# ------------------------------------------------------------------ misc: order 2, Laver, GF(4), band
def laver(n):
    N = 2 ** n
    T = np.zeros((N + 1, N + 1), dtype=np.int64)    # 1-based
    T[N, 1:] = np.arange(1, N + 1)                   # N is a left identity: N * q = q
    for p in range(N - 1, 0, -1):
        T[p, 1] = p + 1
        for q in range(1, N):
            T[p, q + 1] = T[T[p, q], p + 1]          # p*(q+1) = (p*q)*(p+1), row p*q > p already known
    return (T[1:, 1:] - 1).astype(np.int8)


def part_misc():
    out = {}
    rules = []
    for code in range(16):
        T = np.array([[code >> 3 & 1, code >> 2 & 1], [code >> 1 & 1, code & 1]], dtype=np.int8)
        rule = sum(int(T[c, r]) << (4 * l + 2 * c + r) for l in (0, 1) for c in (0, 1) for r in (0, 1))
        rules.append((rule, surjective(T)))
    out['order2_rules'] = sorted(r for r, _ in rules)
    out['order2_surjective_rules'] = sorted(r for r, s in rules if s)
    xor2 = np.array([[0, 1], [1, 0]], dtype=np.int8)
    out['xor_essential_eq_2_popcount'] = all(len(essential(cone(xor2, t))) == 2 ** bin(t).count('1') for t in range(15))
    for nm, n, tm in (('A2', 2, 8), ('A3', 3, 5)):
        T = laver(n)
        out[f'laver_{nm}'] = {'ess': [len(essential(cone(T, t))) for t in range(tm + 1)],
                              'widths': [widths(cone(T, t)) for t in range(tm + 1)],
                              'left_distributive': bool(all(T[a, T[b, c]] == T[T[a, b], T[a, c]] for a in range(2 ** n)
                                                            for b in range(2 ** n) for c in range(2 ** n)))}
    gf4 = np.array([[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]], dtype=np.int8)
    xor4 = (np.arange(4)[:, None] ^ np.arange(4)[None, :]).astype(np.int8)
    out['gf4_widths'] = [widths(cone(gf4, t)) for t in range(8)]
    out['xor4_widths'] = [widths(cone(xor4, t)) for t in range(8)]
    band = np.array([[2 * (x // 2) + (y % 2) for y in range(4)] for x in range(4)], dtype=np.int8)
    out['band'] = {'assoc': is_assoc(band), 'surjective': surjective(band), 'injective': injective(band),
                   'permutive': permutive(band), 'cyclic_bijective_L1_6': all(cyclic_bijective(band, L) for L in range(1, 7))}
    # all order-2 tables: surjective iff permutive
    out['order2_surj_iff_perm'] = all(surjective(np.array([[c >> 3 & 1, c >> 2 & 1], [c >> 1 & 1, c & 1]], np.int8)) ==
                                      permutive(np.array([[c >> 3 & 1, c >> 2 & 1], [c >> 1 & 1, c & 1]], np.int8))
                                      for c in range(16))
    # anchored C06 models: x + 1 + a y mod N
    for nm, (a, N) in {'golden5': (2, 5), 'golden11': (3, 11), 'odd5': (3, 5)}.items():
        X, Y = np.arange(N)[:, None], np.arange(N)[None, :]
        T = ((X + 1 + a * Y) % N).astype(np.int8)
        out[nm] = {'permutive': permutive(T), 'surjective': surjective(T)}
    return out


if __name__ == '__main__':
    part = sys.argv[1]
    t0 = time.time()
    if part == 'fuse':
        res = part_fuse(int(sys.argv[2]) if len(sys.argv) > 2 else 12)
    else:
        res = {'census3': part_census3, 'cycledet': part_cycledet, 'semigroups': part_semigroups,
               'fastforward': part_fastforward, 'misc': part_misc}[part]()
    res['runtime_total_s'] = round(time.time() - t0, 1)
    with open(os.path.join(OUT, f'c15_{part}.json'), 'w') as f:
        json.dump(res, f, indent=1, default=str)
    print(json.dumps({k: v for k, v in res.items() if not str(k).startswith('_')}, default=str)[:5000])
