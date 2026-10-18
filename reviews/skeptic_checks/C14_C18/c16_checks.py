"""Skeptic checks for cycle C16 (Fibonacci dynamics x_{k+1} = x_k * x_{k-1} in finite magmas). Own code only.

usage: python3 c16_checks.py small|latin|certs|isotopes|groups|nimbers
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


# ------------------------------------------------------------------ pair map tools (own)
def cycle_lengths(T):
    """cycle lengths of P(a,b) = (b, T[b,a]) on all n^2 states (functional graph: only periodic states)."""
    n = T.shape[0]
    S = n * n
    nxt = [0] * S
    for a in range(n):
        for b in range(n):
            nxt[a * n + b] = b * n + int(T[b, a])
    # periodic states: iterate S times from each... use colouring
    color = [0] * S
    cycles = []
    for s0 in range(S):
        if color[s0]:
            continue
        path = []
        s = s0
        while color[s] == 0:
            color[s] = 1
            path.append(s)
            s = nxt[s]
        if color[s] == 1:
            i = path.index(s)
            cycles.append(len(path) - i)
        for u in path:
            color[u] = 2
    return cycles


def full_period(T):
    n = T.shape[0]
    a = b = 0
    for k in range(1, n * n + 1):
        a, b = b, int(T[b, a])
        if a == 0 and b == 0:
            return k == n * n
    return False


def full_period_batch(Ts):
    """vectorised: orbit length of (0,0) equals n^2 (and P is a bijection when rows are permutations)."""
    B, n, _ = Ts.shape
    a = np.zeros(B, np.int64)
    b = np.zeros(B, np.int64)
    first_return = np.zeros(B, np.int64)
    idx = np.arange(B)
    for k in range(1, n * n + 1):
        a, b = b, Ts[idx, b, a]
        hit = (a == 0) & (b == 0) & (first_return == 0)
        first_return[hit] = k
    return first_return == n * n


def sign_of(perm):
    perm = list(perm)
    seen = [False] * len(perm)
    s = 1
    for i in range(len(perm)):
        if not seen[i]:
            j, L = i, 0
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                L += 1
            if L % 2 == 0:
                s = -s
    return s


def row_sign_product(T):
    s = 1
    for b in range(T.shape[0]):
        s *= sign_of(T[b])
    return s


def is_latin(T):
    n = T.shape[0]
    r = np.arange(n)
    return bool((np.sort(T, 1) == r).all() and (np.sort(T, 0) == r[:, None]).all())


# ------------------------------------------------------------------ part small: n <= 4
def part_small():
    out = {}
    for n in (2, 3):
        tabs = np.array(list(itertools.product(range(n), repeat=n * n)), np.int64).reshape(-1, n, n)
        rowperm = np.array([all(len(set(T[b])) == n for b in range(n)) for T in tabs])
        maxp, fullq, qmax, nfull = 0, 0, 0, 0
        for T, rp in zip(tabs, rowperm):
            cl = cycle_lengths(T)
            m = max(cl)
            maxp = max(maxp, m)
            if m == n * n:
                nfull += 1
                if is_latin(T):
                    fullq += 1
            if is_latin(T):
                qmax = max(qmax, m)
        out[n] = {'tables': len(tabs), 'row_permutation_tables': int(rowperm.sum()), 'full_period_tables': nfull,
                  'full_period_quasigroups': fullq, 'max_period': maxp, 'quasigroup_max_period': qmax}
    # n = 4: all row-permutation tables (24^4 = 331776)
    perms = np.array(list(itertools.permutations(range(4))), np.int64)
    idx = np.array(list(itertools.product(range(24), repeat=4)), np.int64)
    Ts = perms[idx]                     # row b = perms[idx[b]]  (L_b)
    fp = full_period_batch(Ts)
    lat = np.array([is_latin(T) for T in Ts[fp]]) if fp.any() else np.array([])
    # quasigroup max period n = 4
    lats = [T for T in Ts if is_latin(T)]
    out[4] = {'row_permutation_tables': len(Ts), 'full_period_tables': int(fp.sum()),
              'full_period_quasigroups': int(lat.sum()) if len(lat) else 0, 'latin_squares': len(lats),
              'quasigroup_max_period': max(max(cycle_lengths(T)) for T in lats)}
    # parity check on every full-period table of order 3 and 4
    for n in (3, 4):
        if n == 3:
            tabs = np.array(list(itertools.product(range(3), repeat=9)), np.int64).reshape(-1, 3, 3)
            F = [T for T in tabs if max(cycle_lengths(T)) == 9]
        else:
            F = Ts[fp]
        need = (-1) ** ((n - 1) * (n + 2) // 2)
        out[n]['parity_violations_among_full_period'] = int(sum(row_sign_product(T) != need for T in F))
    T = np.array([[1, 0], [1, 0]])   # x*y = 1 - y : T[x, y] = 1 - y
    out['H-C16-1 example x*y=1-y cycles'] = cycle_lengths(T)
    out['predicted_de_bruijn_counts'] = {n: math.factorial(n) ** n // (n * n) for n in (2, 3, 4)}
    return out


# ------------------------------------------------------------------ part latin: all Latin squares of order <= 5
def latin_squares(n):
    perms = list(itertools.permutations(range(n)))
    out = []

    def rec(rows):
        if len(rows) == n:
            out.append([list(r) for r in rows])
            return
        for p in perms:
            if all(p[c] != r[c] for r in rows for c in range(n)):
                rows.append(p)
                rec(rows)
                rows.pop()
    rec([])
    return np.array(out, np.int64)


def canon_iso(T):
    n = T.shape[0]
    best = None
    for p in itertools.permutations(range(n)):
        p = np.array(p)
        inv = np.argsort(p)
        U = p[T[np.ix_(inv, inv)]]          # U[p[a], p[b]] = p[T[a, b]]
        k = tuple(U.ravel())
        if best is None or k < best:
            best = k
    return best


def automorphisms(T):
    n = T.shape[0]
    cnt = 0
    for p in itertools.permutations(range(n)):
        p = np.array(p)
        inv = np.argsort(p)
        if np.array_equal(p[T[np.ix_(inv, inv)]], T):
            cnt += 1
    return cnt


def isotopic_to_group(T):
    """Albert: a quasigroup is isotopic to a group iff its loop isotope x o y = T[R^-1 x, L^-1 y] is associative."""
    n = T.shape[0]
    R = T[:, 0]                     # R_0(x) = x * 0
    Lr = T[0, :]                    # L_0(y) = 0 * y
    Rinv = np.argsort(R)
    Linv = np.argsort(Lr)
    U = T[np.ix_(Rinv, Linv)]       # U[x, y] = T[R^-1 x, L^-1 y]
    a, b, c = np.ix_(range(n), range(n), range(n))
    return bool((U[U[a, b], c] == U[a, U[b, c]]).all())


def part_latin():
    out = {}
    full5 = None
    for n in (2, 3, 4, 5):
        t0 = time.time()
        L = latin_squares(n)
        fp = full_period_batch(L)
        out[str(n)] = {'latin_squares': len(L), 'full_period': int(fp.sum()), 'time_s': round(time.time() - t0, 1)}
        if n == 5:
            full5 = L[fp]
            L5 = L
        # max period among quasigroups
        if n <= 4:
            out[str(n)]['max_period'] = max(max(cycle_lengths(T)) for T in L)
    keys = {}
    for T in full5:
        keys.setdefault(canon_iso(T), []).append(T)
    auts = [automorphisms(v[0]) for v in keys.values()]
    need = (-1) ** ((5 - 1) * (5 + 2) // 2)
    out['5']['iso_classes'] = len(keys)
    out['5']['class_sizes'] = sorted(set(len(v) for v in keys.values()))
    out['5']['automorphism_group_orders'] = sorted(set(auts))
    out['5']['parity_violations'] = int(sum(row_sign_product(T) != need for T in full5))
    iso_group = [isotopic_to_group(T) for T in full5]
    out['5']['full_period_isotopic_to_Z5'] = int(sum(iso_group))
    # all Latin squares of order 5 isotopic to Z5 (control: expected (5!)^3/100 = 17280)
    out['5']['all_latin_isotopic_to_Z5'] = int(sum(isotopic_to_group(T) for T in L5))
    # example cycle (first full-period square) for later product checks
    T = full5[0]
    seq, a, b = [0], 0, 0
    while True:
        a, b = b, int(T[b, a])
        if (a, b) == (0, 0):
            break
        seq.append(a)
    out['5']['example_cycle'] = seq
    # lab's example cycle in the claim: build its table and test
    claim = [0, 0, 1, 0, 2, 2, 0, 3, 3, 1, 2, 1, 4, 0, 4, 4, 2, 3, 2, 4, 1, 1, 3, 4, 3]
    Tc = table_from_cycle(claim)
    out['5']['claimed_example_is_full_period_quasigroup'] = bool(Tc is not None and is_latin(Tc) and full_period(Tc))
    out['5']['claimed_example_isotopic_to_Z5'] = bool(Tc is not None and isotopic_to_group(Tc))
    return out


def table_from_cycle(seq):
    L = len(seq)
    n = int(round(L ** 0.5))
    T = -np.ones((n, n), np.int64)
    for i in range(L):
        a, b, c = seq[i - 1], seq[i], seq[(i + 1) % L]
        if T[b, a] not in (-1, c):
            return None
        T[b, a] = c
    return T if (T >= 0).all() else None


# ------------------------------------------------------------------ part certs: stored examples 6..16 and products
def product_table(A, B):
    n1, n2 = A.shape[0], B.shape[0]
    i = np.repeat(np.arange(n1), n2)
    j = np.tile(np.arange(n2), n1)
    return A[i[:, None], i[None, :]] * n2 + B[j[:, None], j[None, :]]


def part_certs():
    lab = json.load(open(os.path.join(ROOT, 'results', 'EXP-C16-02.json')))['results']['examples']
    mine = json.load(open(os.path.join(OUT, 'c16_latin.json')))
    out = {}
    base = {5: table_from_cycle(mine['5']['example_cycle'])}
    for k, v in sorted(lab.items(), key=lambda kv: int(kv[0])):
        T = table_from_cycle(v['cycle'])
        n = int(k)
        ok = T is not None and T.shape[0] == n and is_latin(T)
        cl = cycle_lengths(T) if ok else None
        out[k] = {'latin': ok, 'single_cycle_n2': bool(ok and cl == [n * n]),
                  'parity_ok': bool(ok and row_sign_product(T) == (-1) ** ((n - 1) * (n + 2) // 2)),
                  'isotopic_to_group': bool(ok and isotopic_to_group(T)), 'construction': v['construction']}
        base[n] = T
    prods = {}
    for n1, n2 in ((5, 6), (5, 7), (5, 8), (6, 7), (7, 8), (5, 9), (7, 9), (8, 9)):
        P = product_table(base[n1], base[n2])
        prods[f'{n1}x{n2}'] = {'latin': is_latin(P), 'full_period': full_period(P)}
    # non-coprime control: 2-fold product of the same order cannot be full period by CRT (lcm < n^2)
    P = product_table(base[6], base[6])
    prods['6x6 (control, not coprime)'] = {'latin': is_latin(P), 'full_period': full_period(P),
                                           'max_cycle': max(cycle_lengths(P))}
    out['products'] = prods
    return out


# ------------------------------------------------------------------ part isotopes / groups: own group tables
def cyclic(n):
    x = np.arange(n)
    return (x[:, None] + x[None, :]) % n


def direct(A, B):
    return product_table(A, B)


def perm_group(gens):
    deg = len(gens[0])
    e = tuple(range(deg))
    elems, frontier = [e], [e]
    seen = {e}
    while frontier:
        new = []
        for x in frontier:
            for g in gens:
                y = tuple(g[i] for i in x)
                if y not in seen:
                    seen.add(y)
                    elems.append(y)
                    new.append(y)
        frontier = new
    idx = {p: i for i, p in enumerate(elems)}
    n = len(elems)
    T = np.zeros((n, n), np.int64)
    for i, g in enumerate(elems):
        for j, h in enumerate(elems):
            T[i, j] = idx[tuple(g[h[x]] for x in range(deg))]
    return T


def dihedral(m):
    r = tuple((i + 1) % m for i in range(m))
    s = tuple((-i) % m for i in range(m))
    return perm_group([r, s])


def dicyclic(m):
    """Dic_m of order 4m as permutations of its own elements: <a, x | a^2m = 1, x^2 = a^m, x a x^-1 = a^-1>.
    Elements (k, e) = a^k x^e; multiplication: a^k x^e * a^l x^f = a^(k + (-1)^e l) x^(e+f), x^2 = a^m."""
    N = 2 * m
    el = [(k, e) for e in (0, 1) for k in range(N)]
    idx = {v: i for i, v in enumerate(el)}

    def mul(u, v):
        (k, e), (l, f) = u, v
        kk = (k + (l if e == 0 else -l)) % N
        ee = e + f
        if ee == 2:
            kk = (kk + m) % N
            ee = 0
        return (kk, ee)
    T = np.zeros((2 * N, 2 * N), np.int64)
    for i, u in enumerate(el):
        for j, v in enumerate(el):
            T[i, j] = idx[mul(u, v)]
    return T


def is_group(T):
    n = T.shape[0]
    a, b, c = np.ix_(range(n), range(n), range(n))
    return bool((T[T[a, b], c] == T[a, T[b, c]]).all()) and is_latin(T)


def part_isotopes():
    groups = {'Z2': cyclic(2), 'Z4': cyclic(4), 'Z2xZ2': direct(cyclic(2), cyclic(2)), 'Z6': cyclic(6),
              'S3': dihedral(3), 'Z8': cyclic(8), 'Z2xZ4': direct(cyclic(2), cyclic(4)),
              'Z2^3': direct(cyclic(2), direct(cyclic(2), cyclic(2))), 'D4': dihedral(4), 'Q8': dicyclic(2),
              'Z10': cyclic(10), 'D5': dihedral(5), 'Z12': cyclic(12), 'Z2xZ6': direct(cyclic(2), cyclic(6)),
              'A4': perm_group([(1, 2, 0, 3), (1, 0, 3, 2)]), 'D6': dihedral(6), 'Dic3': dicyclic(3),
              'Z14': cyclic(14), 'D7': dihedral(7), 'Z16': cyclic(16), 'Z4xZ4': direct(cyclic(4), cyclic(4)),
              'Z2xZ8': direct(cyclic(2), cyclic(8)), 'D8': dihedral(8), 'Q16': dicyclic(4),
              'Z2xD4': direct(cyclic(2), dihedral(4)), 'Z2xQ8': direct(cyclic(2), dicyclic(2)),
              'Z18': cyclic(18), 'D9': dihedral(9), 'Z3xS3': direct(cyclic(3), dihedral(3)),
              'Z20': cyclic(20), 'Dic5': dicyclic(5), 'S4': perm_group([(1, 2, 3, 0), (1, 0, 2, 3)]),
              'SL(2,3)-free check: Z2xA4': direct(cyclic(2), perm_group([(1, 2, 0, 3), (1, 0, 3, 2)])),
              'Z24': cyclic(24), 'Z30': cyclic(30), 'D15': dihedral(15)}
    rng = np.random.default_rng(1616)
    out = {}
    for name, G in groups.items():
        n = G.shape[0]
        assert is_group(G), name
        m = n // 2
        # exact: sign of the left regular representation product
        lam = 1
        for g in range(n):
            lam *= sign_of(G[g])
        need = (-1) ** ((n - 1) * (n + 2) // 2)
        seen_signs, full = set(), 0
        trials = 300 if n <= 16 else 60
        for _ in range(trials):
            al, be, ga = rng.permutation(n), rng.permutation(n), rng.permutation(n)
            T = ga[G[al[:, None], be[None, :]]]
            seen_signs.add(row_sign_product(T))
            full += full_period(T)
        out[name] = {'order': n, 'prod_sgn_left_regular': lam, 'predicted_(-1)^m': (-1) ** m,
                     'needed_for_full_period': need, 'isotope_row_sign_products': sorted(seen_signs),
                     'random_isotopes': trials, 'full_period_isotopes': full}
    out['all_consistent'] = all(v['prod_sgn_left_regular'] == v['predicted_(-1)^m'] and
                                v['isotope_row_sign_products'] == [v['predicted_(-1)^m']] and
                                v['full_period_isotopes'] == 0 and v['needed_for_full_period'] != v['predicted_(-1)^m']
                                for k, v in out.items() if isinstance(v, dict))
    # odd orders: isotopes of Z_n with a full period exist? (sampling; n = 5 exhaustive in part latin)
    odd = {}
    for n in (7, 9, 11, 13, 15, 17, 19, 21):
        G = cyclic(n)
        hits = 0
        trials = 3000
        for _ in range(trials):
            al, be, ga = rng.permutation(n), rng.permutation(n), rng.permutation(n)
            hits += full_period(ga[G[al[:, None], be[None, :]]])
        odd[n] = {'trials': trials, 'full_period_isotopes': hits, 'rate_times_n2': round(hits / trials * n * n, 2)}
    out['odd_cyclic_isotopes'] = odd
    return out


def part_groups():
    gs = {'S3': dihedral(3), 'D4': dihedral(4), 'Q8': dicyclic(2), 'A4': perm_group([(1, 2, 0, 3), (1, 0, 3, 2)]),
          'S4': perm_group([(1, 2, 3, 0), (1, 0, 2, 3)])}
    out = {}
    for k, G in gs.items():
        cl = cycle_lengths(G)
        out[k] = {'order': G.shape[0], 'max_period': max(cl), 'period_set': sorted(set(cl))}
    return out


def part_nimbers():
    P = np.fromfile(os.path.join(OUT, 'nim256_mex.bin'), np.uint8).reshape(256, 256).astype(np.int64)

    def pisano(m):
        a, b, k = 0, 1, 0
        while True:
            a, b = b, (a + b) % m
            k += 1
            if (a, b) == (0, 1):
                return k
    out = {}
    for q in (4, 16, 256):
        T = P[:q, :q]
        cl = cycle_lengths(T)
        # pairs containing 0 reach (0,0) within two steps
        ok0 = True
        for a in range(q):
            for b in range(q):
                if a == 0 or b == 0:
                    x, y = a, b
                    for _ in range(2):
                        x, y = y, int(T[y, x])
                    ok0 &= (x, y) == (0, 0)
        out[q] = {'max_period': max(cl), 'pisano(q-1)': pisano(q - 1), 'zero_pairs_reach_00_in_2_steps': ok0,
                  'subfield_closed': bool((T < q).all())}
    return out


if __name__ == '__main__':
    part = sys.argv[1]
    t0 = time.time()
    res = {'small': part_small, 'latin': part_latin, 'certs': part_certs, 'isotopes': part_isotopes,
           'groups': part_groups, 'nimbers': part_nimbers}[part]()
    res['runtime_s'] = round(time.time() - t0, 1)
    with open(os.path.join(OUT, f'c16_{part}.json'), 'w') as f:
        json.dump(res, f, indent=1, default=str)
    print(json.dumps(res, default=str)[:4000])
