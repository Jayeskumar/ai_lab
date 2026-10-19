"""Skeptic checks for C19 that compare with stored results or use the phase-2 shortcut (own code).
 (1) exhaustive output (c19_exact.c) vs results/EXP-C19-01.json (L_exact, states) and all flags zero;
 (2) phase-2 deficit (strategy started at lazy(n)) vs full strategy simulation (c19_greedy.c) and
     split-phase length = Psi(lazy(n));
 (3) the provable bound D(n) <= B(n) - Psi(lazy(n)) = O(log^2 n) and its explicit form 1 + (t+1)(t+6)/2;
 (4) timing of the provable phase-2 method vs the conjectured recursion."""
import json, math, os, random, re, time
import c19_checks as C
OUT = C.OUT
# (1)
rows = {}
for fn in ("c19_exact_0_150.txt", "c19_exact_151_200.txt", "c19_exact_233.txt"):
    for line in open(os.path.join(OUT, fn)):
        p = line.split(); kv = {k: int(v) for k, v in re.findall(r'(\w+)=(-?\d+)', line)}
        rows[int(p[0])] = (int(p[1]), int(p[2]), kv)
flags = [n for n, (_, _, kv) in rows.items() if any(kv[k] for k in ("bad_dpsi", "bad_identity", "bad_strategy",
         "bad_split_unique", "bad_split_len")) or kv["nterm"] != 1 or kv["zeck"] != 1
         or (n <= 200 and (kv["lazy"] != 1 or kv["reach"] != rows[n][0]))]
st = json.load(open("/home/user/ai_lab/results/EXP-C19-01.json"))["results"]
print("(1) n with a raised flag:", flags, "| L(n), n<=150 equal to stored:",
      [rows[n][1] for n in range(151)] == st["L_exact"], "| states equal to stored:",
      [rows[n][0] for n in range(151)] == st["states"], "| positions n<=200:",
      sum(rows[n][0] for n in range(201)), "n=233:", rows[233][0], "L(233) =", rows[233][1])
# (2)
L, W, Bv, SL, LZ = C.read_greedy()
rng = random.Random(7)
ns = [rng.randrange(1, 100000) for _ in range(3000)] + list(range(1, 2000))
psi = lambda c: sum(x * (C.FIB[k + 2] - k - 3) for k, x in enumerate(c))
print("(2) phase-2 deficit vs full simulation:", len(ns), "n, mismatches", [n for n in ns if C.D_phase2(n) != W[n]][:5],
      "| split length = Psi(lazy):", [n for n in ns if psi(C.lazy(n)) != SL[n]][:5])
# (3)
bad = [n for n in range(2, 100000) if W[n] > Bv[n] - SL[n]]
def top(n): return len(C.lazy(n)) - 1
badf = [n for n in range(2, 100000) if Bv[n] - SL[n] > 1 + (top(n) + 1) * (top(n) + 6) // 2]
print("(3) D(n) <= B(n)-Psi(lazy(n)) violations (n<1e5):", len(bad), "| B-Psi(lazy) <= 1+(t+1)(t+6)/2 violations:", len(badf))
for n in (10**6, 10**9, 10**12, 10**15):
    d = C.lazy(n); g = C.B(n) - psi(d); t = len(d) - 1
    mv, Wv, _ = C.strategy_from(d)
    print("    n=%.0e: B-Psi(lazy)=%d, bound 1+(t+1)(t+6)/2=%d, phase-2 moves %d, D=%d" % (n, g, 1 + (t + 1) * (t + 6) // 2, mv, Wv))
# (4)
for n in (10**4, 10**7, 10**12, 10**18):
    t0 = time.perf_counter(); d = C.lazy(n); mv, Wv, _ = C.strategy_from(d); Lp = psi(d) + mv; t1 = time.perf_counter() - t0
    t0 = time.perf_counter(); Lr = C.B(n) - C.D_rec(n); t2 = time.perf_counter() - t0
    print("(4) n=%.0e L=%d phase-2==B-W: %s, ==recursion: %s, time phase-2 %.1e s, recursion %.1e s" % (n, Lp, Lp == C.B(n) - Wv, Lp == Lr, t1, t2))
