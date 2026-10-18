"""Historian check (CLM-C04-10): the lab's formula A247983(n) = n - max{j : 2^j + j <= n+1}
answers Clark Kimberling's question in OEIS A083706 / A247983 (2014):
'Is A247983(n+1) = A247983(n) if and only if n is in A083706?'  (A083706(k) = 2^(k+1) + k - 1)."""
import sys, json
sys.path.insert(0, '.')
from lab import oeis
r = oeis._query('id:A247983')['response']
r = r.get('results') if isinstance(r, dict) else r
data = [int(x) for x in r[0]['data'].split(',')]
def J(n):
    j = 0
    while 2 ** (j + 1) + j + 1 <= n + 1: j += 1
    return j
A = {n: n - J(n) for n in range(1, 5000)}
print("formula vs OEIS data (n = 1..%d):" % len(data), all(A[n] == data[n - 1] for n in range(1, len(data) + 1)))
stalls = [n for n in range(1, 4999) if A[n + 1] == A[n]]
a083706 = [2 ** (k + 1) + k - 1 for k in range(0, 12)]
print("stall positions n < 4999:", stalls)
print("A083706 terms < 4999:   ", [x for x in a083706 if x < 4999])
