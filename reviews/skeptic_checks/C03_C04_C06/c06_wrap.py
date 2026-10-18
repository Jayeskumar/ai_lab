"""CLM-C06-01 citation check (own code).  For N <= 64: the system
   p*1 = p+1 (mod N),  p*(q+1) = (p*q)*(p+1) for 1 <= q < N          (1-based, Laver's convention)
has the unique solution computed row by row from p = N downwards (if the recursion never needs an
uncomputed row).  Check (a) uniqueness/existence of that solution, (b) whether it also satisfies the
wrap-around instance q = N, i.e. p*1 = (p*N)*(p*1), (c) whether it is left-distributive.
Writes out/c06_wrap.json."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "out"


def rec(N):
    L = [[0] * (N + 2) for _ in range(N + 2)]
    for q in range(1, N + 1):          # forced: N*q = q (from the recursion with p = N)
        L[N][q] = q
    for p in range(N - 1, 0, -1):
        L[p][1] = p + 1
        for q in range(1, N):
            v = L[p][q]
            if v <= p:
                return None
            L[p][q + 1] = L[v][p + 1]
    return L


def check(N):
    L = rec(N)
    if L is None:
        return {"recursion": "breaks down"}
    succ = lambda p: 1 if p == N else p + 1
    q_lt_N = all(L[p][q + 1] == L[L[p][q]][succ(p)] for p in range(1, N + 1) for q in range(1, N))
    anchor = all(L[p][1] == succ(p) for p in range(1, N + 1))
    wrap = all(L[p][1] == L[L[p][N]][succ(p)] for p in range(1, N + 1))
    ld = all(L[a][L[b][c]] == L[L[a][b]][L[a][c]] for a in range(1, N + 1) for b in range(1, N + 1)
             for c in range(1, N + 1)) if N <= 64 else None
    return {"recursion": "ok", "satisfies_q_lt_N": q_lt_N, "anchor": anchor, "wrap_around_holds": wrap, "LD": ld}


res = {N: check(N) for N in range(1, 65)}
pow2 = [N for N in res if N & (N - 1) == 0]
out = {
    "recursion_never_breaks_down_N_le_64": all(v["recursion"] == "ok" for v in res.values()),
    "all_satisfy_q_lt_N_and_anchor": all(v["satisfies_q_lt_N"] and v["anchor"] for v in res.values()),
    "wrap_around_holds_exactly_at": [N for N, v in res.items() if v["wrap_around_holds"]],
    "LD_exactly_at": [N for N, v in res.items() if v["LD"]],
    "powers_of_two": pow2,
}
(OUT / "c06_wrap.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out))
