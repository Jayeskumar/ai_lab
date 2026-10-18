"""EXP-C18-02: avalanche and bit independence of quasigroup hashes and baselines."""

import numpy as np

from systems.quasigroup_hash import BASELINES, VARIANTS, avalanche, quasigroups

META = {
    "id": "EXP-C18-02",
    "cycle": "C18",
    "title": "Strict avalanche and bit independence: 13 quasigroup hash variants against FNV-1a, MX64, BLAKE2b and "
             "CRC32",
    "agent": "Application Researcher",
    "question": "How close to an ideal 64-bit mixer are e-transformation hashes over the seven quasigroups, with "
                "1, 2 or 4 passes and with or without a reverse pass?",
    "hypothesis": "H-C18-1 (bold): QG-LS with 2 passes and a reverse pass has mean and maximal avalanche bias within "
                  "0.01 of BLAKE2b-64. H-C18-2: every structured quasigroup (AFF, XOR, ARP, ALP) is worse than the "
                  "random Latin square on maximal avalanche bias. H-C18-3a (bold): the nimber inversion quasigroup "
                  "(NIMINV, 2 passes + reverse) has avalanche at least as good as FNV-1a-64. H-C18-5 (from Theorem "
                  "2): every forward-only variant has maximal bias 0.5.",
    "assumptions": ["2000 random 16-byte keys (seeded); all 128 input bits flipped", "bias = |P(output bit flips) "
                    "- 1/2|; with 2000 keys the sampling standard deviation per cell is about 0.011, so BLAKE2b's "
                    "values estimate the noise floor", "CRC32 has 32 output bits"],
    "methodology": "For each hash and input bit, flip the bit in all keys and record which output bits change; "
                   "report mean flip rate, mean and maximal bias, cells with bias > 0.1, deterministic cells, and the "
                   "maximal/mean absolute correlation between output-bit changes (bit independence).",
    "falsification": "H-C18-1: a difference > 0.01 in mean or maximal bias. H-C18-2: a structured quasigroup with "
                     "maximal bias <= that of QG-LS p2+rev. H-C18-3a: NIMINV mean bias above FNV-1a's. H-C18-5: a "
                     "forward-only variant with maximal bias < 0.5.",
    "seed": 1802,
}


def run():
    rng = np.random.default_rng(META["seed"])
    X = rng.integers(0, 256, (2000, 16), dtype=np.uint8)
    Q = quasigroups()
    res = {name: avalanche(name, X, Q) for name in [v[0] for v in VARIANTS] + BASELINES}
    ref = res["BLAKE2b-64"]
    ls = res["QG-LS p2+rev"]
    h1 = abs(ls["mean_bias"] - ref["mean_bias"]) <= 0.01 and abs(ls["max_bias"] - ref["max_bias"]) <= 0.01
    structured = [v[0] for v in VARIANTS if v[1] in ("AFF", "XOR", "ARP", "ALP")]
    h2 = all(res[s]["max_bias"] > ls["max_bias"] for s in structured)
    h3a = res["QG-NIMINV p2+rev"]["mean_bias"] <= res["FNV-1a-64"]["mean_bias"]
    fwd = [v[0] for v in VARIANTS if not v[3]]
    h5 = all(res[f]["max_bias"] == 0.5 for f in fwd)
    order = sorted(res, key=lambda k: (res[k]["max_bias"], res[k]["mean_bias"]))
    return {
        "results": res,
        "ranking_by_max_bias": order,
        "H-C18-1_holds": h1, "H-C18-2_holds": h2, "H-C18-3a_holds": h3a, "H-C18-5_holds": h5,
        "summary": [f"{k}: mean bias {res[k]['mean_bias']}, max bias {res[k]['max_bias']}, cells>0.1 "
                    f"{res[k]['cells_bias_gt_0.1']}/{res[k]['cells']}, BIC max {res[k]['bic_max_abs_corr']}"
                    for k in order] +
                   [f"H-C18-1 {h1}; H-C18-2 {h2}; H-C18-3a {h3a}; H-C18-5 {h5}"],
    }
