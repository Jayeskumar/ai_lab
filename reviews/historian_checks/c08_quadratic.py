"""Historian check (C08): canonical quadratic sequence G(k+1) = 4G(k) + 3G(k-1), G = 1,5,...
(Fraenkel/Messaoudi canonical: G_1 = p + 1).  Messaoudi (Math. Slovaca 50 (2000), Thm 2 and the
remark after it) gives: o_s associative <=> alpha^s nu(a) nu(b) lies in nu(N) for all a, b.
Appending a zero keeps a canonical greedy word greedy, so associativity at s implies it at s+1
[DERIVED].  The lab reports shifts {4} u [6, 10] for this sequence; we look for a failure at s = 4."""
import sys, random
sys.path.insert(0, '.')
from systems.circle import BaseSequence

def run(p, q, g1, s_list, N, seed=1):
    S = BaseSequence('seq', [1, g1], (p, q))
    # Z[alpha] with alpha^2 = p alpha + q, element (c0, c1)
    def mul(u, v):
        a0, a1 = u; b0, b1 = v
        c0 = a0 * b0; c1 = a0 * b1 + a1 * b0; c2 = a1 * b1
        return (c0 + q * c2, c1 + p * c2)
    pw = [(1, 0)]
    for _ in range(200): pw.append(mul(pw[-1], (0, 1)))
    def nu(n):
        u = (0, 0)
        for i, d in S.greedy(n).items():
            u = (u[0] + d * pw[i][0], u[1] + d * pw[i][1])
        return u
    for s in s_list:
        bad = None
        for a in range(1, N):
            na = nu(a)
            for b in range(a, N):
                if nu(S.circle(a, b, s)) != mul(pw[s], mul(na, nu(b))):
                    bad = (a, b); break
            if bad: break
        msg = "no embedding failure for a,b < %d" % N
        if bad:
            a, b = bad
            cs = [c for c in range(1, 2000) if S.circle(S.circle(a, b, s), c, s) != S.circle(a, S.circle(b, c, s), s)][:3]
            msg = "embedding fails at (a,b)=%s; associativity fails with c in %s" % (bad, cs)
            if cs:
                c = cs[0]
                msg += "; (a o b) o c = %d, a o (b o c) = %d" % (S.circle(S.circle(a, b, s), c, s), S.circle(a, S.circle(b, c, s), s))
        print("G(k+1)=%dG(k)+%dG(k-1), G=1,%d, s=%d: %s" % (p, q, g1, s, msg))

if __name__ == "__main__":
    run(4, 3, 5, [4, 5], 400)
