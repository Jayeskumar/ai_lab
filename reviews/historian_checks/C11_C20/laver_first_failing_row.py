"""Historian check (CLM-C17-05): for the recursion table A_N (1-based, p*1 = p+1 mod N,
p*(q+1) = (p*q)*(p+1) for q < N), find the topmost row p with period(p) not dividing N,
for N not a power of 2.  Records N, v2(N), N - p and period(p).  Light (N <= NMAX)."""
import sys, collections
sys.path.insert(0, __import__('os').path.dirname(__file__))
from laver_wraparound import recursion_table, period

def v2(n):
    k = 0
    while n % 2 == 0:
        n //= 2; k += 1
    return k

if __name__ == "__main__":
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 256
    pattern = collections.Counter()
    rows = []
    for N in range(3, NMAX + 1):
        if N & (N - 1) == 0:
            continue
        T = recursion_table(N)
        for p in range(N - 1, 0, -1):
            pr = period(T, N, p)
            if N % pr:
                k = v2(N)
                pattern[(k, N - p, pr)] += 1
                rows.append((N, k, N - p, pr))
                break
    for key, c in sorted(pattern.items()):
        print("v2(N)=%d  topmost failing row N-p=%d  period=%d : %d values of N" % (key[0], key[1], key[2], c))
