"""Historian check: compute sequences from C04, C09, C10 claims for OEIS look-ups."""
import math
from functools import lru_cache

def kappa(n):
    k = 0
    while 2**k + k < n:
        k += 1
    return k

def D_aab_ba(n):            # CLM-C04-09 closed form
    return n - 1 - kappa(n)

def octal_grundy(code_digits, N):
    """Grundy values G(0..N) of the octal game 0.d1 d2 d3 ... (digit k = remove k tokens)."""
    G = [0] * (N + 1)
    for n in range(1, N + 1):
        opts = set()
        for k, d in enumerate(code_digits, start=1):
            if k > n:
                break
            if d & 1 and n == k:                 # remove whole heap
                opts.add(0)
            if d & 2 and n > k:                  # leave one heap
                opts.add(G[n - k])
            if d & 4 and n - k >= 2:             # leave two nonempty heaps
                for a in range(1, (n - k) // 2 + 1):
                    opts.add(G[a] ^ G[n - k - a])
        g = 0
        while g in opts:
            g += 1
        G[n] = g
    return G

# Zeckendorf (G = 1,2,3,5,...) representations and per-step Hamming cost
def zeck(n):
    fib = [1, 2]
    while fib[-1] <= n:
        fib.append(fib[-1] + fib[-2])
    s = set()
    for i in range(len(fib) - 1, -1, -1):
        if fib[i] <= n:
            s.add(i); n -= fib[i]
    return s

def zeck_cost(n):
    return len(zeck(n) ^ zeck(n + 1))

# Knuth circle product via n* = floor((n+1)/phi): a o b = ab + a b* + a* b
PHI = (1 + 5 ** 0.5) / 2
def star(n):
    # exact: n* = floor((n+1)/phi) = floor((n+1)*(sqrt5-1)/2)
    m = n + 1
    return (math.isqrt(5 * m * m) - m) // 2
def circ(a, b):
    return a * b + a * star(b) + star(a) * b

if __name__ == "__main__":
    print("D(aab->ba), n=1..40:", [D_aab_ba(n) for n in range(1, 41)])
    print("kappa, n=1..40:", [kappa(n) for n in range(1, 41)])
    g06 = octal_grundy([0, 6], 120)       # 0.06
    print("0.06 Grundy n=0..80:", g06[:81])
    g6 = octal_grundy([6], 80)            # 0.6 Officers
    print("0.6 Officers n=0..60:", g6[:61])
    g007 = octal_grundy([0, 0, 7], 80)    # 0.007 Treblecross
    print("0.007 n=0..60:", g007[:61])
    g07 = octal_grundy([0, 7], 140)       # 0.07 Dawson's Kayles
    print("0.07 n=0..60:", g07[:61])
    # last n with G(n) != G(n+34) for Dawson's Kayles, up to 2000
    gk = octal_grundy([0, 7], 2200)
    bad = [n for n in range(0, 2100) if gk[n] != gk[n + 34]]
    print("Dawson's Kayles: n with G(n)!=G(n+34):", bad[-5:], "-> periodic from n =", bad[-1] + 1)
    g4 = octal_grundy([4], 2200)
    bad4 = [n for n in range(0, 2100) if g4[n] != g4[n + 34]]
    print("0.4: n with G(n)!=G(n+34):", bad4[-5:], "-> periodic from n =", bad4[-1] + 1)
    print("0.4 vs DK shifted:", all(g4[n + 1] == gk[n] for n in range(0, 2000)))
    # circle products
    N = 200
    prods = set()
    for a in range(1, N + 1):
        for b in range(a, N + 1):
            c = circ(a, b)
            if c <= N:
                prods.add(c)
    irr = [n for n in range(1, N + 1) if n not in prods]
    print("circle irreducibles:", irr[:50])
    print("circle reducibles:", sorted(prods)[:50])
    print("Zeckendorf step cost d(n,n+1), n=0..60:", [zeck_cost(n) for n in range(0, 61)])
    # check total = 2N - s(N)
    tot = 0; ok = True
    for Nn in range(1, 3000):
        tot += zeck_cost(Nn - 1)
        if tot != 2 * Nn - len(zeck(Nn)):
            ok = False; print("fail", Nn); break
    print("sum_{n<N} d(n,n+1) == 2N - s_Z(N) for N<3000:", ok)
