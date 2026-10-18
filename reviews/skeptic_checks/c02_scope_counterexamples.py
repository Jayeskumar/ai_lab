"""Scope counterexamples for the statement of CLM-C02-07 (exact arithmetic).
(1) rule 2[k] -> 3[k+1] (m=2, b=(3)): P~ = 3y - 2 is primitive and irreducible, r = 2/3.
    No stable configuration (digits 0/1) on <= 18 levels has value 2, so rep(2) does not exist
    (and every derivation from 2 tokens is infinite: the value 2 is preserved and never stable).
(2) rule 2[k] -> 4[k+1] (m=2, b=(4)): P~ = 4y - 2 is NOT primitive (content 2), r = 1/2, yet the
    stable configurations (digits 0/1) have pairwise distinct values (exact check on <= 16 levels),
    so the claimed converse 'not primitive => two stable configurations of equal value' fails."""
from fractions import Fraction
import itertools
r = Fraction(2, 3)
vals = set()
hit = False
for L in range(1, 19):
    pass
for digs in itertools.product((0, 1), repeat=18):
    v = sum(Fraction(d) * r ** k for k, d in enumerate(digs) if d)
    if v == 2:
        hit = True
        break
print("(2;3): stable configuration of value 2 on <= 18 levels exists:", hit)
# a few steps of the sweep from n = 2 (each level keeps 1 token and passes 3 up)
c, k = [2], 0
for k in range(8):
    c += [0] * 2
    t = c[k] // 2
    c[k] -= 2 * t
    c[k + 1] += 3 * t
print("(2;3): sweep from n=2 after 8 levels:", c[:9], "(level 8 still holds", c[8], ">= m)")
r2 = Fraction(1, 2)
seen, coll = set(), 0
for digs in itertools.product((0, 1), repeat=16):
    v = sum(Fraction(d) * r2 ** k for k, d in enumerate(digs) if d)
    coll += v in seen
    seen.add(v)
print("(2;4): collisions among 2^16 stable configurations:", coll)
