"""EXP-C11-03: exact expected code lengths versus entropy on synthetic distributions."""

import itertools

from systems.code_bench import Geometric, LogUniform, Uniform, Zipf, expected_length, tuned_golomb
from systems.codes import ExpGolomb, PatternCode, baseline_codes, growth_rate

META = {
    "id": "EXP-C11-03",
    "cycle": "C11",
    "title": "Benchmark: expected length minus entropy on Zipf, geometric, uniform and log-uniform sources",
    "agent": "Application Researcher",
    "question": "Where do pattern-terminated codes beat classical universal codes, and how do they compare with a "
                "Golomb-Rice code tuned to the source?",
    "hypothesis": "H-C11-4: some fixed pattern code (not 11) beats every classical universal baseline (gamma, delta, "
                  "omega, Levenshtein, Fibonacci, LEB128, fixed Exp-Golomb) on at least one realistic source; tuned "
                  "Golomb-Rice wins on geometric sources.",
    "assumptions": ["exact expectations from length breakpoints and cdfs (no sampling)", "Zipf truncated at 1e6; "
                    "geometric tails below 1e-18 ignored", "oracle pattern = best pattern of length <= 8 (up to "
                    "complement) chosen per source, i.e. a tuned code like Golomb-Rice"],
    "methodology": "Expected codeword length E and redundancy E - H for 12 sources and all codes; winners among "
                   "(a) fixed universal codes and (b) all codes including tuned ones.",
    "falsification": "No fixed pattern code (other than 11) is ever the best universal code.",
}

FIXED_PATTERNS = ["111", "1111", "11111", "011", "0111", "00111", "101", "0101", "1011"]


def sources():
    return [Zipf(1.1), Zipf(1.5), Zipf(2.0), Zipf(3.0), Geometric(0.5), Geometric(0.1), Geometric(0.01),
            Geometric(0.001), Uniform(8), Uniform(16), Uniform(32), LogUniform(10 ** 6)]


def run():
    universal = baseline_codes() + [PatternCode(p) for p in FIXED_PATTERNS]
    oracle_pats = sorted({p for k in range(2, 9) for p in ("".join(b) for b in itertools.product("01", repeat=k))
                          if p[0] == "1" and growth_rate(p) > 1.2})
    oracle_codes = [PatternCode(p) for p in oracle_pats]
    table = {}
    for d in sources():
        row = {c.name: round(expected_length(c, d) - d.entropy, 4) for c in universal}
        tg = tuned_golomb(d)
        best_eg = min((expected_length(ExpGolomb(k), d), k) for k in range(0, 31))
        best_pat = min((expected_length(c, d), c.p) for c in oracle_codes)
        row[f"tuned Golomb(M={tg['golomb_M']})"] = round(tg["golomb_E"] - d.entropy, 4)
        row[f"tuned Rice(k={tg['rice_k']})"] = round(tg["rice_E"] - d.entropy, 4)
        row[f"tuned Exp-Golomb(k={best_eg[1]})"] = round(best_eg[0] - d.entropy, 4)
        row[f"oracle pattern T_{best_pat[1]}"] = round(best_pat[0] - d.entropy, 4)
        fixed = {k: v for k, v in row.items() if not k.startswith(("tuned", "oracle"))}
        best_fixed = min(fixed, key=fixed.get)
        classical = {k: v for k, v in fixed.items() if not k.startswith("T_")}
        best_classical = min(classical, key=classical.get)
        best_all = min(row, key=row.get)
        table[d.name] = {"entropy": round(d.entropy, 4), "redundancy": row,
                         "best_fixed_universal": [best_fixed, row[best_fixed]],
                         "best_classical_universal": [best_classical, row[best_classical]],
                         "best_overall": [best_all, row[best_all]]}
    pattern_wins = [s for s, v in table.items() if v["best_fixed_universal"][0].startswith("T_")
                    and v["best_fixed_universal"][0] != "T_11"]
    return {
        "table": table,
        "sources_where_a_new_pattern_code_is_best_fixed_universal": pattern_wins,
        "summary": [f"{s}: H={v['entropy']}; best classical {v['best_classical_universal']}; best fixed "
                    f"{v['best_fixed_universal']}; best overall {v['best_overall']}" for s, v in table.items()],
    }
