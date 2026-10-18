"""Historian check (C08): spot-check the measured associativity thresholds of CLM-C08-05.

For a base sequence with recurrence G_k = a_1 G_{k-1} + ... + a_d G_{k-d}, nu(n) = sum d_i x^i in
Z[x]/(x^d - a_1 x^{d-1} - ... - a_d) is injective (the functional x^i -> G_i recovers n), and
nu(a o_s b) = x^s nu(a) nu(b) for all a, b implies associativity of o_s.  A failure of this identity
is not itself a counterexample, so every reported failure is followed by an explicit search for c with
(a o b) o c != a o (b o c) (exact integers, the lab's own systems.circle implementation)."""
import sys, random
sys.path.insert(0, '.')
from systems.circle import BaseSequence

def check(name, initial, coeffs, s, N=250, extra=3000, seed=7):
    S = BaseSequence(name, initial, coeffs)
    d = len(coeffs)
    def mul(u, v):
        p = [0] * (2 * d - 1)
        for i, x in enumerate(u):
            if x:
                for j, y in enumerate(v):
                    p[i + j] += x * y
        for k in range(2 * d - 2, d - 1, -1):     # x^k = sum a_t x^{k-t}
            c = p[k]; p[k] = 0
            if c:
                for t, a in enumerate(coeffs, start=1):
                    p[k - t] += a * c
        return tuple(p[:d])
    X = tuple([0, 1] + [0] * (d - 2)) if d > 1 else (coeffs[0],)
    pw = [tuple([1] + [0] * (d - 1))]
    for _ in range(400): pw.append(mul(pw[-1], X))
    cache = {}
    def nu(n):
        if n in cache: return cache[n]
        u = [0] * d
        for i, dg in S.greedy(n).items():
            for t in range(d): u[t] += dg * pw[i][t]
        cache[n] = tuple(u); return cache[n]
    pairs = [(a, b) for a in range(1, N) for b in range(a, N)]
    rnd = random.Random(seed)
    pairs += [(rnd.randrange(1, 10**6), rnd.randrange(1, 10**6)) for _ in range(extra)]
    for a, b in pairs:
        if nu(S.circle(a, b, s)) != mul(pw[s], mul(nu(a), nu(b))):
            for c in range(1, 300):
                L = S.circle(S.circle(a, b, s), c, s); R = S.circle(a, S.circle(b, c, s), s)
                if L != R:
                    return "NOT associative: (%d o %d) o %d = %d != %d = %d o (%d o %d)" % (a, b, c, L, R, a, b, c)
            return "embedding fails at (%d,%d) but no c < 300 found" % (a, b)
    return "no failure found (embedding holds on all tested pairs)"

if __name__ == "__main__":
    tests = [
        ("Fibonacci 1,2", [1, 2], (1, 1), [1, 2]),
        ("Pell 1,2,5", [1, 2], (2, 1), [0, 1]),
        ("(2,2) 1,2", [1, 2], (2, 2), [4, 5]),
        ("tribonacci 1,2,4", [1, 2, 4], (1, 1, 1), [3, 4, 5]),
        ("4-bonacci 1,2,4,8", [1, 2, 4, 8], (1, 1, 1, 1), [6, 7, 8, 9, 10]),
        ("G(k+1)=G(k)+G(k-2) 1,2,3", [1, 2, 3], (1, 0, 1), [9, 10, 11]),
        ("(3,3) 1,5", [1, 5], (3, 3), [9, 10, 11]),
    ]
    for name, init, co, ss in tests:
        for s in ss:
            print("%-28s s=%2d: %s" % (name, s, check(name, init, co, s)), flush=True)
