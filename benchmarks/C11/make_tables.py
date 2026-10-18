"""Export the C11 benchmark tables (CSV) from the recorded experiment results.

Run from the repository root:  python benchmarks/C11/make_tables.py
Inputs: results/EXP-C11-03.json (synthetic sources), results/EXP-C11-04.json (data),
results/EXP-C11-05.json (bits per value and machine-dependent timings), results/EXP-C11-09.json (Fraenkel-Klein C3
comparison).  Nothing is recomputed.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def load(eid):
    path = ROOT / "results" / f"{eid}.json"
    return json.loads(path.read_text(encoding="utf-8")), hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, header, rows):
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def main():
    sources = []
    syn, h3 = load("EXP-C11-03")
    rows = []
    for src, v in syn["results"]["table"].items():
        for code, red in sorted(v["redundancy"].items()):
            rows.append([src, v["entropy"], code, red])
    write("synthetic_redundancy.csv", ["source", "entropy_bits", "code", "redundancy_bits"], rows)
    sources.append(("EXP-C11-03", h3, "synthetic_redundancy.csv"))

    dat, h4 = load("EXP-C11-04")
    rows = []
    for src, v in dat["results"]["table"].items():
        for code, bpv in sorted(v["bits_per_value"].items()):
            rows.append([src, v["count"], v["entropy_bits"], code, bpv])
    write("data_bits_per_value.csv", ["data", "count", "H0_bits", "code", "bits_per_value"], rows)
    sources.append(("EXP-C11-04", h4, "data_bits_per_value.csv"))

    spd, h5 = load("EXP-C11-05")
    res = spd["results"]
    rows = []
    for code in sorted(res["total_bits"]):
        t = res["timings"].get(code, {})
        rows.append([code, res["total_bits"][code], res["roundtrip_ok"][code],
                     t.get("encode_us_per_value"), t.get("decode_us_per_value")])
    write("speed_cpython.csv", ["code", "total_bits_1e5_values", "roundtrip_ok", "encode_us_per_value",
                                "decode_us_per_value"], rows)
    sources.append(("EXP-C11-05", h5, "speed_cpython.csv"))

    c3, h9 = load("EXP-C11-09")
    rows = []
    for kind, key in (("synthetic redundancy", "synthetic_redundancy"), ("data bits per value", "data_bits_per_value")):
        for src, row in c3["results"][key].items():
            for code, val in sorted(row.items()):
                rows.append([kind, src, code, val])
    write("c3_comparison.csv", ["measure", "source", "code", "bits"], rows)
    sources.append(("EXP-C11-09", h9, "c3_comparison.csv"))

    with open(OUT / "PROVENANCE.txt", "w", encoding="utf-8") as f:
        f.write("C11 benchmark tables, exported verbatim by make_tables.py from recorded runs.\n")
        f.write("Timings (speed_cpython.csv) are machine-dependent and outside the result hash.\n")
        for eid, h, name in sources:
            f.write(f"{name}: results/{eid}.json (file sha256 {h})\n")
    print("wrote", ", ".join(n for _, _, n in sources))


if __name__ == "__main__":
    main()
