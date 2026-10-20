# Historian audit: finite non-right-cancellative models of ETP law 677 (2026-10-20)

*Batch 1.2, for B4 (law 677 at order 12). Question from the Director: what is proven about finite models of
677, x = y◇(x◇((y◇x)◇y)), that are not right-cancellative (non-RC: the table is not a Latin square), and has
anyone searched order 12? Written by the Historian agent; saved to the repository by the Director, unchanged
except for this header.*

"msg N" = Zulip topic "FINITE: 677 -> 255",
https://leanprover.zulipchat.com/#narrow/channel/458659-Equational/topic/FINITE.3A.20677.20-.3E.20255/near/N (public
mirror updated to Feb 28 2026; all 631 messages to Feb 10 2026 read; later messages need a login and were not
read). "DB" = the live database https://eq677.icarm.cloud (7841 isomorphism classes at the time of reading).

**Correction to the lab's notes: the smallest known non-RC model has order 25, not 55.**

## Q1. Lower bound; "order 12 (or < 55) impossible"

- **Not found.** No source proves a lower bound or a divisibility condition, and none excludes order 12. Le Floch
  asked "Do we have any technique to show non-existence for certain sizes?" (Jan 8 2026, msg 567001135); Reinke
  replied "so far we only have the technique to have an exhaustive search return nothing" (msg 567004975).
- **"< 55" is false**: non-RC models of orders 25, 45 and 49 exist (checked by the Historian, see Q2).
- Searches without certificates: no 677 models of order 2, 3, 4 or 6 (Tencer, Dec 7 2024, msg 486683966); none
  of order 8 (Brox, Mace4, msg 486711939); none of order 10, "no models whatsoever of 677 in size 10 (39h in
  Mace4)" (Brox, Jan 12 2025, msg 493229385); Schneider's DPLL "general model search works til size 11" (msg
  558558838). Every eq677-database model of order ≤ 11 is a Latin square (Historian's scan). So "a non-RC model
  needs order ≥ 12" rests only on these uncertified searches.

## Q2. Constructions (none from an exhaustive search)

- **496.** Tao, Dec 25 2024 (msg 490772441): a translation-invariant model on Z/31 × F; "we get a loss of right
  cancellativity. On the other hand we have idempotence f(0)=0, so 255 holds"; table for q = 16 by Bolan (msg
  490795390). Blueprint §13.1 has a typo (Reinke: "it is ⋄+ that is not right-cancellative", msg 554279887).
- **77, then 55.** Le Floch, Nov 22 2025 (msgs 558778716, 558842589): "Down to a 55-element model"; carrier
  Z/11 × M with (a,h)⋄(b,k) = (2b−a, k) if a−b is a nonzero square and (2b−a, h∘k) otherwise, h∘k = −h−k; the
  diagonal glued from copies of the 5-element model.
- **25.** Reinke, Nov 26 2025 (msg 560418876): "here is an example for F25 that is not right-cancellative":
  x⋄₁y = x+4(y−x), x⋄₂y = x+α(y−x) with α²+3α+4 = 0, the branch chosen by the quadratic character of x−y (msg
  560893937); later "the smallest known example that is not right cancellative" (msg 564499852). Idempotent;
  eq677 repository entry 25/24, DB magma d732efd1.
- **49 and 77, non-idempotent.** Schneider, Dec 25 2025 (msg 565395931): "77/65 is based on 7/0, and 49/18 is
  based on 7/1".
- **55, 77, 121, 143, 155, 176.** Renshaw & Tsoukalas, Feb 4 2026 (msg 571795518), "inspired by the 'magma
  cohomology' approach" (msg 571796530).
- **45, 67, 89, 111, 133, 265 (sizes 11k+1).** DB, Sep 4 2026 (dwrensha with Claude): seed models glued along an
  idempotent over F_11.
- 55 was only the smallest found on Nov 22 2025 and was superseded four days later.
- All known models satisfy 255 (DB: "every known example also satisfies Equation 255"; Le Floch: piecewise
  affine extensions "cannot produce counterexamples", msg 558900089).
- Historian's own check: all 440 non-empty eq677-repository tables and the 100 DB non-RC tables of order ≤ 150
  satisfy 677; the smallest non-RC order among them is 25. In that model each column has twelve 2-element fibres
  and one singleton (so the DB comment's "5-fold fiber structure" is wrong).

## Q3. Structural facts for all finite 677 models

Proven (short proofs in the sources; Lean where noted):

1. L_y is bijective with L_y⁻¹x = x⋄((y⋄x)⋄y); x = (y⋄x)⋄((y⋄(y⋄x))⋄y); y⋄x = x ⇒ y = (x⋄x)⋄x; 255 holds at x
   ⟺ x ∈ im R_x ⟺ ∃y x⋄(y⋄y) = y (blueprint Lemmas 13.1–13.2,
   https://teorth.github.io/equational_theories/blueprint/677-chapter.html; Lean: ETP
   `ManuallyProved/Equation677.lean`, PR #1434, Apr 5 2026).
2. "Star equation" (same Lean file): "a ◇ x = b ◇ x → (a ◇ (a ◇ x)) ◇ a = (b ◇ (b ◇ x)) ◇ b". Corollary (the
   Historian's): if a ≠ b and a⋄x = b⋄x = u then a⋄u ≠ b⋄u. This is the rigorous core of Le Floch's claim
   "im(R_y) has at least as many elements as R_v⁻¹(y∗v)" (msg 488746604), whose sketch has a gap.
3. "a finite 677 model is 'almost' right-cancellative" (Tencer, msg 490341320): rows are pairwise distinct, and
   a ≠ b with a⋄x = b⋄x implies L_a⁻¹x ≠ L_b⁻¹x.
4. Counting: no column is constant (Tao, msg 486697932); each value fills exactly n cells, so a value repeated in
   one column is missing from another; "there must be more than one counterexample to right-cancellativity"
   (Bolan, msgs 497781441, 497786137).
5. "at least one of the right multiplication operators R_y must have a range of size at least n^{1/2}" (Tao, msg
   489600461).
6. (x,y)↦(x,y⋄x) and (x,y)↦(x,(y⋄x)⋄y) are "equally non-invertible" (Tao, msg 489281924), hence
   Σₓ|im Rₓ| = Σₓ|{(y⋄x)⋄y : y}|.
7. a⋄a = a ⟺ (a⋄a)⋄a = a ⟺ a⋄(a⋄a) = a ⟺ (a⋄a)⋄(a⋄a) = a; a right power aⁿ = a with 3∤n holds iff a is
   idempotent (Hyun, msg 558573702; Lean in qawbecrdtey/magma, not compiled by the Historian). L_a has no 2-cycle
   through a, and ab = b ∧ ba = a ⇒ a = b (Tencer, msg 490117798). Idempotents need not exist: 5x+27y+1 mod 31
   has none (Schneider, msg 558578347). Constant squaring ⇒ 255 (Brox, ATP, msg 486650264).
8. Submagmas and quotients satisfy 677 (Tao, msg 488966696); the fixed points of an automorphism form a submagma
   (Reinke, msg 558661660). Inference: a proper submagma or quotient of an order-12 model has order in the
   (uncertified) spectrum {1, 5, 7, 9, 11}.

Refuted conjecture: Hyun's "((b⋄a)⋄a)⋄a = b when a⋄b = a" (msg 509648161) fails in eq677 tables 65/6, 77/65,
77/71–73 and 91/6 — not to be used as a SAT constraint. Not found: any "R_y injective iff …" criterion, or a
decomposition into a quasigroup part.

## Q4. Order-12 searches

- No complete search of order 12, and no quasigroup-only search, is reported. The DB size-10 commentary
  (dwrensha, May 15 2026; AI-written, mixes anti-255 runs with full searches) says "Sizes 12 and 14 are OPEN";
  the DB has no class of size 12.
- 677 ∧ ¬255 (which forces non-RC): Brox, "I believe that I exhausted size 12" (msg 490346469), retracted ("there
  is no way I had exhausted up to size 12 before", msg 492948727); exhausted through order 11 only ("size 11 (57
  days)", msg 505103036); a variant was "running in size 12" with no result reported. Hyun's CaDiCaL runs for
  sizes 12–16 "none of them terminated" (msg 541356883), aborted with "no sign of termination even for size 12"
  (Oct 30 2025, msg 547914401).
- Restricted searches at order 12 (no certificates): "no models of 677+4276 in size 12" (Brox, msg 492948727);
  677 + E16018451 or E16020367 + left-cancellativity, anti-255: none at sizes 12–13 (msg 515674344);
  translation-invariant models x⋄y = x·f(x⁻¹y) exist among groups of order ≤ 17 only on Z5, Z11 and Z2⁴
  (Paolini, Gurobi, msg 488731087), so none of order 12; ETP paper Table 4 exhausts "certain special E677 models"
  at size 12 (class not specified).

## Sources read

Local copies (earlier Historian run): the full 677 topic, about 25 other Equational topics, blueprint `677.tex`,
commentary, arXiv:2512.07087v2, the eq677 manual, three 2026 arXiv papers. Online: the Zulip archive (677 topic,
stream index, 11 neighbouring topics); the blueprint web chapter; teorth/equational_theories at HEAD (Sep 12
2026: `677.tex`, commentary, forcing rules, `Equation677.lean`, `paper/*.tex`, referee response, 2026 commits,
issue #1517); arXiv 2512.07087 version history (v2 latest) and 2605.21200, 2602.16324, 2508.15856, 2609.20028,
2609.05690, 2603.27007 (no 677 content); memoryleak47/eq677; icarm/Equation-677-Database; eq677.icarm.cloud
(home, /api, /recent, manifest, size pages); dwrensha.github.io/eq677; qawbecrdtey/magma; 3 web searches.

## Director's note (2026-10-20)

The corollary of item 2 was re-derived by the Director from (y◇x)◇y = x\(y\x): if a◇x = b◇x = u then
(a◇u)◇a = u\x = (b◇u)◇b, so a◇u = b◇u would give a = b. Added as implied clauses to the non-quasigroup part of
the hardest case of 677 at order 12 (idempotent, row type (11, 1)), it did not decide that part within 1,000,000
conflicts (exploratory probe, not recorded).
