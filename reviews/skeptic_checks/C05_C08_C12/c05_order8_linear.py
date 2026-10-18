"""Order-8 affine models of laws 677 and 1313 over the elementary abelian group GF(2)^3 with arbitrary
3x3 matrix coefficients (x*y = Ax + By + c), and over Z_4 x Z_2 with endomorphism coefficients.
A model needs the homogeneous part to satisfy the law, so c = 0 can be assumed when searching (A, B):
  677 : B A + B^2 A B = I  and  A + B^2 A^2 + B^3 = 0
  1313: B A^2 B + B A B = I and  A + B A^3 + B^2 = 0
(derived in reviews/skeptic_C05_C08_C12.md, Appendix B).  -> out/c05_order8_linear.json"""
import itertools, json
from pathlib import Path
import numpy as np

mats = np.array([np.array(bits, dtype=np.int64).reshape(3, 3) for bits in itertools.product((0, 1), repeat=9)])
I = np.eye(3, dtype=np.int64)
def mm(X, Y):
    return np.einsum("...ij,...jk->...ik", X, Y) % 2
res = {}
A = mats[:, None]; B = mats[None, :]
A = np.broadcast_to(A, (512, 512, 3, 3)); B = np.broadcast_to(B, (512, 512, 3, 3))
BA = mm(B, A); BB = mm(B, B); AA = mm(A, A)
c677_1 = (BA + mm(mm(BB, A), B)) % 2
c677_2 = (A + mm(BB, AA) + mm(BB, B)) % 2
ok677 = np.all(c677_1 == I, axis=(2, 3)) & np.all(c677_2 == 0, axis=(2, 3))
c1313_1 = (mm(mm(B, AA), B) + mm(mm(B, A), B)) % 2
c1313_2 = (A + mm(B, mm(AA, A)) + BB) % 2
ok1313 = np.all(c1313_1 == I, axis=(2, 3)) & np.all(c1313_2 == 0, axis=(2, 3))
res["GF(2)^3 matrix pairs satisfying 677"] = int(ok677.sum())
res["GF(2)^3 matrix pairs satisfying 1313"] = int(ok1313.sum())
# brute-force cross-check of the derivation on random pairs: evaluate the law on all x, y
rng = np.random.default_rng(1)
def law_ok(Am, Bm, law):
    vecs = [np.array(v) for v in itertools.product((0, 1), repeat=3)]
    op = lambda u, v: (Am @ u + Bm @ v) % 2
    for x in vecs:
        for y in vecs:
            r = op(y, op(x, op(op(y, x), y))) if law == 677 else op(y, op(op(op(y, x), x), y))
            if not np.array_equal(r, x):
                return False
    return True
agree = 0
for _ in range(3000):
    i, j = rng.integers(512), rng.integers(512)
    agree += (law_ok(mats[i], mats[j], 677) == bool(ok677[i, j])) and (law_ok(mats[i], mats[j], 1313) == bool(ok1313[i, j]))
res["derivation_cross_check_random_pairs_agree"] = f"{agree}/3000"
# Z_4 x Z_2 with endomorphisms (u1, u2) -> (p u1 + 2 q u2, r u1 + s u2), and constants c
els = [(u1, u2) for u1 in range(4) for u2 in range(2)]
ends = [(p, q, r, s) for p in range(4) for q in range(2) for r in range(2) for s in range(2)]
def ap(E, u):
    p, q, r, s = E
    return ((p * u[0] + 2 * q * u[1]) % 4, (r * u[0] + s * u[1]) % 2)
def add(u, v):
    return ((u[0] + v[0]) % 4, (u[1] + v[1]) % 2)
cnt = {677: 0, 1313: 0}
for EA in ends:
    for EB in ends:
        for c in els:
            op = lambda u, v: add(add(ap(EA, u), ap(EB, v)), c)
            for law in (677, 1313):
                good = True
                for x in els:
                    for y in els:
                        r = op(y, op(x, op(op(y, x), y))) if law == 677 else op(y, op(op(op(y, x), x), y))
                        if r != x:
                            good = False
                            break
                    if not good:
                        break
                cnt[law] += good
res["Z4xZ2 affine models 677"] = cnt[677]
res["Z4xZ2 affine models 1313"] = cnt[1313]
(Path(__file__).resolve().parent / "out/c05_order8_linear.json").write_text(json.dumps(res, indent=1))
print(res)
