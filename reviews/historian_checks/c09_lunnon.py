"""Historian check (CLM-C09-01): the lab's formula a o b = ab + a b* + a* b, n* = floor((n+1)/phi),
versus Lunnon's formula in OEIS A101330 (2008): T(n,k) = 3nk - n floor((k+1)/phi^2) - k floor((n+1)/phi^2).
[DERIVED] floor((k+1)/phi^2) = (k+1) - ceil((k+1)/phi) = k - k*, hence the two agree."""
import math, sys
sys.path.insert(0, 'reviews/historian_checks')
from seqs import circ, star
def fl_phi2(m):           # floor(m / phi^2) = floor(m (3 - sqrt5)/2), exact
    return (3 * m - math.isqrt(5 * m * m) - 1) // 2 if False else (3 * m - (math.isqrt(5 * m * m) + 1)) // 2
bad = 0
for n in range(1, 400):
    for k in range(1, 400):
        lunnon = 3 * n * k - n * fl_phi2(k + 1) - k * fl_phi2(n + 1)
        if lunnon != circ(n, k) or fl_phi2(k + 1) != k - star(k):
            bad += 1
print("pairs n,k < 400 where Lunnon's A101330 formula != lab formula:", bad)
