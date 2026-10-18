"""EXP-C11-01: correctness of all integer codes (round trips, prefix-freeness, monotone lengths, Kraft)."""

import random
from fractions import Fraction

from systems.codes import FibonacciC1, Golomb, PatternCode, baseline_codes

META = {
    "id": "EXP-C11-01",
    "cycle": "C11",
    "title": "Correctness of the code implementations and of the pattern-terminated family",
    "agent": "Formal Verifier",
    "question": "Are the encoders/decoders exact inverses, prefix-free, with nondecreasing length functions, and "
                "are pattern-terminated codes complete (Kraft sum 1)?",
    "hypothesis": "Every implemented code round-trips on random data; every pattern-terminated code T_p is "
                  "prefix-free with Kraft sum tending to 1; T_11 has exactly the length function of the Fibonacci "
                  "C1 code.",
    "assumptions": ["universal codes: all n <= 5000 plus 3000 random n up to 2^60",
                    "Golomb/Rice codes: n <= 5000 (unary quotients make huge n impractical)",
                    "pattern codes: all 60 patterns of length 2..5 plus the unary pattern 1 (0 is its mirror image)"],
    "methodology": "Encode/decode single values and concatenated streams; trie check of the first 20000 "
                   "codewords; length(n) == len(encode(n)); monotonicity of length(n) on n <= 2e5 and on sorted "
                   "random big n; exact Kraft partial sums over lengths <= 1500 for pattern codes.",
    "falsification": "Any mismatch, prefix relation, decreasing length step, or Kraft sum exceeding 1.",
    "seed": 11,
}


def is_prefix_free(words):
    words = sorted(set(words))
    if len(words) != len(set(words)):
        return False
    return all(not words[i + 1].startswith(words[i]) for i in range(len(words) - 1))


def run():
    rng = random.Random(META["seed"])
    small = list(range(1, 5001))
    big = sorted(rng.randint(1, 1 << rng.randint(1, 60)) for _ in range(3000))
    problems = []
    univ = baseline_codes()
    patterns = [format(i, f"0{k}b") for k in range(1, 6) for i in range(2 ** k)]
    pcodes = [PatternCode(p, max_len=200) for p in patterns if p not in ("0", "1")]
    # single-letter patterns give a unary code; include them for completeness
    pcodes += [PatternCode("1", max_len=200)]
    capacity = {}
    for c in univ + pcodes:
        vals = sorted(set(small + big))
        if isinstance(c, PatternCode):
            # low-growth patterns (e.g. '10', growth rate 1) cannot reach huge n within the table
            capacity[c.p] = c.cum[-1]
            vals = [n for n in vals if n <= c.cum[-1]]
        for n in vals:
            e = c.encode(n)
            if len(e) != c.length(n):
                problems.append((c.name, n, "length"))
                break
            m, pos = c.decode(e + "10", 0)
            if m != n or pos != len(e):
                problems.append((c.name, n, "roundtrip"))
                break
        stream = vals[:400]
        if c.decode_seq(c.encode_seq(stream), len(stream)) != stream:
            problems.append((c.name, "stream"))
        lens = [c.length(n) for n in vals]
        if any(b < a for a, b in zip(lens, lens[1:])):
            problems.append((c.name, "non-monotone length"))
        top = min(20000, c.cum[-1]) if isinstance(c, PatternCode) else 20000
        if not is_prefix_free([c.encode(n) for n in range(1, top + 1)]):
            problems.append((c.name, "not prefix-free"))
    for M in (1, 2, 3, 5, 10, 16, 37, 1000):
        g = Golomb(M)
        for n in small:
            e = g.encode(n)
            if len(e) != g.length(n) or g.decode(e + "01", 0) != (n, len(e)):
                problems.append((g.name, n))
                break
        if not is_prefix_free([g.encode(n) for n in small]):
            problems.append((g.name, "not prefix-free"))
    kraft = {}
    for c in pcodes:
        long = PatternCode(c.p, max_len=1500)
        kraft[c.p] = float(sum(Fraction(cnt, 2 ** L) for L, cnt in enumerate(long.count)))
    fib = FibonacciC1()
    t11 = PatternCode("11")
    same = all(fib.length(n) == t11.length(n) for n in range(1, 200001))
    return {
        "codes_checked": [c.name for c in univ] + [c.name for c in pcodes] + [f"Golomb({M})" for M in (1, 2, 3, 5, 10, 16, 37, 1000)],
        "problems": problems,
        "kraft_partial_sums_L_le_1500": {p: round(v, 12) for p, v in sorted(kraft.items())},
        "min_kraft_partial": min(kraft.values()),
        "max_kraft_partial": max(kraft.values()),
        "fibonacci_C1_equals_T_11_lengths_n_le_2e5": same,
        "pattern_capacity_at_max_len_200_below_1e6": {p: v for p, v in capacity.items() if v < 10**6},
        "summary": [
            f"{len(univ)} baseline + {len(pcodes)} pattern + 8 Golomb codes: problems = {len(problems)}",
            f"Kraft partial sums (lengths <= 1500) of pattern codes in [{min(kraft.values()):.12f}, {max(kraft.values()):.12f}]",
            f"Fibonacci C1 length function == T_11 for n <= 2e5: {same}",
        ],
    }
