"""EXP-C05-02: what structure do restricted-spectrum identities force?  Spectra extended to n <= 10."""

import json
import time

from lab.paths import RESULTS
from pysat.card import CardEnc, EncType

from systems.magma import MagmaSAT, is_quasigroup, models_up_to_iso, parse, satisfies

META = {
    "id": "EXP-C05-02",
    "cycle": "C05",
    "title": "Restricted-spectrum identities: extended spectra (n = 7, 8) and forced structure",
    "agent": "Mathematical Explorer",
    "question": "For identities whose spectrum is restricted, which classical laws hold in all their small models, "
                "and how do the spectra continue beyond n = 7?",
    "hypothesis": "Restricted spectra come from identities that force quasigroups with extra laws (idempotence, "
                  "semisymmetry, total symmetry), i.e. classical combinatorial designs; their spectra continue "
                  "with the corresponding design spectra.",
    "assumptions": ["input: the restricted identities found by EXP-C05-01 (read from results/EXP-C05-01.json)",
                    "SAT conflict budget 5e5 per instance for n = 7, 8 (UNKNOWN recorded as such)",
                    "sound implied constraints (Lemma 1/4 of proofs/paper/C05.md): rows are permutations when "
                    "t = y*(...), columns are permutations when t = (...)*y; symmetry break 0*0 in {0,1}"],
    "methodology": "Extend each spectrum to n = 7, 8. Enumerate all models up to isomorphism for n <= 5 "
                   "(cap 5000 per size) and test a battery of classical laws on every model; group identities "
                   "with identical model sets for n <= 5 (candidate equivalent laws).",
    "falsification": "A restricted identity with a non-quasigroup model, or spectra that do not match any "
                     "design-type pattern.",
}

def extended_status(law, n):
    """SAT status at order n with the sound implied constraints of Lemma 1/4."""
    t = law[0]
    sat = MagmaSAT(n, [law])
    R = range(n)
    if t[0] == "y":      # t = y * (...): left translations are bijective
        for a in R:
            for c in R:
                sat.clauses += CardEnc.equals([sat.v[a, b, c] for b in R], 1, vpool=sat.pool,
                                              encoding=EncType.pairwise).clauses
    if t[1] == "y":      # t = (...) * y: right translations are bijective
        for b in R:
            for c in R:
                sat.clauses += CardEnc.equals([sat.v[a, b, c] for a in R], 1, vpool=sat.pool,
                                              encoding=EncType.pairwise).clauses
    sat.clauses.append([sat.v[0, 0, 0], sat.v[0, 0, 1]])
    status, T = sat.solve(conf_budget=500_000)
    if status == "SAT":
        assert satisfies(T, law)
    return status


BATTERY = {
    "idempotent  xx=x": (parse("xx"), "x"),
    "commutative xy=yx": (parse("xy"), parse("yx")),
    "semisymmetric x(yx)=y": (parse("x(yx)"), "y"),
    "left-symmetric x(xy)=y": (parse("x(xy)"), "y"),
    "right-symmetric (yx)x=y": (parse("(yx)x"), "y"),
    "Stein x(xy)=yx": (parse("x(xy)"), parse("yx")),
    "Schroeder (xy)(yx)=x": (parse("(xy)(yx)"), "x"),
    "unipotent xx=yy": (parse("xx"), parse("yy")),
    "associative": (parse("(xy)z"), parse("x(yz)")),
    "medial (xy)(zw)=(xz)(yw)": (parse("(xy)(zw)"), parse("(xz)(yw)")),
}


def run():
    e01 = json.load(open(RESULTS / "EXP-C05-01.json"))["results"]
    restricted = [r for r in e01["rows"] if r["spectrum_1_6"] not in ("111111", "100000")]
    only_one = [r for r in e01["rows"] if r["spectrum_1_6"] == "100000"]
    t0 = time.time()
    rows = []
    for r in restricted + only_one:
        law = (parse(r["identity"].split(" = ")[0]), "x")
        ext = {n: extended_status(law, n) for n in range(7, 9)}
        props = {name: True for name in BATTERY}
        qg = True
        reps_all = []
        iso_counts = {}
        for n in (2, 3, 4, 5):
            if r["spectrum_1_6"][n - 1] != "1":
                iso_counts[n] = 0
                continue
            total, iso, complete, reps = models_up_to_iso([law], n, limit=5000)
            iso_counts[n] = iso if complete else f">={iso} (cap)"
            reps_all += [T.tolist() for T in reps]
            for T in reps:
                qg &= is_quasigroup(T)
                for name, idn in BATTERY.items():
                    if props[name] and not satisfies(T, idn):
                        props[name] = False
        pattern = r["spectrum_1_6"] + "".join({"SAT": "1", "UNSAT": "0", "UNKNOWN": "?"}[ext[n]] for n in range(7, 9))
        rows.append({"identity": r["identity"], "spectrum_1_8": pattern, "iso_models_n2_5": iso_counts,
                     "all_models_quasigroups_n_le_5": qg,
                     "laws_holding_in_all_models_n_le_5": [k for k, v in props.items() if v],
                     "model_signature": sorted(map(str, reps_all))})
    # group identities with identical small-model sets
    groups = {}
    for row in rows:
        groups.setdefault(json.dumps(row["model_signature"]), []).append(row["identity"])
    for row in rows:
        row.pop("model_signature")
    by_pattern = {}
    for row in rows:
        by_pattern.setdefault(row["spectrum_1_8"], []).append(row["identity"])
    return {
        "rows": rows,
        "patterns_1_10": {p: v for p, v in sorted(by_pattern.items())},
        "n_model_equivalence_groups": len(groups),
        "model_equivalence_groups": [g for g in groups.values()],
        "timings": {"seconds": round(time.time() - t0, 1)},
        "summary": [
            f"{len(rows)} identities studied; spectrum patterns over n = 1..8: "
            f"{ {p: len(v) for p, v in sorted(by_pattern.items())} }",
            f"all small models quasigroups for {sum(r['all_models_quasigroups_n_le_5'] for r in rows)}/{len(rows)}",
            f"{len(groups)} groups of identities with identical model sets for n <= 5",
        ],
    }
