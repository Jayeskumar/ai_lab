"""Historian check (C03): compare the lab's classification of 0^p 1^q -> 1^r 0^s
(p, q, r, s <= 5) and hypothesis H-C03-4 with Theorem 1 of Zantema-Geser,
AAECC 11 (2000) 1-25, p. 2:

  terminates  iff  (1) p >= s or q >= r, or
                   (2) p < s < 2p and q < r and q does not divide r, or
                       q < r < 2q and p < s and p does not divide s.
"""
import json, itertools, sys

def zg_terminates(p, q, r, s):
    if p >= s or q >= r:
        return True
    if p < s < 2 * p and q < r and r % q != 0:
        return True
    if q < r < 2 * q and p < s and s % p != 0:
        return True
    return False

def h4_nonterminating(p, q, r, s):   # CLM-C03-10 as stated by the lab
    a = r >= 2 * q and s >= 2 * p
    b = s >= 2 * p and q < r < 2 * q and s % p == 0
    c = r >= 2 * q and p < s < 2 * p and r % q == 0
    return a or b or c

def h3_nonterminating(p, q, r, s):   # CLM-C03-09
    return r > q and s > p and (r >= 2 * q or s >= 2 * p)

def h2_terminating(p, q, r, s):      # CLM-C03-08
    return r < 2 * q or s < 2 * p

# 1. H-C03-4 versus Zantema-Geser on a large box
bad = [t for t in itertools.product(range(1, 41), repeat=4)
       if h4_nonterminating(*t) == zg_terminates(*t)]
print("H-C03-4 vs ZG Thm 1, 1<=p,q,r,s<=40:", "identical" if not bad else bad[:10])

# 2. lab statuses (EXP-C03-02 rows, + mirror resolutions of EXP-C03-03) versus ZG
rows = json.load(open(sys.argv[1]))["results"]["rows"]
mism, unk = [], []
for row in rows:
    t = tuple(row["rule"]); st = row["status"]
    z = "TERMINATING" if zg_terminates(*t) else "NON-TERMINATING"
    if st == "UNKNOWN":
        unk.append((t, z))
    elif st != z:
        mism.append((t, st, z))
print("rows:", len(rows), "decided mismatches with ZG:", mism)
print("lab UNKNOWN rules and their ZG status:")
from collections import Counter
print(Counter(z for _, z in unk))
for t, z in unk:
    print("  ", t, z)

# 3. hypotheses H-C03-2/3 against ZG in the same 5-box
c2 = [t for t in itertools.product(range(1, 6), repeat=4) if h2_terminating(*t) != zg_terminates(*t)]
c3 = [t for t in itertools.product(range(1, 6), repeat=4) if h3_nonterminating(*t) == zg_terminates(*t)]
print("H-C03-2 disagreements with ZG (<=5):", len(c2))
print("H-C03-3 disagreements with ZG (<=5):", len(c3), c3)
