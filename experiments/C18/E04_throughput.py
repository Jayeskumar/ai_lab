"""EXP-C18-04: throughput of quasigroup hashes and baselines (indicative; shared machine)."""

import time

import numpy as np

from systems.quasigroup_hash import BASELINES, VARIANTS, hash_fixed, quasigroups

META = {
    "id": "EXP-C18-04",
    "cycle": "C18",
    "title": "Throughput in bytes per second for batches of equal-length keys",
    "agent": "Application Researcher",
    "question": "What does the mixing quality of quasigroup hashes cost in speed, compared with the baselines in "
                "comparable implementations?",
    "hypothesis": "H-C18-4: every quasigroup variant with a reverse pass is slower than FNV-1a-64 when both are "
                  "implemented in the same numpy batch style.",
    "assumptions": ["batches of 16384 keys of 8 and of 64 bytes (seeded)", "QG, FNV-1a and MX64 are numpy-vectorised "
                    "over keys (Python loop over byte positions); BLAKE2b and CRC32 are C library calls, one per key "
                    "(per-call overhead included)", "median of 3 runs; the machine is shared with other jobs, so "
                    "absolute numbers are indicative only; checksums of the outputs make the result deterministic"],
    "methodology": "Time hash_fixed on each batch; report MB/s; record an XOR checksum of all outputs.",
    "falsification": "H-C18-4: a reverse-pass quasigroup variant at least as fast as FNV-1a-64 on both batches.",
    "seed": 1804,
}


def run():
    rng = np.random.default_rng(META["seed"])
    Q = quasigroups()
    batches = {L: rng.integers(0, 256, (16384, L), dtype=np.uint8) for L in (8, 64)}
    checks, timings, mbps = {}, {}, {}
    for name in [v[0] for v in VARIANTS] + BASELINES:
        for L, X in batches.items():
            ts = []
            for _ in range(3):
                t0 = time.perf_counter()
                h = hash_fixed(name, X, Q)
                ts.append(time.perf_counter() - t0)
            t = float(np.median(ts))
            checks[f"{name}/{L}"] = hex(int(np.bitwise_xor.reduce(h)))
            timings[f"{name}/{L}"] = round(t, 4)
            mbps[f"{name}/{L}"] = round(X.size / t / 1e6, 2)
    fnv = {L: mbps[f"FNV-1a-64/{L}"] for L in batches}
    rev = [v[0] for v in VARIANTS if v[3]]
    h4 = all(mbps[f"{r}/{L}"] < fnv[L] for r in rev for L in batches)
    return {
        "checksums": checks,
        "timings": {"seconds": timings, "MB_per_s": mbps, "H-C18-4_holds_on_this_run": h4},
        "summary": [f"checksums recorded for {len(checks)} (hash, length) pairs; throughput (MB/s, indicative) is "
                    f"stored under timings"],
    }
