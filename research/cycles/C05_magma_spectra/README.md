# Cycle C05 — Spectra of single-identity magma varieties

**Branch:** B (invented composition rules) · **Status:** complete
**Experiments:** EXP-C05-01 … EXP-C05-05 · **Claims:** CLM-C05-01 … CLM-C05-09
**Proofs:** `proofs/lean/Infinity/C05_Magmas.lean`, `proofs/paper/C05.md`
**Toolkit:** `systems/magma.py` (terms, identities, exact SAT encoding, isomorphism classes, affine models)

## Step 1 — Hypotheses

System B assumes nothing about a binary operation except that it is total.
Research question: *can a single invented identity t(x, y) = x — with no
other axioms — force arithmetic restrictions on the number of elements of a
finite model?*

| ID | Hypothesis | Proposer | Outcome |
|---|---|---|---|
| H-C05-1 | *(bold)* Every identity t = x has spectrum {1} or all n. | Inventor | **refuted** (law 167 and 57 other identities) |
| H-C05-Q | *(bold)* Every nontrivial identity t = x forces its finite models to be quasigroups. | Inventor | **refuted** (a 4-element non-Latin model of law 167) |
| H-C05-A | *(bold)* Full spectrum ⇔ affine models x∗y = ax + by + c over every ℤ_n. | Inventor | see EXP-C05-05 |
| H-C05-2 | Restricted spectra are classical design spectra (Mendelsohn, Steiner, Euler's 36 officers…). | Explorer | partly supported |
| H-C05-3 | The open spectra of the ETP notes can be extended by SAT to n ≤ 12. | Verifier | see EXP-C05-03 |

## Step 2 — Definitions

Terms, identities, models, *spectrum* (set of orders of finite models),
*nontrivial* identities (x occurs in t but is neither its leftmost nor its
rightmost leaf — otherwise a projection is a model of every order, or only
n = 1 is possible) and the exact SAT encoding are in `proofs/paper/C05.md`
(Lemma 0). Identities are taken up to renaming; mirror images (t read
right-to-left) have equal spectra.

## Step 3 — Falsification design

* Exhaustive census of **all 115 nontrivial two-variable identities t = x
  with 2–4 operations**, SAT model existence for n = 1..7 (each UNSAT/SAT
  answer recorded; budgets bounded, UNKNOWN reported as such).
* Model enumeration up to isomorphism to test quasigroup forcing (H-C05-Q).
* Affine-model search over ℤ_n for every identity (H-C05-A).
* SAT with a *sound* implied constraint (rows of the Cayley table are
  permutations for laws x = y∗(…), Lemma 1) to push open ETP spectra to n ≤ 12,
  cross-checking every size already stated in the literature.
* Every satisfiable answer is re-verified in Python, and every new membership
  is re-certified by Lean's kernel (`decide`).

## Steps 4–5 — Implementation and execution

(results table below)

## Step 6 — Analysis

(see below)

## Step 8 — Comparison with existing mathematics (Historian)

* **Spectra of order ≤ 4 laws were studied by the Equational Theories
  Project (ETP).** The write-up "Spectra of order-3 equations" (Lean Zulip,
  attributed in Le Floch's notes to Ben Gunby-Mann) proves: law 66,
  x = y(x(yy)), has spectrum {n ≡ 0,1 mod 3}∖{6} (Mendelsohn triple systems);
  law 167, x = (yx)(xy), has spectrum {n ≡ 0,1 mod 4}; law 168 (central
  groupoids, Knuth) has spectrum {k²}. B. Le Floch's notes "Spectrum of
  equational laws" (Lean Zulip, `spectrum.pdf`) treat all 741 classes of order
  ≤ 4 and list 48 laws with possibly non-full spectrum, many with "unknown
  spectrum starting with …". The ETP paper (arXiv:2512.07087, Sec. 9)
  separates full from non-full spectra and defers detailed spectra to a
  forthcoming publication.
* Hence the **census itself is a REDISCOVERY**: the patterns we found
  independently (before reading the notes) agree with the ETP knowledge.
  What this cycle adds: (i) a machine-checked (Lean) proof of the necessity
  half of the law-167 theorem; (ii) SAT-decided spectrum memberships for open
  laws at sizes the notes do not state, with Lean certificates for the
  memberships (EXP-C05-03/04); (iii) the refutations of H-C05-Q and H-C05-A in
  this family.
* Classical spectra used for comparison: Mendelsohn triple systems
  (v ≡ 0,1 mod 3, v ≠ 6; N. S. Mendelsohn 1971); Steiner triple systems
  (v ≡ 1,3 mod 6; Kirkman 1847); pairs of orthogonal Latin squares (all n
  except 2, 6; Bose–Shrikhande–Parker 1959–60); Stein quasigroups
  (Bennett–Mendelsohn, Bull. Austral. Math. Soc.).
