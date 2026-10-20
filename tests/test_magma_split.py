"""Tests for the certified case split of systems/magma_split.py (proofs/paper/C05.md, Lemmas 8 and 9)."""

import numpy as np

from systems.magma import parse, satisfies
from systems.magma_split import admits, canonical_form, canonical_permutation, cases, decide, partitions

LAW_1313 = "y(((yx)x)y)"
LAW_677 = "y(x((yx)y))"


def _linear_models(law, q):
    """All tables x*y = a x + b y (mod q, q prime) satisfying x = law."""
    identity = (parse(law), "x")
    r = np.arange(q)
    out = []
    for a in range(q):
        for b in range(q):
            T = (a * r[:, None] + b * r[None, :]) % q
            if satisfies(T, identity):
                out.append(T)
    return out


def test_number_of_cases_is_sum_of_partition_numbers():
    p = [sum(1 for _ in partitions(k)) for k in range(12)]
    for n, expected in [(8, 45), (10, 97), (12, 195)]:
        assert len(cases(n)) == expected == sum(p[:n])


def test_canonical_form_is_invariant_under_relabelling():
    rng = np.random.default_rng(0)
    for law, q in [(LAW_1313, 7), (LAW_677, 7), (LAW_1313, 5)]:
        for T in _linear_models(law, q):
            case, lam, ell, C = canonical_form(T)
            perm = canonical_permutation(lam, ell)
            assert C[0] == [perm[b] for b in range(q)]
            assert satisfies(np.array(C), (parse(law), "x"))
            p = rng.permutation(q)
            inv = np.argsort(p)
            R = [[int(p[T[inv[x], inv[y]]]) for y in range(q)] for x in range(q)]
            assert canonical_form(R)[:3] == (case, lam, ell)


def test_known_models_are_admitted_and_broken_tables_are_not():
    pairs = [(law, T) for law in (LAW_1313, LAW_677) for T in _linear_models(law, 7)]
    assert pairs
    for law, T in pairs:
        res = admits(law, T)
        assert res["admitted"] and res["satisfies_law"]
        B = T.copy()
        B[1, [0, 1]] = B[1, [1, 0]]                      # still a Latin row, no longer a model
        bad = admits(law, B)
        assert not bad["satisfies_law"] and not bad["admitted"]


def test_decide_small_orders_of_law_1313():
    found, _, _ = decide(LAW_1313, 5, 100_000)
    assert found["verdict"] == "model found"
    gap, records, _ = decide(LAW_1313, 6, 100_000)        # no checker: UNSAT without proof checking
    assert gap["verdict"] == "no model (not all proofs checked)" and len(records) == len(cases(6))
