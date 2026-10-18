"""EXP-C18-01: the quasigroups of order 256 used as mixing primitives - construction checks and structure."""

import time

import numpy as np

from systems.mex import NIM_PRODUCT, table
from systems.quasigroup_hash import (N, d_transform, e_transform, is_gf2_affine, is_quasigroup, is_t_function,
                                     nim_inverse, nim_mul, nim_product_table, qg_hash_fixed, quasigroups)

META = {
    "id": "EXP-C18-01",
    "cycle": "C18",
    "title": "Seven quasigroups of order 256: Latin property, T-function and GF(2)-affinity tests, bijectivity of "
             "e-transformations, difference propagation, and the structural predictions of the written theorems",
    "agent": "Formal Verifier",
    "question": "Are the constructed tables quasigroups, which of them are T-functions or GF(2)-affine, and do the "
                "predictions of Theorems 1-5 (bijectivity, forward-only difference propagation, the T-function "
                "obstruction, linearity, anagram blindness) hold on random inputs?",
    "hypothesis": "Theorems 1-5 of proofs/paper/C18.md: e-transformations are bijections with the d-transformation as "
                  "inverse; a single-position input difference at i changes exactly the output positions >= i; for "
                  "T-function quasigroups output bits below the flipped bit position never change; for XOR every "
                  "output difference is independent of the key; the 1-pass x + c(y) hash is blind to permutations "
                  "of the message prefix.",
    "assumptions": ["random inputs: 2000 strings of 24 bytes (seeded)", "the random Latin square is built row by row "
                    "with randomly relabelled maximum matchings and is not uniformly distributed"],
    "methodology": "Direct checks on all 256 x 256 tables; e/d round trips; single-byte differences at random "
                   "positions; bit flips at every bit position r for the T-function quasigroups; output differences "
                   "for XOR across keys; 1-pass ARP hashes of keys and of permutations of their prefixes.",
    "falsification": "Any failed check (a non-Latin table, a failed round trip, a changed output position < i, a "
                     "changed output bit below position r for a T-function quasigroup, a key-dependent XOR "
                     "difference, a changed 1-pass ARP hash under prefix permutation).",
    "seed": 1801,
}


def run():
    rng = np.random.default_rng(META["seed"])
    t0 = time.perf_counter()
    Q = quasigroups()
    t_build = time.perf_counter() - t0
    props = {k: {"quasigroup": is_quasigroup(T), "t_function": is_t_function(T), "gf2_affine": is_gf2_affine(T)}
             for k, T in Q.items()}
    P64 = table(NIM_PRODUCT, 64)
    P = nim_product_table()
    inv = nim_inverse()
    nim = {"nim_mul_equals_C07_mex_table_on_64": bool(all(nim_mul(a, b) == P64[a, b]
                                                          for a in range(64) for b in range(64))),
           "row0_of_nim_product_is_zero": bool((P[0] == 0).all()),
           "nim_product_is_quasigroup_on_256": is_quasigroup(P),
           "nonzero_part_is_group_rows_are_permutations": bool(all(
               sorted(P[a, 1:].tolist()) == list(range(1, N)) for a in range(1, N))),
           "inverse_ok": bool(all(P[a, inv[a]] == 1 for a in range(1, N)))}
    X = rng.integers(0, N, (2000, 24), dtype=np.uint8)
    roundtrip = {k: bool(np.array_equal(d_transform(T, e_transform(T, X, 7), 7), X)) for k, T in Q.items()}
    # Theorem 2: single-position differences
    prop = {}
    for k, T in Q.items():
        bad = 0
        pos = rng.integers(0, 24, X.shape[0])
        Xd = X.copy()
        Xd[np.arange(X.shape[0]), pos] ^= rng.integers(1, N, X.shape[0], dtype=np.uint8)
        Y, Yd = e_transform(T, X, 9), e_transform(T, Xd, 9)
        diff = Y != Yd
        for r in range(X.shape[0]):
            i = pos[r]
            if diff[r, :i].any() or not diff[r, i:].all():
                bad += 1
        prop[k] = bad
    # Theorem 3: T-function obstruction for the full hash (2 passes + reverse)
    tfun = {}
    for k in ("AFF", "XOR", "ALP"):
        viol = 0
        base = qg_hash_fixed(Q[k], X[:500, :16], 2, True)
        for r in range(8):
            for byte in (0, 7, 15):
                Xf = X[:500, :16].copy()
                Xf[:, byte] ^= np.uint8(1 << r)
                d = base ^ qg_hash_fixed(Q[k], Xf, 2, True)
                low_mask = np.uint64(sum(((1 << r) - 1) << (8 * j) for j in range(8)))
                viol += int(((d & low_mask) != 0).sum())
        tfun[k] = viol
    # Theorem 4: XOR differences are key-independent
    Xf = X[:, :16].copy()
    Xf[:, 3] ^= np.uint8(0x21)
    dx = qg_hash_fixed(Q["XOR"], X[:, :16], 2, True) ^ qg_hash_fixed(Q["XOR"], Xf, 2, True)
    xor_distinct_differences = int(np.unique(dx).size)
    # Theorem 5: anagram blindness of the 1-pass ARP hash (message prefix = all but the last 8 message bytes)
    K = X[:, :16].copy()
    Kp = K.copy()
    for r in range(K.shape[0]):
        Kp[r, :9] = K[r, rng.permutation(9)]          # message length 17; positions 0..8 precede the tail
    changed_rows = int((Kp != K).any(axis=1).sum())
    same = int((qg_hash_fixed(Q["ARP"], K, 1, False) == qg_hash_fixed(Q["ARP"], Kp, 1, False)).sum())
    same_lsp2 = int((qg_hash_fixed(Q["LS"], K, 2, True) == qg_hash_fixed(Q["LS"], Kp, 2, True))[
        (Kp != K).any(axis=1)].sum())
    return {
        "properties": props,
        "nimbers": nim,
        "roundtrip_d_of_e": roundtrip,
        "single_difference_violations": prop,
        "t_function_low_bit_changes": tfun,
        "xor_distinct_output_differences_for_one_input_difference": xor_distinct_differences,
        "arp_1pass_prefix_permutation": {"keys": int(K.shape[0]), "keys_actually_changed": changed_rows,
                                         "hash_unchanged": same, "QG-LS p2+rev unchanged among changed": same_lsp2},
        "timings": {"build_quasigroups_s": round(t_build, 2)},
        "summary": [
            "quasigroups: " + ", ".join(f"{k} (T-fn {v['t_function']}, GF2-affine {v['gf2_affine']})"
                                        for k, v in props.items() if v["quasigroup"]),
            f"nim-product on [0,256): quasigroup {nim['nim_product_is_quasigroup_on_256']}, nonzero part a group "
            f"{nim['nonzero_part_is_group_rows_are_permutations']}; nim_mul = C07 table on [0,64): "
            f"{nim['nim_mul_equals_C07_mex_table_on_64']}",
            f"d(e(X)) = X for all: {all(roundtrip.values())}; single-difference violations: {sum(prop.values())}",
            f"T-function obstruction violations (AFF, XOR, ALP): {tfun}; XOR: {xor_distinct_differences} distinct "
            f"output difference(s) over 2000 keys",
            f"ARP 1-pass: {same}/{K.shape[0]} hashes unchanged under prefix permutation ({changed_rows} keys changed); "
            f"QG-LS p2+rev unchanged: {same_lsp2}",
        ],
    }
