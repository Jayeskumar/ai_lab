# Skeptic review of cycles C03, C04 and C06

**Reviewer:** Mathematical Skeptic (independent of the researchers who produced the claims)
**Date:** 2026-10-18 · **Scope:** CLM-C03-01 … CLM-C03-11, CLM-C04-01 … CLM-C04-16, CLM-C06-01 … CLM-C06-12 (39 claims).

**Material read:**
- The three cycle READMEs and `record.yaml` files; all 39 claim records in `db/claims/`.
- `proofs/paper/C03.md`, `C04.md`, `C06.md`; `proofs/lean/Infinity/C03_Termination.lean`, `C04_Derivations.lean`, `C06_Laver.lean`.
- All scripts in `experiments/C03`, `experiments/C04`, `experiments/C06`; `systems/srs_termination.py`, `derivations.py`, `magma.py`, `laver.py`, the parts of `systems/rewriting.py` they use, and `lab/runner.py`.
- `results/EXP-C03-*.json`, `EXP-C04-*.json`, `EXP-C06-*.json`; the cached OEIS entries the claims cite (`cache/oeis/`).
- Literature (for CLM-C03-07/09/10): Geser–Hofbauer–Waldmann, arXiv:2003.01696 (read: Example 7.11 gives automated termination proofs of Zantema's problem a²b² → b³a³); Geser–Zantema, RAIRO ITA 33 (1999); Geser–Waldmann–Wenzel, WST 2016. Like the Historian, **I could not retrieve the statement of the Zantema–Geser characterization** (Utrecht repository 403/500, Springer paywalled; none of the papers I could open restates it).

**Rules followed:**
- No existing file was edited. My code is in `reviews/skeptic_checks/C03_C04_C06/` (`c03_checks.py`, `c04_checks.py`, `c06_checks.py`), raw outputs in `reviews/skeptic_checks/C03_C04_C06/out/`. None of my scripts imports `systems/` or `lab/`; they only *read* stored results to compare (pysat is used only as a SAT solver, with my own CNF encoding; mpmath and sympy as arithmetic libraries).
- Lab experiments re-run (allowed): EXP-C03-02, EXP-C03-03, EXP-C04-04, EXP-C04-06, EXP-C04-10, EXP-C06-03.
  - This rewrote those `results/*.json`, appended runs to `db/experiments/*.json` and `db/audit_log.jsonl`, and may have refreshed git-ignored `__pycache__` files.
  - The pre-run result files are kept in `out/lab_rerun_before/`.
  - The audit log now holds a `reproduced: false` entry for EXP-C06-03. It is a false alarm caused by bug C1.
- Not run: `lab sync`, `lab lean`, `lab book`, any git command. Nothing committed.
- All heavy jobs ran under `nice -n 10`, one at a time, each well under 15 minutes. Every check below was actually run.

## Bottom line

- **No claim is refuted. No code bug invalidates a mathematical conclusion.** Every number I recomputed with my own code agrees with the records.
- **All eight written proofs marked "awaiting independent skeptic review" are correct** (CLM-C03-02, C04-06, C04-09, C04-10, C04-13, C06-05, C06-07, C06-12; step checks in Appendix A). Two need a wording fix:
  - CLM-C04-10 is false at n = 0 and must say n ≥ 1 (harmless: OEIS A247983 has offset 1).
  - CLM-C06-12's "no law has the set of primes as its spectrum" is trivially true because N = 1 lies in every spectrum; the meaningful statement is about {1} ∪ P.
- **Lean:** all three files compile (exit 0), only propext / Classical.choice / Quot.sound, no `sorry`/`admit`/`native_decide`. The formal statements say what the claims say, with two coverage caveats (CLM-C04-04: `p_positions` is the kernel property, not P-positions; CLM-C06-02/03/08: the converse/inverse parts are written, not formal).
- **The conjectures survive larger searches:**
  - CLM-C06-10: all 17 laws have exactly the conjectured spectrum for every N ≤ 16 (lab: N ≤ 9).
  - CLM-C03-10: no loop for any of the 24 rules predicted terminating; own loops for all 76 predicted looping rules and for 12 new base rules with q = 7.
  - CLM-C04-03: no loop and no matrix interpretation found.
- **Sharper observation for CLM-C03-11:** the loop length is exactly (k^q − 1)/(k − 1) + 1 in all 26 tested cases (q = 2…7), not just "like k^q" (Appendix B).
- **Problems found** (details in (c)):
  - C1: EXP-C06-03 and EXP-C06-04 hash a wall-clock `runtime_s`, so `lab verify` reports them as CHANGED on every re-run. Confirmed by re-running EXP-C06-03.
  - C2: a C03 journal entry claims matrix-interpretation searches that no committed experiment performs.
  - C3: the C03 paper labels the divisibility conjecture as CLM-C03-08 (it is CLM-C03-10).
  - C4: the loop certificates behind CLM-C03-10's "proved for q ≤ 6" are not stored.
  - Minor count and wording issues.

---

## (a) Verdicts

| Claim | Verdict | Details | Recommended status change |
|---|---|---|---|
| CLM-C03-01 (count-decreasing rules terminate) | **UPHELD** | Lean re-run OK. `Terminating l r` is well-foundedness of the converse step relation, i.e. no infinite derivation. `terminating_of_count_lt` is stated for any alphabet and any rule, as in the English. | None. |
| CLM-C03-02 (conserving rules terminate) | **UPHELD** | The written proof is correct (Appendix A.1). The ordering of zeros is invariant; N₁ never increases; by induction each zero participates finitely often; pigeonhole gives the contradiction. `terminating_swap` matches the swap case. Checks: the proof's key fact "N₁ never increases" held on 300 random derivations (0 violations). 9,490 words (length ≤ 8, all 64 conserving rules with parameters ≤ 4) have finite reachable sets; 130 were inconclusive (sets > 50,000, rules 01 → 1000, 01 → 10000 and mirrors). | Mark "written proof, skeptic-reviewed 2026-10-18". |
| CLM-C03-03 (self-embedding ⇒ non-termination; doubling region loops) | **UPHELD** | Lean re-run OK; `not_terminating_of_loop` and `not_terminating_double` state exactly the English, with p, q ≥ 1 (q is not even needed). I checked the two-step loop by hand. | None. |
| CLM-C03-04 (011 → 11100 loops) | **UPHELD** | The four steps were checked by `decide` in Lean and replayed by my own code. | None. |
| CLM-C03-05 (lifting lemma) | **UPHELD** | `step_map`/`loop_map` hold for arbitrary letter-to-word substitutions (`flatMap`), so they are more general than the English. The mirror map φ was checked by hand: (p,q,r,s) ↦ (q,p,s,r), steps at i ↦ \|w\| − i − \|l\|. My own lift and mirror implementations produced valid loops. | None. |
| CLM-C03-06 (601 of 625 rules classified) | **UPHELD** | My own replay verifies all 76 certificates: 28 (EXP-C03-01), 71 (EXP-C03-02), and 5 mirror certificates that I rebuilt from the text "mirror of …". An independent search (own strategies, 0.8 s) found loops for all 76; the classification equals H-C03-4's prediction. All 218 matrix certificates of EXP-C03-01 re-verified exactly. The counts 525 / 76 / 24 are confirmed. Caveat C4: the 5 mirror certificates are stored only as text. | None. |
| CLM-C03-07 (H-C03-1 refuted via Zantema's problem) | **UPHELD WITH CAVEATS** | The refutation rests on the literature, as the record says. Geser–Hofbauer–Waldmann (arXiv:2003.01696, Ex. 7.11) give automated termination proofs of a²b² → b³a³ (= 0011 → 111000), confirming the citation. 3747/3747 words of length ≤ 12 containing 0011 have finite reachable sets (largest 33). | None. |
| CLM-C03-08 (H-C03-2 refuted) | **UPHELD** | The counterexample is Lean-verified. With the 5 mirror loops of EXP-C03-03 there are **40** counterexamples with parameters ≤ 5, not 35 (the 35 counts EXP-C03-02 only). | Optionally update the count. |
| CLM-C03-09 (H-C03-3 inconclusive) | **UPHELD** (status correct) | H-C03-3 predicts loops for 8 of the 24 open rules (e.g. 0011 → 11100000). I found none, and all strategy runs and reachable sets are finite. Note the asymmetry: H-C03-1 was refuted by citing a published termination proof. If the Zantema–Geser theorem classifies (2,2,3,5) as terminating, H-C03-3 is refuted the same way. | None until the Zantema–Geser statement is obtained. |
| CLM-C03-10 (divisibility characterization) | **UPHELD** (no counterexample) | Own loops for all 76 rules predicted non-terminating with parameters ≤ 5. Own loops for all 75 base rules (1,q,r,k) with q ≤ 6, k ≤ 6, plus 12 new ones with q = 7, k = 2, 3. For the 24 rules predicted terminating: no loop in a larger search; 2,768/2,768 leftmost/rightmost runs from 0^a 1^b reach a normal form; 6,019 words of length ≤ 10 have finite reachable sets. Caveat C4 (unstored base loops). Novelty "REDISCOVERY" presumes agreement with Zantema–Geser, which nobody has checked. | Keep COMPUTATIONALLY SUPPORTED. |
| CLM-C03-11 (loop lengths ~ k^q) | **UPHELD** | My own rightmost simulation gives exactly 16, 32, 64 and 260, 1556, 9332 steps, with final lengths 53, 95, 171 and 1581, 9367, 56035. Stronger: steps = (k^q − 1)/(k − 1) + 1 in all 26 cases with r = q + 1, q = 2…7 (Appendix B). | Optionally state the exact (conjectural) formula. |
| CLM-C04-01 (census \|l\|,\|r\| ≤ 3) | **UPHELD** | Own certificates for all 162 terminating rules: 70 length-decreasing; 70 length-preserving, with the lexicographic argument (proof checked; 0 direction inconsistencies in random contexts); 20 own 2×2 matrix interpretations; 2 factor counts (aa, bb). The 34 non-terminating rules are exactly those where l is a factor of r. | None. |
| CLM-C04-02 (H-C04-0 refuted) | **UPHELD** | ab → bbaa loop replayed. Own re-check of all 868 records of EXP-C04-02: every certificate passes my independent checker (linear interpretations, factor counts, the 8 LP-found weighted factor counts in exact integers, self-embeddings). Exactly 18 looping rules have l not a factor of r. A loop hunt on the 332 certified length-increasing rules found none. | None. |
| CLM-C04-03 (aab → ababa / babaa terminate) | **UPHELD** (conjecture; no counterexample) | No loop (strategy runs from all seeds of length ≤ 12 containing aab). No matrix interpretation (2×2 full, entries ≤ 5; 3×3 upper-triangular, entries ≤ 3). Exhaustive D_max: aab → ababa 0,0,0,1,3,7,15,31,63,127,255 (n ≤ 10, one more than the lab); aab → babaa 0,0,0,1,2,3,6,9,14,21,30,45 (n ≤ 11). | Keep COMPUTATIONALLY SUPPORTED. |
| CLM-C04-04 (ab → ba) | **UPHELD WITH CAVEATS** | Lean re-run OK; `inv_step`, `normal_iff_inv_zero` and `derivation_length_eq_inv` match. Caveat: `p_positions` proves the *kernel* property; "kernel = P-positions" (true for terminating games) and D(n) = ⌊n²/4⌋ are written, not formal. Own D(n) = ⌊n²/4⌋ for n ≤ 18; the parity of the Grundy values is checked in the RD sweep. | proof_check: say that the P-position step and ⌊n²/4⌋ are written arguments. |
| CLM-C04-05 (unbordered ⇒ random descent) | **UPHELD** | Lean re-run OK. `LocalRD`, `random_descent`, `Unbordered` (no nonempty proper suffix that is a prefix; vacuous for \|l\| ≤ 1 and l = ε) and `unbordered_diamond` match (a) and (b). Own check: all 84 unbordered rules with \|l\|,\|r\| ≤ 3 have RD on all words ≤ 10. | None. |
| CLM-C04-06 (constant-step potential; confluent ⇔ RD) | **UPHELD** | The written proof is correct (Appendix A.2; Vandermonde step and binomial expansion checked, including the 0⁰ = 1 convention). The Lean coverage (`steps_length_unique`, `length_changing_unique`) is stated honestly. Own potential on all 5365 rules: 351,927 steps, 0 violations, K ≤ 2. For length-preserving \|l\| ≤ 3 and all words ≤ 7, no pair u, v has two derivation lengths. Notes reproduced: 770 rules, 94 confluent, 126 length-uniform but not confluent; aaaba → baabb gives two normal forms from aaabaaaba. | Mark skeptic-reviewed. |
| CLM-C04-07 (H-C04-1 refuted) | **UPHELD** | aa → a has RD (own check). Exactly 18 bordered rules with RD (own list). | None. |
| CLM-C04-08 (parity of RD games) | **UPHELD** | Proof correct (every option has D − 1). Own check: all 102 RD rules, words ≤ 10 (≤ 8 for the four doubling rules), 0 violations. | Mark skeptic-reviewed. |
| CLM-C04-09 (aab → ba: D(n) = n − 1 − κ(n)) | **UPHELD** | Written proof correct, steps (i)–(vi) (Appendix A.3). Own full derivation graphs n ≤ 16. The per-word configuration formula holds on all 4.2 M words of length ≤ 21 (0 mismatches). f(n) = 1 + κ(n) for n ≤ 200,000. Stalls at 2, 4, 7, 12, 21, 38, 71. | Mark skeptic-reviewed (see C7 on "n = 20000"). |
| CLM-C04-10 (A247983 = D(n+2)) | **UPHELD WITH CAVEATS** | The proof (Jensen plus tail bound) is correct **for n ≥ 1**. At n = 0 the least k ≥ 1 is 1, while n − J(0) = 0 = D(2). The proof's "k* = n − J ≥ 1" also needs n ≥ 1. Own mpmath computation (n + 120 bits) agrees for n = 1…1200. All 68 cached OEIS terms (offset 1) match. | Add "n ≥ 1" to the statement; mark skeptic-reviewed. |
| CLM-C04-11 (H-C04-G refuted) | **UPHELD** | It follows from CLM-C04-09 (step (vi): a finite-valued linear recurrence sequence is eventually periodic; the 1s of e(n) have unbounded gaps). | None. |
| CLM-C04-12 (complexity classes, closed forms) | **UPHELD** | Own D_max for all 55 classes: n ≤ 18 (length-preserving), ≤ 16 (length-decreasing), ≤ 12 (growing), ≤ 15 (doubling, single derivation by RD, plus a brute-force graph for n ≤ 9). All 54 closed forms hold on every term and agree with the stored D. The quadratic classes are exactly ab→ba, aab→aba, aba→aab, aab→baa (14 rules). | None (now checked to n = 18). |
| CLM-C04-13 (unary lhs ⇒ octal games) | **UPHELD** | Written proof correct. All 17 named rule/code pairs: word-game Grundy value = XOR of own octal values over runs, on all words ≤ 12, 0 mismatches. | Mark skeptic-reviewed. |
| CLM-C04-14 (H-C04-6 refuted) | **UPHELD** | Own derivation-graph Grundy value of a¹⁴ under aa → b is 4 (first n with value 4). Max over n ≤ 3000: 0.07 → 9, 0.6 → 91. | None. |
| CLM-C04-15 (Dawson's Kayles period 34 from 53) | **UPHELD** | Own 0.07 recursion: G(n+34) = G(n) on the Guy–Smith window 53 ≤ n < 2·53 + 34 + 2, and it **fails at n = 52**, so 53 is the exact preperiod. 0.4 = 0.07 shifted by one (period 34 from 54). | None. |
| CLM-C04-16 (Officers, 0.007, 0.06 periodic?) | **UPHELD** (status correct) | Own recursion to 3000: no period ≤ 300 for any of the three (max values 91, 120, 117). OEIS search for the first 20 terms of 0.06 returns no match (2026-10-18). A395248 is ".007" in the cache. | None. |
| CLM-C06-01 (Laver tables) | **UPHELD** | Own SAT encoding: anchored LD models 1,1,0,1,0,0,0,1,0,0 for N = 1…10; the models at N = 2, 4, 8 equal my Laver tables. My own recursion: LD exactly at N = 1, 2, 4, …, 64 for N ≤ 64 (it never breaks down; non-powers give non-LD tables). A_n LD exhaustively to N = 256. Lean `laver3` equals my A₃. | Optional: the finite statement (N ≤ 10) is now established by two independent complete SAT enumerations; it could be PROVEN (computer-assisted). |
| CLM-C06-02 (anchored associativity) | **UPHELD** | Lean `anchored_assoc_unique` for every N ≥ 1 (NeZero). The converse is not in Lean (trivial; checked: SAT count 1 for N ≤ 10 and the model is x+y+1). | None. |
| CLM-C06-03 (anchored RD) | **UPHELD** | Lean `anchored_rd_unique`; the written proof is correct. SAT count 1 for N ≤ 10, model x + 1. | None. |
| CLM-C06-04 (H-C06-2 refuted) | **UPHELD** | Own enumeration of all 382 laws and own SAT for N ≤ 6: 283 trivial, 77 all-N, 22 restricted. The per-law spectra are identical to the lab's for all 382 laws. | None. |
| CLM-C06-05 (right-permutable: x + c(y), N^(N−1)) | **UPHELD** | The written proof is correct (R_y commutes with the successor ⇒ translation). Own SAT counts 1, 2, 9, 64, 625, **7776** (N ≤ 6, one more than the lab). Every model for N ≤ 5 has the form x + c(y). | Mark skeptic-reviewed. |
| CLM-C06-06 (odd law) | **UPHELD** | Lean: even sizes impossible; 2(x⋆y − x − 1) = y for odd N; existence. They match the English (N = 1 included). Own SAT: exactly one model at each odd N ≤ 13, none at even N; it equals x + 1 + y/2. | None. |
| CLM-C06-07 (golden law) | **UPHELD** | The written proof is correct, steps (i)–(v) (Appendix A.4). Own SAT counts equal the root counts of a² + a ≡ 1 and every model is affine with a = root, for N ≤ 13 (2 models at N = 11) — RESULT_GOLDEN19. The spectrum description equals the root set for N ≤ 2000, and the count equals 2^ω(m) there. The cached A089270 (55 terms) and A087781 (105 terms) match my own computation. | Mark skeptic-reviewed. |
| CLM-C06-08 (left-permutable ↔ commutative monoids) | **UPHELD** | The Lean core matches (a·b := (a−1)⋆b is an associative, commutative monoid with identity 0); the converse is a correct written step. Two independent counts agree: own SAT LP counts 1, 2, 9, 94, 1486, and own brute-force count of commutative monoids with identity 0 gives the same. The cached A058156 data match. | None. |
| CLM-C06-09 (H-C06-3 refuted) | **UPHELD** | The four named laws have models for all N ≤ 6 (own SAT), and their affine conditions have no common complex root. Affine spectrum {1} for N ≤ 300. x(yz) = y((yx)z) has a model at N = 2 but affine spectrum {1}. | None. |
| CLM-C06-10 (17 finite spectra) | **UPHELD** (conjecture survives) | Own SAT: every one of the 17 laws has exactly the conjectured spectrum for all **N ≤ 16** (lab: N ≤ 9). The affine conditions of the 16 affine-only laws have no common complex root, and their affine spectra are {1,3}/{1,2} for N ≤ 300. | Keep COMPUTATIONALLY SUPPORTED; record N ≤ 16. |
| CLM-C06-11 (mirror twins) | **UPHELD** | Own SAT counts of both twins equal those of the golden and odd laws, with all models affine, for N ≤ 13 — RESULT_TWIN19. By hand: the twins' affine conditions are a² + a = 1 and 2a = 1. | Optionally record the larger range. |
| CLM-C06-12 (coprime products) | **UPHELD WITH CAVEATS** | The proof is correct. Own CRT transports of actual models (9 law/size pairs, e.g. golden 5×11, odd 5×7, LP 3×4) all satisfy law and anchor. Wording: since N = 1 lies in every spectrum, "exactly the primes" is impossible for a trivial reason. The paper's "every spectrum is determined by which products of prime powers it contains" is vacuous. | Reword to "{1} ∪ P, P an infinite set of primes (indeed any set containing two primes but not their product)"; mark skeptic-reviewed. |

---

## (b) Independent checks (commands and results)

Unless noted, commands run from `reviews/skeptic_checks/C03_C04_C06/` with `nice -n 10`. Outputs: `out/<script>_<part>.json`.

**L. Lean.**
- `cd proofs/lean && PATH=$HOME/.elan/bin:$PATH lake env lean Infinity/<f>.lean` for C03_Termination, C04_Derivations, C06_Laver → exit 0 each (`out/lean_*.txt`).
- The axioms of every `#print axioms` ⊆ {propext, Classical.choice, Quot.sound}.
- `grep -nE "sorry|admit|native_decide|axiom|unsafe|implemented_by|extern|opaque"` on the three files → no hits.

**C03** (`python3 c03_checks.py <part>`):

| part | what | result |
|---|---|---|
| certs | own replay of every stored loop; rebuild the 5 mirror loops; recount classes | 28/28, 71/71, 5/5 valid; 525 + 76 + 24; non-terminating set = H-C03-4 prediction; stored statuses of EXP-C03-02 have 10 symmetry violations (resolved by the mirrors) |
| matrices | exact re-check of 218 matrix certificates + strict decrease along random derivations | 218/218 (156 count-decreasing, 62 conserving) |
| search | own strategy search (leftmost/rightmost from 0^a 1^b), own mirror/lift | loops for all 76 predicted-NT rules (71 direct, 5 via own mirror), longest 157 steps |
| open | the 24 predicted-terminating rules: larger search incl. random strategy; finiteness | no loop; 2,768/2,768 strategy runs reach a normal form; 6,019/6,019 words ≤ 10 finite (largest set 26) |
| zantema | 0011 → 111000 on all words ≤ 12 containing 0011; EXP-C03-03 false alarm | 3747/3747 finite (largest 33); 001001001111 under 0011 → 11100000: 232 words, longest 104 (as recorded) |
| conserving | 64 conserving rules (params ≤ 4), words ≤ 8; proof's N₁ monotonicity | 9,490 finite, 130 inconclusive (> 50,000 words); 0 violations |
| obs11 | CLM-C03-11; base rules q ≤ 7 | exact match (Appendix B); loops for all base rules q ≤ 6, k ≤ 6 and for (1,7,r,k), k = 2, 3 (12 rules, ≤ 1094 steps) |

**C04** (`python3 c04_checks.py <part>`):

| part | result |
|---|---|
| census | 196 rules: 34 with l ⊑ r (all non-terminating), 162 with own certificates (70 + 70 + 20 own 2×2 matrices + 2 factor counts), 0 unknown |
| ext | 868 EXP-C04-02 records: 0 certificates fail my checker; 18 looping rules with l ⋢ r (listed in `out/c04_ext.json`); 8 undecided = the two classes of CLM-C04-03; no loop among 332 certified length-increasing rules |
| potential | 5365 rules (binary ≤ 5, ternary ≤ 3), 351,927 random steps: ΔΦ = δ always, K ≤ 2 |
| rd | 84/84 unbordered RD; 18/78 bordered RD (list in output); 0 length-uniform-not-confluent; critical-peak criterion agrees on 162/162; \|l\| = 4, 5 bordered family: 770 rules, 94 confluent, 126 length-uniform not confluent |
| complexity | 55 classes, closed forms hold on all computed terms (n ≤ 18/16/15/12); stored D agrees; ab → bba brute-force graphs n ≤ 9: 2^(n−1) − 1 |
| aabba | graphs n ≤ 16 and RD runs n ≤ 21 match n − 1 − κ(n); per-word formula 0 mismatches on all words ≤ 21; f(n) = 1 + κ(n) for n ≤ 200,000 |
| games / octal | see (a) CLM-C04-13…16 |
| log2 | n = 1…1200 agree; single mismatch n = 0 (A = 1, formula 0); OEIS terms match |
| hard | aab → ababa, aab → babaa: no matrix interpretation (tiers above), no loop |

**C06** (`python3 c06_checks.py <part>`; own parser and CNF, CaDiCaL via pysat; every SAT model is re-evaluated against the law by brute force):

| part | result |
|---|---|
| selftest | SAT count = brute-force count over all anchored tables for 390 laws at N = 2, 3: 0 mismatches |
| basic | LD/RD/assoc counts N ≤ 10; right-permutable N^(N−1) for N ≤ 6; left-permutable 1, 2, 9, 94, 1486; odd law 1 model iff N odd (N ≤ 13), formula x + 1 + y/2 |
| monoids | own backtracking count of commutative monoids with identity 0: 1, 2, 9, 94, 1486 |
| laver | recursion LD exactly at powers of 2 (N ≤ 64); A_n LD for N ≤ 256; Lean A₃ = own A₃; SAT models = Laver tables at 2, 4, 8 |
| family | 382 laws, N ≤ 6: 283 / 77 / 22, identical per-law spectra to EXP-C06-03 |
| conj10 1 12, conj10 13 16 | all 17 laws exactly as conjectured for N ≤ 16 (slowest instance 29.5 s, x(yz) = y((yx)z) at N = 16) |
| golden 13 / golden 19 | counts = roots, all models affine; twins equal; RESULT_GOLDEN19_TABLE |
| products | CRT transports of real models: 9/9 law–size pairs valid (all model pairs) |
| affine | affine conditions of the 17 + 4 laws, no common complex root (sympy Gröbner over ℚ), spectra for N ≤ 300 |

**R. Lab re-runs** (`python -m lab run <id>` from the repository root; `out/lab_reruns.log`):

| experiment | stored code sha256 = current script? | outcome |
|---|---|---|
| EXP-C03-02 | yes | reproduced previous hash |
| EXP-C03-03 | yes | reproduced previous hash |
| EXP-C04-04 | yes | reproduced previous hash |
| EXP-C04-06 | yes | reproduced previous hash |
| EXP-C04-10 | yes | reproduced previous hash |
| EXP-C06-03 | yes | **RESULT HASH CHANGED** — the only differing key is `runtime_s` (46.8 → 37.1); everything else is identical (bug C1) |

All 18 C03/C04/C06 result files carry a code sha256 equal to the current script. `systems_sha256` differs between runs because it hashes the whole `systems/` directory, which other cycles keep extending.

---

## (c) Bugs and problems in code, records and documents

None of these changes a mathematical conclusion.

- **C1 (reproducibility bug, EXP-C06-03 and EXP-C06-04).**
  - Both scripts return `"runtime_s": round(time.perf_counter() - t0, 1)` inside the results dict.
  - The runner excludes only the key `timings` from the hash (`lab/runner.py`, `VOLATILE_KEYS`).
  - So every re-run, and `python -m lab verify`, reports these experiments as CHANGED. Confirmed on EXP-C06-03, where only `runtime_s` differs.
  - Fix: move `runtime_s` under `timings` (as EXP-C06-02 does).
- **C2 (unreproducible negative claim, C03 journal C03-11).**
  - `record.yaml` (journal key C03-11) and `journal/JOURNAL.md` say no matrix interpretation exists with "upper-triangular d = 3 entries ≤ 5, d = 4 entries ≤ 2; full d = 3 entries ≤ 1".
  - The committed searches are only:
    - EXP-C03-01: d = 2 full ≤ 4, d = 3 upper ≤ 3, d = 4 upper ≤ 1, parameters ≤ 4;
    - EXP-C03-02: d = 2 full ≤ 4, d = 3 upper ≤ 3.
  - The README states the committed tiers correctly. Either add the larger search as an experiment or reword the journal entry.
- **C3 (label, `proofs/paper/C03.md`).** The heading "Conjecture 7 (CLM-C03-08)" should read CLM-C03-10. CLM-C03-08 is the refuted H-C03-2.
- **C4 (traceability).**
  - EXP-C03-04 stores only step counts for its 75 base loops, and EXP-C03-03 stores the 5 mirror loops only as the text "mirror of […]". CLM-C03-10's "proved for (b)/(c) whenever the base rule has a known loop (all q ≤ 6)" therefore rests on certificates that are not in the repository.
  - They are re-derivable; I re-found all of them with my own code.
  - Store at least start word + strategy (or positions).
- **C5 (count, CLM-C03-08).** "35 counterexamples with parameters ≤ 5" counts EXP-C03-02 alone; with EXP-C03-03 it is 40. Similarly, EXP-C03-01's "12" becomes 16 for parameters ≤ 4 once the four looping rules it left UNKNOWN — (1,3,4,3), (1,3,4,4) and their mirrors — are counted.
- **C6 (edge case, CLM-C04-10 and C04.md Theorem 8).** The identity is false at n = 0; the statement needs n ≥ 1, which is the OEIS offset.
- **C7 (wording, EXP-C04-04 record and the CLM-C04-09 proof_check).** "Closed form checked to n = 20000" checks only the arithmetic identity between the max-over-m expression (proof step iv) and n − 1 − κ(n) (step v). Derivation lengths themselves were checked to n = 21. The proof covers all n, so this is wording only.
- **C8 (Lean coverage wording, CLM-C04-04).** `p_positions` formalises the kernel property; Lean contains no game semantics. "Kernel = P-positions" and D(n) = ⌊n²/4⌋ are standard written steps; the proof_check should say so.
- **C9 (wording, CLM-C06-12 and C06.md Theorem 8).**
  - "No set of laws has exactly the primes as its spectrum" is true for a trivial reason: N = 1 is always a model.
  - "Every spectrum is determined by which products of prime powers it contains" is vacuous.
  - Intended content: no spectrum contains two primes p ≠ q without pq.
- **C10 (garbled summary, EXP-C03-02).** "H-C03-3 predicts ['NON-TERMINATING', 'TERMINATING'] for all unknown rules" means H-C03-3 predicts loops for some of them (8 of the final 24).
- **C11 (minor, C06 README).** "12 theorems" in `C06_Laver.lean`: the file has 19 theorem declarations, 12 of which are printed with `#print axioms`.

Audited and found correct:
- `check_loop`, `lift_zeros` and `mirror` (C03).
- `derivation_extremes`' cycle detection: the on-stack set is exactly the DFS path.
- `linear_interpretation`: both composition orders are sound.
- `factor_count_certificate` and `weighted_factor_certificate`: contexts of length ≤ \|f\| − 1, shorter contexts modelling word ends, are sufficient.
- `graph_values`, `octal_grundy`, `run_game_grundy`.
- `formula_D`'s early break: for 2^m ≥ T the value T − 1 decreases in m.
- `MagmaSAT`'s subterm sharing. Exactness was also confirmed indirectly: my independent encoder reproduces all of its spectra.
- `recursion_table` (it never breaks down for N ≤ 64).

Faults in my own harness, fixed before the reported runs:
- The first conserving-rule check used words ≤ 10 with a 200,000-word cap. It ran too long on rules with exponential reachable sets; I stopped it and reduced the check to words ≤ 8 with a 50,000 cap, reporting the over-limit words as inconclusive.
- The first `ext` loop hunt used seeds that mostly did not contain l, so it was vacuous. I rewrote it to use seeds containing l.
- The base-family extension's first budget was too small for (1,6,7,6), which needs 9332 steps. The `obs11` run itself found that loop.

---

## Appendix A — checks of the written proofs

**A.1 C03 Theorem 2 (CLM-C03-02).**
- s = p preserves the number and order of zeros. Numbering them from the right is therefore well defined.
- A step whose redex contains z_j…z_{j+p−1}:
  - lowers their N by q;
  - changes N of every zero to the left by r − q;
  - leaves the zeros to the right unchanged.
  A redex not containing z₁ lies entirely to the left of z₁, because the block 0^p 1^q is contiguous. So N₁ never increases.
- Induction: if z₁…z_{i−1} take part finitely often, only finitely many redexes lie right of z_i, so N_i is bounded above while every participation lowers it by q. Hence z_i also takes part finitely often.
- An infinite derivation needs some zero to take part infinitely often (pigeonhole over m zeros, p ≥ 1 per step), a contradiction.
- The case r = q follows by φ. **Correct.**

**A.2 C04 Theorem 2 (CLM-C04-06).**
- Some letter c has P ≠ Q. The power sums p₀…p_{k−1} are the image of the indicator vector under the invertible Vandermonde matrix (j^m), 0 ≤ j, m < k. So some p_m(P) ≠ p_m(Q), and K is well defined.
- The binomial expansion with i₀^{K−m} (0⁰ = 1) gives ΔΦ = p_K(Q) − p_K(P), independent of i₀. Positions outside the window are unchanged because \|l\| = \|r\|.
- Consequences: (1) derivation length = ΔΦ/δ; (2) terminating ⇒ (confluent ⇔ unique normal form ⇔ RD by (1)). **Correct.**

**A.3 C04 Theorem 7 (CLM-C04-09).**
- (i) Encoding: aab ending at the (k+1)-th b needs x_k ≥ 2 and gives x_k − 2, x_{k+1} + 1.
- (ii) aab is unbordered.
- (iii) V is invariant, and the normal form (x_k ≤ 1 for k < m) is unique for a given V.
- (iv) Lower bound s₂(ρ) + q ≥ ⌈T/2^m⌉ (both cases checked). The upper bound by splitting tokens down from q = ⌈T/2^m⌉ tokens on level m works because q ≤ T ≤ q·2^m.
- (v) f(n) ≤ k + 1 ⇔ n ≤ 2^k + k. The "only if" uses g(m+1) − g(m) = 1 + 2^m(k − m − 1) ≥ 0; the cases m ≥ k + 1 and n ≤ k are handled by m = n. With f ≥ 1 this gives f = 1 + κ.
- (vi) Non-rationality: a sequence with finitely many values that satisfies a linear recurrence is eventually periodic, but the stalls have unbounded gaps. **Correct.**

**A.3′ C04 Theorem 8 (CLM-C04-10).**
- t(k) = 2^{−k} Σ_{i≥1} 2^{−i}/(k+i). Jensen with mean 2 gives the lower bound 2^{−k}/(k+2); the strict upper bound is 2^{−k}/(k+1).
- t(k*) < 2^{−n} ⇔ 2^J + J ≤ n + 1, which is the definition of J.
- t(k* − 1) ≥ 2^{−n} ⇔ 2^{J+1} + J + 1 ≥ n + 2, which is the maximality of J.
- **Correct for n ≥ 1.** At n = 0, k* = 0 is not admissible.

**A.4 C06 Theorem 6 (CLM-C06-07).**
- (i) z = 0 gives x⋆σ(y) = x⋆y + 1. Hence 0⋆σ^k(0) = 1 + k are distinct, so σ is an N-cycle through 0 with σ^N(0) = 0, κ is a bijection, and x⋆y = x + 1 + κ(y).
- (ii) The identity (∗) was re-derived.
- (iii) κ(y + jc) = κ(y) + j with c = 1 + κ(1); gcd(c, N) = d > 1 would give N/d ≡ 0 (mod N). So κ(y) = c^{−1}y.
- (iv) a² + a ≡ 1. Conversely the residual of (∗) is (a² + a − 1)(1 + a z).
- (v) No root mod 2 or mod 25; Hensel for p ∤ 10 since 2a + 1 is a unit; quadratic reciprocity gives p ≡ ±1 (mod 5); CRT. **Correct.**

**A.5 C06 Theorems 4, 7, 8 (CLM-C06-05, -08, -12).**
- Theorem 4: z = 0 gives (x+1)⋆y = (x⋆y) + 1, i.e. R_y commutes with the successor. This holds for arbitrary maps, not only permutations, and gives R_y(x) = x + R_y(0).
- Theorem 7:
  - The centraliser argument (a) is valid (g(m) = f_m(g(0)) = f_{g(0)}(m)).
  - (b) gives closure under composition and identity = f₀.
  - Commutativity comes from f_a(f_b(0)) = f_b(f_a(0)).
  - The converse is direct.
- Theorem 8:
  - Identities pass to products.
  - φ(x + 1) = φ(x) + (1, 1) transports the anchor. **Correct** (wording caveat C9).

**A.6 Proofs given as Lean or one-liners.** Checked by hand:
- C03 Theorem 3(b) (two-step loop);
- C04 Theorems 6, 9, 10 (the octal digits of all five codes, including the dead middle runs of bab/aba);
- C06 Theorems 1, 2, 5 (identical to their Lean versions). **Correct.**

## Appendix B — exact loop lengths in the base family (observation)

For 0 1^q → 1^{q+1} 0^k, my own rightmost-redex simulation from 0 1^{q(q+1)} first contains the start word after exactly (k^q − 1)/(k − 1) + 1 steps, in all 26 computed cases: q = 2…6 with k = 2…6, and q = 7 with k = 2, 3. For example 9332 = (6⁶ − 1)/5 + 1, and 1094 = (3⁷ − 1)/2 + 1 for (1,7,8,3). The lab's six data points are special cases. This is an observation, not proved. It sharpens CLM-C03-11 ("grow like k^q") and is a natural target for the "explain the k^q loop lengths" direction in the C03 README. Data: `out/c03_obs11.json`.
