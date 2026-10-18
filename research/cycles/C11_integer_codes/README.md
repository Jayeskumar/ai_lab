# Cycle C11 — Pattern-terminated universal integer codes

**Branch:** C-A: representations → application (data compression), using C01's border theory (System A) · **Status:** complete
**Experiments:** EXP-C11-01 … EXP-C11-09 · **Claims:** CLM-C11-01 … CLM-C11-09
**Proofs:** `proofs/paper/C11.md`; `proofs/lean/Infinity/C11_Codes.lean` (prefix-freeness, no axioms)
**Code:** `systems/codes.py` (encoders/decoders), `systems/code_bench.py` (exact expected lengths)

## Step 1 — Hypotheses

The Fibonacci code is "the binary words in which 11 occurs for the first time
at the end". Replace 11 by an arbitrary terminator pattern p: the invented
family T_p. Question: *which terminator is best, and are these codes useful?*

| ID | Hypothesis | Proposer | Outcome |
|---|---|---|---|
| H-C11-1 | Among length-k terminators, 1^k (and 0^k) maximise the growth rate λ_p. | Explorer | **proved** (Theorem 2), verified k ≤ 10 |
| H-C11-2 | (bold) Hence 1^k is the best length-k terminator beyond small n. | Inventor | **refuted** at practical sizes (k ≥ 4) |
| H-C11-3 | Unbordered terminators of length k have the (k−1)-bonacci growth rate. | Explorer | **proved** (Theorem 3) |
| H-C11-4 | Some new pattern code beats all classical universal codes on a realistic source. | Application Researcher | **supported**: 5/12 synthetic sources, 2/4 data sets |
| T-C11-A | f_u = partial sums of f_{1^k} for unbordered u (k+1 letters). | Formal Verifier | **proved**; T_011 beats Fibonacci by one bit almost everywhere |
| (6→8) | Average gain log_λ(1/(λ−1)); then "the average converges". | Explorer | **both refuted**; oscillation between two explicit constants proved |
| H-C11-5 | T_011 also beats Fraenkel–Klein's C3 (1996), the classical improvement of C1 that already decodes by the pattern 011. | Skeptic | **proved** except n ∈ {2, 4, 8} (Corollary 6); C3 still wins on light-tailed sources |

## Step 2 — Definitions

T_p, codeword counts f_p(L), cumulative counts, length function L_p(n),
growth rate λ_p (smallest positive root of x^k + (1 − 2x)c_p(x)), with c_p the
autocorrelation polynomial of C01. Baselines: Elias γ, δ, ω, Levenshtein,
Fibonacci C1, LEB128 varint, Exp-Golomb(k), Golomb/Rice (tuned per source).
Codes defined on n ≥ 0 are applied to n − 1.

## Step 3 — Falsification design

Round trips and prefix checks for every code (a broken implementation would
invalidate every benchmark); exact count identities with big integers; exact
length comparisons over 2·10⁶ integers and over Fibonacci blocks up to L = 90;
exact expected lengths (no sampling) for synthetic sources; tuned Golomb–Rice
as a deliberately strong baseline; refutation-seeking checks of every
predicted constant at several scales.

## Steps 4–5 — Implementation and execution

| Experiment | Outcome |
|---|---|
| EXP-C11-01 | 9 baseline + 61 pattern + 8 Golomb codes: 0 problems (round trips incl. n up to 2⁶⁰, prefix-free, monotone lengths); Kraft partial sums ≥ 0.999999999993; Fibonacci C1 ≡ T_11 for n ≤ 2·10⁵ |
| EXP-C11-02 | all 2044 patterns of length 2–10: 1^k, 0^k uniquely maximal (0 violations); unbordered ⇒ (k−1)-bonacci λ (0 violations); rival terminators beat 1^k at many n ≥ 1000 for k = 4, 5, 6 (up to n ≈ 1.3·10¹⁹ for k = 6); count sequences all in the OEIS (A000071, A005314, A059633, A008937, A112575) |
| EXP-C11-03 | 12 synthetic sources, exact expectations (table below) |
| EXP-C11-04 | prime gaps ≤ 10⁷ (raw/halved) and two simulated posting lists |
| EXP-C11-05 | throughput (CPython): pattern codes ≈ 3 µs/value vs 0.4–0.7 µs for the Elias codes, 2.1 µs Fibonacci |
| EXP-C11-06 | x/(1−x) identity: 0 mismatches (unbordered lengths 3–9); T_011 longer than Fibonacci only for n ∈ {1, 2, 4}; for n ≤ 2·10⁶ it is 1 bit shorter on 1,999,568 values, equal on 429; predicted average gain refuted for k ≥ 3 |
| EXP-C11-07 | corrected constant matches at 2⁴⁰ and 2¹²⁰ but not at 2⁸⁰ (0.310 for k = 3): the average does not converge |
| EXP-C11-08 | running average at level ends = (2−λ)/(λ−1)² and at saved-segment ends = λ(2−λ)/(λ−1), to 6 digits for k = 2..6 (liminf/limsup: k = 2: 1/1; k = 3: 0.228155/0.352201; k = 4: 0.084194/0.150533; k = 5: 0.036495/0.069304; k = 6: 0.016970/0.033108) |
| EXP-C11-09 | Fraenkel–Klein C3 implemented from the paper (first 12 codewords match its list, 0 problems): for n ≤ 2·10⁶, C3 is longer than C1 only at n = 1 and T_011 longer than C3 only at n ∈ {2, 4, 8}; cum_011/cum_C3 → φ²/2 = 1.309017; C3 beats T_011 on 7 light-tailed sources/data sets and loses on the other 9 |

**Redundancy (bits above entropy) on synthetic sources (EXP-C11-03):**

| source | H | γ | δ | ω | C3 | Fibonacci | LEB128 | T_111 | T_011 | T_0111 | T_101 | tuned Golomb | tuned Exp-Golomb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Zipf 1.1 | 10.90 | 3.66 | 1.20 | 2.00 | 0.60 | 0.77 | 1.98 | 0.25 | 0.42 | 0.33 | **0.19** | 5.38 | 1.72 |
| Zipf 1.5 | 4.62 | 0.28 | 0.26 | 0.40 | 0.38 | **0.10** | 3.96 | 0.83 | 0.52 | 1.38 | 0.60 | 6.07 | 0.25 |
| Zipf 2.0 | 2.36 | **0.08** | 0.32 | 0.22 | 1.19 | 0.61 | 5.68 | 1.56 | 1.38 | 2.36 | 1.42 | 2.00 | **0.08** |
| Zipf 3.0 | 0.98 | 0.44 | 0.58 | 0.47 | 2.11 | 1.29 | 7.02 | 2.28 | 2.23 | 3.23 | 2.24 | **0.39** | 0.44 |
| geometric 0.5 | 2.00 | 0.27 | 0.65 | 0.38 | 1.32 | 0.82 | 6.00 | 1.82 | 1.63 | 2.63 | 1.64 | **0.00** | 0.27 |
| geometric 0.1 | 4.69 | 1.02 | 1.42 | 1.64 | 0.53 | 0.59 | 3.31 | 1.37 | 0.72 | 1.67 | 0.93 | **0.04** | 0.30 |
| geometric 0.01 | 8.08 | 3.68 | 2.70 | 3.89 | 1.20 | 1.56 | 2.13 | 1.57 | 0.93 | 1.45 | 1.25 | **0.03** | 0.28 |
| geometric 0.001 | 11.41 | 6.88 | 3.98 | 4.96 | 2.51 | 2.93 | 3.63 | 1.99 | 2.02 | 1.74 | 1.94 | **0.03** | 0.28 |
| uniform 2⁸ | 8 | 5.08 | 3.98 | 4.84 | 2.27 | 2.67 | 4.00 | 2.50 | 1.93 | 2.32 | 2.23 | **0.50** | 1.00 |
| uniform 2¹⁶ | 16 | 13.00 | 6.00 | 6.00 | 5.71 | 6.15 | 5.98 | 3.57 | 5.15 | 3.30 | 4.04 | **0.50** | 1.00 |
| uniform 2³² | 32 | 29.00 | 8.00 | 10.00 | 12.76 | 13.19 | 7.50 | 5.73 | 12.19 | 5.49 | 7.70 | **0.50** | 1.00 |
| log-uniform 10⁶ | 13.41 | 5.84 | 1.94 | 3.03 | 1.36 | 1.64 | 1.86 | 0.47 | 1.05 | **0.40** | 0.56 | 3.93 | 2.00 |

(Best fixed universal codes not shown: Exp-Golomb(2) on geometric 0.1 (0.30),
Exp-Golomb(4) on geometric 0.01 (0.70) and uniform 2⁸ (1.75), Levenshtein on
Zipf 3 (0.39) and geometric 0.5 (0.19), T_00111 on uniform 2³² (4.44). The tuned columns choose the
Golomb modulus M or the Exp-Golomb order k per source, so they are not universal
codes; their parameters are in `benchmarks/C11/`. The C3 column (Fraenkel–Klein
1996, a uniquely decipherable non-prefix code) is from EXP-C11-09.)

**Bits per value on data (EXP-C11-04):**

| data | H₀ | δ | C3 | Fibonacci | LEB128 | T_011 | T_0111 | T_101 | tuned Golomb | tuned Exp-Golomb |
|---|---|---|---|---|---|---|---|---|---|---|
| prime gaps ≤ 10⁷, raw | 4.17 | 7.41 | 5.94 | 6.18 | 8.00 | 6.14 | 7.07 | 6.42 | **5.27** | 5.58 |
| prime gaps, halved | 4.17 | 5.64 | 4.92 | 4.94 | 8.00 | 5.11 | 6.06 | 5.27 | **4.27** | 4.58 |
| posting list, geometric gaps | 11.36 | 15.40 | 13.93 | 14.36 | 15.06 | 13.44 | 13.15 | 13.36 | **11.45** | 11.70 |
| bursty posting list | 10.71 | 12.85 | 11.82 | 12.15 | 12.65 | 11.54 | 11.52 | **11.47** | 12.80 | 11.79 |

(Best fixed universal code on the prime gaps: Exp-Golomb(4), 5.72 bits, raw;
Exp-Golomb(2), 4.58 bits, halved.)

## Step 6 — Analysis

* **What the terminator controls.** The growth rate λ_p sets the asymptotic
  cost (log₂ n / log₂ λ_p bits); all-ones terminators maximise it
  (EXP-C11-02: λ_11 = 1.618034, λ_101 = 1.754878, λ_111 = λ_0111 = 1.839287,
  λ_1011 = λ_0110 = 1.866760, λ_0101 = 1.883204, λ_1111 = 1.927562,
  λ_11111 = 1.965948). But the
  *constant* matters at every practical size: an unbordered terminator of
  length k+1 has the same growth rate as 1^k and strictly more codewords at
  every length (its counts are the partial sums of 1^k's).
* **A clean win over the Fibonacci code.** T_011 (any unbordered 3-letter
  terminator) is never longer than the Fibonacci code for n ≥ 5 and is
  exactly one bit shorter for all but a vanishing fraction of integers. It also
  beats Fraenkel–Klein's C3, the classical improvement of C1 (which is not even
  prefix-free), except at n = 2, 4, 8; C3 recovers only 0.40–0.48 of that bit on
  average (measured over n ≤ 2⁴⁰, 2⁸⁰, 2¹²⁰).
* **Where pattern codes win in practice.** Heavy-tailed or wide-range sources
  (Zipf 1.1, log-uniform, geometric 0.001, uniform 2¹⁶–2³², bursty posting
  list): 0.3–3.1 bits per value better than every fixed classical universal
  code, Fraenkel–Klein's C3 included. Only on the heavy-tailed ones (Zipf 1.1,
  log-uniform, bursty posting list) do they also beat Golomb and Exp-Golomb
  codes tuned to the source; on uniform and geometric sources the tuned codes
  are far better (0.03–1 bit of redundancy).
* **Where they lose.** Light-tailed sources (Zipf ≥ 1.5, geometric ≥ 0.01,
  prime gaps): γ, Levenshtein, Fibonacci or Exp-Golomb are better; on
  geometric sources a tuned Golomb–Rice code is nearly optimal (≤ 0.04 bits
  redundancy) and no universal code comes close. C3 beats T_011 on Zipf ≥ 1.5,
  geometric 0.5 and 0.1 and the prime gaps, where its three shorter codewords
  (n = 2, 4, 8) carry much mass. Pattern codes also cost 4–10× more time than
  the Elias and Exp-Golomb codes (≈1.5× the Fibonacci code) in our unoptimised
  CPython implementation.

## Step 7 — Proofs and counterexamples

Theorems 1–3, Corollaries 4 and 6 and Proposition 5 in `proofs/paper/C11.md`;
prefix-freeness and unique parsing machine-checked in Lean. Refuted: H-C11-2
(1^k optimal at practical sizes), the log-form average-gain prediction, and the
claim that the average gain converges.

## Step 8 — Literature (Historian)

* Elias (1975); Apostolico & Fraenkel, IEEE Trans. IT 33 (1987) 238–245;
  Fraenkel & Klein, Discrete Applied Math. 64 (1996) 31–55 (robust universal
  complete Fibonacci codes); the "N consecutive ones" generalisation
  (Wikipedia, *Fibonacci coding*) — T_11 and T_{1^k} are **rediscoveries**.
* Closest prior art for T_011: Fraenkel & Klein's code C3 (same paper,
  Propositions 5–6): uniquely decipherable but not prefix-free, decoded by
  searching for 011, never longer than C1 for n > 1. T_011 is a prefix code and
  beats C3 except at n = 2, 4, 8 (Corollary 6). The idea of improving C1 with a
  011-based code is therefore theirs.
* Guibas & Odlyzko (1981) give the generating functions (Theorem 1c) and the
  correlation ordering behind Theorem 2 — **rediscovery**.
* Closest to the unbordered terminators: Gilbert's prefix-synchronised codes
  (IRE Trans. IT 6, 1960) and Guibas–Odlyzko's *Maximal prefix-synchronized
  codes* (SIAM J. Appl. Math. 35, 1978), where markers of the form 1…10 are
  optimal at finite lengths — the same phenomenon in a fixed-length setting;
  and Anisimov & Zavadskyi's multi-delimiter codes with delimiters 01…10
  (IEEE Trans. IT 63, 2017; arXiv:1508.01360), reported superior to Fibonacci
  codes. We found no statement of Corollaries 4, 6 or Proposition 5 for universal
  integer codes; marked **potentially novel, low confidence**.
* OEIS: all codeword-count sequences used are catalogued.

## Step 9 — Applications (Application Researcher)

A practical recommendation, with its limits: for heavy-tailed integer streams
of unknown scale (posting lists with bursty terms, log-uniform magnitudes), a
fixed pattern code such as T_0111 or T_101 is a strong universal choice; for
geometric gaps use Golomb–Rice; for values of known range use a tuned Golomb or
Exp-Golomb code; for small values use γ, Fibonacci or C3. All
improvements are empirical, measured on 12 synthetic sources and 4 data sets;
none is claimed optimal. Optimised implementations (table-driven decoding)
were not attempted, so the speed penalty is unresolved.

## Step 10 — Documentation

`record.yaml`; benchmark tables in `benchmarks/C11/`. Proposed textbook
chapter (for the Scientific Author): "Codes from forbidden patterns"
(applications).

## Next directions

1. Table-driven (byte-wise) decoders for T_p and a fair speed comparison.
2. Multi-pattern terminators (a set of delimiters, as in multi-delimiter
   codes) — best sets for given sources.
3. Robustness/synchronisation after bit errors, the classical selling point of
   Fibonacci codes, for unbordered terminators.
