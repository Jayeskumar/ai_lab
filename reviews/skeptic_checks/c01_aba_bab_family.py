"""Check the paper's remark (C01.md, Conjecture 7 status): aba <-> bab completes to
bab -> aba together with b a^j b a -> a b a a b^(j-1) (j >= 2).
(1) soundness: each family rule is a consequence of aba = bab (BFS in the length-(j+3) class), j = 2..9;
(2) completeness on short words: #words of length n avoiding {bab} U {b a^j b a} equals the exact
    number of classes (C union-find) for n <= 22, and both equal the formula (no common border)."""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c01_border_search import run_c, formula

def cls(w, u, v):
    seen, st = {w}, [w]
    while st:
        x = st.pop()
        for i in range(len(x) - 2):
            for a, b in ((u, v), (v, u)):
                if x[i:i + 3] == a:
                    y = x[:i] + b + x[i + 3:]
                    if y not in seen:
                        seen.add(y); st.append(y)
    return seen

sound = all(("abaa" + "b" * (j - 1)) in cls("b" + "a" * j + "ba", "aba", "bab") for j in range(2, 10))
N = 22
pats = ["bab"] + ["b" + "a" * j + "ba" for j in range(2, N)]
# count avoiders by DP over suffixes (patterns up to length N+1; use simple automaton on last <= N letters)
from collections import Counter
cur = Counter({"": 1}); avoid = [1]
maxlen = max(len(p) for p in pats)
for n in range(1, N + 1):
    nxt = Counter()
    for s, c in cur.items():
        for ch in "ab":
            t = s + ch
            if any(t.endswith(p) for p in pats):
                continue
            nxt[t[-(maxlen - 1):]] += c
    cur = nxt; avoid.append(sum(cur.values()))
brute = [1] + run_c([("010", "101")], 2, N)[("010", "101")]
pred = [1] + formula("aba", "bab", 2, N)
print("family rules sound for j=2..9:", sound)
print("avoiders == classes == formula for n<=%d:" % N, avoid == brute == pred)
