"""Skeptic checks for cycle C17 (deciding laws of finite magmas).  Independent of systems/ and lab/;
pysat is used only as a SAT solver on my own CNF encoding.  Lab results are only read for comparison.

usage: python3 c17_checks.py <part>
parts: light anchored rs bench anchor_counts anchor_census ld
"""
import itertools
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


# ------------------------------------------------------------------ basic magma helpers
def is_assoc(T):
    n = len(T)
    return all(T[T[a][b]][c] == T[a][T[b][c]] for a in range(n) for b in range(n) for c in range(n))


def generated(T, S):
    cur = set(S)
    while True:
        new = {T[a][b] for a in cur for b in cur} - cur
        if not new:
            return cur
        cur |= new


def light_verdict(T, S):
    n = len(T)
    return all(T[T[x][s]][y] == T[x][T[s][y]] for s in S for x in range(n) for y in range(n))


def part_light():
    res = {}
    for n in (1, 2, 3):
        bad, checked, n_assoc = 0, 0, 0
        for flat in itertools.product(range(n), repeat=n * n):
            T = [list(flat[i * n:(i + 1) * n]) for i in range(n)]
            A = is_assoc(T)
            n_assoc += A
            for k in range(1, n + 1):
                for S in itertools.combinations(range(n), k):
                    if len(generated(T, S)) == n:
                        checked += 1
                        if light_verdict(T, S) != A:
                            bad += 1
        res[n] = {"tables": n ** (n * n), "associative": n_assoc, "generating_sets_checked": checked,
                  "wrong_verdicts": bad}
    # n = 4: random tables and all subsets that generate
    rng = np.random.default_rng(4)
    bad, checked = 0, 0
    for _ in range(20000):
        T = rng.integers(0, 4, (4, 4)).tolist()
        A = is_assoc(T)
        for k in range(1, 5):
            for S in itertools.combinations(range(4), k):
                if len(generated(T, S)) == 4:
                    checked += 1
                    bad += light_verdict(T, S) != A
    res["4_random_20000"] = {"generating_sets_checked": checked, "wrong_verdicts": bad}
    # a generating set is necessary: a non-associative table that passes the test for a non-generating S
    return res


def part_anchored():
    res = {}
    for n in (2, 3):
        cnt = {"tables": 0, "assoc": 0, "instance": 0, "is_x_plus_y_plus_1": 0, "disagree": 0}
        free = [(x, y) for x in range(n) for y in range(1, n)]
        for vals in itertools.product(range(n), repeat=len(free)):
            T = [[(x + 1) % n if y == 0 else 0 for y in range(n)] for x in range(n)]
            for (x, y), v in zip(free, vals):
                T[x][y] = v
            cnt["tables"] += 1
            A = is_assoc(T)
            I = all(T[x][(y + 1) % n] == (T[x][y] + 1) % n for x in range(n) for y in range(n))
            E = all(T[x][y] == (x + y + 1) % n for x in range(n) for y in range(n))
            cnt["assoc"] += A
            cnt["instance"] += I
            cnt["is_x_plus_y_plus_1"] += E
            cnt["disagree"] += not (A == I == E)
        res[n] = cnt
    return res


# ------------------------------------------------------------------ Rajagopalan-Schulman: exact detection probability
def rs_exact_prob(T):
    """Exact Pr over uniform u, v, w in GF(2)^n that (u*v)*w != u*(v*w) in the magma algebra."""
    n = T.shape[0]
    D = np.zeros((n, n, n, n), dtype=np.int64)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                D[a, b, c, T[T[a, b], c]] ^= 1
                D[a, b, c, T[a, T[b, c]]] ^= 1
    U = np.array(list(itertools.product((0, 1), repeat=n)), dtype=np.int64)       # all subsets
    R = np.einsum("ia,jb,kc,abcd->ijkd", U, U, U, D) & 1
    return float((R.any(axis=3)).mean())


def part_rs():
    res = {}
    for n in (2, 3):
        minp, n_nonassoc, below, assoc_rejected = 1.0, 0, 0, 0
        argmin = None
        for flat in itertools.product(range(n), repeat=n * n):
            T = np.array(flat).reshape(n, n)
            p = rs_exact_prob(T)
            if is_assoc(T.tolist()):
                assoc_rejected += p > 0
                continue
            n_nonassoc += 1
            if p < minp:
                minp, argmin = p, T.tolist()
            below += p < 1 / 8
        res[n] = {"non_associative": n_nonassoc, "min_detection_probability": minp, "argmin": argmin,
                  "tables_below_1/8": below, "associative_tables_ever_rejected": assoc_rejected}
    # n = 4: random non-associative tables, and one-entry corruptions of Z_4
    rng = np.random.default_rng(5)
    ps = []
    for _ in range(300):
        T = rng.integers(0, 4, (4, 4))
        if not is_assoc(T.tolist()):
            ps.append(rs_exact_prob(T))
    Z = (np.arange(4)[:, None] + np.arange(4)[None, :]) % 4
    pc = []
    for a in range(4):
        for b in range(4):
            for v in range(4):
                if v != Z[a, b]:
                    U = Z.copy()
                    U[a, b] = v
                    pc.append(rs_exact_prob(U))
    res["4_random_300_min"] = min(ps)
    res["4_Z4_corruptions_min"] = min(pc)
    return res


# ------------------------------------------------------------------ benchmark: early-exit exhaustive baseline
def first_violation_probes(T):
    """Sequential exhaustive check in lexicographic order (a, b, c), 4 probes per triple, stopping at the first
    violation.  Returns probes used (4 n^3 for associative tables)."""
    n = T.shape[0]
    for a in range(n):
        ab = T[a, :]                         # a*b
        left = T[ab, :]                      # (a*b)*c   (b, c)
        right = T[a, T]                      # a*(b*c)   (b, c)
        bad = np.nonzero((left != right).ravel())[0]
        if bad.size:
            return 4 * (a * n * n + int(bad[0]) + 1)
    return 4 * n ** 3


def greedy_gens(T):
    n = T.shape[0]
    inside = np.zeros(n, dtype=bool)
    gens, probes = [], 0
    while not inside.all():
        g = int(np.argmin(inside))
        gens.append(g)
        inside[g] = True
        while True:
            idx = np.nonzero(inside)[0]
            prod = T[np.ix_(idx, idx)].ravel()
            probes += idx.size ** 2
            if inside[prod].all():
                break
            inside[prod] = True
    return gens, probes


def light_probes(T, gens):
    n = T.shape[0]
    p = 0
    for s in gens:
        p += 2 * n + 2 * n * n
        if not np.array_equal(T[T[:, s], :], T[:, T[s, :]]):
            return False, p
    return True, p


def part_bench():
    rng = np.random.default_rng(20261018)
    rows = []
    for n in (32, 64, 128, 256, 512):
        x = np.arange(n)
        fams = [("cyclic", (x[:, None] + x[None, :]) % n), ("anchored", (x[:, None] + x[None, :] + 1) % n),
                ("left_zero", np.tile(x[:, None], (1, n)))]
        for i in range(3):
            for base in ("cyclic", "anchored"):
                T = dict(fams[:2])[base].copy()
                while True:
                    a, b = (int(v) for v in rng.integers(0, n, 2))
                    if base == "anchored" and b == 0:
                        continue
                    break
                T[a, b] = (T[a, b] + 1 + int(rng.integers(0, n - 1))) % n
                fams.append((f"{base}+1err", T))
            fams.append(("random", rng.integers(0, n, (n, n))))
        for fam, T in fams:
            ex = first_violation_probes(T)
            gens, pg = greedy_gens(T)
            ok, pl = light_probes(T, gens)
            slab = 4 * n ** 3 if ex == 4 * n ** 3 else 4 * min(64, n) * n * n    # the lab's slab accounting
            rows.append({"n": n, "family": fam, "associative": ex == 4 * n ** 3, "early_exit_probes": ex,
                         "light_incl_gens": pl + pg, "n_gens": len(gens),
                         "ratio_early_exit_over_light": round(ex / (pl + pg), 4),
                         "slab64_probes": slab, "ratio_slab64_over_light": round(slab / (pl + pg), 2)})
    summ = {}
    for r in rows:
        k = (r["family"], r["n"])
        summ.setdefault(f"{k[0]}@{k[1]}", []).append([r["ratio_early_exit_over_light"], r["ratio_slab64_over_light"],
                                                       r["early_exit_probes"]])
    return {"rows": rows, "summary_[early_exit_ratio, slab64_ratio, early_exit_probes]": summ}


# ------------------------------------------------------------------ laws (my own generation of the C06 family)
def shapes(k):
    if k == 1:
        return ["."]
    out = []
    for i in range(1, k):
        for L in shapes(i):
            for R in shapes(k - i):
                out.append((L, R))
    return out


def fill(sh, labels):
    it = iter(labels)

    def go(s):
        if s == ".":
            return next(it)
        return (go(s[0]), go(s[1]))
    return go(sh)


def tstr(t):
    if isinstance(t, str):
        return t
    a, b = tstr(t[0]), tstr(t[1])
    return (a if isinstance(t[0], str) else f"({a})") + (b if isinstance(t[1], str) else f"({b})")


def nleaves(sh):
    return 1 if sh == "." else nleaves(sh[0]) + nleaves(sh[1])


def all_laws():
    rhs = []
    for k in (3, 4):
        for sh in shapes(k):
            for lab in itertools.product("xyz", repeat=k):
                if set(lab) == {"x", "y", "z"}:
                    rhs.append(fill(sh, lab))
    out = []
    for lhs in (("x", ("y", "z")), (("x", "y"), "z")):
        for t in rhs:
            if t != lhs:
                out.append((f"{tstr(lhs)} = {tstr(t)}", lhs, t))
    return out


def parse(s):
    """'x(yz)' -> ('x', ('y','z')).  A term is one factor or two factors; a factor is a letter or (term)."""
    pos = 0

    def factor():
        nonlocal pos
        if s[pos] == "(":
            pos += 1
            t = term()
            assert s[pos] == ")"
            pos += 1
            return t
        c = s[pos]
        pos += 1
        return c

    def term():
        nonlocal pos
        a = factor()
        if pos < len(s) and s[pos] != ")":
            b = factor()
            return (a, b)
        return a
    t = term()
    assert pos == len(s)
    return t


def evaluate(T, t, env):
    if isinstance(t, str):
        return env[t]
    return T[evaluate(T, t[0], env)][evaluate(T, t[1], env)]


def subst0(t):
    if isinstance(t, str):
        return "0" if t == "z" else t
    return (subst0(t[0]), subst0(t[1]))


class Enc:
    """My own CNF: table variables t[x][y][k], one-hot term values with subterm sharing."""

    def __init__(self, N):
        self.N = N
        self.nv = 0
        self.cl = []
        self.tv = [[[self.new() for _ in range(N)] for _ in range(N)] for _ in range(N)]
        for x in range(N):
            for y in range(N):
                v = self.tv[x][y]
                self.cl.append(v[:])
                for i in range(N):
                    for j in range(i + 1, N):
                        self.cl.append([-v[i], -v[j]])
        self.memo = {}

    def new(self):
        self.nv += 1
        return self.nv

    def const(self, c):
        return ("c", c)

    def val(self, t, env):
        """Returns ('c', value) for a constant or ('v', [one-hot vars])."""
        if isinstance(t, str):
            return ("c", 0 if t == "0" else env[t])
        key = (tstr_any(t), tuple(sorted(env.items())))
        if key in self.memo:
            return self.memo[key]
        L, R = self.val(t[0], env), self.val(t[1], env)
        N = self.N
        if L[0] == "c" and R[0] == "c":
            out = ("v", self.tv[L[1]][R[1]])
        else:
            P = [self.new() for _ in range(N)]
            for i in range(N):
                for j in range(N):
                    li = [] if L[0] == "c" else [-L[1][i]]
                    if L[0] == "c" and L[1] != i:
                        continue
                    rj = [] if R[0] == "c" else [-R[1][j]]
                    if R[0] == "c" and R[1] != j:
                        continue
                    for k in range(N):
                        self.cl.append(li + rj + [-self.tv[i][j][k], P[k]])
            for i in range(N):
                for j in range(i + 1, N):
                    self.cl.append([-P[i], -P[j]])
            out = ("v", P)
        self.memo[key] = out
        return out

    def lits(self, v):
        """one-hot literal list of a value (constants become fresh fixed variables)."""
        if v[0] == "v":
            return v[1]
        vs = [self.new() for _ in range(self.N)]
        for k in range(self.N):
            self.cl.append([vs[k]] if k == v[1] else [-vs[k]])
        return vs

    def equal(self, a, b):
        A, B = self.lits(a), self.lits(b)
        for k in range(self.N):
            self.cl.append([-A[k], B[k]])
            self.cl.append([A[k], -B[k]])

    def differ_var(self, a, b):
        A, B = self.lits(a), self.lits(b)
        d = self.new()
        for k in range(self.N):
            self.cl.append([-d, -A[k], -B[k]])
        return d


def tstr_any(t):
    if isinstance(t, str):
        return t
    return "(" + tstr_any(t[0]) + tstr_any(t[1]) + ")"


def build(N, lhs, rhs, violation):
    e = Enc(N)
    for x in range(N):
        e.cl.append([e.tv[x][0][(x + 1) % N]])                     # anchor x*0 = x+1
    s0, t0 = subst0(lhs), subst0(rhs)
    for x in range(N):
        for y in range(N):
            env = {"x": x, "y": y}
            e.equal(e.val(s0, env), e.val(t0, env))
    if violation:
        ds = []
        for x in range(N):
            for y in range(N):
                for z in range(N):
                    env = {"x": x, "y": y, "z": z}
                    ds.append(e.differ_var(e.val(lhs, env), e.val(rhs, env)))
        e.cl.append(ds)
    return e


def table_of(e, model):
    s = set(l for l in model if l > 0)
    N = e.N
    return [[next(k for k in range(N) if e.tv[x][y][k] in s) for y in range(N)] for x in range(N)]


def solve(e, enumerate_limit=0):
    from pysat.solvers import Cadical153
    with Cadical153(bootstrap_with=e.cl) as S:
        if not enumerate_limit:
            ok = S.solve()
            return ok, (table_of(e, S.get_model()) if ok else None)
        tabs = []
        while S.solve():
            T = table_of(e, S.get_model())
            tabs.append(T)
            S.add_clause([-e.tv[x][y][T[x][y]] for x in range(e.N) for y in range(1, e.N)])
            if len(tabs) >= enumerate_limit:
                return False, tabs
        return True, tabs


def check_instance_model(T, lhs, rhs):
    N = len(T)
    s0, t0 = subst0(lhs), subst0(rhs)
    ok_anchor = all(T[x][0] == (x + 1) % N for x in range(N))
    ok_inst = all(evaluate(T, s0, {"x": x, "y": y, "0": 0}) == evaluate(T, t0, {"x": x, "y": y, "0": 0})
                  for x in range(N) for y in range(N))
    full = all(evaluate(T, lhs, {"x": x, "y": y, "z": z}) == evaluate(T, rhs, {"x": x, "y": y, "z": z})
               for x in range(N) for y in range(N) for z in range(N))
    return ok_anchor and ok_inst, full


def part_anchor_counts():
    cases = [("x(yz)", "(xy)z", [2, 3, 4, 5]), ("x(yz)", "y(y(xz))", [2, 3, 4, 5]), ("x(yz)", "x(zy)", [3]),
             ("(xy)z", "(z(xy))x", [3, 4]), ("x(yz)", "y(x(zx))", [4]), ("x(yz)", "(xy)(xz)", [2, 3, 4, 5])]
    res = {}
    for l, r, Ns in cases:
        lhs, rhs = parse(l), parse(r)
        for N in Ns:
            complete, tabs = solve(build(N, lhs, rhs, False), enumerate_limit=20000)
            nviol, bad = 0, 0
            for T in tabs:
                inst_ok, full = check_instance_model(T, lhs, rhs)
                bad += not inst_ok
                nviol += not full
            res[f"{l} = {r} @N={N}"] = {"models_of_instance": len(tabs), "complete": complete,
                                         "violating_full_law": nviol, "models_failing_my_direct_check": bad}
            print(f"{l} = {r} @N={N}", res[f"{l} = {r} @N={N}"], flush=True)
    return res


def part_anchor_census():
    laws = all_laws()
    lab = json.load(open(os.path.join(ROOT, "results", "EXP-C17-02.json")))["results"]
    lab_rows = {r["law"]: r for r in lab["rows"]}
    res = {"n_laws": len(laws), "laws_match_lab_names": sorted(n for n, _, _ in laws) == sorted(lab_rows)}
    status = {}
    t0 = time.time()
    for name, lhs, rhs in laws:
        first_viol = None
        for N in (2, 3, 4, 5):
            sat, T = solve(build(N, lhs, rhs, True))
            if sat:
                inst_ok, full = check_instance_model(T, lhs, rhs)
                assert inst_ok and not full, (name, N)
                first_viol = (N, T)
                break
        status[name] = {"insufficient": first_viol is not None,
                        "first_N_with_counterexample": first_viol[0] if first_viol else None,
                        "counterexample": first_viol[1] if first_viol else None}
    ins = [k for k, v in status.items() if v["insufficient"]]
    dec = [k for k, v in status.items() if not v["insufficient"]]
    lab_dec = {k for k, r in lab_rows.items() if r["instance_decides"]}
    lab_ins = {k for k, r in lab_rows.items() if not r["instance_decides"] and not r["not_decided_by_enumeration"]}
    lab_und = {k for k, r in lab_rows.items() if r["not_decided_by_enumeration"]}
    res.update({"decides_N_le_5": len(dec), "insufficient_N_le_5": len(ins),
                "lab_counts_decides_insufficient_undecided": [len(lab_dec), len(lab_ins), len(lab_und)],
                "my_decides_equals_lab_decides": set(dec) == lab_dec,
                "lab_insufficient_subset_of_mine": lab_ins <= set(ins),
                "lab_undecided_that_are_insufficient": sorted(lab_und & set(ins)),
                "lab_undecided_that_decide_N_le_5": sorted(lab_und & set(dec)),
                "seconds": round(time.time() - t0, 1)})
    json.dump(status, open(os.path.join(OUT, "c17_anchor_census_status.json"), "w"), indent=0)
    return res


# ------------------------------------------------------------------ LD wrap-around instance
def forced_table(N):
    """Unique solution of x*0 = x+1, x*(y+1) = (x*y)*(x+1) for y <= N-2 (rows from N-1 downwards).
    Returns (T, stuck) where stuck is True if a needed row was not yet computed (never expected)."""
    T = [[None] * N for _ in range(N)]
    for x in range(N):
        T[x][0] = (x + 1) % N                      # the anchor column is known for every row
    for x in range(N - 1, -1, -1):
        for y in range(N - 1):
            v = T[x][y]
            if T[v][(x + 1) % N] is None:
                return T, True
            T[x][y + 1] = T[v][(x + 1) % N]
    return T, False


def laver(n):
    """Laver table A_n on {1..2^n} by the standard recursion, returned 0-based (p -> p-1)."""
    N = 2 ** n
    L = [[0] * (N + 1) for _ in range(N + 1)]
    for p in range(N, 0, -1):
        L[p][1] = p % N + 1
        for q in range(1, N):
            L[p][q + 1] = L[L[p][q]][p % N + 1]
    return [[L[p + 1][q + 1] - 1 for q in range(N)] for p in range(N)]


def is_ld_np(T):
    T = np.array(T)
    N = T.shape[0]
    for x in range(N):
        left = T[x, T]                            # x*(y*z)
        right = T[T[x, :][:, None], T[x, :][None, :]]   # (x*y)*(x*z)
        if not np.array_equal(left, right):
            return False
    return True


def part_ld():
    import subprocess
    res = {}
    # Python version (cross-check) for N <= 200
    sols, stuck_py = [], []
    for N in range(1, 201):
        T, stuck = forced_table(N)
        if stuck:
            stuck_py.append(N)
            continue
        if all(T[x][0] == T[T[x][N - 1]][(x + 1) % N] for x in range(N)):
            sols.append(N)
    res["python_N_le_200_solutions"] = sols
    res["python_N_le_200_stuck"] = stuck_py
    # C version for N <= 4096
    out = subprocess.run(["nice", "-n", "10", os.path.join(HERE, "ldforce"), "4096"], capture_output=True,
                         text=True, check=True).stdout.split("\n")
    res["c_N_le_4096_solutions"] = [int(s.split()[1]) for s in out if s.startswith("solution")]
    res["c_N_le_4096_stuck"] = [int(s.split()[1]) for s in out if s.startswith("stuck")]
    res["c_last_line"] = [s for s in out if s.startswith("done")]
    # forced table = Laver table and LD at powers of two (N <= 512)
    lv = {}
    for n in range(0, 10):
        N = 2 ** n
        T, _ = forced_table(N)
        lv[N] = {"equals_laver": T == laver(n), "LD": is_ld_np(T)}
    res["powers_of_two"] = lv
    # complete SAT enumeration of anchored models of the instance (with wrap-around), N = 2..12
    sat = {}
    lhs, rhs = parse("x(yz)"), parse("(xy)(xz)")
    for N in range(2, 13):
        complete, tabs = solve(build(N, lhs, rhs, False), enumerate_limit=50)
        sat[N] = {"models": len(tabs), "complete": complete,
                  "equal_forced": [T == forced_table(N)[0] for T in tabs], "LD": [is_ld_np(T) for T in tabs]}
    res["sat_enumeration"] = sat
    return res


if __name__ == "__main__":
    part = sys.argv[1]
    t0 = time.time()
    res = globals()["part_" + part]()
    res["_seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(OUT, f"c17_{part}.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=str)
    print(json.dumps(res, indent=1, default=str)[:5000])
