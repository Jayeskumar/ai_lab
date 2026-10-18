"""Re-verify explicit associativity failures found by c08_assoc with plain Python big integers
(own greedy expansion and circle product; nothing imported from the lab).  -> out/c08_verify_triples.json"""
import json
from pathlib import Path

def seq(coeffs, init, upto):
    G = list(init)
    while G[-1] <= upto:
        G.append(sum(c * G[-1 - i] for i, c in enumerate(coeffs)))
    return G

def greedy(n, G):
    d = {}
    for k in range(len(G) - 1, -1, -1):
        if G[k] <= n:
            d[k] = n // G[k]
            n -= d[k] * G[k]
    assert n == 0
    return d

def circ(a, b, s, coeffs, init):
    G = seq(coeffs, init, max(a, b))
    da, db = greedy(a, G), greedy(b, G)
    top = max(da) + max(db) + s + 2
    while len(G) <= top:
        G.append(sum(c * G[-1 - i] for i, c in enumerate(coeffs)))
    return sum(x * y * G[i + j + s] for i, x in da.items() for j, y in db.items())

CASES = [
    ("4-bonacci 1,2,4,8", (1, 1, 1, 1), (1, 2, 4, 8), 7, (384723, 160586, 707599)),
    ("G(k+1)=G(k)+G(k-2) 1,2,3", (1, 0, 1), (1, 2, 3), 10, (194040, 37982, 925743)),
    ("(3,3) 1,5", (3, 3), (1, 5), 10, (84247, 985522, 148455)),
    ("(2,2) 1,2", (2, 2), (1, 2), 4, (152649, 280060, 538452)),
    ("Fibonacci s=0", (1, 1), (1, 2), 0, (2, 4, 4)),
    ("Fibonacci s=1", (1, 1), (1, 2), 1, (1, 4, 4)),
]
out = {}
for name, c, g, s, (a, b, cc) in CASES:
    l = circ(circ(a, b, s, c, g), cc, s, c, g)
    r = circ(a, circ(b, cc, s, c, g), s, c, g)
    out[name] = {"s": s, "triple": [a, b, cc], "(ab)c": str(l), "a(bc)": str(r), "associative_on_triple": l == r}
    print(name, s, l == r)
Path(__file__).resolve().parent.joinpath("out", "c08_verify_triples.json").write_text(json.dumps(out, indent=1))
