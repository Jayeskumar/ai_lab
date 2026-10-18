"""Cross-validate the skeptic's tools against the lab's tools on small cases (sanity of both).

* C union-find counter vs the lab's length_preserving_classes (binary k<=4, n<=9; ternary k<=3, n<=6)
* skeptic formula() vs the lab's predicted()
* an extra pure-Python BFS class count (third implementation) on a few relations
"""
import itertools
import os
import sys

sys.path.insert(0, "/home/user/ai_lab")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from c01_border_search import formula, run_c  # noqa: E402
from experiments.C01.E06_common_border_conjecture import predicted  # noqa: E402
from systems.rewriting import length_preserving_classes  # noqa: E402


def bfs_classes(u, v, alphabet, n):
    """Third method: explicit BFS over the undirected rewrite graph (both directions)."""
    ws = ["".join(t) for t in itertools.product(alphabet, repeat=n)]
    seen, classes = set(), 0
    k = len(u)
    for w in ws:
        if w in seen:
            continue
        classes += 1
        stack = [w]
        seen.add(w)
        while stack:
            x = stack.pop()
            for i in range(n - k + 1):
                f = x[i:i + k]
                for a, b in ((u, v), (v, u)):
                    if f == a:
                        y = x[:i] + b + x[i + k:]
                        if y not in seen:
                            seen.add(y)
                            stack.append(y)
    return classes


def main():
    mism_c, mism_f, checked = 0, 0, 0
    for alphabet, k, nmax in (("ab", 2, 9), ("ab", 3, 9), ("ab", 4, 9), ("abc", 2, 6), ("abc", 3, 6)):
        q = len(alphabet)
        digits = "0123456789"[:q]
        tr = str.maketrans(alphabet, digits)
        ws = ["".join(t) for t in itertools.product(alphabet, repeat=k)]
        pairs = list(itertools.combinations(ws, 2))
        cres = run_c([(u.translate(tr), v.translate(tr)) for u, v in pairs], q, nmax)
        for u, v in pairs:
            lab = [len(length_preserving_classes([(u, v)], alphabet, n)) for n in range(1, nmax + 1)]
            mine = cres[(u.translate(tr), v.translate(tr))]
            checked += 1
            if lab != mine:
                mism_c += 1
            if formula(u, v, q, nmax) != predicted(u, v, q, nmax)[0]:
                mism_f += 1
    print(f"C counter vs lab union-find: {checked} relations, mismatches {mism_c}")
    print(f"skeptic formula vs lab predicted(): mismatches {mism_f}")
    # third implementation on a few relations
    bad = 0
    tests = [("aba", "bab", "ab", 10), ("aaba", "abaa", "ab", 10), ("abab", "baba", "ab", 10),
             ("aab", "bba", "ab", 10), ("abca", "acba", "abc", 7)]
    for u, v, alphabet, nmax in tests:
        q = len(alphabet)
        tr = str.maketrans(alphabet, "0123456789"[:q])
        c = run_c([(u.translate(tr), v.translate(tr))], q, nmax)[(u.translate(tr), v.translate(tr))]
        b = [bfs_classes(u, v, alphabet, n) for n in range(1, nmax + 1)]
        bad += c != b
    print(f"C counter vs independent BFS on {len(tests)} relations: mismatches {bad}")


if __name__ == "__main__":
    main()
