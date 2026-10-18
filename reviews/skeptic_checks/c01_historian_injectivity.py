"""Test the injectivity premise of the Historian's (E) derivation (see grinj.c) on relations with
at least one common border: the 12 lab relations, all two-common-border binary orbits k = 8, 9,
and random binary (k <= 9) / ternary (k <= 5) relations, including border-containment ones."""
import json, os, random, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from c01_border_search import borders, canonical
from c01_historian_checks import two_common_hard

def run(rels, q, Lmax):
    inp = "".join(f"{q} {Lmax} {u} {v} {sorted(borders(u) & borders(v), key=len)[-1]}\n" for u, v in rels)
    out = subprocess.run([os.path.join(HERE, "grinj")], input=inp, capture_output=True, text=True, check=True).stdout
    res, cur = {}, None
    for line in out.splitlines():
        p = line.split()
        if p[0] == "REL":
            cur = (p[1], p[2]); res[cur] = []
        else:
            res[cur].append((int(p[0]), int(p[1]), int(p[2])))
    return res

tr = str.maketrans("ab", "01")
lab12 = [("aaaaa","ababa"),("aabaa","ababa"),("babab","bbabb"),("babab","bbbbb"),("aaaaaa","abaaba"),("aaabaa","abaaba"),
         ("aabaaa","abaaba"),("aabbaa","abaaba"),("babbab","bbaabb"),("babbab","bbabbb"),("babbab","bbbabb"),("babbab","bbbbbb")]
sets = {"lab_one_common": ([(u.translate(tr), v.translate(tr)) for u, v in lab12], 2, 17)}
sets["two_common_k8_k9"] = (two_common_hard(8)[1] + two_common_hard(9)[1], 2, 17)
rng = random.Random(77)
for q, kmax, Lmax, name in ((2, 9, 16, "random_binary"), (3, 5, 10, "random_ternary")):
    al = "012"[:q]; rels = set()
    while len(rels) < (150 if q == 2 else 100):
        k = rng.randint(2, kmax)
        u = "".join(rng.choice(al) for _ in range(k)); v = "".join(rng.choice(al) for _ in range(k))
        if u != v and borders(u) & borders(v):
            rels.add(canonical(u, v))
    sets[name] = (sorted(rels), q, Lmax)
summary = {}
for name, (rels, q, Lmax) in sets.items():
    res = run(rels, q, Lmax)
    degs = sum(len(v) for v in res.values())
    bad = [(r, d) for r, ds in res.items() for d in ds if d[2] == 0]
    nonempty = sum(1 for ds in res.values() for d in ds if d[1] > 0)
    summary[name] = {"relations": len(res), "degrees_tested": degs, "degrees_with_columns": nonempty, "non_injective": bad[:10]}
    print(f"{name}: {len(res)} relations, {degs} degrees tested ({nonempty} with >= 1 column): non-injective degrees {len(bad)}")
json.dump(summary, open(os.path.join(HERE, "out", "c01_historian_injectivity.json"), "w"), indent=1)
