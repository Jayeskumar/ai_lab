# Research Journal

_Rendered from the append-only log `journal/entries.jsonl`. Entries are never edited or removed; corrections appear as later `revision` entries._


## C01

### [2026-10-18T06:44:01Z] Research Director — decision (`C01-01`)

Opened Branch A with the question "can quantity be derived from transformations alone?" Chose the swap system and one-symbol relations as minimal test beds; meta-level use of ordinary mathematics declared explicitly in SYSTEMS.md section 0.

*Evidence:* research/systems/SYSTEMS.md

### [2026-10-18T06:44:01Z] Mathematical Inventor — hypothesis (`C01-02`)

Proposed H-C01-1 (counting is the complete invariant of commutation), H-C01-2/3 (one-symbol relations give threshold-plus-cycle structures) and the emergence of multiplication as composition.

*Evidence:* EXP-C01-01, EXP-C01-02, EXP-C01-03

### [2026-10-18T06:44:01Z] Mathematical Explorer — result (`C01-03`)

EXP-C01-01..03 confirmed all three on exhaustive finite slices (25 slices; 6159 relation sets with two independent algorithms; all semiring laws on a^0..a^12). Two-symbol substitutions do not commute in 154/200 random pairs.

*Evidence:* EXP-C01-01, EXP-C01-02, EXP-C01-03

### [2026-10-18T06:44:01Z] Mathematical Inventor — hypothesis (`C01-04`)

Proposed the deliberately bold H-C01-4 - any single rearranging relation eventually generates counting equivalence.

*Evidence:* CLM-C01-05

### [2026-10-18T06:44:01Z] Mathematical Skeptic — rejection (`C01-05`)

H-C01-4 rejected. EXP-C01-04 found counterexamples for all 33 relations of length 3 and 4; the simplest is aab <-> aba, under which baa is isolated.

*Evidence:* EXP-C01-04, CLM-C01-05

### [2026-10-18T06:44:01Z] Mathematical Explorer — surprise (`C01-06`)

The class counts in EXP-C01-04 were not random - every length-3 relation gave 2,4,7,12,20,33,... = F(n+3)-1 and 25 of the 27 length-4 relations gave tribonacci partial sums, while aaba<->abaa (and its complement) gave 97 instead of 96 at n = 7.

*Evidence:* EXP-C01-04

### [2026-10-18T06:44:01Z] Mathematical Explorer — hypothesis (`C01-07`)

Explanation proposed (H-C01-5) - if u is unbordered, u -> v has no critical pairs and terminates by lexicographic monotonicity, so classes are u-avoiding words (Guibas-Odlyzko count 1/(1-qx+x^k)). The exceptional pair has both sides bordered.

*Evidence:* EXP-C01-05

### [2026-10-18T06:44:01Z] Formal Verifier — result (`C01-08`)

EXP-C01-05 tested H-C01-5 on 1037 relations (binary k<=5, ternary k<=3) - 0 failures among 756 with an unbordered side; 81 both-bordered relations deviate.

*Evidence:* EXP-C01-05

### [2026-10-18T06:44:01Z] Mathematical Explorer — pattern (`C01-09`)

All 81 deviations share a common border between u and v, and their counts match avoidance of a word whose borders are exactly the common borders. Formulated H-C01-7 (common-border conjecture).

*Evidence:* EXP-C01-05, CLM-C01-08

### [2026-10-18T06:44:01Z] Formal Verifier — proof (`C01-10`)

Proved the border-containment theorem (Borders(u) in Borders(v) implies {u -> v} convergent) - the overlap along a common border joins in one step on each side. The one-step joinability identity is checked in Lean (common_border_joinable).

*Evidence:* CLM-C01-06, proofs/lean/Infinity/C01_Quantity.lean

### [2026-10-18T06:44:01Z] Formal Verifier — result (`C01-11`)

EXP-C01-06 confirmed H-C01-7 on 2159 relations including 1326 hard ones. EXP-C01-07 turned 1632 of them into proofs for all n (finite completion re-verified independently, rational generating function, recurrence-order bound). 527 hard relations have infinite completions, e.g. aba <-> bab completes to b a^j b a -> a b a a b^(j-1).

*Evidence:* EXP-C01-06, EXP-C01-07, CLM-C01-07

### [2026-10-18T06:44:01Z] Formal Verifier — proof (`C01-12`)

Lean 4 + Mathlib proofs compiled with standard axioms only - commEq_iff_count, projection_is_unary, gen_iff, exactly_m_add_p_classes, common_border_joinable.

*Evidence:* proofs/lean/Infinity/C01_Quantity.lean

### [2026-10-18T06:44:01Z] Historian and Novelty Analyst — novelty (`C01-13`)

Theorems 1-4 are textbook rediscoveries (Parikh vectors, monogenic semigroups, endomorphisms of N). Theorem 5 is very likely folklore (Newman + critical pairs + Guibas-Odlyzko). Two quick searches found no general common-border formula; CLM-C01-08 marked POTENTIALLY NOVEL pending a deeper audit.

*Evidence:* CLM-C01-06, CLM-C01-08

### [2026-10-18T06:44:01Z] Mathematical Skeptic — review (`C01-14`)

Caution recorded - the computer-assisted proofs (CLM-C01-07) trust the Python implementation; the guard is an independent convergence re-check plus brute-force agreement for n <= 8. Written proofs of CLM-C01-03/04/06 still need an independent review.

*Evidence:* CLM-C01-07

