"""EXP-C11-05: encode/decode throughput of the reference Python implementations."""

import random
import time

from systems.codes import Golomb, PatternCode, baseline_codes

META = {
    "id": "EXP-C11-05",
    "cycle": "C11",
    "title": "Throughput of the reference implementations (Python, string-based)",
    "agent": "Application Researcher",
    "question": "What do pattern-terminated codes cost computationally relative to classical codes?",
    "hypothesis": "Enumerative pattern codes are markedly slower than gamma/delta in a naive implementation "
                  "(rank/unrank against a count table per bit).",
    "assumptions": ["1e5 values, log-uniform on [1, 2^20], seeded", "CPython string implementations; absolute speeds "
                    "are NOT representative of optimised bit-level code, only the relative ordering of these "
                    "implementations", "timings are machine-dependent and excluded from the result hash"],
    "methodology": "Encode the stream, decode it back, check equality; record total bits (deterministic) and "
                   "microseconds per value (timings).",
    "falsification": "n/a (measurement)",
    "seed": 5,
}


def run():
    rng = random.Random(META["seed"])
    vals = [max(1, int(2 ** (20 * rng.random()))) for _ in range(100_000)]
    codes = baseline_codes() + [Golomb(64)] + [PatternCode(p) for p in ("11", "111", "0111", "101")]
    bits, timings, ok = {}, {}, {}
    for c in codes:
        t0 = time.perf_counter()
        s = c.encode_seq(vals)
        t1 = time.perf_counter()
        back = c.decode_seq(s, len(vals))
        t2 = time.perf_counter()
        ok[c.name] = back == vals
        bits[c.name] = len(s)
        timings[c.name] = {"encode_us_per_value": round(1e6 * (t1 - t0) / len(vals), 3),
                           "decode_us_per_value": round(1e6 * (t2 - t1) / len(vals), 3)}
    return {
        "total_bits": bits,
        "roundtrip_ok": ok,
        "timings": timings,
        "summary": [f"all round trips ok: {all(ok.values())}",
                    "bits per value: " + ", ".join(f"{k} {v / len(vals):.2f}" for k, v in bits.items())],
    }
