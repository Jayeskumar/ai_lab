"""Skeptic batch 1.1 -- CLM-C17-08: numerical checks of the row-period argument, written from scratch.

0-based convention of the lab: elements 0..N-1, x*0 = x+1 (mod N), x*(y+1) = (x*y)*(x+1) for y <= N-2.
F_N denotes the forced table (unique by C17_ForcedTable.lean).  Facts checked (the lemmas of my written
proof in reviews/skeptic_batch1.1.md, section 1):

 L1  row N-1 is the identity; for x < N-1 every entry of row x is > x;
 L2  for x < N-1 the row of x increases strictly until it reaches N-1 and then restarts, so it is periodic
     with period pi(x) = 1 + (first y with x*y = N-1);
 L3  wrap-around at x  <=>  x*(N-1) = N-1  <=>  pi(x) divides N;
 L4  N = 2^m: all rows satisfy the wrap-around and all periods are powers of 2 (checked up to 2^10);
 L5  N not a power of 2, k = v2(N), B = 2^(k+1), s = N - B (0-based s is also the first row of the block):
     (i)   F_N(x, y) = s + F_B(x - s, y mod 2^k)   for s <= x <= N-2 and all y;
     (ii)  F_N(s-1, y) = s + (y mod B) for all y, so pi(s-1) = B, which does not divide N;
     (iii) hence the wrap-around fails at x = s - 1 (1-based p = s).

usage: python c17_row_period.py [NMAX_FULL] [NMAX_BLOCK]
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def forced(N, lowest=0):
    """Rows lowest..N-1 of F_N (row r is a list of length N); rows are filled from N-1 downwards."""
    T = {N - 1: list(range(N))}
    for x in range(N - 2, lowest - 1, -1):
        row = [0] * N
        row[0] = x + 1
        for y in range(N - 1):
            v = row[y]
            row[y + 1] = T[v][x + 1]       # v > x, so row v is known
        T[x] = row
    return T


def v2(n):
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def is_pow2(n):
    return n & (n - 1) == 0


def period(row, N):
    for y, v in enumerate(row):
        if v == N - 1:
            return y + 1
    return None


def check_full(N):
    """L1-L3 on the whole table, plus L4 / L5 depending on N.  Returns a list of failures."""
    bad = []
    T = forced(N)
    if T[N - 1] != list(range(N)):
        bad.append("L1 identity")
    wrap_ok = []
    for x in range(N - 1):
        row = T[x]
        if min(row) <= x:
            bad.append(("L1", x))
        p = period(row, N)
        if p is None:
            bad.append(("L2 no top", x))
            continue
        if any(row[y] >= row[y + 1] for y in range(p - 1)):
            bad.append(("L2 not increasing", x))
        if any(row[y] != row[y % p] for y in range(N)):
            bad.append(("L2 not periodic", x))
        w = T[row[N - 1]][x + 1] if row[N - 1] < N - 1 else x + 1   # (x*(N-1))*(x+1); row N-1 is identity
        wrap = (w == x + 1)
        if not (wrap == (row[N - 1] == N - 1) == (N % p == 0)):
            bad.append(("L3", x))
        wrap_ok.append(wrap)
        if is_pow2(N) and (p & (p - 1)):
            bad.append(("L4 period not a power of 2", x, p))
    # x = N-1: (N-1)*(N-1) = N-1, then (N-1)*0 = 0 = (N-1)+1 mod N: always holds
    full = all(wrap_ok)
    if full != is_pow2(N):
        bad.append(("full instance", full))
    return bad, T


def check_block(N, cache):
    """L5 for N not a power of 2, computing only rows s-1..N-1 of F_N."""
    k = v2(N)
    B = 2 ** (k + 1)
    s = N - B
    if B not in cache:
        cache[B] = forced(B)
    FB = cache[B]
    T = forced(N, lowest=s - 1)
    m = 2 ** k
    bad = []
    for x in range(s, N - 1):
        u = x - s
        if any(T[x][y] != s + FB[u][y % m] for y in range(N)):
            bad.append(("(i)", x))
    if any(T[s - 1][y] != s + (y % B) for y in range(N)):
        bad.append(("(ii)", s - 1))
    if period(T[s - 1], N) != B or N % B == 0:
        bad.append(("(ii) period", s - 1))
    x = s - 1
    v = T[x][N - 1]
    w = T[v][x + 1] if v < N - 1 else x + 1
    if w == x + 1:
        bad.append(("(iii) wrap-around holds", x))
    # the lemma used in the induction: rows u <= B-2 of F_B have a period dividing 2^k
    for u in range(B - 1):
        p = period(FB[u], B)
        if m % p:
            bad.append(("period lemma", B, u, p))
    return bad


def main():
    nfull = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    nblock = int(sys.argv[2]) if len(sys.argv) > 2 else 1100
    extra = [1536, 1792, 2560, 3072, 3584, 3840, 4095, 2 * 3 * 5 * 7 * 9, 12 * 256 + 256]
    t0 = time.time()
    out = {"full_check_N": [1, nfull], "full_failures": {}, "block_check": [], "block_failures": {}}
    for N in range(1, nfull + 1):
        bad, _ = check_full(N)
        if bad:
            out["full_failures"][N] = bad[:5]
    for N in (512, 1024):
        bad, _ = check_full(N)
        if bad:
            out["full_failures"][N] = bad[:5]
    cache = {}
    Ns = [N for N in range(3, nblock + 1) if not is_pow2(N)] + extra
    for N in Ns:
        bad = check_block(N, cache)
        if bad:
            out["block_failures"][N] = bad[:5]
    out["block_check"] = {"count": len(Ns), "range": [3, nblock], "extra": extra}
    out["seconds"] = round(time.time() - t0, 1)
    print(json.dumps(out, indent=1))
    with open(os.path.join(HERE, "c17_row_period.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
