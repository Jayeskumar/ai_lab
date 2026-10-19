"""EXP-C17-03: the anchor instance of left-distributivity forces at most one table, for every N.

Take x*0 = x + 1 (mod N) and x*(y+1) = (x*y)*(x+1) for y = 0..N-2. Row N-1 is forced to (N-1)*y = y, and for
x < N-1 (downward) every entry x*(y+1) = v*(x+1), v = x*y > x, refers to an already determined row (or to row
N-1), so the whole table is forced (argument of the Skeptic's review of C17, reviews/skeptic_C07_C17_C20.md, A.5;
proofs/paper/C17.md). The forced table is a model of the anchor instance iff the remaining wrap-around instance
x + 1 = (x*(N-1))*(x+1) holds. This experiment builds the forced table for every N <= 4096, records where the
wrap-around holds, and checks left-distributivity and equality with the Laver table at the powers of 2 <= 512.
"""

import numpy as np

from systems.laver import laver_table

META = {
    "id": "EXP-C17-03",
    "cycle": "C17",
    "title": "Forced anchored tables of the left-distributive anchor instance, N <= 4096",
    "agent": "Mathematical Explorer",
    "question": "For which N does the anchor instance of left-distributivity have a model, and is it the Laver "
                "table?",
    "hypothesis": "The instance has a model exactly when N is a power of 2, and then it is the Laver table A_n "
                  "(CLM-C17-05, previously checked by SAT for N <= 10).",
    "assumptions": ["the forced-table construction of proofs/paper/C17.md (uniqueness)", "N = 1..4096",
                    "left-distributivity checked exhaustively (N^3 triples) for the powers of 2 up to 512"],
    "methodology": "Build the forced table row by row from N-1 down to 0; test the wrap-around instance; for powers "
                   "of 2 compare with systems.laver.laver_table and test x*(y*z) = (x*y)*(x*z) on all triples.",
    "falsification": "A non-power of 2 with a model, a power of 2 without one, or a forced table at a power of 2 "
                     "that differs from the Laver table or is not left-distributive.",
}


def forced_table(N: int):
    """The unique candidate table (as a list of rows), or None if some entry is not determined (cannot happen)."""
    T = [None] * N
    T[N - 1] = list(range(N))
    for x in range(N - 2, -1, -1):
        row = [0] * N
        row[0] = x + 1
        for y in range(N - 1):
            v = row[y]
            if not v > x:
                return None
            row[y + 1] = T[v][x + 1]
        T[x] = row
    return T


def run():
    holds, stuck = [], []
    powers = {1 << k for k in range(13)}
    laver_ok = {}
    for N in range(1, 4097):
        T = forced_table(N)
        if T is None:
            stuck.append(N)
            continue
        wrap = all((x + 1) % N == T[T[x][N - 1]][(x + 1) % N] for x in range(N))
        if wrap:
            holds.append(N)
        if N in powers and N <= 512:
            A = np.array(T, dtype=np.int64)
            L = laver_table(N.bit_length() - 1)
            same = bool(np.array_equal(A, np.asarray(L))) if L is not None else None
            ld = all(np.array_equal(A[x][A], A[A[x][:, None], A[x][None, :]]) for x in range(N))  # x*(y*z) = (x*y)*(x*z)
            laver_ok[str(N)] = {"equals_laver_table": same, "left_distributive": ld}
    non_powers = [N for N in holds if N not in powers]
    missing_powers = sorted(p for p in powers if p <= 4096 and p not in holds)
    return {
        "wrap_around_holds_for": holds,
        "non_powers_of_2_with_model": non_powers,
        "powers_of_2_without_model": missing_powers,
        "undetermined_entries": stuck,
        "powers_of_2_checked": laver_ok,
        "summary": [
            f"N = 1..4096: the forced table exists for every N (undetermined entries: {len(stuck)}); the wrap-around "
            f"instance holds exactly for N in {holds}",
            f"non-powers of 2 with a model: {len(non_powers)}; powers of 2 without a model: {missing_powers}",
            "powers of 2 <= 512: forced table = Laver table and left-distributive: " +
            ", ".join(f"{k}: {v['equals_laver_table'] and v['left_distributive']}" for k, v in laver_ok.items()),
        ],
    }
