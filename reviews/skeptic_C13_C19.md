# Skeptic review of cycles C13 and C19

**Reviewer:** Mathematical Skeptic (independent of the researchers who produced the claims)
**Date:** 2026-10-18 · **Scope:** CLM-C13-01 … CLM-C13-12 (anchored spectra II) and CLM-C19-01 … CLM-C19-14 (the longest Zeckendorf game), 26 claims. Priority: the five written proofs marked "awaiting independent skeptic review" (CLM-C13-01, CLM-C13-03 (iv), CLM-C13-06, CLM-C19-02, CLM-C19-03).

**Material read:**
- `research/cycles/C13_anchored_spectra/` and `research/cycles/C19_zeckendorf_game/` (README, `record.yaml`); all 26 claim records in `db/claims/` (they agree field by field with the two `record.yaml` files; checked by script).
- `proofs/paper/C13.md`, `proofs/paper/C19.md`; `proofs/lean/Infinity/C13_Spectra.lean`, `C19_Zeckendorf.lean`.
- All scripts in `experiments/C13/` (E01–E09) and `experiments/C19/` (E01–E04); `systems/anchored.py`, `systems/zeckendorf_game.py`, the parts of `systems/magma.py` they use (parser, SAT encoding), `lab/runner.py`, `lab/__main__.py`, `lab/oeis.py`.
- `results/EXP-C13-01 … 09.json`, `results/EXP-C19-01 … 04.json`; CLM-C06-10 (the conjecture C13 settles in part).
- Textbook chapters `textbook/src/08_anchored_spectra.md` (C13) and `textbook/src/16_zeckendorf_game.md` (C19).
- Literature, URLs actually read (full text unless stated):
  - A. Cusenza, A. Dunkelberg, K. Huffman, D. Ke, M. McClatchey, S. J. Miller, C. Mizgerd, V. Tiwari, J. Ye, X. Zheng, *Bounds on Zeckendorf games*: arXiv abstract page https://arxiv.org/abs/2009.09510 and full text https://arxiv.org/pdf/2009.09510 (v1, 20 Sep 2020); published version Fibonacci Quart. 60 (2022), no. 1, 57–71: abstract page https://www.mathstat.dal.ca/FQ/Abstracts/60-1/cusenza.pdf and full text https://www.mathstat.dal.ca/FQ/Papers/60-1/miller01152021.pdf (Theorems 1.2–1.4, Lemmas 2.1–2.3, Section 3 incl. eq. (3.16), Lemmas 3.2–3.3). (The author list differs from the one in my brief: the paper has McClatchey and Zheng; Kleber is a co-author of the companion paper arXiv:2009.03708 on multiplayer games, which I did not read.)
  - J. Cheigh et al., *Towards the Gaussianity of random Zeckendorf games*, https://arxiv.org/abs/2210.11038 and https://arxiv.org/pdf/2210.11038 (v1): read the introduction (the "remains open" sentence and their Theorems 1.4–1.5 quoting Cusenza et al.).
  - Search for spectra of equational laws (one web search; I read only the result snippets and the abstract page https://arxiv.org/abs/2512.07087 of *The Equational Theories Project*, Bolan et al. 2025). Not needed for any correctness verdict; mentioned once in (c) for the Historian.
  - Not read: Baird-Smith–Epstein–Flynt–Miller (arXiv:1809.04881), Li et al. (arXiv:2006.16457), Brown 1965, Taylor 1980, Schur 1912. Their content is not needed for the verdicts; the game rules I used are Definition 1.1 of Cusenza et al., which quotes Baird-Smith et al.

**Rules followed:**
- No existing file was edited. My code is in `reviews/skeptic_checks/C13_C19/`, raw outputs in `reviews/skeptic_checks/C13_C19/out/`:
  - C13: `c13_lib.py` (own terms, law enumeration, affine evaluation, SAT encoding, offset closure, exhaustive tables), `c13_atlas.py`, `c13_identifications.py`, `c13_exceptional.py`, `c13_single_poly.py`, `c13_three_square.py`, `c13_noncoprime.py`, `c13_count_infinite.py`, `c13_nbonacci.py`, `c13_closure.py`, `c13_models.py`.
  - C19: `c19_exact.c` (exhaustive dynamic programming over all positions), `c19_greedy.c` (strategy simulation), `c19_checks.py`, `c19_lazy_unique.py`.
- None of my scripts imports `systems/` or `lab/`, with one deliberate exception: stage 2 of `c13_closure.py` runs `systems.anchored.offset_closure_bound`, because CLM-C13-06 is a claim *about that procedure*; its output is compared with truth computed by my own code. pysat (CaDiCaL) is used only as a SAT solver with my own CNF encoding; sympy and numpy only as arithmetic libraries.
- Lab runs: `python -m lab run --dry` for EXP-C19-02, EXP-C13-07, EXP-C13-08 and EXP-C13-09 (no result written; `PYTHONDONTWRITEBYTECODE=1`). Experiments that call the OEIS module (EXP-C13-01, C13-03, C19-04) were not re-run, because an uncached query would write into `cache/oeis/`.
- Lean: `lake env lean` on the two files (read-only).
- Not run: `lab sync`, `lab lean`, `lab book`, `lab catalogue`, `lab verify`, `lab run` without `--dry`, any git command. Nothing committed.
- All heavy jobs ran under `nice -n 10`, one at a time. The longest single job was 11 min (28,890 SAT instances, `c13_closure.py stage3`); the exhaustive Zeckendorf search for n = 151 … 200 took 5 min 43 s. Every check reported below was actually run; the commands and outputs are in (b) and `out/`.

PLACEHOLDER_REST
