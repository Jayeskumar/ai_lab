"""Historian check (CLM-C10-02/03): two different 'costs of the successor' in the Zeckendorf system.
 - Hamming cost (the lab): number of digit positions that differ between rep(n) and rep(n+1).
 - carry propagation of Berthe-Frougny-Rigo-Sakarovitch (Adv. Appl. Math. 120 (2020) 102062,
   Def. 3.1): length of the suffix after the longest common prefix (max length if lengths differ).
BFRS formula (3)/Cor. 3.16 predicts gamma/(gamma-1) = phi^2 = 2.618... for the second one."""
def zeck_word(n):
    fib = [1, 2]
    while fib[-1] <= n: fib.append(fib[-1] + fib[-2])
    w = []
    for f in reversed(fib):
        if f <= n: w.append("1"); n -= f
        else: w.append("0")
    s = "".join(w).lstrip("0")
    return s if s else ""
def hamming(u, v):
    L = max(len(u), len(v)); u = u.rjust(L, "0"); v = v.rjust(L, "0")
    return sum(a != b for a, b in zip(u, v))
def bfrs_cp(u, v):
    if len(u) != len(v): return max(len(u), len(v))
    k = 0
    while k < len(u) and u[k] == v[k]: k += 1
    return len(u) - k
N = 200000
H = C = 0
prev = zeck_word(0)
for n in range(N):
    nxt = zeck_word(n + 1)
    H += hamming(prev, nxt); C += bfrs_cp(prev, nxt)
    prev = nxt
phi = (1 + 5 ** 0.5) / 2
print("N=%d  mean Hamming cost %.5f   mean BFRS carry propagation %.5f   phi^2 = %.5f" % (N, H / N, C / N, phi * phi))
print("check cp(12) =", bfrs_cp(zeck_word(12), zeck_word(13)), "(BFRS Example 3.2 says 6)")
