"""EXP-C18-03: bucket distribution and collisions on four key sets."""

import numpy as np

from systems.quasigroup_hash import BASELINES, VARIANTS, chi2_z, collisions, hash_keys, quasigroups

META = {
    "id": "EXP-C18-03",
    "cycle": "C18",
    "title": "Hash-table behaviour: chi-square of bucket counts (1024 buckets by mask, 1021 by modulus) and collisions "
             "in 2^16 buckets on random, sequential, near-duplicate and word-like keys",
    "agent": "Application Researcher",
    "question": "Do quasigroup hashes distribute realistic key sets as evenly as standard hashes?",
    "hypothesis": "H-C18-3b (bold): the nimber inversion hash (QG-NIMINV p2+rev) has |chi-square z| <= 3 on every key "
                  "set and bucket-collision ratio within 2% of the uniform expectation, like FNV-1a-64. H-C18-6: the "
                  "1-pass x + c(y) hash (QG-ARP p1) fails on near-duplicate keys.",
    "assumptions": ["key sets (seeded): 65536 random byte strings of length 4-32; the decimal strings of 0..65535; "
                    "near-duplicates = 16 random 16-byte bases with all 4080 single-byte substitutions each (65296 "
                    "keys); 65536 distinct synthetic pronounceable words (no dictionary file is available offline)",
                    "z = (chi2 - df)/sqrt(2 df); |z| > 3 is flagged; collisions counted among the low 16 bits"],
    "methodology": "Hash every key set with every variant; compute z-scores for 1024 buckets (low 10 bits) and 1021 "
                   "buckets (h mod 1021); count keys landing in an occupied bucket among 2^16 (low 16 bits) and full "
                   "64-bit collisions.",
    "falsification": "H-C18-3b: |z| > 3 or a collision ratio outside [0.98, 1.02] for NIMINV. H-C18-6: QG-ARP p1 "
                     "within bounds on near-duplicates.",
    "seed": 1803,
}

CONS, VOW = "bcdfghjklmnprstvwz", "aeiou"


def key_sets(rng):
    lens = rng.integers(4, 33, 65536)
    rand = [rng.integers(0, 256, L, dtype=np.uint8).tobytes() for L in lens]
    seq = [str(i).encode() for i in range(65536)]
    near = []
    for _ in range(16):
        base = rng.integers(0, 256, 16, dtype=np.uint8)
        for pos in range(16):
            for v in range(256):
                if v != base[pos]:
                    k = base.copy()
                    k[pos] = v
                    near.append(k.tobytes())
    words = set()
    while len(words) < 65536:
        n = int(rng.integers(1, 5))
        w = ""
        for _ in range(n):
            w += CONS[rng.integers(len(CONS))] + VOW[rng.integers(len(VOW))]
            if rng.random() < 0.3:
                w += CONS[rng.integers(len(CONS))]
        words.add(w)
    return {"random": rand, "sequential": seq, "near_duplicates": near, "words": [w.encode() for w in sorted(words)]}


def run():
    rng = np.random.default_rng(META["seed"])
    ks = key_sets(rng)
    Q = quasigroups()
    res = {}
    for name in [v[0] for v in VARIANTS] + BASELINES:
        res[name] = {}
        for kname, keys in ks.items():
            h = hash_keys(name, keys, Q)
            res[name][kname] = {"z_mask1024": chi2_z(h, 1024, "mask"), "z_mod1021": chi2_z(h, 1021, "mod"),
                                **collisions(h)}
    flagged = {name: [k for k, v in r.items() if abs(v["z_mask1024"]) > 3 or abs(v["z_mod1021"]) > 3
                      or not 0.98 <= v["ratio"] <= 1.02] for name, r in res.items()}
    nim = flagged["QG-NIMINV p2+rev"]
    arp = res["QG-ARP p1"]["near_duplicates"]
    return {
        "key_set_sizes": {k: len(v) for k, v in ks.items()},
        "results": res,
        "flagged": flagged,
        "H-C18-3b_holds": not nim,
        "H-C18-6_holds": bool(abs(arp["z_mask1024"]) > 3 or abs(arp["z_mod1021"]) > 3 or not 0.98 <= arp["ratio"] <= 1.02),
        "summary": [f"{name}: flagged on {v if v else 'none'}" for name, v in flagged.items()] +
                   [f"QG-ARP p1 near-duplicates: {arp}"],
    }
