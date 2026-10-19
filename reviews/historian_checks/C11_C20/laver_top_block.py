"""Historian check (CLM-C17-05), testing a [DERIVED] argument:
for N not a power of 2, k = v2(N), s = N - 2^(k+1):
  (i)  rows s+1..N-1 of the recursion table A_N are shifted copies of rows 1..2^(k+1)-1 of the
       Laver table A_(k+1):  v *_N c = s + ((v-s) *_(k+1) c*),  c* = ((c-1) mod 2^k) + 1;
  (ii) row s of A_N is s+1, s+2, ..., N, so its period is 2^(k+1), which does not divide N;
hence the wrap-around instance fails at p = s.  Only rows s..N are computed (cheap)."""
import sys

def top_rows(N, s):
    T = {N: list(range(0, N + 1))}          # T[v][c], 1-based columns; row N is the identity
    for p in range(N - 1, s - 1, -1):
        row = [0] * (N + 1)
        row[1] = p + 1
        for q in range(1, N):
            row[q + 1] = T[row[q]][p + 1]
        T[p] = row
    return T

def laver(n):
    M = 2 ** n
    return top_rows(M, 1) if M > 1 else {1: [0, 1]}

def v2(n):
    k = 0
    while n % 2 == 0:
        n //= 2; k += 1
    return k

if __name__ == "__main__":
    Ns = list(range(3, int(sys.argv[1]) + 1)) if len(sys.argv) > 1 else list(range(3, 1025))
    Ns += [int(x) for x in sys.argv[2:]]
    bad, tested = [], 0
    cache = {}
    for N in Ns:
        if N & (N - 1) == 0:
            continue
        k = v2(N); B = 2 ** (k + 1); s = N - B
        if k + 1 not in cache:
            cache[k + 1] = laver(k + 1)
        L = cache[k + 1]
        T = top_rows(N, s)
        ok = all(T[v][c] == s + L[v - s][((c - 1) % (2 ** k)) + 1] for v in range(s + 1, N) for c in range(1, N + 1))
        ok2 = T[s][1:B + 1] == list(range(s + 1, N + 1)) and T[s][N] != N
        tested += 1
        if not (ok and ok2):
            bad.append(N)
    print("tested", tested, "values of N; failures:", bad[:20])
