# Project Infinity — Research Report, Batch 1 (cycles C01–C20)

*Generated 2026-10-19 from the laboratory database. Every number below is
read from `db/` or `reports/batch_statistics.json`
(`python -m lab report`, tables in [`REPORT_DATA.md`](REPORT_DATA.md)).
Claim identifiers (CLM-…) and experiment identifiers (EXP-…) point to the
database records in `db/claims/` and `db/experiments/`.*

## Summary

*Update 2026-10-20: the batch 1.1 hardening sprint and batch 1.2 (next sections)
changed some of these numbers — now 241 claims, 147 PROVEN, 364 Lean theorems —
settled two of the open problems of section 9, and determined the spectrum of ETP
law 501.*

Twenty research cycles were run across five foundational systems. They
produced 113 deterministic experiments (203 recorded runs) and 225 claims:
131 PROVEN, 39 COMPUTATIONALLY SUPPORTED, 4 CONJECTURE, 49 REFUTED and
2 INCONCLUSIVE. 103 claims are rediscoveries of known mathematics, 52 are
"potentially novel" (nothing equivalent was found in the sources searched —
this is **not** a claim of priority), and 70 were not assessed. Lean 4 +
Mathlib checks 194 theorems in 15 files with only the standard axioms.
Independent Skeptic reviews gave a verdict on 217 of the 225 claims. They
refuted two of the laboratory's own claims outright (CLM-C05-09 and
CLM-C08-05), forced a third to be withdrawn (CLM-C08-07), exposed three code
bugs that had changed stated numbers (two in C17, one in C13), and downgraded one "potentially
novel" result to a rediscovery (CLM-C14-06). All of these corrections are in
the records, with the failed versions kept.

The batch produced no breakthrough. What it did produce:

- a number of small, exact, checkable results on invented or little-studied
  systems;
- a set of honestly negative application results;
- a reproducible, append-only infrastructure that caught its own mistakes.

## Batch 1.1 — hardening sprint (2026-10-19/20)

After the batch-1 report the Director, acting as project manager, ran a
sprint that hardened batch 1 instead of starting new cycles. The plan, with
the reasons for each item and its outcome, is
[`PM_PLAN_batch1.1.md`](PM_PLAN_batch1.1.md). All numbers in this section are
read from the database after the sprint; the numbers in sections 1–10 above
are those of the batch-1 report, kept for the record.

| | batch 1 report | after batch 1.1 |
|---|---|---|
| claims | 225 | 230 (new: CLM-C05-11 … -14, CLM-C17-08) |
| PROVEN / COMP. SUPPORTED / CONJECTURE / REFUTED / INCONCLUSIVE | 131 / 39 / 4 / 49 / 2 | 138 / 37 / 4 / 49 / 2 |
| REDISCOVERY / POTENTIALLY NOVEL / NOT ASSESSED | 103 / 52 / 70 | 109 / 51 / 70 |
| PROVEN by kind: Lean complete / Lean + written or computational / computer-assisted / literature / written only | 14 / 36 / 15 / 2 / 64 | 17 / 43 / 15 / 3 / 60 |
| Lean 4 + Mathlib | 194 theorems in 15 files | 334 theorems in 21 files |
| experiments / recorded runs | 113 / 203 | 114 / 205 |
| journal entries | 255 (30 of them duplicate revisions, see item 5) | 239 |
| PROVEN claims not fully formal with an independent review | 115 of 117 | 121 of 121 |
| claims with a Skeptic verdict | 217 of 225 | 224 of 230 |

**What the sprint established.**

1. **Laws 677 and 1313 have no models of order 8 or 10** (G4; CLM-C05-11,
   -12, -13; textbook Theorem 6.11). A complete case split — idempotent or not,
   then the cycle type of the row of an element with the fewest fixed points
   (`proofs/paper/C05.md`, Lemma 8) — reduces each question to 45 (n = 8) or
   97 (n = 10) CNFs. With implied division clauses (Lemma 9) and, for 1313,
   Latin columns (Lemma 7: finite models of 1313 are quasigroups, proved in
   Lean), all 284 CNFs are UNSAT, and every DRAT proof — 40.5 million lines —
   was verified by drat-trim (EXP-C05-08). So both laws have exactly the
   orders 1, 5, 7, 9 up to 10. Literature: Mace4 already exhausts size 8 for
   law 677 (ETP paper, §7.3.1), so CLM-C05-11 is a rediscovery with a new
   certificate; order 10 for 677 and orders 8 and 10 for 1313 were not found
   in the sources read. Law 677 is the premise of the ETP's last open finite
   implication, 677 ⇒ 255; there is no counterexample of order 8 or 10.
2. **Four written proofs are now Lean proofs** (G2): skew-binary counting
   (CLM-C10-07, now fully formal, including the uniqueness of canonical
   representations that the paper had cited), the structure of affine spectra
   (CLM-C13-01, all parts; the infinite case by Gauss's lemma instead of
   Schur's theorem), the forced anchored table (CLM-C17-05: uniqueness,
   existence and the reduction to the wrap-around equations for every N), and
   the arithmetic core of the Zeckendorf deficit bound (CLM-C19-15). Two more
   Lean files came out of the sprint itself: finite models of law 1313 are
   quasigroups (CLM-C05-14), and the row-period proof of CLM-C17-08 (item 6).
3. **The novelty audit of C11–C20** (G1, `reviews/historian_C11_C20.md`)
   changed four labels and corrected twenty novelty bases:
   - CLM-C17-05 is a rediscovery, and the all-N statement it left open is
     published (Biane's refereed survey, footnote 1; Aguilera–Iannella 2026,
     Prop. 2.5, with Dehornoy's Lemma X.1.7 and Prop. X.1.6) — recorded as
     CLM-C17-08;
   - CLM-C11-04 and CLM-C11-09 are partial rediscoveries (T_011 is Capocelli's
     code C(3), 1989; Fraenkel–Klein 1996);
   - CLM-C14-07 is a partial rediscovery (Oh–Yoo–Yun 2013 prove part (b));
   - Klimov (2026) poses as open whether a "UFS-groupoid" can be a
     quasigroup; CLM-C16-07 answers this positively from order 5 on;
   - several surveys state Laver's recursion for all q, which is false at
     N = 3 — the slip the lab corrected in C17, and Biane in his published
     version. CLM-C06-01 states the published theorem and is now PROVEN
     (literature).
4. **Reproducibility** (G3, [`REPRODUCIBILITY_batch1.1.md`](REPRODUCIBILITY_batch1.1.md)):
   all 113 experiments recorded in batch 1 were re-run with `lab verify --dry`;
   112 reproduced their result hash exactly. EXP-C19-04 had stored wall-clock
   benchmark times inside its hashed results, so no re-run could reproduce it;
   its mathematical results were identical. The times now live under
   `timings`, the experiment was re-recorded and a second run reproduced the
   new hash.
5. **Infrastructure** (G5, G6): `python -m lab check` validates records
   (duplicate YAML keys rejected), references and proof anchors, the database
   against the records, every result file's hash, the journal, and flags
   wall-clock fields inside hashed results. Its first run found five broken
   proof links and a `sync` bug that had appended the same revision of two
   journal entries on every run (32 duplicate lines by the time it was found,
   now removed; the batch-1 journal count of 255 included 30 of them). The
   textbook has a generated *Corrections log* appendix listing every change of a status, label or
   statement with its reason. 24 tests, including a regression test for the
   sync bug.
6. **Independent review of the sprint** (G7, `reviews/skeptic_batch1.1.md`):
   nothing was refuted and no gap was found. The Skeptic completed the
   Historian's row-period argument for CLM-C17-08 and machine-checked it
   (`C17_RowPeriod.lean`: for every N the full anchor instance has a model iff
   N is a power of 2, with Laver's theorem as the only hypothesis), so
   CLM-C17-08 is PROVEN and the literature chain through Dehornoy's book is no
   longer needed. It rebuilt all 401 CNFs of EXP-C05-08 with matching hashes
   and re-decided both laws at orders 8 and 10 with its own encoding and a
   different case split (677 at order 10 twice), every case UNSAT with
   verified DRAT proofs. It reviewed the two PROVEN claims that had no
   independent review (CLM-C05-10, CLM-C19-15) and found the new Lean
   statements faithful. Two corrections: CLM-C05-13 cited the solver run
   instead of the certified one (EXP-C05-06) for the orders 2, 3, 4, 6, and
   CLM-C05-10 claimed that every linear model had been re-checked on its full
   table, while EXP-C05-07 re-checks one per law and order (the Skeptic's
   computation re-checked all of them).

**Not done, and why.** Rauzy-window computations for C08 and a proof of the
Zeckendorf recursion (CLM-C19-05) are research, not hardening; orders 12 and
14 of laws 677 and 1313 are the natural next computation (195 and 373 cases
per law; the hardest order-10 case of 677 already needed 1.3 million
conflicts).

**For a human expert** (sources the agents could not read): Capocelli 1989
and Lakshmanan 1981 (IEEE, blocked) for CLM-C11-04/-09; Kobayashi,
Katsura and Shikishima-Tsuji, TCS 262 (2001) for CLM-C20-02 and C04;
Dehornoy, *Braids and Self-Distributivity*, Ch. X for CLM-C17-08. Whether to
tell P. Klimov that CLM-C16-07 answers his Problems 7.3–7.5, and whether to
submit sequences to the OEIS, are human decisions.

## Batch 1.2 — "find more": spectra of the open ETP laws (2026-10-20)

Asked to "find more", the Director (as project manager) took the front where batch 1.1 had left a working,
certifying method: the spectra (the sets of orders of finite models) of the open laws of the Equational
Theories Project, cycle C05. The plan, the decisions taken on the way and their reasons are in
[`PM_PLAN_batch1.2.md`](PM_PLAN_batch1.2.md). Numbers are read from the database after the batch.

| | after batch 1.1 | after batch 1.2 |
|---|---|---|
| claims | 230 | 241 (new: CLM-C05-15 … -25) |
| PROVEN / COMP. SUPPORTED / CONJECTURE / REFUTED / INCONCLUSIVE | 138 / 37 / 4 / 49 / 2 | 147 / 37 / 5 / 50 / 2 |
| REDISCOVERY / POTENTIALLY NOVEL / NOT ASSESSED | 109 / 51 / 70 | 115 / 55 / 71 |
| Lean 4 + Mathlib | 334 theorems in 21 files | 364 theorems in 23 files |
| experiments / recorded runs | 114 / 205 | 121 / 215 |

**What batch 1.2 established.**

1. **The spectrum of law 501, x = y(y(x(xy))), is exactly the orders n ≡ 0, 1 (mod 4)** (CLM-C05-22; textbook
   Theorem 6.19; `proofs/paper/C05.md`, Theorem 14). The ETP notes list 501 with "unknown spectrum containing
   1, 4, 5, 8, 9", and its ETP commentary still called the spectrum unknown in September 2026. A probe of the
   open orders found a model of order 12, which no product of known orders gives, and the model showed the
   mechanism: x□y = x(xy) is a semi-symmetric quasigroup whose translations are the squares of the model's, and
   in a finite semi-symmetric quasigroup the product of the signs of the translations is (−1)^{n(n−1)/2}, since
   (x, y) ↦ (y, x□y) has order 3. (The Historian found this sign identity to be a case of the Janssen–Zappa
   parity relation for Latin squares; its use for 501 was found nowhere.) Square roots of the translations of
   x□y = −x−y over Z_n or Z_2×Z_2×Z_{n/4} give models of every admissible order. The necessity is proved in Lean
   (`law501_card_mod_four`); the construction is checked for every n ≤ 100 (EXP-C05-15).
2. **26 new certified gaps** at orders 8–13 for twelve laws (CLM-C05-15, -16, -25): for each pair every case CNF
   of the complete case split (Lemma 8) is refuted by a DRAT proof that drat-trim verified (EXP-C05-09, -10,
   -14), with controls of known answer. With EXP-C05-11 to -13, about 420 million proof lines were verified.
3. **Complete spectra** up to order 10 of the 13 laws x = y∗T (CLM-C05-17), every order resting on the lab's own
   certificate or re-checked model (EXP-C05-12 re-certifies every order n ≤ 7), and up to 13 for 467, 704 and the
   six laws x = y∗(S∗y) (CLM-C05-16, -25) — e.g. 1076: 1, 5, 13.
4. **Law 677 at order 12** (open in every source; premise of the ETP's last open finite implication 677 ⇒ 255):
   there is no quasigroup model (CLM-C05-24). The 195 cases were cut to 57 (EXP-C05-11) and each split by right
   cancellation (EXP-C05-13): all 57 quasigroup parts fall within 276,023 conflicts, and 51 non-quasigroup
   CNFs remain. A model of order 12 would be the smallest known non-right-cancellative model (now known:
   order 25, not 55 as our notes had said).
5. **Structure, in Lean:** finite models of every law x = y∗(S∗y) are quasigroups (CLM-C05-19), and so are those
   of 704 and 883 (CLM-C05-23).
6. **A conjecture refuted the same day.** "A law x = y∗T without a model of order 2 has none of order 2 (mod 4)"
   (CLM-C05-18) was drawn from the twelve open laws and refuted by the lab's own census: law 474 has a model of
   order 6 (Lean-certified). The restricted form for the twelve laws is kept as a conjecture (CLM-C05-21), now a
   theorem for 501.

**Method.** `systems/magma_split.py` generalises the batch-1.1 case split to every law x = y∗T, with division
clauses on both sides (Lemma 9′), an exhaustive quasigroup / non-quasigroup split of a case, and a new kind of
control: every known model, relabelled into its case, must satisfy that case's CNF (`admits`), which tests the
clauses that could wrongly exclude models directly. Checkpoints now carry the hashes of the code and of the
proof checker.

**What did not work.** 677 at order 12: the non-quasigroup half resisted a split by the missing (column,
value) pair and implied "star" clauses from the ETP's structure theory. 1313 at 14, 670 at 12 and 13, 883 and
907 at 12 have hard cases and are handed on. The first decision control of EXP-C05-10 (1083 at 12) would have
taken a day — its model sits in the 190th of 195 cases — and was replaced by the direct known-model check.
Simple sign invariants (of rows, columns, squaring) do not extend the 501 argument to other laws.

**Review.** The Skeptic (`reviews/skeptic_batch1.2.md`) re-decided 16 of the 24 pairs of CLM-C05-15/-16 with an
independent encoder and solver (every proof verified), audited every entry of the spectrum tables, checked the
proof of Theorem 14 step by step and rebuilt the construction, and found no encoding bug; it upheld every
claim, two with corrections to their evidence (501 at order 8 had no stored table; EXP-C05-10 had read its
case results from checkpoints — a clean re-run without them reproduced the result hash exactly), and in a
follow-up upheld CLM-C05-24 and -25 after re-deciding three quasigroup parts of 677 at order 12 independently. The Historian (`reviews/historian_501.md`,
`reviews/historian_677_nonqg.md`) found none of the new results in the sources read and corrected the lab's
statement about the smallest non-right-cancellative model of 677.

## 1. Number of experiments performed

| | count |
|---|---|
| research cycles | 20 (all complete) |
| experiment scripts (EXP-Cnn-mm, deterministic, hashed results) | 113 |
| recorded runs (first runs, reproducibility re-runs, corrected re-runs) | 203 |
| independent check scripts written by the Skeptic and Historian agents (`reviews/*_checks/`) | 86 |

Per-cycle counts are in `REPORT_DATA.md` §1. Every run stores its code hash,
the hash of `systems/`, the environment and a result hash. Timings are
excluded from the result hash, so `python -m lab verify` can re-run any cycle
and detect changes.

## 2. Systems investigated

Five foundational systems with explicit minimal assumptions
(`research/systems/SYSTEMS.md`). At the object level nothing beyond the stated
axioms is assumed; at the meta level proofs use ordinary mathematics (Lean's
type theory).

| system | objects and rules | cycles | claims |
|---|---|---|---|
| A — objects and transformations without numbers | words over an alphabet, rewriting rules | C01, C02, C03, C04, C11, C20 | 39 |
| B — invented composition rules | magmas given by tables or identities, anchored magmas x⋆0 = x+1 | C05, C06, C07, C08, C09, C13, C15, C16, C17, C18 | 62 |
| C — alternative representations of quantity | exchange (carry) systems, greedy numeration, circle products, integer codes | C02, C08, C09, C10, C11, C19 | 41 |
| D — structures based on relations | rewriting games, relational one-heap games, local graph products | C04, C07, C12, C14, C19 | 45 |
| E — local-rule dynamics over invented algebras | magma cellular automata, Fibonacci recurrences in magmas | C15, C16 | 37 |

(A cycle can use two systems, so the cycle lists overlap.) The twenty cycles
in one line each:

- quantity as the invariant of rewriting (C01);
- exchange systems and numeration (C02);
- termination of 0^p1^q → 1^r0^s (C03);
- derivation lengths and rewriting games (C04);
- spectra of magma laws (C05);
- successor-anchored magmas (C06, C13);
- mex-defined arithmetic (C07);
- circle products on recurrence numerations (C08, C09);
- the cost of counting (C10);
- pattern-terminated integer codes (C11);
- relational one-heap games (C12);
- the 256 local graph products (C14);
- magma automata and fast-forwarding (C15);
- Fibonacci dynamics in finite magmas (C16);
- deciding laws of finite magmas (C17);
- quasigroups as mixing primitives (C18);
- the longest Zeckendorf game (C19);
- the last open one-rule systems (C20).

## 3. Verified theorems

**131 claims are PROVEN.** The kind of evidence is read from each claim's
`proof_check`:

| evidence | claims |
|---|---|
| Lean 4 + Mathlib, nothing else listed | 14 |
| Lean core plus written or computational parts | 36 |
| computer-assisted (exhaustive search or certificates, stated trust base) | 15 |
| written proof only | 64 |
| published proof read in the literature | 2 |

Of the 117 PROVEN claims that are not fully formal, 115 were re-checked by an
independent Skeptic agent (UPHELD in a review table or marked in
`proof_check`). The other two were added after their cycle's review:

- CLM-C05-10, a simple exhaustive search;
- CLM-C19-15, whose argument came from the Skeptic and was written out by
  the Director, so a third check is still missing.

Selected theorems, the most substantial first:

| claim | statement (short) | evidence | novelty |
|---|---|---|---|
| CLM-C02-11, -04 | a carry rule m[k] → Σ b_j [k+j] terminates from every unary start iff Σ b_j < m; at Σ b_j = m a uniform glider never stops | two independent written proofs (spectral; Perron–Frobenius by the Skeptic) | potentially novel (critical case) |
| CLM-C04-09, -10 | aab → ba has derivational complexity D(n) = n − 1 − min{k : 2^k + k ≥ n}, not rational; D(n+2) equals OEIS A247983 (n ≥ 1) | written, reviewed | potentially novel (low/medium confidence) |
| CLM-C05-07, -08, -10 | new spectrum members and gaps for open laws of the Equational Theories Project, and their linear models over GF(q), q ≤ 128 | Lean tables; DRUP refutations checked by drat-trim, re-derived by the Skeptic with Kissat; exhaustive search | potentially novel relative to the ETP notes (small) |
| CLM-C06-06, -07; C13-02, -03, -04 | anchored magma laws whose models are arithmetic sets — the odd law, the golden law a² + a ≡ 1 (mod N), the W-family, exact finite spectra {1,3} and {1,2} | Lean + written | potentially novel (small) |
| CLM-C07-01, -05 | the associative mex operations are exactly 11 (44 specs), including + and min; row 2 of the mex-XOR operation is the Jacobsthal block swap | written, reviewed (the 33-spec argument is the Skeptic's) | potentially novel (small) |
| CLM-C09-03 | at least a proportion 1/φ² of the integers are irreducible for Knuth's circle product (window obstruction) | written, reviewed; checked to 10⁸ | potentially novel |
| CLM-C11-04, -07, -09 | the code T_011 is never longer than the Fibonacci code for n ≥ 5 and almost always 1 bit shorter; exact oscillation constants of the gain | written, reviewed | potentially novel (low confidence) |
| CLM-C12-04 | Grundy function of the deleting-divisors game: v₂(n) except on odd parts ≤ 15 | computer-assisted + written induction, reviewed; checked to 10⁸ | potentially novel |
| CLM-C14-02, -04, -05, -07 | exactly 20 of the 256 local graph products are associative (Lean decide); six are Kronecker products of a linear matrix form; complete bipartite graphs multiply as (order, imbalance) | Lean, written, reviewed | rediscovery (count) / potentially novel (characters) |
| CLM-C15-04 | the "fuse" magma automaton has linearly growing streaming width yet an O(L) fast-forward for every t | written, reviewed | potentially novel |
| CLM-C16-05, -07, -09, -15 | full-period quasigroups (every pair occurs once at distance 1 and once at distance 2); none of order 2–4, 3360 of order 5; no isotope of an even-order group qualifies; Fibonacci orbits in Laver tables | written + exhaustive, reviewed | potentially novel |
| CLM-C17-05 (with proof of uniqueness) | the anchor instance x⋆(y+1) = (x⋆y)⋆(x+1) forces at most one table for every N; for N ≤ 4096 a model exists exactly at powers of 2 (the Laver table) | uniqueness written (Skeptic's argument), existence pattern computed (EXP-C17-03) | not assessed |
| CLM-C19-02, -03 | the split phase of the longest Zeckendorf game ends at the lazy Fibonacci representation; L(F_k) = F_{k+2} − k − 2 − ⌊(k−1)²/4⌋ | written, reviewed (exhaustive check to F_12 = 233), arithmetic core in Lean | potentially novel |
| CLM-C19-14, -15 | L(n) is computed with O(log² n) moves from the lazy representation; D(n) ≤ 1 + (t+1)(t+6)/2 unconditionally, so L(n) = φ²n − O(log² n) | written (argument by the Skeptic, written out by the Director) | potentially novel / not assessed |
| CLM-C20-01, -02, -03 | aab → ababa has D(n) = 2^{n−2} − 1; aab → babaa has an exact per-word length; with them all 868 one-rule systems with \|l\| ≤ 3, \|r\| ≤ 5 are classified (480 terminate) | written, reviewed | termination rediscovered (barren rules); complexities potentially novel |

The full list of 131 is in `REPORT_DATA.md` §3, and Volume 6 of the textbook
prints the catalogue.

## 4. Conjectures

**4 CONJECTURE** and **39 COMPUTATIONALLY SUPPORTED** claims. Every
supported claim states its tested range, and none of them is presented as a
theorem.

The four conjectures:

| claim | conjecture | status of evidence |
|---|---|---|
| CLM-C04-16 | the rewriting games of aa → ab (Officers), aaa → b (0.007) and aaa → ab (0.06) are ultimately periodic | famous open octal-game questions; no claim beyond the literature |
| CLM-C09-05 | the circle irreducibles have density exactly 1/φ² | fraction in the "product zone" 0.255 (10⁶) → 0.231 (10⁸), consistent with decay to 0 but not decisive |
| CLM-C12-13 | subtract-a-Fibonacci-number has bounded Grundy values | weak: the Skeptic found new records 15 (n = 206,025) and 16 (n = 63,331,966) |
| CLM-C15-18 | bounded streaming width implies a fast-forward | no counterexample found among the order-3 automata |

Notable supported claims include:

- CLM-C01-08/-10: the common-border class-count formula.
- CLM-C08-02: non-Pisot circle products are never associative. The dominant
  root must exceed 1.
- CLM-C08-04: the sign-of-β rule for non-monotone shift sets.
- CLM-C13-10: spectra of one-variable laws are finite or cofinite.
- CLM-C14-13: two-graphs are a free commutative monoid under ⊕ — no collision
  among 53,703 multisets up to product order 64.
- CLM-C16-10: full-period quasigroups exist for every n ≥ 5 — examples for all
  n ≤ 26.
- CLM-C16-13: the maximal affine period equals the order of a 3×3 matrix —
  exhaustive for N ≤ 60.
- CLM-C19-05: a two-sequence recursion for the longest Zeckendorf game,
  inferred from all n < 30,000. It is confirmed on 103,799 further n up to
  10¹⁵ against the provably correct method of CLM-C19-14, and against
  strategy-free exhaustive search for n ≤ 233.

## 5. Refuted hypotheses

**49 REFUTED**, each with a counterexample in its record. They are kept in the
database and in Volume 9 of the textbook. They fall into three groups:

- *Bold hypotheses refuted by experiment, as designed* (most of the 49).
  Examples:
  - H-C03-2: termination iff r < 2q or s < 2p — 011 → 11100 loops.
  - H-C04-0: a rule with \|l\| ≤ 3 terminates iff l is not a factor of r —
    ab → bbaa loops.
  - H-C09-1: circle irreducibles have density 0 — at least 1/φ² of all
    integers are irreducible.
  - H-C13-1: anchored spectra are divisor-closed — x = x(x(xx)) misses only
    size 2.
  - H-C15-1: streaming width is bounded or geometric — the fuse magma.
  - H-C16-5: no quasigroup has a full-period pair map — 3360 of order 5.
  - H-C18-3: the nimber-field quasigroup gives an FNV-competitive hash —
    32,624 full collisions on near-duplicate keys.
  - H-C19-1…4: four structural models of the Zeckendorf-game deficit.
- *The laboratory's own published claims, refuted by its review process.*
  - CLM-C05-09: laws 677 and 1313 have spectrum {1} ∪ {odd n ≥ 5}. Refuted
    by linear models of order 16 over GF(16). The search had a blind spot:
    affine models had been tried only over ℤ_n.
  - CLM-C08-05: the measured associativity thresholds. Five of the eight
    were too small.
  - CLM-C08-07: the first corrected thresholds. Two were still too small.

  Both C08 failures have the same cause: random and small-input searches miss
  failures that happen only at inputs with extreme conjugate coordinates. The
  targeted search EXP-C08-07, aimed where the theory says failures live,
  reproduced every counterexample the Skeptic found.
- *Hypotheses settled by the literature.* For example, H-C03-1 is refuted by
  Zantema's problem a²b² → b³a³, which terminates.

## 6. Rediscoveries

**103 claims are REDISCOVERY**, with references in `novelty_basis`. The lab
treated a rediscovery as a validation of its method, not as a failure. The
most instructive ones:

- *C03 → Zantema–Geser.* The lab's divisibility conjecture for
  0^p1^q → 1^r0^s is equivalent to Theorem 1.1 of Zantema–Geser (tech. report
  UU-CS-1994-44; AAECC 2000). The Historian found the scanned report after the
  usual hosts refused the download.
- *C20 → McNaughton / Geser.* The two last open one-rule systems are "right
  barren", and barren one-rule systems terminate. The exact derivational
  complexities appear to be new.
- *C14-06 → Abiad–Butler–Haemers (2018).* S(G ⊕ H) + I = (S(G) + I) ⊗ (S(H) + I)
  for the symmetric-difference graph product. The lab's four searches missed
  the paper; the Skeptic found it.
- *C06-01 → Laver tables.* Left-distributivity with a successor anchor
  recovers Laver's tables; the lab's first citation of Laver's recursion was
  imprecise and was corrected.
- *C08-01 → Knuth / Arnoux / Messaoudi* (circle-product associativity), and
  C08-03 → Grabner–Pethő–Tichy–Woeginger 1994.
- *C01 → Gray–Steinberg* (one-relation monoids). C16-03 → the
  van Aardenne-Ehrenfest–de Bruijn count. C17-01 → Light's associativity test.
  C19-04 → a new, shorter proof of Cusenza et al.'s Theorem 1.4.

## 7. Potentially novel findings

**52 claims are POTENTIALLY NOVEL**: after web, OEIS and literature searches
(recorded per claim), nothing equivalent was found. The batch itself shows
how unreliable this label is. One such finding (CLM-C14-06) turned out to be
published, and the Historian's audit had earlier moved several others to
REDISCOVERY. A human expert should treat every item below as a candidate for
a literature check, not as a contribution. The most substantial, in our
judgement:

1. **Carry rules at the critical sum** (CLM-C02-04, -11): the complete
   termination classification from unary starts.
2. **Exact derivational complexities of one-rule systems**:
   - aab → ba (CLM-C04-09) and its identity with OEIS A247983, an open
     question in that entry (CLM-C04-10);
   - aab → babaa, with an exact per-word formula (CLM-C20-02).
3. **Anchored magma spectra as arithmetic sets** (CLM-C06-06/07, C13-02/03/04,
   C13-11): laws whose anchored models exist exactly for odd N, for N with a
   root of a² + a ≡ 1, or for an exact finite set.
4. **The Jacobsthal row** of the mex-XOR operation (CLM-C07-05).
5. **The window obstruction** for Knuth's circle product (CLM-C09-03): at
   least 1/φ² of all integers are irreducible.
6. **Grundy values of the deleting-divisors game** (CLM-C12-04).
7. **Full-period quasigroups** (CLM-C16-05/07/09) and Fibonacci orbits in
   Laver tables (CLM-C16-15).
8. **The fuse automaton** (CLM-C15-04): unbounded streaming width with an
   O(L) fast-forward, separating two notions of "predictability".
9. **The longest Zeckendorf game**:
   - the lazy-phase theorem and the closed form L(F_k) (CLM-C19-02/03);
   - a proved O(log² n)-move method (CLM-C19-14);
   - an unconditional O(log² n) bound on the deficit (CLM-C19-15);
   - a conjectured recursion (CLM-C19-05).
10. **New ETP spectrum data** (CLM-C05-07/08/10): small, and ETP
    participants could easily have them.

## 8. Performance improvements

Nine claims are algorithmic, each measured against stated baselines:

- **IMPROVEMENT** — 3 claims: CLM-C15-13, CLM-C15-15, CLM-C19-14.
- **MIXED** — 4 claims: CLM-C11-08, CLM-C15-14, CLM-C15-16, CLM-C17-04.
- **NO IMPROVEMENT** — 2 claims: CLM-C16-17, CLM-C18-13.

No claim of general or universal optimality is made. Timings come from a
shared, loaded machine and are meaningful only to their order of magnitude.

| claim | method vs baseline | result |
|---|---|---|
| CLM-C19-14 | longest Zeckendorf game from the lazy representation (proved, given Cusenza et al.'s strategy theorem) vs simulation of Θ(n) moves | n = 10⁷: 9.3·10⁻⁵ s vs 8.0 s; 109 moves at n = 10¹⁸. The first version rested on the conjectured recursion; the Skeptic showed that the lab's own theorems give a provable method |
| CLM-C15-13 | affine automaton fast-forward (operator powers, FFT) vs direct numpy simulation | about 10³× at t = 10⁵ (L = 1024); t = 10⁹ in milliseconds; **loses for t ≲ 20** |
| CLM-C15-15 | fuse automaton burn-time fast-forward vs simulation | about 10³× at t = 10⁵ (4,021× first run, 1,363× on re-run); **loses for t ≲ 20–70** |
| CLM-C15-14 | commutative-semigroup exponent arithmetic vs simulation | ~10²× at t = 10⁵, no gain near t = 10³ — MIXED |
| CLM-C15-16 | cycle detection as a generic fast-forward | exact when rows repeat (1590/1734 classes at L = 32); useless for long periods — MIXED |
| CLM-C17-04 | Light's generator test / anchored O(n²) test vs exhaustive n³ associativity check | certification of associative tables: 23–614× fewer probes when a small generating set exists, 1.7× for left-zero bands; **no gain for refutation** (an early-exit exhaustive check is cheaper). The first version overstated this; see §9 |
| CLM-C11-08 | fixed pattern-terminated codes vs Elias, Levenshtein, Fibonacci, Fraenkel–Klein C3, LEB128, Exp-Golomb | better by 0.34–3.06 bits/value on 5 of 12 heavy-tailed or wide-range sources and on both posting-list data sets; worse on light-tailed sources; implementation 4–10× slower — MIXED |
| CLM-C16-17 | magma Fibonacci generators vs PCG64 | NO IMPROVEMENT: every magma generator fails at least two tests that PCG64 passes |
| CLM-C18-13 | quasigroup string hashes vs FNV-1a, MX64, BLAKE2b, CRC32 | NO (significant) IMPROVEMENT: good cascades only match MX64/BLAKE2b in quality and are several times slower |

Benchmark data: EXP-C19-04, EXP-C15-03, EXP-C15-04, EXP-C17-01, EXP-C11-03/04/05/09,
EXP-C16-04, EXP-C18-02…05 and EXP-C14-07 (spectra of graph products from their
factors, about 3 orders of magnitude faster than direct diagonalisation; the
first claim of 4–5 orders was inflated by BLAS thread contention).

## 9. Unresolved problems

The open claims are listed in the textbook's Volume 10 and in `REPORT_DATA.md`
§9. The most important:

1. **Common borders** (C01): the one-relation class-count formula with two or
   more common borders, and the missing injectivity lemma in the one-border
   case.
2. **The anchored left-distributive instance** (CLM-C17-05): prove that the
   forced table fails at every N that is not a power of 2. This would give an
   O(N²) test for left-distributivity of anchored tables. *Settled in batch 1.1:
   published (Biane; Aguilera–Iannella) and proved in Lean from Laver's theorem
   (CLM-C17-08).*
3. **Circle products** (C08):
   - exact associativity thresholds — only lower bounds are certified
     (CLM-C08-08);
   - non-Pisot never associative (CLM-C08-02);
   - the sign-of-β conjecture (CLM-C08-04);
   - all three need exact computations of the fractal windows.
4. **Density of circle irreducibles** (CLM-C09-05).
5. **Spectra of ETP laws 677 and 1313**: the even orders 8–14 and the odd
   orders without linear models (17, 23, 29 for 677). *Batch 1.1: orders 8 and
   10 excluded for both laws (CLM-C05-11 … -13); 12 and 14 remain. Batch 1.2:
   1313 has no model of order 11 or 12; 677 has no quasigroup model of order 12,
   and the rest of order 12 is reduced to 51 CNFs (CLM-C05-24).*
6. **The longest Zeckendorf game**: prove the recursion CLM-C19-05 and the
   bound CLM-C19-09.
7. **Full-period quasigroups for all n ≥ 5** (CLM-C16-10), and the affine
   period conjecture (CLM-C16-13).
8. **Streaming width vs fast-forwarding** (CLM-C15-18).
9. **Octal games** 0.06 and Officers (CLM-C04-16). These are famous and hard.
10. **Graph products**: unique factorisation of two-graphs under ⊕ (CLM-C14-13)
    and of product 141 on connected graphs (CLM-C14-12).
11. **Mex rows** beyond the Jacobsthal row (C07).
12. **Grundy values** of subtract-a-Fibonacci (CLM-C12-13, now doubtful) and
    subtract-a-prime (CLM-C12-12).

## 10. Recommended next research directions

Ranked by expected value per unit of effort:

1. **Formalise the written proofs that carry the most weight** in Lean:
   - C20 Theorems 1–2 (run encoding and journeys);
   - CLM-C19-02;
   - the C12-04 induction;
   - the C07 Jacobsthal row;
   - the C09 window obstruction.

   64 PROVEN claims rest on written proofs alone, and each was reviewed by
   one agent at most. *(Batch 1.1 formalised four more theorems; 60 remain.)*
2. **Replace threshold searches by window computations** (C08). Computing the
   greedy windows (Rauzy-type fractals) exactly would settle CLM-C08-02, -04
   and -08 at once.
3. **Prove the anchored-LD conjecture** (CLM-C17-05). The forced-table
   structure is fully explicit. *(Done in batch 1.1, CLM-C17-08; what remains is
   a Lean proof of Laver's theorem itself.)*
4. **ETP spectra** (C05): decide 677 and 1313 at orders 8–14 with stronger
   symmetry breaking and certify (orders 8 and 10 done in batch 1.1); study which laws admit linear models over
   GF(2^k).
5. **Zeckendorf game** (C19): prove the recursion. Generalise the lazy-phase
   theorem to the generalised Zeckendorf games.
6. **A human literature pass** over the 52 POTENTIALLY NOVEL claims before
   anything is written up. Submitting sequences to the OEIS (L(n) and L(F_k)
   of C19, circle irreducibles, prime two-graph counts) is a human decision.
7. **Method changes for batch 2**:
   - certificate- or theory-guided searches instead of random sampling;
   - one timing protocol for both sides of every benchmark;
   - no wall-clock values outside `timings`;
   - every review finding fixed in code and re-run, not only in prose.

## Limitations of this batch (read before citing anything)

- **Independence is procedural, not epistemic.** The Inventor, Explorer,
  Formal Verifier, Skeptic, Historian, Application Researcher and Author roles
  were played by separate agent instances of the same language model, with
  separate contexts and instructions. No human reviewed any result. The
  reviews did catch real errors (§5, §8, §9). But two instances of one model
  can share a blind spot.
- **Written proofs.** 64 PROVEN claims rest on written proofs only, and 36
  have formal cores with written parts (after batch 1.1: 60 and 43). "PROVEN" means a proof was written
  and, in most cases, checked once by an independent agent. It does not mean
  peer-reviewed.
- **Searches are not proofs.** Every COMPUTATIONALLY SUPPORTED claim states
  its range. Twice in C08 the lab's own searches missed rare
  counterexamples.
- **Novelty.** Searches were limited to the open web, the OEIS (cached) and
  the papers that could be retrieved. Several sources were paywalled or
  unreachable, and each failed retrieval is recorded. "Potentially novel"
  has already proved wrong at least once (CLM-C14-06).
- **Performance.** All timings come from Python implementations on a shared
  machine. They support statements about orders of magnitude only. No
  security claims are made for any hash or generator.

## Deliverables

| deliverable | location |
|---|---|
| research journal (append-only; 239 entries after batch 1.1, which removed 32 duplicate lines written by a sync bug) | `journal/JOURNAL.md`, `journal/entries.jsonl` |
| discovery database and audit log | `db/claims/`, `db/experiments/`, `db/audit_log.jsonl`, `db/DATABASE.md`, `DISCOVERY_INDEX.md` |
| research cycles (ten-step reports + machine-readable records) | `research/cycles/*/README.md`, `record.yaml` |
| reproducible code | `systems/` (mathematical systems), `experiments/` (114 scripts), `lab/` (infrastructure, incl. `python -m lab check`) |
| raw results and benchmarks | `results/EXP-*.json` |
| proofs | `proofs/lean/Infinity/*.lean` (334 theorems after batch 1.1), `proofs/lean_results.json`, `proofs/paper/C01.md … C20.md` |
| independent reviews and their check code | `reviews/skeptic_*.md`, `reviews/historian_*.md`, `reviews/*_checks/` |
| textbook *Beyond Conventional Mathematics*, version 1.1 | `textbook/build/book.pdf` (129 pages), `book.html`; sources `textbook/src/`; 21 chapters in 10 volumes and a generated corrections log |
| statistics and tables for this report | `reports/batch_statistics.json`, `reports/REPORT_DATA.md` |
| continuation instructions | `CONTINUATION.md`, `checkpoints/state.json` |
| batch 1.1 sprint plan and reproducibility audit | `reports/PM_PLAN_batch1.1.md`, `reports/REPRODUCIBILITY_batch1.1.md` |

## Key literature consulted

- H. Zantema, A. Geser, *A complete characterization of termination of
  0^p1^q → 1^r0^s*, tech. report UU-CS-1994-44 —
  [scan](https://ics-archive.science.uu.nl/research/techreps/repo/CS-1994/1994-44.pdf).
- A. Geser, *Termination of string rewriting rules that have one pair of
  overlaps*, ICASE Report 2002-33 —
  [NASA NTRS](https://ntrs.nasa.gov/api/citations/20020088729/downloads/20020088729.pdf).
- A. Abiad, S. Butler, W. H. Haemers, [arXiv:1801.01149](https://arxiv.org/abs/1801.01149) (§5).
- The Equational Theories Project — [site](https://teorth.github.io/equational_theories/),
  [paper arXiv:2512.07087](https://arxiv.org/abs/2512.07087); B. Le Floch,
  [Spectra of equational laws](https://leanprover.zulipchat.com/user_uploads/3121/apvdoKH3jwd1mrnPxZcvlXL_/spectrum.pdf).
- Zeckendorf games: [arXiv:2009.09510](https://arxiv.org/abs/2009.09510),
  [arXiv:2210.11038](https://arxiv.org/abs/2210.11038), Cusenza et al.,
  [Fibonacci Quarterly 60](https://www.mathstat.dal.ca/FQ/Abstracts/60-1/cusenza.pdf).
- Laver tables: P. Biane, *Laver tables and combinatorics*,
  [Sém. Lothar. Combin. 80 (2019) B80c](https://www.mat.univie.ac.at/~slc/wpapers/s80biane.pdf)
  (its arXiv v1, [arXiv:1810.00548](https://arxiv.org/pdf/1810.00548), states the recursion for all q);
  J. P. Aguilera, M. Iannella, *Non-dyadic Laver algebras*, [arXiv:2610.06106](https://arxiv.org/abs/2610.06106).
- Batch 1.1 audit sources: the ETP blueprint chapter on
  [equation 677](https://teorth.github.io/equational_theories/blueprint/677-chapter.html);
  S. Oh, H. Yoo, T. Yun, [arXiv:1108.6143](https://arxiv.org/abs/1108.6143);
  M. J. de C. Lima, V. C. da Rocha Jr., [JCIS 2013](https://jcis.sbrt.org.br/jcis/article/download/17/11/127);
  A. S. Fraenkel, S. T. Klein, [robust universal codes](https://u.cs.biu.ac.il/~tomi/Postscripts/robust.pdf);
  C. Dürr, I. Rapaport, G. Theyssier, [arXiv:cs/0210008](https://arxiv.org/abs/cs/0210008);
  P. Klimov, [arXiv:2604.05754](https://arxiv.org/abs/2604.05754).
- One-rule string rewriting survey: [arXiv:2608.19397](https://arxiv.org/pdf/2608.19397).
- drat-trim proof checker: [source](https://raw.githubusercontent.com/marijnheule/drat-trim/master/drat-trim.c).

Every other reference is recorded in the `novelty_basis` of the claim that
uses it.
