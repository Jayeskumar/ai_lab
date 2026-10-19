# Cycle C18 — Invented operations as mixing primitives

**Branch:** B (applications) · **Status:** complete
**Experiments:** EXP-C18-01 … EXP-C18-05 · **Claims:** CLM-C18-01 … CLM-C18-13
**Proofs:** `proofs/paper/C18.md` (Theorems 1–7), `proofs/lean/Infinity/C18_Quasigroups.lean`
(5 theorems, standard axioms only) · **Module:** `systems/quasigroup_hash.py`

*None of this is a security evaluation; no claim of cryptographic strength is made.*

## Step 1 — Hypotheses

Question (Phase 5): *can the lab's invented operations — Latin squares, the
nimber field of C07, the anchored quasigroups of C06 — serve as practical
non-cryptographic hash mixers, measured against standard baselines?*
Construction: Markovski's e-transformation b_i = b_{i−1} * a_i, iterated.

| ID | Hypothesis | Proposer | Outcome |
|---|---|---|---|
| H-C18-1 | *(bold)* A random Latin square with 2 passes + a reverse pass has BLAKE2b-level avalanche. | Inventor | holds — but irrelevant: the same hash fails structured key sets |
| H-C18-2 | Structured quasigroups are worse than a random Latin square (max avalanche bias). | Explorer | proved for T-function/affine ones; **inconclusive** for x + c(y) |
| H-C18-3 | *(bold)* The nimber-field quasigroup gives a hash competitive with FNV-1a. | Inventor | **refuted** (z = 1084, 32,624 full collisions) |
| H-C18-4 | Quasigroup hashes are slower than FNV-1a. | Application Researcher | holds |
| H-C18-5 | Forward-only variants have max bias 1/2. | Formal Verifier | holds; proved |
| H-C18-6 | The one-pass x + c(y) hash fails on near-duplicates. | Skeptic | holds |
| H-C18-7 | The tail-information bound on data. | Formal Verifier | holds exactly (256 values) |
| H-C18-8 | *(bold)* An 8-pass cascade over LS, ISO, NIMINV passes every test. | Application Researcher | **refuted** by NIMINV; LS and ISO pass |
| H-C18-9 | The cascade over x + c(y) still fails bit independence. | Skeptic | **refuted** (0.176) |

## Step 2 — Definitions

Quasigroups of order 256: a random Latin square (row-by-row random matchings —
not uniform), a random isotope of ℤ/256, the nimber inversion quasigroup
(x ⊕ y)⁻¹ (the nim-product itself is not a quasigroup: row 0 is zero),
affine 77x + 141y + 5, x ⊕ y, and the anchored x + c(y) and (x + 1) ⊕ y of C06.
QG(T, p, rev): message key ‖ len ‖ padding, p e-transformations, optional
reversed pass, output = last 8 bytes. QC(T, 8): eight passes in parallel,
output = final state of each. Baselines: FNV-1a-64, MX64 (multiply-xorshift +
splitmix64 finaliser), BLAKE2b-64, CRC32.

## Step 3 — Falsification design

Every hypothesis had a numeric threshold fixed before running (Step 1 and the
META blocks). Avalanche noise is calibrated by BLAKE2b; key sets include the
structured families (sequential decimals, near-duplicates, word-like strings)
on which weak hashes fail.

## Steps 4–5 — Implementation and execution

| Experiment | Outcome |
|---|---|
| EXP-C18-01 | 7 quasigroups verified; T-function/affinity classification; all structural predictions hold |
| EXP-C18-02 | reverse-pass LS/ISO/NIMINV variants and MX64 at BLAKE2b's noise floor; forward-only variants, FNV-1a, AFF, ALP, XOR, CRC32 fail; x + c(y): ideal flip rates, BIC 1.0 |
| EXP-C18-03 | every reverse-pass variant fails structured key sets (32,624 full collisions on near-duplicates) |
| EXP-C18-04 | throughput (indicative, load-dependent): FNV-1a 640, MX64 428, CRC32 127, BLAKE2b 74, quasigroup 11–52 MB/s (20–98 MB/s on the Skeptic's re-run; the ordering is stable) |
| EXP-C18-05 | tail bound attained exactly; cascades QC-LS, QC-ISO pass everything; QC-NIMINV biased; ~10–13 MB/s |

Incidents: the first EXP-C18-03 run failed (words passed as str) and was
fixed; a container restart interrupted the cycle after EXP-C18-01 and the
remaining experiments were run from the committed scripts.

## Step 6 — Analysis

* The decisive finding is a theorem (Theorem 3): the last 8 bytes of an
  e-transformation are determined by **one state byte** plus 7 input bytes. A
  byte-level e-transformation is a "narrow pipe" with an 8-bit state, so
  tail-output hashes collide massively on structured keys — no matter how good
  their avalanche looks. Single-bit avalanche tests are blind to this.
* Arithmetic (T-function) and GF(2)-affine quasigroups are disqualified by
  theorem; the anchored x + c(y) hides its weakness from the avalanche test
  and shows it only in bit independence.
* The fix suggested by the theorem — keep a full 8-byte state (the cascade) —
  works for random-like quasigroups, but the result is only as good as MX64,
  and much slower.

## Step 7 — Proofs and counterexamples

Lean: `eT_length`, `eT_injective`, `eT_ne_of_ne`, `eT_append`,
`eT_tail_factors`. Written: Theorems 1–7. Counterexamples: QG-NIMINV p2+rev on
sequential and near-duplicate keys (H-C18-3); QC-NIMINV d8 (H-C18-8);
QC-ARP d8 (H-C18-9).

## Step 8 — Comparison with existing mathematics (Historian)

* e/d-transformations and their bijectivity: Markovski, Gligoroski, Bakeva,
  *Quasigroup string processing* Part 1 (1999), as cited in
  [US 8041031](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8041031)
  and [Part 4](https://www.academia.edu/115482463/Quasigroup_String_Processing_Part_4). **REDISCOVERY.**
* T-functions: Klimov and Shamir (CHES 2002; [FSE 2004](https://www.iacr.org/archive/fse2004/30170001/30170001.pdf);
  [overview](https://en.wikipedia.org/wiki/T-function)). **REDISCOVERY** in substance.
* Quasigroup hashes in the SHA-3 competition used huge quasigroups in
  wide-pipe designs: Edon-R ([submission](https://ehash.isec.tugraz.at/uploads/7/74/Edon.pdf);
  cryptanalysis by Khovratovich, Nikolić and Weinmann) and NaSHA
  ([ePrint 2008/519](https://eprint.iacr.org/2008/519)); Gligoroski's quasigroup
  one-way functions ([ePrint 2005/352](https://ia.cr/2005/352)). The
  byte-level tail-information bound was not found stated explicitly. **NOT
  ASSESSED** (elementary).

## Step 9 — Applications

**No significant improvement** (CLM-C18-13). The best quasigroup constructions
match MX64 and BLAKE2b in quality on our tests but are several times slower;
MX64 is at least as good on every axis within noise (some quasigroup hashes
are numerically slightly better on single statistics, within noise). Against
FNV-1a alone, the good cascades mix better but are much slower; FNV-1a's
z = −9.8 on sequential keys means *more* uniform than random, not a defect.
Not a security evaluation.

## Step 10 — Documentation

`record.yaml` (13 claims, journal). Textbook: Chapter 20, "Quasigroups as
mixers: an honest negative" (Volume 8).

## Next directions

1. Larger quasigroups (order 2¹⁶) in a wide-state cascade, optimised C, full
   SMHasher-style testing.
2. Why the nimber-inversion cascade keeps a bias (x * x = 0, commutativity).
3. A probabilistic model of cascade depth versus avalanche bias.
