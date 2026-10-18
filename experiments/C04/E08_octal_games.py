"""EXP-C04-08: rewriting games with lhs a^k are octal games (Dawson's Kayles, Officers, ...)."""

from systems.derivations import derivation_graph, graph_values, octal_grundy

from experiments.C04.E07_rewriting_games import run_game_grundy

META = {
    "id": "EXP-C04-08",
    "cycle": "C04",
    "title": "Unary rewriting games = octal games: Dawson's Kayles (aa -> b), Officers (aa -> ab) and others",
    "agent": "Historian and Novelty Analyst",
    "question": "Which classical take-and-break games are the rewriting games of rules a^k -> u?",
    "hypothesis": "H-C04-7: on the word a^n, the game of aa -> b (also bb, bbb, bab) is Dawson's Kayles 0.07; "
                  "aa -> ab (also ba, abb, bba) is Officers 0.6; aaa -> b (bb, bbb, bab) is 0.007; aaa -> ab "
                  "(ba, abb, bba) is 0.06; aaa -> aba is 0.4. H-C04-6 (bold, from EXP-C04-07): Grundy values of "
                  "rewriting games in the family never exceed 3.",
    "assumptions": ["run decomposition (EXP-C04-07)", "Guy-Smith periodicity theorem for finite octal games"],
    "methodology": "(1) Grundy value of the single word a^n from its exact derivation graph (no decomposition), "
                   "n <= 20, compared with the octal recursion and with the generic run-game recursion. (2) Octal "
                   "Grundy values to n = 3000; smallest period p <= 300 with preperiod n0 holding over the whole "
                   "range, and the Guy-Smith window n0 <= n < 2 n0 + p + t checked explicitly.",
    "falsification": "Any n <= 20 where the word game, the run game and the octal recursion disagree; a Grundy "
                     "value >= 4 refutes H-C04-6.",
}

CASES = [
    ("aa", "b", "0.07", "Dawson's Kayles"), ("aa", "bb", "0.07", "Dawson's Kayles"),
    ("aa", "bab", "0.07", "Dawson's Kayles"), ("aa", "ab", "0.6", "Officers"),
    ("aa", "abb", "0.6", "Officers"), ("aa", "ba", "0.6", "Officers"),
    ("aaa", "b", "0.007", "octal 0.007"), ("aaa", "bab", "0.007", "octal 0.007"),
    ("aaa", "ab", "0.06", "octal 0.06"), ("aaa", "aba", "0.4", "octal 0.4"),
    ("aaa", "aab", None, "not octal (left heap >= 2)"),
]
NMAX = 3000


def period(G, max_p=300):
    N = len(G) - 1
    for p in range(1, max_p + 1):
        # smallest n0 such that G(n+p) = G(n) for all n0 <= n <= N - p
        n0 = None
        for n in range(N - p, -1, -1):
            if G[n + p] != G[n]:
                n0 = n + 1
                break
        else:
            n0 = 0
        if n0 is not None and N - p - n0 > 3 * p + 50:
            return p, n0
    return None


def run():
    rows = []
    for l, u, code, name in CASES:
        k = len(l)
        word_g = []
        for n in range(0, 21):
            succ = derivation_graph(["a" * n], (l, u), limit=3_000_000)
            word_g.append(graph_values(succ)["a" * n][2])
        run_g = run_game_grundy(k, u, NMAX)
        row = {"rule": [l, u], "name": name, "octal_code": code, "word_game_n0_20": word_g,
               "run_game_matches_word_game": run_g[:21] == word_g}
        if code:
            oct_g = octal_grundy(code, NMAX)
            row["octal_matches_run_game_n_le_3000"] = oct_g == run_g
        G = run_g
        per = period(G)
        row["max_grundy_n_le_3000"] = max(G)
        row["first_n_with_grundy_ge_4"] = next((n for n, g in enumerate(G) if g >= 4), None)
        if per:
            p, n0 = per
            window_end = 2 * n0 + p + k
            row["period"] = p
            row["preperiod_n0"] = n0
            row["guy_smith_window"] = [n0, window_end]
            row["guy_smith_window_verified"] = window_end + p <= NMAX and all(
                G[n + p] == G[n] for n in range(n0, window_end))
        else:
            row["period"] = None
        row["first_40"] = G[:40]
        rows.append(row)
    return {
        "rows": rows,
        "all_correspondences_hold": all(r["run_game_matches_word_game"] and r.get("octal_matches_run_game_n_le_3000", True)
                                        for r in rows),
        "summary": [
            f"word game = run game for n <= 20 and run game = octal recursion for n <= {NMAX}: "
            f"{all(r['run_game_matches_word_game'] and r.get('octal_matches_run_game_n_le_3000', True) for r in rows)}",
        ] + [f"{r['rule'][0]}->{r['rule'][1]} ({r['name']}): period {r['period']}"
             f"{' from n0=' + str(r.get('preperiod_n0')) if r['period'] else ' (none <= 300 up to n=3000)'}, "
             f"max G {r['max_grundy_n_le_3000']}, first G>=4 at n={r['first_n_with_grundy_ge_4']}" for r in rows],
    }
