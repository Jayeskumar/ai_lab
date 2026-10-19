"""Historian check (CLM-C16-05/07 vs Klimov, arXiv:2604.05754, Problem 7.5):
does the lab's order-5 full-period example give a UFS-groupoid (Klimov: f_n = f_{n-2} * f_{n-1},
periodic UFS = de Bruijn cycle B(n,2)) that is a quasigroup?  Tiny check."""
seq = [0,0,1,0,2,2,0,3,3,1,2,1,4,0,4,4,2,3,2,4,1,1,3,4,3]
n, L = 5, len(seq)
pairs = [(seq[i], seq[(i + 1) % L]) for i in range(L)]
dist2 = [(seq[i], seq[(i + 2) % L]) for i in range(L)]
print("length", L, "| de Bruijn B(5,2) (all pairs at distance 1 once):", len(set(pairs)) == n * n)
print("all pairs at distance 2 once:", len(set(dist2)) == n * n)
# Klimov's convention: u_{k+2} = u_k * u_{k+1}  -> table T[a][b] = next element after window (a,b)
T = [[None] * n for _ in range(n)]
for i in range(L):
    a, b, c = seq[i], seq[(i + 1) % L], seq[(i + 2) % L]
    assert T[a][b] in (None, c); T[a][b] = c
rows_ok = all(sorted(T[a]) == list(range(n)) for a in range(n))
cols_ok = all(sorted(T[a][b] for a in range(n)) == list(range(n)) for b in range(n))
print("Klimov-convention table is a quasigroup (Latin square):", rows_ok and cols_ok)
for r in T: print("   ", r)
# check that the Fibonacci sequence from every pair is a suffix of the periodic sequence (UFS)
def orbit(a, b, steps):
    out = [a, b]
    for _ in range(steps): out.append(T[out[-2]][out[-1]])
    return out
ok = all(len(set(zip(orbit(a, b, L)[:-1], orbit(a, b, L)[1:]))) == L for a in range(n) for b in range(n))
print("pair map is a single 25-cycle from every start:", ok)
