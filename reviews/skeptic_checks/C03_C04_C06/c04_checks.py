"""Skeptic checks for cycle C04 (one-rule systems: derivation lengths, random descent, games).
Own code only (nothing from systems/ or lab/); stored lab results are read only to compare.

Usage: python3 c04_checks.py <part> ...   parts: census, ext, complexity, aabba, rd, potential, games, octal,
                                           log2, hard
Outputs: out/c04_<part>.json
"""
import itertools
import json
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
sys.setrecursionlimit(100000)


def words(alpha, n):
    return ("".join(t) for t in itertools.product(alpha, repeat=n))


def succ(w, l, r):
    out = []
    i = w.find(l)
    while i >= 0:
        out.append(w[:i] + r + w[i + len(l):])
        i = w.find(l, i + 1)
    return out


def rules_census(maxl=3, maxr=3, alpha="ab"):
    L = [w for n in range(1, maxl + 1) for w in words(alpha, n)]
    R = [""] + [w for n in range(1, maxr + 1) for w in words(alpha, n)]
    return [(l, r) for l in L for r in R if l != r]


def unbordered(l):
    return all(l[:i] != l[-i:] for i in range(1, len(l)))


# ------------------------------------------------------------ termination certificates (own)
def matmul(A, B):
    return [[sum(A[i][t] * B[t][j] for t in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def wordmat(w, M):
    d = len(next(iter(M.values())))
    P = [[int(i == j) for j in range(d)] for i in range(d)]
    for ch in w:
        P = matmul(P, M[ch])
    return P


def matrix_ok(l, r, M):
    d = len(next(iter(M.values())))
    if any(X[0][0] < 1 or X[d - 1][d - 1] < 1 for X in M.values()):
        return False
    A, B = wordmat(l, M), wordmat(r, M)
    return all(A[i][j] >= B[i][j] for i in range(d) for j in range(d)) and A[0][d - 1] > B[0][d - 1]


def find_matrix(l, r, alpha="ab", d=2, ent=range(0, 4), upper=True, limit=None):
    """Own brute-force search for a d x d matrix interpretation (numpy vectorised, exact re-check)."""
    import numpy as np
    pos = [(i, j) for i in range(d) for j in range(d) if (j >= i or not upper)]
    cands = []
    for vals in itertools.product(ent, repeat=len(pos)):
        M = np.zeros((d, d), dtype=np.int64)
        for (i, j), v in zip(pos, vals):
            M[i, j] = v
        if M[0, 0] >= 1 and M[d - 1, d - 1] >= 1:
            cands.append(M)
    C = np.array(cands)
    if limit:
        C = C[:limit]

    def prodw(w, mats):  # mats: dict letter -> (n,d,d) or (d,d)
        P = None
        for ch in w:
            P = mats[ch] if P is None else P @ mats[ch]
        return P

    if len(alpha) != 2:
        raise ValueError
    a, b = alpha
    n = len(C)
    for ia in range(n):
        Ma = C[ia]
        mats = {a: np.broadcast_to(Ma, C.shape), b: C}
        Lm = prodw(l, mats) if l else np.broadcast_to(np.eye(d, dtype=np.int64), C.shape)
        Rm = prodw(r, mats) if r else np.broadcast_to(np.eye(d, dtype=np.int64), C.shape)
        ok = np.all(Lm >= Rm, axis=(1, 2)) & (Lm[:, 0, d - 1] > Rm[:, 0, d - 1])
        if ok.any():
            ib = int(np.argmax(ok))
            M = {a: C[ia].tolist(), b: C[ib].tolist()}
            if matrix_ok(l, r, M):
                return M
    return None


def occ(w, f):
    return sum(1 for i in range(len(w) - len(f) + 1) if w.startswith(f, i))


def factor_drop_cert(l, r, alpha="ab", maxf=3):
    """A factor f whose occurrence count drops in every context (contexts of length <= |f|-1 suffice)."""
    for n in range(1, maxf + 1):
        for f in words(alpha, n):
            ctx = [w for k in range(n) for w in words(alpha, k)]
            if all(occ(x + l + y, f) > occ(x + r + y, f) for x in ctx for y in ctx):
                return f
    return None


def has_selfembedding(l, r, seeds, depth=12, maxlen=40, maxstates=20000):
    for s in seeds:
        seen = {s}
        frontier = [s]
        for _ in range(depth):
            nxt = []
            for w in frontier:
                for v in succ(w, l, r):
                    if s in v:
                        return s
                    if v not in seen and len(v) <= maxlen and len(seen) < maxstates:
                        seen.add(v)
                        nxt.append(v)
            frontier = nxt
            if not frontier:
                break
    return None


def part_census():
    rules = rules_census()
    out = {"rules": len(rules)}
    kinds = {}
    nonterm, unknown = [], []
    for l, r in rules:
        if l in r:
            kind = "l factor of r (self-embedding l -> r)"
            nonterm.append((l, r))
        elif len(r) < len(l):
            kind = "length decreasing"
        elif len(r) == len(l):
            kind = "length preserving (lex monotone)"
        else:
            M = find_matrix(l, r, d=2, ent=range(0, 4))
            if M is not None:
                kind = "2x2 matrix interpretation"
            else:
                f = factor_drop_cert(l, r)
                kind = f"factor count ({f})" if f else "UNKNOWN"
                if not f:
                    unknown.append((l, r))
        kinds[kind] = kinds.get(kind, 0) + 1
    # evidence for the lexicographic argument: every step of a length-preserving rule moves the word in the
    # same lexicographic direction (random contexts)
    cyc = 0
    for l, r in rules:
        if len(l) == len(r):
            rng = random.Random(0)
            sign = None
            for _ in range(200):
                w = "".join(rng.choice("ab") for _ in range(rng.randint(0, 6))) + l + "".join(rng.choice("ab") for _ in range(rng.randint(0, 6)))
                for v in succ(w, l, r):
                    sg = (v > w) - (v < w)
                    if sign is None:
                        sign = sg
                    if sg != sign or sg == 0:
                        cyc += 1
    out.update(certificate_kinds=kinds, nonterminating=len(nonterm), unknown=unknown,
               lex_direction_inconsistencies=cyc,
               nonterminating_all_l_factor_of_r=all(l in r for l, r in nonterm))
    return out


# ------------------------------------------------------------ extended census |r| <= 5
def own_loop(l, r, seeds, max_steps=3000, max_len=20000):
    """Deterministic strategies from seeds; return (seed, strategy) if seed reappears as a factor."""
    for s in seeds:
        for strat in ("leftmost", "rightmost"):
            w = s
            for _ in range(max_steps):
                i = w.find(l) if strat == "leftmost" else w.rfind(l)
                if i < 0:
                    break
                w = w[:i] + r + w[i + len(l):]
                if s in w:
                    return s, strat
                if len(w) > max_len:
                    break
    return None


def linear_ok(l, r, interp, direction):
    """[w](x) = composition; interp letter -> (c, d) with c >= 1; check [l](x) > [r](x) for all x >= 0."""
    def comp(w):
        c, d = 1, 0
        seq = reversed(w) if direction == "right-to-left" else iter(w)
        for ch in seq:
            ca, da = interp[ch]
            c, d = ca * c, ca * d + da
        return c, d
    if any(c < 1 or d < 0 for c, d in interp.values()):
        return False
    cl, dl = comp(l)
    cr, dr = comp(r)
    return cl >= cr and dl > dr


def part_ext():
    """Re-check every certificate of EXP-C04-02 with own code and hunt for loops in rules marked TERMINATING."""
    e2 = json.load(open(ROOT / "results/EXP-C04-02.json"))["results"]
    rows = e2["rows"]
    stats = {}
    bad = []
    nonfactor_nt = []
    seeds = [w for n in range(1, 9) for w in words("ab", n)]
    loops_in_terminating = []
    for row in rows:
        l, r = row["rule"]
        st, proof = row["status"], row.get("proof")
        key = f"{st} / {proof}"
        stats[key] = stats.get(key, 0) + 1
        c = row.get("certificate")
        good = None
        if st == "NON-TERMINATING":
            path = c
            good = len(path) >= 2 and all(path[i + 1] in succ(path[i], l, r) for i in range(len(path) - 1)) \
                and path[0] in path[-1]
            if l not in r:
                nonfactor_nt.append(f"{l}->{r}")
        elif proof and proof.startswith("linear interpretation"):
            interp = {k: tuple(v) for k, v in c["interpretation"].items()}
            good = linear_ok(l, r, interp, c["direction"])
        elif proof and proof.startswith("weighted factor"):
            wts = c["weights"]
            mf = max(len(f) for f in wts)
            ctx = [w for k in range(mf) for w in words("ab", k)]
            good = all(sum(wt * (occ(x + l + y, f) - occ(x + r + y, f)) for f, wt in wts.items()) >= 1
                       for x in ctx for y in ctx)
        elif proof == "factor count decreases":
            f = c["factor"]
            ctx = [w for k in range(len(f)) for w in words("ab", k)]
            good = all(occ(x + l + y, f) > occ(x + r + y, f) for x in ctx for y in ctx)
        elif proof in ("length decreases",):
            good = len(r) < len(l)
        elif proof and proof.startswith("length-preserving"):
            good = len(r) == len(l)
        if good is False:
            bad.append([l, r, proof])
        # own loop hunt on rules certified terminating and length-increasing (would expose a wrong certificate)
        if st == "TERMINATING" and len(r) > len(l):
            sd = [w for w in seeds if l in w][:150]
            hit = own_loop(l, r, sd, max_steps=600, max_len=4000)
            if hit:
                loops_in_terminating.append([l, r, hit])
    und = [f"{row['rule'][0]}->{row['rule'][1]}" for row in rows if row["status"] == "UNKNOWN"]
    hunted = sum(1 for row in rows if row["status"] == "TERMINATING" and len(row["rule"][1]) > len(row["rule"][0]))
    return {"rules": len(rows), "status_proof_counts": stats, "certificates_failing_own_check": bad,
            "nonterminating_with_l_not_factor_of_r": sorted(nonfactor_nt), "count_nonfactor_nt": len(nonfactor_nt),
            "loops_found_in_rules_certified_terminating": loops_in_terminating, "rules_hunted": hunted,
            "undecided": und}


# ------------------------------------------------------------ derivational complexity
def longest_from(starts, l, r, cap=3_000_000):
    """Longest derivation length from each start word (memoised iterative DFS); None if cap exceeded."""
    memo = {}
    for s in starts:
        if s in memo:
            continue
        stack = [(s, iter(succ(s, l, r)), 0)]
        onpath = {s}
        while stack:
            w, it, best = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                memo[w] = best
                onpath.discard(w)
                stack.pop()
                if stack:
                    pw, pit, pbest = stack[-1]
                    stack[-1] = (pw, pit, max(pbest, best + 1))
                continue
            if nxt in memo:
                stack[-1] = (w, it, max(best, memo[nxt] + 1))
                continue
            if nxt in onpath:
                raise RuntimeError("cycle")
            onpath.add(nxt)
            stack.append((nxt, iter(succ(nxt, l, r)), 0))
            if len(memo) > cap:
                return None
    return memo


def rd_length(w, l, r, limit=10 ** 7):
    """Length of the leftmost derivation (equals every derivation length for random-descent rules)."""
    n = 0
    i = w.find(l)
    while i >= 0:
        w = w[:i] + r + w[i + len(l):]
        n += 1
        if n > limit:
            raise RuntimeError("limit")
        i = w.find(l, max(0, i - len(l) + 1))
    return n


def canonical(l, r):
    sw = str.maketrans("ab", "ba")
    return min([(l, r), (l[::-1], r[::-1]), (l.translate(sw), r.translate(sw)), (l[::-1].translate(sw), r[::-1].translate(sw))])


def eval_form(form, n):
    if form == "2^(n-1) - 1":
        return 2 ** (n - 1) - 1
    # 'floor((a n^2 + b n + c)/d)'
    inner = form[len("floor(("):]
    num, d = inner.rsplit(")/", 1)
    d = int(d.rstrip(")"))
    parts = num.replace(" ", "").replace("n^2", "*N2").replace("n", "*N1")
    a = b = c = 0
    toks = parts.split("+")
    for t in toks:
        if t.endswith("*N2"):
            a = int(t[:-3])
        elif t.endswith("*N1"):
            b = int(t[:-3])
        else:
            c = int(t)
    return (a * n * n + b * n + c) // d


def part_complexity(nmax_default=12):
    e3 = json.load(open(ROOT / "results/EXP-C04-03.json"))["results"]
    forms = {k: v["D_max_closed_form_n_ge_2"] for k, v in e3["symmetry_classes"].items()}
    stored = {k: v["D_max"] for k, v in e3["per_rule"].items()}
    terminating = [(l, r) for l, r in rules_census() if l not in r]
    reps = sorted({canonical(l, r) for l, r in terminating})
    res = {}
    t0 = time.time()
    for l, r in reps:
        key = f"{l}->{r}"
        doubling = key in ("ab->baa",)
        nmax = 18 if len(r) == len(l) else (16 if len(r) < len(l) else nmax_default)
        if doubling:
            nmax = 15
        D = []
        for n in range(0, nmax + 1):
            ws = list(words("ab", n))
            if doubling:  # lhs unbordered -> random descent (Lean-proved); one derivation per word
                D.append(max(rd_length(w, l, r) for w in ws))
            else:
                memo = longest_from(ws, l, r)
                if memo is None:
                    break
                D.append(max(memo[w] for w in ws))
        form = forms.get(key)
        mism = [n for n in range(2, len(D)) if form and eval_form(form, n) != D[n]]
        st = stored.get(key)
        agree_stored = st[:len(D)] == D[:len(st)] if st else None
        res[key] = {"D": D, "closed_form": form, "form_mismatches_n_ge_2": mism, "agrees_with_stored": agree_stored}
    # doubling: brute-force graph for n <= 9 (no random-descent shortcut)
    l, r = "ab", "bba"
    dbl = []
    for n in range(0, 10):
        ws = list(words("ab", n))
        memo = longest_from(ws, l, r, cap=5_000_000)
        dbl.append(max(memo[w] for w in ws))
    growth = {"quadratic": [], "exponential": [], "aab->ba": []}
    for k, v in res.items():
        f = v["closed_form"] or ""
        if "n^2" in f and not f.startswith("floor((0 n^2"):
            growth["quadratic"].append(k)
        if f.startswith("2^"):
            growth["exponential"].append(k)
    return {"classes": len(reps), "seconds": round(time.time() - t0, 1),
            "classes_with_form_mismatch": {k: v["form_mismatches_n_ge_2"] for k, v in res.items() if v["form_mismatches_n_ge_2"]},
            "classes_disagreeing_with_stored_D": [k for k, v in res.items() if v["agrees_with_stored"] is False],
            "ab->bba_bruteforce_graph_n_le_9": dbl, "ab->bba_formula_ok": dbl == [max(0, 2 ** (n - 1) - 1) for n in range(10)],
            "quadratic_classes": growth["quadratic"], "detail": res}


# ------------------------------------------------------------ aab -> ba
def kappa(n):
    k = 0
    while 2 ** k + k < n:
        k += 1
    return k


def part_aabba(nmax_graph=16, nmax_rd=21):
    l, r = "aab", "ba"
    out = {}
    # (1) full derivation graphs (no random-descent shortcut)
    Dg = []
    for n in range(0, nmax_graph + 1):
        ws = list(words("ab", n))
        memo = longest_from(ws, l, r)
        Dg.append(max(memo[w] for w in ws))
    out["graph_D"] = Dg
    out["graph_matches_formula"] = all(Dg[n] == max(0, n - 1 - kappa(n)) for n in range(1, len(Dg)))
    # (2) per-word: leftmost derivation length vs configuration formula, all words up to nmax_rd
    mism = 0
    Drd = []
    for n in range(0, nmax_rd + 1):
        best = 0
        for w in words("ab", n):
            d = rd_length(w, l, r)
            # configuration formula: x_k a's before the (k+1)-th b; level m inert
            runs = [len(x) for x in w.split("b")]
            m = len(runs) - 1
            T = n - m
            V = sum(x << k for k, x in enumerate(runs))
            pred = T - bin(V % (1 << m)).count("1") - (V >> m)
            if pred != d:
                mism += 1
            best = max(best, d)
        Drd.append(best)
    out["rd_D"] = Drd
    out["per_word_formula_mismatches"] = mism
    out["rd_matches_formula"] = all(Drd[n] == max(0, n - 1 - kappa(n)) for n in range(1, len(Drd)))
    # (3) arithmetic part (v): min_m (m + ceil((n-m)/2^m)) == 1 + kappa(n), n <= 200000
    bad = []
    for n in range(1, 200001):
        f = min(m + (-(-(n - m) // (1 << m)) if n - m > 0 else 0) for m in range(0, min(n, 40) + 1))
        if f != 1 + kappa_fast(n):
            bad.append(n)
            if len(bad) > 5:
                break
    out["arith_identity_n_le_200000_failures"] = bad
    out["stalls_n_le_80"] = [n for n in range(2, 81) if (n - 1 - kappa(n)) == (n - 2 - kappa(n - 1))]
    return out


_K = [2 ** k + k for k in range(64)]


def kappa_fast(n):
    for k, v in enumerate(_K):
        if v >= n:
            return k


# ------------------------------------------------------------ random descent census
def nf_profile(w, l, r, memo):
    """Set of (normal form, length) over all maximal derivations from w."""
    if w in memo:
        return memo[w]
    ss = succ(w, l, r)
    if not ss:
        res = frozenset([(w, 0)])
    else:
        acc = set()
        for v in set(ss):
            for nf, k in nf_profile(v, l, r, memo):
                acc.add((nf, k + 1))
        res = frozenset(acc)
    memo[w] = res
    return res


DOUBLING = {("ab", "bba"), ("ab", "baa"), ("ba", "abb"), ("ba", "aab")}


def part_rd(nmax=10):
    terminating = [(l, r) for l, r in rules_census() if l not in r]
    res = {"unbordered": {"total": 0, "RD": 0}, "bordered": {"total": 0, "RD": 0, "confluent": 0, "length_uniform": 0}}
    bordered_rd = []
    lu_not_conf = []
    peak_disagree = []
    for l, r in terminating:
        memo = {}
        rd = conf = lu = True
        for n in range(0, (8 if (l, r) in DOUBLING else nmax) + 1):
            for w in words("ab", n):
                prof = nf_profile(w, l, r, memo)
                nfs = {a for a, _ in prof}
                lens = {b for _, b in prof}
                if len(nfs) > 1:
                    conf = False
                if len(lens) > 1:
                    lu = False
                if len(prof) > 1:
                    rd = False
        # critical-peak criterion: every critical peak joinable with equal-length derivations
        ok_peaks = True
        for i in range(1, len(l)):
            if l[:i] == l[-i:]:
                p_, s_ = l[:len(l) - i], l[i:]
                left, right = r + s_, p_ + r
                found = False
                A, B = {left}, {right}
                for _ in range(40):
                    if A & B:
                        found = True
                        break
                    A = {v for u in A for v in succ(u, l, r)}
                    B = {v for u in B for v in succ(u, l, r)}
                    if not A or not B:
                        break
                ok_peaks &= found
        if ok_peaks != rd:
            peak_disagree.append(f"{l}->{r}")
        cls = "unbordered" if unbordered(l) else "bordered"
        res[cls]["total"] += 1
        res[cls]["RD"] += rd
        if cls == "bordered":
            res[cls]["confluent"] += conf
            res[cls]["length_uniform"] += lu
            if rd:
                bordered_rd.append(f"{l}->{r}")
            if lu and not conf:
                lu_not_conf.append(f"{l}->{r}")
    # the |l| = 4, 5 bordered length-preserving family (EXP-C04-06 claim: 770 rules, 94 confluent, 126 LU not confluent)
    fam = [(l, r) for n in (4, 5) for l in words("ab", n) for r in words("ab", n) if l != r and not unbordered(l)]
    conf_c = lu_nc = 0
    for l, r in fam:
        memo = {}
        conf = lu = True
        for n in range(len(l), 11):
            for w in words("ab", n):
                prof = nf_profile(w, l, r, memo)
                if len({a for a, _ in prof}) > 1:
                    conf = False
                if len({b for _, b in prof}) > 1:
                    lu = False
        conf_c += conf
        lu_nc += lu and not conf
    return {"census_162": res, "bordered_RD_rules": bordered_rd, "length_uniform_not_confluent_in_162": lu_not_conf,
            "critical_peak_criterion_disagreements": peak_disagree,
            "family_l4_5_bordered_length_preserving": {"rules": len(fam), "confluent_on_words_le_10": conf_c,
                                                       "length_uniform_not_confluent": lu_nc},
            "aaaba->baabb_on_aaabaaaba": sorted(set(succ("aaabaaaba", "aaaba", "baabb")))}


# ------------------------------------------------------------ constant-step potential (own)
def potential_spec(l, r):
    if len(l) != len(r):
        return ("length", None, len(r) - len(l))
    alph = sorted(set(l) | set(r))
    for c in alph:
        P = [j for j, ch in enumerate(l) if ch == c]
        Q = [j for j, ch in enumerate(r) if ch == c]
        if P == Q:
            continue
        for K in range(0, len(l) + 1):
            pk = lambda S: sum((j ** K if not (j == 0 and K == 0) else 1) for j in S)
            if pk(P) != pk(Q):
                return ("power", (c, K), pk(Q) - pk(P))
    raise RuntimeError("no letter found")


def Phi(w, spec):
    kind, ck, _ = spec
    if kind == "length":
        return len(w)
    c, K = ck
    return sum((i ** K if not (i == 0 and K == 0) else 1) for i, ch in enumerate(w) if ch == c)


def part_potential():
    rules = [(l, r, "ab") for l, r in rules_census(5, 5, "ab")] + [(l, r, "abc") for l, r in rules_census(3, 3, "abc")]
    rng = random.Random(42)
    viol, steps, maxK = 0, 0, 0
    for l, r, alph in rules:
        spec = potential_spec(l, r)
        if spec[0] == "power":
            maxK = max(maxK, spec[1][1])
        if spec[2] == 0:
            viol += 1
        for _ in range(40):
            w = "".join(rng.choice(alph) for _ in range(rng.randint(0, 8))) + l + "".join(rng.choice(alph) for _ in range(rng.randint(0, 8)))
            for v in succ(w, l, r):
                steps += 1
                if Phi(v, spec) - Phi(w, spec) != spec[2]:
                    viol += 1
    # exhaustive mini-check: all derivations u ->* v between words of length <= 7 have equal length (length-preserving)
    lp_viol = 0
    for l, r in rules_census(3, 3, "ab"):
        if len(l) != len(r):
            continue
        for n in range(len(l), 8):
            for u in words("ab", n):
                dist = {u: {0}}
                frontier = {u}
                for k in range(1, 40):
                    nxt = set()
                    for w in frontier:
                        for v in succ(w, l, r):
                            dist.setdefault(v, set()).add(k)
                            nxt.add(v)
                    frontier = nxt
                    if not frontier:
                        break
                if any(len(s) > 1 for s in dist.values()):
                    lp_viol += 1
    return {"rules": len(rules), "steps_checked": steps, "violations": viol, "max_K": maxK,
            "length_preserving_multi_length_paths": lp_viol}


# ------------------------------------------------------------ games
def grundy_graph(starts, l, r):
    memo = {}

    def g(w):
        if w in memo:
            return memo[w]
        opts = {g(v) for v in set(succ(w, l, r))}
        m = 0
        while m in opts:
            m += 1
        memo[w] = m
        return m
    return {w: g(w) for w in starts}, memo


def octal(code, nmax):
    ds = [int(ch) for ch in code.split(".")[1]]
    G = [0] * (nmax + 1)
    for n in range(1, nmax + 1):
        opts = set()
        for k, d in enumerate(ds, 1):
            if n < k:
                continue
            rem = n - k
            if d & 1 and rem == 0:
                opts.add(0)
            if d & 2 and rem >= 1:
                opts.add(G[rem])
            if d & 4 and rem >= 2:
                for a in range(1, rem // 2 + 1):
                    opts.add(G[a] ^ G[rem - a])
        m = 0
        while m in opts:
            m += 1
        G[n] = m
    return G


def part_games():
    out = {}
    # a^14 under aa -> b, directly from the derivation graph
    vals, _ = grundy_graph(["a" * n for n in range(0, 21)], "aa", "b")
    out["aa->b_grundy_a^n_n<=20"] = [vals["a" * n] for n in range(21)]
    out["a^14_value"] = vals["a" * 14]
    out["first_n_with_value_4"] = next(n for n in range(21) if vals["a" * n] == 4)
    # word games = sum of run games = octal recursion, on all words <= 12
    pairs = {("aa", "b"): "0.07", ("aa", "bb"): "0.07", ("aa", "bbb"): "0.07", ("aa", "bab"): "0.07",
             ("aa", "ab"): "0.6", ("aa", "ba"): "0.6", ("aa", "abb"): "0.6", ("aa", "bba"): "0.6",
             ("aaa", "b"): "0.007", ("aaa", "bb"): "0.007", ("aaa", "bbb"): "0.007", ("aaa", "bab"): "0.007",
             ("aaa", "ab"): "0.06", ("aaa", "ba"): "0.06", ("aaa", "abb"): "0.06", ("aaa", "bba"): "0.06",
             ("aaa", "aba"): "0.4"}
    mism = {}
    for (l, r), code in pairs.items():
        G = octal(code, 40)
        allw = [w for n in range(0, 13) for w in words("ab", n)]
        vals, _ = grundy_graph(allw, l, r)
        bad = 0
        for w in allw:
            x = 0
            for run in w.split("b"):
                x ^= G[len(run)]
            if x != vals[w]:
                bad += 1
        mism[f"{l}->{r} = {code}"] = bad
    out["word_game_vs_octal_mismatches_words_le_12"] = mism
    # parity theorem for RD rules: Grundy = D mod 2 (words <= 10), using own RD test
    viol = rdcount = 0
    for l, r in [(l, r) for l, r in rules_census() if l not in r]:
        memo = {}
        allw = [w for n in range(0, (9 if (l, r) in DOUBLING else 11)) for w in words("ab", n)]
        is_rd = all(len(nf_profile(w, l, r, memo)) == 1 for w in allw)
        if not is_rd:
            continue
        rdcount += 1
        vals, _ = grundy_graph(allw, l, r)
        for w in allw:
            (nf, D), = nf_profile(w, l, r, memo)
            if vals[w] != D % 2:
                viol += 1
    out["RD_rules"] = rdcount
    out["parity_violations"] = viol
    return out


def part_octal(nmax=3000):
    out = {}
    for code in ("0.07", "0.4", "0.6", "0.007", "0.06"):
        G = octal(code, nmax)
        # smallest (preperiod, period) with p <= 300 holding on all n0 <= n <= nmax - p
        best = None
        for p in range(1, 301):
            # largest n where G[n+p] != G[n]
            last_bad = max((n for n in range(0, nmax - p + 1) if G[n + p] != G[n]), default=-1)
            n0 = last_bad + 1
            if n0 <= nmax - 2 * p - 10:  # periodic tail with room to spare
                if best is None or (n0, p) < best:
                    best = (n0, p)
        out[code] = {"max_value": max(G), "argmax": G.index(max(G)), "first_terms": G[:20],
                     "apparent_(preperiod,period)": best}
    # Guy-Smith window for 0.07 with n0 = 53, p = 34, t = 2: check n0 <= n < 2 n0 + p + t
    G = octal("0.07", 400)
    out["0.07_guy_smith_window_53_34"] = all(G[n + 34] == G[n] for n in range(53, 2 * 53 + 34 + 2))
    out["0.07_fails_at_52"] = G[52 + 34] != G[52]
    G4 = octal("0.4", 400)
    out["0.4_equals_0.07_shift"] = all(G4[n] == G[n - 1] for n in range(1, 400))
    out["0.4_period_34_from_54_window"] = all(G4[n + 34] == G4[n] for n in range(54, 2 * 54 + 34 + 1))
    return out


# ------------------------------------------------------------ A247983
def part_log2(nmax=1200):
    import mpmath
    out = {"mismatch": [], "checked": 0}
    for n in range(0, nmax + 1):
        mpmath.mp.prec = n + 120
        ln2 = mpmath.log(2)
        thr = mpmath.mpf(2) ** (-n)
        s = mpmath.mpf(0)
        k = 0
        while True:
            k += 1
            s += mpmath.mpf(1) / (k * mpmath.mpf(2) ** k)
            t = ln2 - s
            # guard: require a clear margin relative to precision
            if t < thr:
                break
        J = max(j for j in range(0, n + 2) if 2 ** j + j <= n + 1)
        pred = n - J
        D = (n + 2) - 1 - kappa_fast(n + 2)
        out["checked"] += 1
        if k != pred or k != D:
            out["mismatch"].append({"n": n, "A": k, "n-J": pred, "D(n+2)": D})
    # compare with the cached OEIS data
    cache = json.load(open(ROOT / "cache/oeis/76ce7aed68dff37a5c3c365b.json"))["response"]
    ent = next(e for e in cache if e.get("number") == 247983)
    data = [int(x) for x in ent["data"].split(",")]
    out["oeis_offset"] = ent["offset"]
    out["oeis_terms_match_formula"] = all(data[i] == (i + 1) - max(j for j in range(0, i + 3) if 2 ** j + j <= i + 2)
                                          for i in range(len(data)))
    return out


# ------------------------------------------------------------ hard rules aab -> ababa, aab -> babaa
def part_hard():
    out = {}
    for l, r in (("aab", "ababa"), ("aab", "babaa")):
        res = {}
        # matrix interpretations (own search): 2x2 entries 0..5, 3x3 upper-triangular entries 0..3
        M = find_matrix(l, r, d=2, ent=range(0, 6), upper=False)
        res["matrix_2x2_full_0..5"] = M
        if M is None:
            M3 = find_matrix(l, r, d=3, ent=range(0, 4), upper=True)
            res["matrix_3x3_upper_0..3"] = M3
        # loop hunt
        seeds = [w for n in range(3, 13) for w in words("ab", n) if l in w]
        hit = own_loop(l, r, seeds, max_steps=4000, max_len=40000)
        res["loop_found"] = hit
        # exhaustive: all words <= 11 reach normal forms; record maximal derivation length
        D = []
        for n in range(0, 12):
            ws = list(words("ab", n))
            memo = longest_from(ws, l, r, cap=4_000_000)
            if memo is None:
                break
            D.append(max(memo[w] for w in ws))
        res["D_max_by_length"] = D
        out[f"{l}->{r}"] = res
    return out


PARTS = {"census": part_census, "ext": part_ext, "complexity": part_complexity, "aabba": part_aabba,
         "rd": part_rd, "potential": part_potential, "games": part_games, "octal": part_octal,
         "log2": part_log2, "hard": part_hard}

if __name__ == "__main__":
    for name in sys.argv[1:]:
        t0 = time.time()
        res = PARTS[name]()
        res["_seconds"] = round(time.time() - t0, 1)
        (OUT / f"c04_{name}.json").write_text(json.dumps(res, indent=1, default=str))
        print(f"== {name} ({res['_seconds']} s)")
        print(json.dumps({k: v for k, v in res.items() if k != "detail"}, default=str)[:4000], flush=True)
