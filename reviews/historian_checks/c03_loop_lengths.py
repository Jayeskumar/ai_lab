"""Historian check (CLM-C03-11): loop lengths stored in results/EXP-C03-04.json for the base rules
0 1^q -> 1^(q+1) 0^k versus the closed form 1 + (k^q - 1)/(k - 1) = 1 + sum_{i<q} k^i, the same
expression as the minimal loop length 1 + sum_{i<l} r^i of A. Geser's family 1 0^p -> 0^p 1^r 0^q
(RTA 2002, LNCS 2378, Theorem 1, l = ceil(p/q))."""
import json
d = json.load(open("results/EXP-C03-04.json"))["results"]
rows = [l for l in d["loops"] if l["rule"][2] == l["rule"][1] + 1]
ok = 0
for l in rows:
    p, q, r, k = l["rule"]
    f = 1 + sum(k ** i for i in range(q))
    ok += (f == l["steps"])
print("base rules with r = q + 1:", len(rows), " matching 1 + sum_{i<q} k^i:", ok)
