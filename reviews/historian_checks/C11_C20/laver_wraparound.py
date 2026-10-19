"""Historian check (C11-C20 review, CLM-C17-05 literature question).

1-based convention of the surveys (Biane arXiv:1810.00548 sec. 2.1; Dehornoy arXiv:1401.3302 Thm 1.1):
  p*1 = p+1 mod N (values in 1..N),  p*(q+1) = (p*q)*(p+1) for q < N   (recursion, unique table A_N)
The surveys state (1.2) p*(q*1) = (p*q)*(p*1) 'for all p, q'; at q = N this is the wrap-around
equation p+1 = (p*N)*(p+1).  We check, for small N:
  (a) brute force at N = 3: no table at all satisfies (1.1) and (1.2) for all p, q;
  (b) for the recursion table A_N: wrap-around holds at p  <=>  p*N = N  <=>  period(p) | N;
  (c) the N <= NMAX for which A_N satisfies the full instance, and for which it is left-distributive.
Light computation (NMAX = 128 by default)."""
import itertools, sys

def recursion_table(N):
    T = [[0] * (N + 1) for _ in range(N + 1)]
    for q in range(1, N + 1):
        T[N][q] = q                     # row N is the identity (forced, see Biane 2.1)
    for p in range(N - 1, 0, -1):
        T[p][1] = p + 1
        for q in range(1, N):
            v = T[p][q]
            T[p][q + 1] = T[v][p + 1]   # v > p, row v already known
    return T

def full_instance(T, N):
    s1 = lambda x: x % N + 1            # x*1 = x+1 mod N in 1..N
    return all(T[p][T[q][1]] == T[T[p][q]][T[p][1]] for p in range(1, N + 1) for q in range(1, N + 1))

def left_distributive(T, N):
    R = range(1, N + 1)
    return all(T[p][T[q][r]] == T[T[p][q]][T[p][r]] for p in R for q in R for r in R)

def period(T, N, p):
    for q in range(1, N + 1):
        if T[p][q] == N:
            return q
    return None

def brute_force_N3():
    N = 3
    count = 0
    cells = [(p, q) for p in range(1, 4) for q in range(2, 4)]  # column 1 fixed by (1.1)
    for vals in itertools.product(range(1, 4), repeat=len(cells)):
        T = [[0] * 4 for _ in range(4)]
        for p in range(1, 4):
            T[p][1] = p % N + 1
        for (p, q), v in zip(cells, vals):
            T[p][q] = v
        if full_instance(T, N):
            count += 1
    return count

if __name__ == "__main__":
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 128
    print("(a) N=3: tables satisfying (1.1) and (1.2) for all p,q:", brute_force_N3())
    full, ld, bad_equiv = [], [], 0
    for N in range(1, NMAX + 1):
        T = recursion_table(N)
        for p in range(1, N + 1):
            wrap = T[T[p][N]][p % N + 1] == T[p][T[N][1]]
            pr = period(T, N, p)
            if wrap != (T[p][N] == N) or (T[p][N] == N) != (pr is not None and N % pr == 0):
                bad_equiv += 1
        if full_instance(T, N):
            full.append(N)
        if N <= 64 and left_distributive(T, N):
            ld.append(N)
    print("(b) violations of 'wrap(p) <=> p*N=N <=> period(p) | N':", bad_equiv)
    print("(c) N <= %d with full instance:" % NMAX, full)
    print("    N <= 64 with left-distributive recursion table:", ld)
    T = recursion_table(3)
    print("    A_3 rows:", [T[p][1:] for p in range(1, 4)], " 1*3 =", T[1][3])
