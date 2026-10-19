"""Historian check (C11-C20 review): first terms of the Grundy sequence of the
'deleting divisors' game G03 (move n -> n - d, d | n, 1 < d < n), for an OEIS lookup.
Light computation (n <= 200)."""
import sys

def grundy(N):
    g = [0] * (N + 1)
    for n in range(1, N + 1):
        opts = set()
        d = 2
        while d * d <= n:
            if n % d == 0:
                for e in {d, n // d}:
                    if 1 < e < n:
                        opts.add(g[n - e])
            d += 1
        m = 0
        while m in opts:
            m += 1
        g[n] = m
    return g

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    g = grundy(N)
    print(",".join(str(x) for x in g[1:]))
    print("P-positions:", ",".join(str(n) for n in range(1, N + 1) if g[n] == 0))
