"""Corollary 3a/3b of C13 Theorem 3: #models = #{a: a*P(a) = 1 mod N} equals #roots of the n-bonacci polynomial
(right comb) and of k a^2 + a - 1 (left comb), N <= 300; tribonacci-law spectrum head (textbook)."""
def cnt_a(P, N):
    return sum(1 for a in range(N) if (a * sum(c * pow(a, i, N) for i, c in enumerate(P)) - 1) % N == 0)
bad = []
for n in range(1, 7):
    P = [1] * n
    for N in range(1, 301):
        nb = sum(1 for t in range(N) if (pow(t, n, N) - sum(pow(t, i, N) for i in range(n))) % N == 0)
        if cnt_a(P, N) != nb:
            bad.append(("right comb", n, N))
for k in range(1, 7):
    P = [1, k]
    for N in range(1, 301):
        q = sum(1 for a in range(N) if (k * a * a + a - 1) % N == 0)
        if cnt_a(P, N) != q:
            bad.append(("left comb", k, N))
print("Corollaries 3a/3b, n,k <= 6, N <= 300: mismatches", bad[:5])
trib = [N for N in range(1, 60) if cnt_a([1, 1, 1], N) > 0]
print("tribonacci-law spectrum head:", trib[:12])
