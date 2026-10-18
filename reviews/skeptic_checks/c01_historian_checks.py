"""Skeptic checks of the Historian's [DERIVED]/[COMPUTED] statements on CLM-C01-08
(reviews/historian_C01_C02.md, section 2, parts (A) and (C)).

1. Recompute the border classification of the lab's 2159 relations (EXP-C01-06/07 cases):
   open relations with c = 1, hard relations by number of common borders, first/last letters.
2. Count binary hard relations with >= 2 common borders at k = 8, 9.
3. Test the growth identities numerically (C program classsuffix.c):
     (P)  H = G_y + x^(k-|y|) G_z          (y shortest, z longest common border)
     (E)  H (1 - q x) + x^k G_z = 1        (z = longest common border, z = empty word if none)
   where G_w(x) = sum_{s in M[w]} x^(|s|-|w|), M[w] = M.[w] = classes containing a word ending in w.
   Also checks the derived consequences G_z = H/c and the conjectured formula.
"""
import itertools
import json
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from c01_border_search import borders, canonical, formula  # noqa: E402

OUT = os.path.join(HERE, "out")
LAB_CASES = [("ab", 2, False), ("ab", 3, False), ("ab", 4, False), ("ab", 5, False), ("ab", 6, True),
             ("abc", 2, False), ("abc", 3, False), ("abc", 4, True)]


def common(u, v):
    return sorted(borders(u) & borders(v), key=len)


def classification():
    lab = json.load(open("/home/user/ai_lab/results/EXP-C01-07.json"))["results"]["open_relations"]
    open_set = {(r["alphabet"], tuple(r["relation"])) for r in lab}
    stats = {"relations": 0, "hard": 0, "hard_c1": 0, "hard_c1_diff_first_or_last": 0,
             "hard_c1_same_first_and_last": 0, "hard_by_n_common": {}, "open": 0, "open_c1": 0,
             "open_c1_diff_first_or_last": 0, "open_c1_same_first_and_last": 0,
             "hard_proven": 0, "hard_proven_c1": 0, "hard_proven_one_common": [], "open_same_fl_examples": []}
    for alphabet, k, hard_only in LAB_CASES:
        for u, v in itertools.combinations(["".join(t) for t in itertools.product(alphabet, repeat=k)], 2):
            bu, bv = borders(u), borders(v)
            hard = not (bu <= bv or bv <= bu)
            if hard_only and not hard:
                continue
            stats["relations"] += 1
            cb = common(u, v)
            diff = u[0] != v[0] or u[-1] != v[-1]
            is_open = (alphabet, (u, v)) in open_set
            if is_open:
                stats["open"] += 1
                if not cb:
                    stats["open_c1"] += 1
                    stats["open_c1_diff_first_or_last" if diff else "open_c1_same_first_and_last"] += 1
                    if not diff and len(stats["open_same_fl_examples"]) < 8:
                        stats["open_same_fl_examples"].append(u + "<->" + v)
            if hard:
                stats["hard"] += 1
                stats["hard_by_n_common"][len(cb)] = stats["hard_by_n_common"].get(len(cb), 0) + 1
                if not cb:
                    stats["hard_c1"] += 1
                    stats["hard_c1_diff_first_or_last" if diff else "hard_c1_same_first_and_last"] += 1
                if not is_open:
                    stats["hard_proven"] += 1
                    if not cb:
                        stats["hard_proven_c1"] += 1
                    elif len(cb) == 1:
                        stats["hard_proven_one_common"].append(u + "<->" + v)
    return stats


def two_common_hard(k):
    ws = ["".join(t) for t in itertools.product("ab", repeat=k)]
    pairs, orbits = [], set()
    for u, v in itertools.combinations(ws, 2):
        bu, bv = borders(u), borders(v)
        if bu <= bv or bv <= bu:
            continue
        if len(bu & bv) >= 2:
            pairs.append((u, v))
            orbits.add(canonical(u.translate(str.maketrans("ab", "01")), v.translate(str.maketrans("ab", "01"))))
    return pairs, sorted(orbits)


def run_suffix_counts(jobs):
    """jobs: list of (q, nmax, u, v, [w...]) with digit-string words; returns dict -> {n: (h, [s_i])}."""
    exe = os.path.join(HERE, "classsuffix")
    inp = "".join(f"{q} {nmax} {u} {v} {len(ws)} " + " ".join(w if w else "-" for w in ws) + "\n"
                  for q, nmax, u, v, ws in jobs)
    tmp_in = os.path.join(OUT, "_suffix_in.txt")
    tmp_out = os.path.join(OUT, "_suffix_out.txt")
    open(tmp_in, "w").write(inp)
    subprocess.run([exe], stdin=open(tmp_in), stdout=open(tmp_out, "w"), check=True)
    res, cur = {}, None
    for line in open(tmp_out):
        p = line.split()
        if p[0] == "REL":
            cur = (p[1], p[2])
            res[cur] = {}
        else:
            res[cur][int(p[0])] = (int(p[1]), [int(x) for x in p[2:]])
    os.remove(tmp_in)
    os.remove(tmp_out)
    return res


def test_identities(rel_list, q, nmax):
    """rel_list: digit-string pairs. Returns per-relation results of (P), (E), G_z = H/c, formula."""
    jobs = []
    for u, v in rel_list:
        cb = common(u, v)
        y = cb[0] if cb else ""
        z = cb[-1] if cb else ""
        jobs.append((q, nmax, u, v, [y, z]))
    res = run_suffix_counts(jobs)
    out = []
    for (q_, nmax_, u, v, (y, z)) in jobs:
        data = res[(u, v)]
        k = len(u)
        h = [data[n][0] for n in range(nmax + 1)]
        gy = lambda j: data[j + len(y)][1][0] if 0 <= j and j + len(y) <= nmax else None
        gz = lambda j: data[j + len(z)][1][1] if 0 <= j and j + len(z) <= nmax else (0 if j < 0 else None)
        P_ok, P_tested = True, 0
        if y:
            for n in range(nmax + 1):
                a = gy(n)
                j = n - k + len(y)
                b = 0 if j < 0 else gz(j)
                if a is None or b is None:
                    continue
                P_tested += 1
                if h[n] != a + b:
                    P_ok = False
        E_ok, E_tested = True, 0
        for n in range(nmax + 1):
            g = gz(n - k)
            if g is None:
                continue
            E_tested += 1
            if h[n] - (q * h[n - 1] if n >= 1 else 0) + g != (1 if n == 0 else 0):
                E_ok = False
        pred = [1] + formula(u, v, q, nmax)
        out.append({"u": u, "v": v, "common_borders": common(u, v), "P_ok": P_ok if y else None,
                    "P_terms": P_tested, "E_ok": E_ok, "E_terms": E_tested, "formula_ok": h == pred})
    return out


def main():
    report = {}
    st = classification()
    report["classification"] = st
    print("classification:", json.dumps({k: v for k, v in st.items() if k not in ("open_same_fl_examples",)}))
    for k in (8, 9):
        pairs, orbits = two_common_hard(k)
        report[f"binary_k{k}_hard_two_or_more_common"] = {"unordered_pairs": len(pairs), "orbits": len(orbits),
                                                         "pairs": [u + "<->" + v for u, v in pairs]}
        print(f"binary k={k}: hard relations with >= 2 common borders: {len(pairs)} unordered pairs, "
              f"{len(orbits)} orbits (alphabet swap, reversal, u<->v)")
    tests = {}
    tr = str.maketrans("abc", "012")
    # (a) the 12 one-common-border hard relations of the lab's range
    one = [tuple(s.split("<->")) for s in st["hard_proven_one_common"]]
    tests["one_common_border_lab"] = test_identities([(u.translate(tr), v.translate(tr)) for u, v in one], 2, 18)
    # (b) two common borders, binary k = 8, 9 (all orbits)
    for k in (8, 9):
        _, orbits = two_common_hard(k)
        tests[f"two_common_k{k}"] = test_identities(orbits, 2, 19)
    # (c) random relations with >= 1 common border incl. containment, binary k<=9, ternary k<=5
    rng = random.Random(4242)
    for q, kmax, nmax, label in ((2, 9, 17, "random_binary"), (3, 5, 10, "random_ternary")):
        al = "012"[:q]
        rels = set()
        while len(rels) < 120:
            k = rng.randint(2, kmax)
            u = "".join(rng.choice(al) for _ in range(k))
            v = "".join(rng.choice(al) for _ in range(k))
            if u != v and borders(u) & borders(v):
                rels.add(canonical(u, v))
        tests[label + "_with_common_border"] = test_identities(sorted(rels), q, nmax)
        rels = set()
        while len(rels) < 60:
            k = rng.randint(2, kmax)
            u = "".join(rng.choice(al) for _ in range(k))
            v = "".join(rng.choice(al) for _ in range(k))
            if u != v and not (borders(u) & borders(v)):
                rels.add(canonical(u, v))
        tests[label + "_c1"] = test_identities(sorted(rels), q, nmax)
    report["identity_tests"] = tests
    for name, rows in tests.items():
        nP = [r for r in rows if r["P_ok"] is not None]
        print(f"{name}: {len(rows)} relations; (P) holds {sum(r['P_ok'] for r in nP)}/{len(nP)}; "
              f"(E) holds {sum(r['E_ok'] for r in rows)}/{len(rows)}; formula holds "
              f"{sum(r['formula_ok'] for r in rows)}/{len(rows)}; "
              f"#common borders {sorted({len(r['common_borders']) for r in rows})}")
        bad = [r for r in rows if r["P_ok"] is False or not r["E_ok"] or not r["formula_ok"]]
        for r in bad[:5]:
            print("   FAIL", r)
    json.dump(report, open(os.path.join(OUT, "c01_historian_checks.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
