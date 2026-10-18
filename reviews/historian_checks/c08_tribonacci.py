"""Historian check (C08): tribonacci circle products.

Messaoudi (Math. Slovaca 50 (2000), Thm 2/Thm 3) shows: the shifted product a o_s b =
sum d_i(a) d_j(b) G_{i+j+s} (G = 1,2,4,7,13,...) is associative iff beta^s * x * y is a
beta-integer for all beta-integers x, y.  Ambroz-Frougny-Masakova-Pelantova (2003) show
L_otimes >= 4 for the tribonacci number, i.e. some product x*y of beta-integers has 4
fractional digits.  We look for such x, y and test associativity of o_3 directly.
"""
import itertools, sys
import mpmath as mp
mp.mp.dps = 80

# Z[beta] elements as (c0, c1, c2): c0 + c1 b + c2 b^2, with b^3 = b^2 + b + 1
def mul(u, v):
    p = [0] * 5
    for i in range(3):
        for j in range(3):
            p[i + j] += u[i] * v[j]
    # reduce b^4 = b^3 + b^2 + b = (b^2+b+1) + b^2 + b = 2b^2 + 2b + 1
    c0 = p[0] + p[3] * 1 + p[4] * 1
    c1 = p[1] + p[3] * 1 + p[4] * 2
    c2 = p[2] + p[3] * 1 + p[4] * 2
    return (c0, c1, c2)
def add(u, v): return (u[0]+v[0], u[1]+v[1], u[2]+v[2])
def sub(u, v): return (u[0]-v[0], u[1]-v[1], u[2]-v[2])
ONE = (1, 0, 0); B = (0, 1, 0); BINV = (-1, -1, 1)   # b^-1 = b^2 - b - 1
_pow = {0: ONE}
def bpow(k):
    if k not in _pow:
        if k > 0: _pow[k] = mul(bpow(k - 1), B)
        else: _pow[k] = mul(bpow(k + 1), BINV)
    return _pow[k]
beta = mp.findroot(lambda x: x**3 - x**2 - x - 1, 1.84)
def val(u): return u[0] + u[1] * beta + u[2] * beta**2

def greedy(u, kmin=-60):
    """greedy beta-expansion of u > 0 (exact check); returns dict k->digit."""
    digs = {}
    r = u
    x = val(r)
    k = int(mp.floor(mp.log(x) / mp.log(beta))) + 1
    while True:
        if r == (0, 0, 0): return digs
        if k < kmin: return None
        x = val(r)
        if val(bpow(k)) <= x * (1 + mp.mpf(10)**-60):
            # exact confirmation
            rr = sub(r, bpow(k))
            if val(rr) >= -mp.mpf(10)**-50:
                digs[k] = 1; r = rr
        k -= 1

G = [1, 2, 4]
while len(G) < 80: G.append(G[-1] + G[-2] + G[-3])
def zdigits(n):
    d = {}
    for k in range(len(G) - 1, -1, -1):
        if G[k] <= n: d[k] = 1; n -= G[k]
    return d
def nu(n):
    u = (0, 0, 0)
    for k in zdigits(n): u = add(u, bpow(k))
    return u
def circ(a, b, s):
    da, db = zdigits(a), zdigits(b)
    return sum(G[i + j + s] for i in da for j in db)

if __name__ == '__main__':
    # admissible digit strings of length <= L (no 111), as beta-integers x = sum d_k b^k
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    words = []
    for n in range(1, G[L]):
        words.append(n)
    best = 0; ex = None
    for a in words:
        for b in words:
            if b < a: continue
            prod = mul(nu(a), nu(b))
            e = greedy(prod)
            fl = -min(e) if min(e) < 0 else 0
            if fl > best:
                best, ex = fl, (a, b, sorted(e, reverse=True))
    print("max fractional length of x*y over beta-integers with < %d digits: %d, example a,b=%s" % (L, best, ex[:2]))
    print("  expansion exponents:", ex[2])
    a, b = ex[0], ex[1]
    for s in (3, 4, 5):
        lhs_ok = (nu(circ(a, b, s)) == mul(bpow(s), mul(nu(a), nu(b))))
        bad = None
        for c in range(1, 400):
            if circ(circ(a, b, s), c, s) != circ(a, circ(b, c, s), s):
                bad = c; break
        print("s=%d: nu(a o b)==b^s nu(a)nu(b)? %s; associativity counterexample c=%s" % (s, lhs_ok, bad))
        if bad:
            c = bad
            print("    (%d o %d) o %d = %d  vs  %d o (%d o %d) = %d" % (a, b, c, circ(circ(a, b, s), c, s), a, b, c, circ(a, circ(b, c, s), s)))
