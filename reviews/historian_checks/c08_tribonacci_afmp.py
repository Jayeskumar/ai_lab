"""Historian check (C08): explicit non-associativity of the shifted tribonacci circle
product o_3 (lab's G-indexing, G = 1,2,4,7,13,...), from the example of
Ambroz-Frougny-Masakova-Pelantova (Bull. Belg. Math. Soc. 10 (2003) 641-659, Sec. 5):
x = (110100100101101)_beta has x*x = (110010001000100001001001011011.0011)_beta."""
import sys
sys.path.insert(0, 'reviews/historian_checks')
from c08_tribonacci import G, zdigits, nu, circ, mul, bpow, greedy

w = "110100100101101"
a = sum(G[k] for k, ch in enumerate(reversed(w)) if ch == "1")
print("a =", a, " zeckendorf-tribonacci digits:", "".join("1" if k in zdigits(a) else "0" for k in range(max(zdigits(a)), -1, -1)))
e = greedy(mul(nu(a), nu(a)))
print("beta-expansion of x*x: exponents", sorted(e, reverse=True), " fractional length", -min(e))
for s in (3, 4, 5):
    same = nu(circ(a, a, s)) == mul(bpow(s), mul(nu(a), nu(a)))
    bad = []
    for c in range(1, 3000):
        if circ(circ(a, a, s), c, s) != circ(a, circ(a, c, s), s):
            bad.append(c)
            if len(bad) >= 3: break
    print("s=%d: nu(a o a) == beta^s nu(a)^2: %s; c with (a o a) o c != a o (a o c): %s" % (s, same, bad))
    if bad:
        c = bad[0]
        L = circ(circ(a, a, s), c, s); R = circ(a, circ(a, c, s), s)
        print("    (%d o %d) o %d = %d,  %d o (%d o %d) = %d" % (a, a, c, L, a, a, c, R))
