"""EXP-C18-05: the tail-information bound, and a wide-state cascade designed to avoid it."""

import time

import numpy as np

from experiments.C18.E03_distribution import key_sets
from systems.quasigroup_hash import (CASCADES, avalanche_ext, chi2_z, collisions, e_transform, hash_fixed_ext,
                                     hash_keys_ext, quasigroups)

META = {
    "id": "EXP-C18-05",
    "cycle": "C18",
    "title": "Tail-information bound of e-transformation hashes, and an 8-pass cascade with a 64-bit state",
    "agent": "Application Researcher",
    "question": "EXP-C18-03 showed massive collisions of the tail-output hashes on structured keys. Does the "
                "tail-information bound (Theorem 6) account for them exactly, and does a cascade whose output is the "
                "final state of 8 parallel passes behave like the good baselines?",
    "hypothesis": "H-C18-7: for the reverse-pass hash, keys sharing their first 7 bytes receive at most 256 distinct "
                  "hash values; for the p-pass forward hash, keys sharing the last 7 message bytes receive at most "
                  "256^p values (Theorem 6, checked on data). H-C18-8 (bold): the cascade QC (8 passes, final state "
                  "output, 8 zero bytes of finalisation) over the random Latin square, the group isotope and the "
                  "nimber inversion quasigroup has avalanche at the BLAKE2b noise floor, |z| <= 3 and collision ratio "
                  "within 2% on all four key sets, and no full 64-bit collisions. H-C18-9: the cascade over x + c(y) "
                  "(ARP) still fails bit independence.",
    "assumptions": ["same keys as EXP-C18-02 (avalanche, seed 1802) and EXP-C18-03 (key sets, seed 1803)",
                    "throughput (batch of 16384 keys of 64 bytes, median of 3, shared machine) is stored under "
                    "timings only"],
    "methodology": "(a) For 50 random 7-byte prefixes, hash 4096 keys with that prefix (random 9-byte suffixes) with "
                   "QG-LS p2+rev and count distinct values; for 50 random 7-byte suffixes do the same with the forward "
                   "1-pass hash (bound 256). (b) Avalanche, bit independence, chi-square and collisions for the four "
                   "cascades, exactly as in EXP-C18-02/03.",
    "falsification": "H-C18-7: more than 256 (resp. 256^p) distinct values. H-C18-8: any flag for QC-LS, QC-ISO or "
                     "QC-NIMINV. H-C18-9: QC-ARP with BIC max < 0.5.",
    "seed": 1805,
}


def run():
    rng = np.random.default_rng(META["seed"])
    Q = quasigroups()
    from systems.quasigroup_hash import qg_hash_fixed
    # (a) the tail-information bound on data
    rev_counts, fwd_counts = [], []
    for _ in range(50):
        pre = rng.integers(0, 256, 7, dtype=np.uint8)
        X = rng.integers(0, 256, (4096, 16), dtype=np.uint8)
        X[:, :7] = pre
        rev_counts.append(int(np.unique(qg_hash_fixed(Q["LS"], X, 2, True)).size))
        suf = rng.integers(0, 256, 6, dtype=np.uint8)       # key bytes 10..15; message byte 16 = length
        Y = rng.integers(0, 256, (4096, 16), dtype=np.uint8)
        Y[:, 10:] = suf
        fwd_counts.append(int(np.unique(qg_hash_fixed(Q["LS"], Y, 1, False)).size))
    # (b) the cascades
    Xa = np.random.default_rng(1802).integers(0, 256, (2000, 16), dtype=np.uint8)
    ks = key_sets(np.random.default_rng(1803))
    names = [c[0] for c in CASCADES] + ["MX64", "BLAKE2b-64"]
    aval = {name: avalanche_ext(name, Xa, Q) for name in names}
    dist = {}
    for name in names:
        dist[name] = {}
        for kname, keys in ks.items():
            h = hash_keys_ext(name, keys, Q)
            dist[name][kname] = {"z_mask1024": float(chi2_z(h, 1024, "mask")),
                                 "z_mod1021": float(chi2_z(h, 1021, "mod")), **collisions(h)}
    flagged = {name: [k for k, v in r.items() if abs(v["z_mask1024"]) > 3 or abs(v["z_mod1021"]) > 3
                      or not 0.98 <= v["ratio"] <= 1.02 or v["full_64bit_collisions"] > 0]
               for name, r in dist.items()}
    ref = aval["BLAKE2b-64"]
    good = ("QC-LS d8", "QC-ISO d8", "QC-NIMINV d8")
    h8 = all(not flagged[g] and abs(aval[g]["mean_bias"] - ref["mean_bias"]) <= 0.01
             and abs(aval[g]["max_bias"] - ref["max_bias"]) <= 0.01 for g in good)
    h9 = aval["QC-ARP d8"]["bic_max_abs_corr"] >= 0.5
    timings = {}
    Xt = rng.integers(0, 256, (16384, 64), dtype=np.uint8)
    for name in names:
        ts = []
        for _ in range(3):
            t0 = time.perf_counter()
            hash_fixed_ext(name, Xt, Q)
            ts.append(time.perf_counter() - t0)
        timings[name] = {"seconds": round(float(np.median(ts)), 4),
                         "MB_per_s": round(Xt.size / float(np.median(ts)) / 1e6, 2)}
    return {
        "tail_bound": {"reverse_pass_distinct_per_prefix": {"max": max(rev_counts), "min": min(rev_counts)},
                       "forward_1pass_distinct_per_suffix": {"max": max(fwd_counts), "min": min(fwd_counts)},
                       "H-C18-7_holds": max(rev_counts) <= 256 and max(fwd_counts) <= 256},
        "avalanche": aval,
        "distribution": dist,
        "flagged": flagged,
        "H-C18-8_holds": h8,
        "H-C18-9_holds": h9,
        "timings": timings,
        "summary": [f"tail bound: reverse-pass hash takes {min(rev_counts)}-{max(rev_counts)} distinct values on 4096 "
                    f"keys sharing a 7-byte prefix; forward 1-pass hash {min(fwd_counts)}-{max(fwd_counts)} on keys "
                    f"sharing the last 7 message bytes (bound 256)"] +
                   [f"{n}: mean bias {aval[n]['mean_bias']}, max bias {aval[n]['max_bias']}, BIC max "
                    f"{aval[n]['bic_max_abs_corr']}, flagged on {flagged[n] if flagged[n] else 'none'}" for n in names] +
                   [f"H-C18-8 {h8}; H-C18-9 {h9}"],
    }
