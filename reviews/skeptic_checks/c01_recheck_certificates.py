"""Skeptic re-check of CLM-C01-07 (computer-assisted proofs for 1632 relations).

The lab's KB completion (systems/rewriting.knuth_bendix, same parameters as EXP-C01-07) is used ONLY
as an untrusted certificate generator.  Everything below is re-implemented independently:

 (a) termination: every rule is length-preserving and strictly decreasing in the lex order of the
     chosen alphabet order (= shortlex on equal lengths);
 (b) local confluence: own enumeration of ALL superpositions (overlaps + inclusions, both orders)
     and joinability by a RIGHTMOST-redex normal-form strategy (the lab uses leftmost);
 (c) u and v have equal normal forms;
 (d) SOUNDNESS (every rule is a consequence of u = v; the lab does not re-check this): if R' is
     convergent and u <->*_R' v, then the R'-classes are unions of (u=v)-classes, so on each slice
     Sigma^n we have #R'-irreducible words <= #(u=v)-classes with equality iff the partitions coincide.
     Equality of the two counts for every n <= max rule length therefore proves l ~ r for each rule.
     (u=v)-class counts come from the C union-find counter (classcount.c), irreducible counts from (e).
 (e) counting: own automaton built by brute-force suffix matching (no failure links); the irreducible
     count sequence a_n satisfies a recurrence of order <= s (s = reachable live states), the formula
     one of order <= k, so equality for n = 0..s+k suffices; we compare n = 0..s+k+2.
 (f) on a sample, the generating function of R'-irreducible words is recomputed as an exact rational
     function by the Goulden-Jackson cluster method (sympy), a method that uses no automaton and no
     recurrence-order argument, and compared with c/(x^k + (1-qx)c) symbolically.

Usage: python c01_recheck_certificates.py [--sample-cluster N]
"""
import itertools
import json
import os
import sys
import time

sys.path.insert(0, "/home/user/ai_lab")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from c01_border_search import borders, formula, run_c  # noqa: E402
from systems.rewriting import knuth_bendix  # noqa: E402  (untrusted certificate generator)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

CASES = [("ab", 2, False), ("ab", 3, False), ("ab", 4, False), ("ab", 5, False), ("ab", 6, True),
         ("abc", 2, False), ("abc", 3, False), ("abc", 4, True)]


def words(alphabet, k):
    return ["".join(t) for t in itertools.product(alphabet, repeat=k)]


def certificate(u, v, alphabet):
    """Replicates the search of EXP-C01-07 try_prove (first complete order), returning the FULL rule set."""
    k = len(u)
    for perm in itertools.permutations(alphabet):
        order = "".join(perm)
        for direction in ("ltr", "rtl"):
            uu, vv = (u, v) if direction == "ltr" else (u[::-1], v[::-1])
            rules, complete = knuth_bendix([(uu, vv)], order, max_rules=120, max_steps=6000, max_word=4 * k)
            if complete:
                return order, direction, uu, vv, rules
    return None


# ------------------------------------------------------------------ independent rewriting
def nf_rightmost(w, rules, limit=10 ** 6):
    for _ in range(limit):
        best = None
        for l, r in rules:
            i = w.rfind(l)
            if i >= 0 and (best is None or i > best[0]):
                best = (i, l, r)
        if best is None:
            return w
        i, l, r = best
        w = w[:i] + r + w[i + len(l):]
    raise RuntimeError("no termination")


def superpositions(r1, r2, same):
    (l1, s1), (l2, s2) = r1, r2
    out = []
    for d in range(-(len(l2) - 1), len(l1)):
        if same and d == 0:
            continue
        lo, hi = min(0, d), max(len(l1), d + len(l2))
        ok = all(l1[p] == l2[p - d] for p in range(max(0, d), min(len(l1), d + len(l2))))
        if not ok:
            continue
        W = [None] * (hi - lo)
        for p in range(len(l1)):
            W[p - lo] = l1[p]
        for p in range(len(l2)):
            W[p + d - lo] = l2[p]
        W = "".join(W)
        a = W[:0 - lo] + s1 + W[0 - lo + len(l1):]
        b = W[:d - lo] + s2 + W[d - lo + len(l2):]
        out.append((a, b))
    return out


def check_convergent(rules, order, uu, vv):
    rank = {c: i for i, c in enumerate(order)}
    for l, r in rules:
        if len(l) != len(r):
            return "not length preserving"
        if not [rank[c] for c in l] > [rank[c] for c in r]:
            return "not decreasing"
    for i, r1 in enumerate(rules):
        for j, r2 in enumerate(rules):
            for a, b in superpositions(r1, r2, i == j):
                if nf_rightmost(a, rules) != nf_rightmost(b, rules):
                    return f"critical pair not joinable {a} {b}"
    if nf_rightmost(uu, rules) != nf_rightmost(vv, rules):
        return "u, v not joinable"
    return None


# ------------------------------------------------------------------ independent automaton
def automaton(lhss, alphabet):
    prefixes = {l[:i] for l in lhss for i in range(len(l))}
    states, idx, trans = [""], {"": 0}, []
    q = 0
    while q < len(states):
        s = states[q]
        row = []
        for a in alphabet:
            t = s + a
            if any(t.endswith(l) for l in lhss):
                row.append(None)
                continue
            j = next(j for j in range(len(t) + 1) if t[j:] in prefixes)   # longest suffix in prefix set
            nxt = t[j:]
            if nxt not in idx:
                idx[nxt] = len(states)
                states.append(nxt)
            row.append(idx[nxt])
        trans.append(row)
        q += 1
    return trans


def counts_from_automaton(trans, nmax):
    vec = [0] * len(trans)
    vec[0] = 1
    out = [1]
    for _ in range(nmax):
        nxt = [0] * len(trans)
        for s, c in enumerate(vec):
            if c:
                for t in trans[s]:
                    if t is not None:
                        nxt[t] += c
        vec = nxt
        out.append(sum(vec))
    return out


# ------------------------------------------------------------------ Goulden-Jackson cluster method
def cluster_total(lhss):
    """Total Goulden-Jackson cluster weight C(x) of a reduced pattern set (exact, sympy).
    Words avoiding the set have generating function 1/(1 - q x - C(x))."""
    import sympy as sp
    x = sp.Symbol("x")
    W = sorted(set(lhss))
    for a in W:
        for b in W:
            if a != b and a in b:
                return None, x
    n = len(W)
    A = sp.zeros(n, n)
    rhs = sp.zeros(n, 1)
    for i, w in enumerate(W):
        A[i, i] += 1
        rhs[i] = -x ** len(w)
        for j, w2 in enumerate(W):
            for o in range(1, min(len(w), len(w2))):          # suffix of w2 (length o) = prefix of w
                if w2[-o:] == w[:o]:
                    A[i, j] += x ** (len(w) - o)
    sol = A.LUsolve(rhs)
    return sp.cancel(sum(sol)), x


def main():
    sample_cluster = -1          # -1 = all certificates
    if len(sys.argv) > 2 and sys.argv[1] == "--sample-cluster":
        sample_cluster = int(sys.argv[2])
    t0 = time.time()
    rows, problems = [], []
    todo = []
    for alphabet, k, hard_only in CASES:
        for u, v in itertools.combinations(words(alphabet, k), 2):
            bu, bv = borders(u), borders(v)
            hard = not (bu <= bv or bv <= bu)
            if hard_only and not hard:
                continue
            todo.append((alphabet, u, v, hard))
    n_cert = 0
    soundness_needed = {}   # (q, nmax) -> list of (u, v) digit pairs for the C counter
    for alphabet, u, v, hard in todo:
        cert = certificate(u, v, alphabet)
        if cert is None:
            rows.append({"alphabet": alphabet, "u": u, "v": v, "hard": hard, "status": "open"})
            continue
        n_cert += 1
        order, direction, uu, vv, rules = cert
        q, k = len(alphabet), len(u)
        why = check_convergent(rules, order, uu, vv)
        lhss = [l for l, _ in rules]
        trans = automaton(lhss, alphabet)
        s = len(trans)
        maxlen = max(len(l) for l in lhss)
        N = max(s + k + 2, maxlen)
        a = counts_from_automaton(trans, N)
        pred = [1] + formula(u, v, q, N)
        row = {"alphabet": alphabet, "u": u, "v": v, "hard": hard, "order": order, "direction": direction,
               "n_rules": len(rules), "max_rule_len": maxlen, "states": s, "convergence": why or "ok",
               "formula_match_0_to_s+k+2": a == pred, "status": "certificate", "irreducible_counts": a}
        rows.append(row)
        if why or a != pred:
            problems.append(row)
        tr = str.maketrans(alphabet, "0123456789"[:q])
        soundness_needed.setdefault(q, []).append((u.translate(tr), v.translate(tr), maxlen, len(rows) - 1))
    # (d) soundness via brute-force class counts up to the maximal rule length (C union-find)
    for q, items in soundness_needed.items():
        by_n = {}
        for du, dv, maxlen, ri in items:
            by_n.setdefault(maxlen, []).append((du, dv, ri))
        for nmax, its in sorted(by_n.items()):
            res = run_c([(a, b) for a, b, _ in its], q, nmax)
            for du, dv, ri in its:
                brute = [1] + res[(du, dv)]
                row = rows[ri]
                ok = brute == row["irreducible_counts"][:nmax + 1]
                row["soundness_counts_equal_up_to_max_rule_len"] = ok
                if not ok:
                    problems.append(row)
    # (f) cluster method for EVERY certificate: the formula c/(x^k + (1-qx)c) is equivalent to
    #     C(x) * c(x) + x^k == 0 for the total cluster weight C of the left-hand sides.
    import sympy as sp
    cluster_ok = cluster_bad = cluster_skip = 0
    for r in rows:
        if r["status"] != "certificate":
            continue
        if sample_cluster >= 0 and cluster_ok + cluster_bad + cluster_skip >= sample_cluster:
            break
        rules = certificate(r["u"], r["v"], r["alphabet"])[4]
        C, x = cluster_total([l for l, _ in rules])
        if C is None:
            cluster_skip += 1
            continue
        k = len(r["u"])
        common = borders(r["u"]) & borders(r["v"])
        c = 1 + sum(x ** (k - len(b)) for b in common)
        ok = sp.expand(sp.cancel(C * c + x ** k)) == 0
        r["cluster_method_identity"] = bool(ok)
        if ok:
            cluster_ok += 1
        else:
            cluster_bad += 1
            problems.append({"cluster_mismatch": [r["u"], r["v"]], "C": str(C)})
    summary = {
        "relations": len(rows),
        "with_certificate": n_cert,
        "open": sum(r["status"] == "open" for r in rows),
        "convergence_ok": sum(r.get("convergence") == "ok" for r in rows),
        "formula_match": sum(bool(r.get("formula_match_0_to_s+k+2")) for r in rows),
        "soundness_ok": sum(bool(r.get("soundness_counts_equal_up_to_max_rule_len")) for r in rows),
        "max_rule_len_hist": {L: sum(r.get("max_rule_len") == L for r in rows)
                              for L in sorted({r.get("max_rule_len") for r in rows if r.get("max_rule_len")})},
        "max_states": max(r.get("states", 0) for r in rows),
        "cluster_identity_ok": cluster_ok, "cluster_identity_bad": cluster_bad, "cluster_skipped": cluster_skip,
        "problems": len(problems),
        "seconds": round(time.time() - t0, 1),
    }
    for r in rows:
        r.pop("irreducible_counts", None)
    json.dump({"summary": summary, "problems": problems[:50], "rows": rows},
              open(os.path.join(OUT, "c01_recheck_certificates.json"), "w"), indent=0)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
