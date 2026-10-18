"""Skeptic check for CLM-C01-06/07/08: exact class counts modulo one relation u = v
(union-find in C, independent of systems/rewriting.py) compared with the common-border formula
c(x) / (x^k + (1 - q x) c(x)),  c(x) = 1 + sum_{b in Borders(u) & Borders(v)} x^(k - |b|).

Usage:  python c01_border_search.py CASE_NAME
Each case enumerates relations up to the symmetries (alphabet permutation, reversal, u<->v),
optionally keeps only 'hard' pairs (neither border set contains the other) and compares the
counts for n = 1..nmax.  Results go to skeptic_checks/out/<case>.json.
"""
import itertools
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)


def borders(w):
    return {w[:i] for i in range(1, len(w)) if w[:i] == w[-i:]}


def formula(u, v, q, nmax):
    """Exact coefficients 1..nmax of c/(x^k + (1-qx)c) (integer recurrence, den[0] = 1)."""
    k = len(u)
    common = borders(u) & borders(v)
    c = [0] * k
    c[0] = 1
    for b in common:
        c[k - len(b)] += 1
    den = [0] * (k + 1)
    for i, ci in enumerate(c):
        den[i] += ci
        den[i + 1] -= q * ci
    den[k] += 1
    assert den[0] == 1
    num = c + [0] * (nmax + 1)
    out = []
    for n in range(nmax + 1):
        val = num[n] - sum(den[i] * out[n - i] for i in range(1, min(n, k) + 1))
        out.append(val)
    return out[1:]


def _relabel(s, t):
    m = {}
    for ch in s + t:
        if ch not in m:
            m[ch] = "0123456789"[len(m)]
    return "".join(m[c] for c in s), "".join(m[c] for c in t)


def canonical(u, v, alphabet=None):
    """Orbit representative under alphabet permutations, reversal and u<->v
    (first-appearance relabelling of each of the 4 ordered variants, then the minimum)."""
    return min(_relabel(a, b) for a, b in ((u, v), (v, u), (u[::-1], v[::-1]), (v[::-1], u[::-1])))


def orbit_reps(q, k, hard_only):
    alphabet = "0123456789"[:q]
    ws = ["".join(t) for t in itertools.product(alphabet, repeat=k)]
    reps = set()
    for u, v in itertools.combinations(ws, 2):
        if hard_only:
            bu, bv = borders(u), borders(v)
            if bu <= bv or bv <= bu:
                continue
        reps.add(canonical(u, v, alphabet))
    return sorted(reps)


def run_c(pairs, q, nmax, nproc=4):
    """Run the C counter on the pairs, split over nproc processes (file-based I/O: no pipe deadlock)."""
    import tempfile
    exe = os.path.join(HERE, "classcount")
    tmp = tempfile.mkdtemp(prefix="cc_", dir=os.environ.get("SKEPTIC_TMP", "/tmp"))
    chunks = [pairs[i::nproc] for i in range(nproc)]
    procs = []
    for ci, ch in enumerate(chunks):
        if not ch:
            continue
        fin, fout = os.path.join(tmp, f"in{ci}.txt"), os.path.join(tmp, f"out{ci}.txt")
        with open(fin, "w") as f:
            f.write("".join(f"{q} {nmax} {u} {v}\n" for u, v in ch))
        procs.append((subprocess.Popen([exe], stdin=open(fin), stdout=open(fout, "w")), fout))
    res = {}
    for p, fout in procs:
        p.wait()
        assert p.returncode == 0
        for line in open(fout):
            parts = line.split()
            res[(parts[0], parts[1])] = [int(x) for x in parts[2:]]
    for p, fout in procs:
        os.remove(fout)
    for ci in range(nproc):
        fin = os.path.join(tmp, f"in{ci}.txt")
        if os.path.exists(fin):
            os.remove(fin)
    os.rmdir(tmp)
    assert len(res) == len(set(pairs)), "missing output lines"
    return res


CASES = {
    # name: (q, k, nmax, hard_only, explicit pair list or None)
    "bin_k3_n24": (2, 3, 24, False, None),
    "bin_k4_n24": (2, 4, 24, False, None),
    "bin_k5_n24": (2, 5, 24, False, None),
    "bin_k6_hard_n24": (2, 6, 24, True, None),
    "bin_k6_all_n20": (2, 6, 20, False, None),
    "bin_k7_all_n20": (2, 7, 20, False, None),
    "bin_k7_hard_n23": (2, 7, 23, True, None),
    "bin_k8_hard_n21": (2, 8, 21, True, None),
    "bin_k9_hard_n19": (2, 9, 19, True, None),
    "ter_k2_n13": (3, 2, 13, False, None),
    "ter_k3_n13": (3, 3, 13, False, None),
    "ter_k4_n13": (3, 4, 13, False, None),
    "ter_k5_hard_n11": (3, 5, 11, True, None),
    "qua_k2_n10": (4, 2, 10, False, None),
    "qua_k3_n10": (4, 3, 10, False, None),
    "qua_k4_n9": (4, 4, 9, False, None),
    "qui_k3_n8": (5, 3, 8, False, None),
    # extended runs (second round)
    "bin_k2_n27": (2, 2, 27, False, None),
    "bin_k3_n27": (2, 3, 27, False, None),
    "bin_k4_n27": (2, 4, 27, False, None),
    "bin_k5_n27": (2, 5, 27, False, None),
    "bin_k6_n26": (2, 6, 26, False, None),
    "bin_k7_n25": (2, 7, 25, False, None),
    "bin_k8_n23": (2, 8, 23, False, None),
    "bin_k9_hard_n23": (2, 9, 23, True, None),
    "bin_k10_hard_n22": (2, 10, 22, True, None),
    "bin_k11_hard_n22": (2, 11, 22, True, None),
    "ter_k2_n16": (3, 2, 16, False, None),
    "ter_k3_n16": (3, 3, 16, False, None),
    "ter_k4_n16": (3, 4, 16, False, None),
    "ter_k5_n14": (3, 5, 14, False, None),
    "ter_k6_hard_n13": (3, 6, 13, True, None),
    "qua_k2_n12": (4, 2, 12, False, None),
    "qua_k3_n12": (4, 3, 12, False, None),
    "qua_k4_n11": (4, 4, 11, False, None),
    "qua_k5_hard_n10": (4, 5, 10, True, None),
    "qui_k2_n10": (5, 2, 10, False, None),
    "qui_k3_n10": (5, 3, 10, False, None),
    "qui_k4_hard_n9": (5, 4, 9, True, None),
    "sex_k3_n8": (6, 3, 8, False, None),
}


def main(name):
    q, k, nmax, hard_only, pairs = CASES[name]
    t0 = time.time()
    if pairs is None:
        pairs = orbit_reps(q, k, hard_only)
    res = run_c(pairs, q, nmax)
    fails, n_hard, n_common = [], 0, 0
    for (u, v), counts in sorted(res.items()):
        bu, bv = borders(u), borders(v)
        hard = not (bu <= bv or bv <= bu)
        n_hard += hard
        n_common += bool(bu & bv)
        pred = formula(u, v, q, nmax)
        if counts != pred:
            first = next(i for i in range(nmax) if counts[i] != pred[i]) + 1
            fails.append({"u": u, "v": v, "hard": hard, "first_bad_n": first,
                          "counts": counts, "predicted": pred})
    out = {"case": name, "q": q, "k": k, "nmax": nmax, "hard_only": hard_only,
           "relations_tested": len(res), "hard": n_hard, "with_common_border": n_common,
           "failures": fails, "n_failures": len(fails), "seconds": round(time.time() - t0, 1)}
    json.dump(out, open(os.path.join(OUT, name + ".json"), "w"), indent=1)
    print(f"{name}: tested {len(res)} relation orbits (hard {n_hard}, common border {n_common}), "
          f"n<= {nmax}: failures {len(fails)}  [{out['seconds']} s]")
    for f in fails[:5]:
        print("   FAIL", f["u"], f["v"], "first bad n =", f["first_bad_n"])


if __name__ == "__main__":
    for nm in sys.argv[1:]:
        main(nm)
