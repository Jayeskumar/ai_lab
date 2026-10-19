"""EXP-C20-01: the last open termination cases of C04 - aab -> ababa and aab -> babaa (and their symmetric images)."""

import itertools

META = {
    "id": "EXP-C20-01",
    "cycle": "C20",
    "title": "Termination and exact derivational complexity of aab -> ababa and aab -> babaa",
    "agent": "Formal Verifier",
    "question": "Do the two one-rule systems left open in C04 terminate, and what is their derivational complexity?",
    "hypothesis": "H-C20-1 (from the run-encoding analysis, proofs/paper/C20.md): both terminate; "
                  "D(n) = 2^(n-2) - 1 for aab -> ababa (n >= 2) and D(n) = max_b b(2^floor((n-b)/2) - 1) for "
                  "aab -> babaa; for aab -> babaa every word has D(w) = sum_k d_k (2^floor(x_k/2) - 1) "
                  "(runs x_k of a's, d_k = b's to the right of run k when its journeys start).",
    "assumptions": ["all words over {a, b} of length <= 12 (formulas) and <= 8 (exhaustive maximal derivations)",
                    "the 8 rules of the two symmetry classes (reversal, letter exchange) are checked separately"],
    "methodology": "Simulate the rightmost and the leftmost strategy on every word; compare with the exact maximal "
                   "derivation length from the full derivation DAG (n <= 8); compare D(w) with the per-word formula "
                   "for aab -> babaa and D(n) with both closed forms.",
    "falsification": "A word whose strategies give different lengths (would contradict random descent), a word whose "
                     "derivation does not end within 10^6 steps, or any mismatch with the formulas.",
}

RULES = [("aab", "ababa"), ("aab", "babaa")]


def images(l, r):
    swap = str.maketrans("ab", "ba")
    out = {(l, r), (l[::-1], r[::-1]), (l.translate(swap), r.translate(swap)),
           (l[::-1].translate(swap), r[::-1].translate(swap))}
    return sorted(out)


def run_strategy(w, l, r, rightmost=True, cap=10 ** 6):
    s = 0
    while True:
        i = w.rfind(l) if rightmost else w.find(l)
        if i < 0:
            return s
        w = w[:i] + r + w[i + len(l):]
        s += 1
        if s > cap:
            return None


def exhaustive_max(w, l, r, limit=300_000):
    seen, stack = {w}, [w]
    while stack:
        x = stack.pop()
        i = x.find(l)
        while i >= 0:
            y = x[:i] + r + x[i + len(l):]
            if y not in seen:
                if len(seen) > limit:
                    return None
                seen.add(y)
                stack.append(y)
            i = x.find(l, i + 1)
    memo = {}
    for x in sorted(seen, key=len, reverse=True):     # every step makes the word longer
        best, i = 0, x.find(l)
        while i >= 0:
            best = max(best, 1 + memo[x[:i] + r + x[i + len(l):]])
            i = x.find(l, i + 1)
        memo[x] = best
    return memo[w]


def formula_babaa(w):
    """D(w) for aab -> babaa: runs x_0 b x_1 b ... b x_m; right to left, d_k = (m - k) + steps so far."""
    xs = [len(t) for t in w.split("b")]
    m = len(xs) - 1
    steps = 0
    for k in range(m - 1, -1, -1):
        d = (m - k) + steps
        steps += d * (2 ** (xs[k] // 2) - 1)
    return steps


def run():
    out = {}
    for base in RULES:
        for (l, r) in images(*base):
            mism_strat, mism_exh, skipped, nonterm, D = 0, 0, 0, 0, {}
            for n in range(1, 13):
                best = 0
                for t in itertools.product("ab", repeat=n):
                    w = "".join(t)
                    a = run_strategy(w, l, r, True)
                    b = run_strategy(w, l, r, False)
                    if a is None or b is None:
                        nonterm += 1
                        continue
                    mism_strat += a != b
                    if n <= 8:
                        e = exhaustive_max(w, l, r)
                        skipped += e is None          # reachable set above the limit: not compared, but counted
                        mism_exh += (e is not None and e != a)
                    best = max(best, a)
                D[n] = best
            out[f"{l} -> {r}"] = {"base": f"{base[0]} -> {base[1]}", "D": D, "strategy_mismatches": mism_strat,
                                  "exhaustive_mismatches": mism_exh, "exhaustive_skipped": skipped,
                                  "not_terminated_within_cap": nonterm}
    # formulas, on the base rules
    fa = {n: 2 ** (n - 2) - 1 for n in range(2, 13)}
    fb = {n: max(b * (2 ** ((n - b) // 2) - 1) for b in range(1, n + 1)) for n in range(1, 13)}
    word_mism = 0
    for n in range(1, 13):
        for t in itertools.product("ab", repeat=n):
            w = "".join(t)
            word_mism += formula_babaa(w) != run_strategy(w, "aab", "babaa")
    A = out["aab -> ababa"]["D"]
    B = out["aab -> babaa"]["D"]
    ok_a = all(A[n] == fa[n] for n in fa)
    ok_b = all(B[n] == fb[n] for n in fb)
    return {
        "rules": out,
        "closed_form_ababa_ok": ok_a,
        "closed_form_babaa_ok": ok_b,
        "per_word_formula_babaa_mismatches": word_mism,
        "summary": [
            f"8 rules (2 classes): words of length <= 12 - non-terminating within 10^6 steps: "
            f"{sum(v['not_terminated_within_cap'] for v in out.values())}; rightmost vs leftmost mismatches: "
            f"{sum(v['strategy_mismatches'] for v in out.values())}; vs exhaustive maximum (n <= 8): "
            f"{sum(v['exhaustive_mismatches'] for v in out.values())} (words skipped for a reachable set above "
            f"300000: {sum(v['exhaustive_skipped'] for v in out.values())})",
            f"aab -> ababa D(n), n = 1..12: {[A[n] for n in range(1, 13)]}; = 2^(n-2) - 1: {ok_a}",
            f"aab -> babaa D(n): {[B[n] for n in range(1, 13)]}; = max_b b(2^floor((n-b)/2) - 1): {ok_b}; "
            f"per-word formula mismatches: {word_mism}",
        ],
    }
