"""EXP-C10-02: exact cost of Zeckendorf counting - the recurrence and its limit."""

from systems.counting_cost import changes, zeckendorf

META = {
    "id": "EXP-C10-02",
    "cycle": "C10",
    "title": "Zeckendorf counting costs exactly 2 digit changes per increment on average",
    "agent": "Formal Verifier",
    "question": "What is the exact total number of digit changes T_m when counting from 0 to G_m - 1 in the "
                "Zeckendorf system (G = 1, 2, 3, 5, 8, ...)?",
    "hypothesis": "T_(m+1) = T_m + T_(m-1) + ceil(m/2) + 1 (the step G_m - 1 -> G_m clears an alternating "
                  "string), hence T_m / G_m -> 2; refutes H-C10-0.",
    "assumptions": ["exact big-integer arithmetic for m <= 90; brute force for m <= 24"],
    "methodology": "Compute T_m by brute force (m <= 24) and by the recurrence (m <= 90); compare; examine "
                   "D_m = 2 G_m - T_m.",
    "falsification": "Recurrence and brute force disagree, or T_m/G_m does not approach 2.",
}


def run():
    G = [1, 2]
    while len(G) < 92:
        G.append(G[-1] + G[-2])
    # brute force: T[m] = total changes over increments 0 -> 1 -> ... -> G[m]-1
    brute = {}
    prev, tot, n = zeckendorf(0), 0, 0
    targets = {G[m] - 1: m for m in range(0, 25)}
    while n < G[24] - 1:
        n += 1
        cur = zeckendorf(n)
        tot += changes(prev, cur)
        prev = cur
        if n in targets:
            brute[targets[n]] = tot
    brute[0] = 0  # G[0]-1 = 0: no increments
    T = {0: 0, 1: brute[1]}
    for m in range(1, 90):
        T[m + 1] = T[m] + T[m - 1] + (m + 1) // 2 + 1
    agree = all(T[m] == brute[m] for m in range(0, 25))
    D = [2 * G[m] - T[m] for m in range(0, 30)]
    ratio = {m: float(T[m]) / G[m] for m in (10, 20, 40, 60, 89)}
    return {
        "recurrence_matches_brute_force_m<=24": agree,
        "T_first": [T[m] for m in range(0, 16)],
        "D_m = 2G_m - T_m (m=0..29)": D,
        "T_m/G_m": {str(k): round(v, 15) for k, v in ratio.items()},
        "summary": [f"recurrence agrees with brute force for m <= 24: {agree}",
                    f"T_m/G_m at m = 10, 20, 40, 60, 89: {[round(v, 12) for v in ratio.values()]}",
                    f"D_m = 2G_m - T_m: {D[:16]}"],
    }
