# Discovery Index

_Generated 2026-10-18T06:44:01Z by `python -m lab sync` from `db/claims/`. Do not edit by hand._

Every claim carries two independent labels: a **verification status** (PROVEN, COMPUTATIONALLY SUPPORTED, CONJECTURE, REFUTED, INCONCLUSIVE) and a **novelty status** (REDISCOVERY, POTENTIALLY NOVEL, NOT ASSESSED). A claim may therefore appear in more than one section below.

## Summary

| Verification status | Claims |
|---|---|
| PROVEN | 6 |
| COMPUTATIONALLY SUPPORTED | 1 |
| CONJECTURE | 0 |
| REFUTED | 1 |
| INCONCLUSIVE | 0 |

| Novelty status | Claims |
|---|---|
| REDISCOVERY | 4 |
| POTENTIALLY NOVEL | 1 |
| NOT ASSESSED | 3 |

## 1. Verified theorems (PROVEN)

| Claim | Title | Proof check | Novelty | Evidence |
|---|---|---|---|---|
| CLM-C01-01 | Symbol counts are the complete invariant of the commutation congruence | Lean 4 + Mathlib (commEq_iff_count, projection_is_unary); s… | REDISCOVERY | EXP-C01-01 |
| CLM-C01-02 | One symbol, one relation a^m = a^(m+p) gives exactly m+p classes (index m, period p) | Lean 4 + Mathlib (gen_iff, exactly_m_add_p_classes); standa… | REDISCOVERY | EXP-C01-02 |
| CLM-C01-03 | Several one-symbol relations have index min m_i and period gcd(n_i - m_i) | written proof (proofs/paper/C01.md, Theorem 3); computation… | REDISCOVERY | EXP-C01-02 |
| CLM-C01-04 | Multiplication emerges as composition of substitutions; with two symbols it is non-commut… | written proof (proofs/paper/C01.md, Theorem 4) with exhaust… | REDISCOVERY | EXP-C01-03 |
| CLM-C01-06 | Border-containment theorem for one length-preserving relation | written proof (proofs/paper/C01.md, Theorem 5); its overlap… | NOT ASSESSED | EXP-C01-04, EXP-C01-05, EXP-C01-07 |
| CLM-C01-07 | Common-border formula proved for 1632 specific relations by verified finite completions | computer-assisted (Python) - independently re-verified conv… | NOT ASSESSED | EXP-C01-07 |

## 2. Unproven conjectures (CONJECTURE and COMPUTATIONALLY SUPPORTED)

| Claim | Title | Verification | Novelty | Evidence |
|---|---|---|---|---|
| CLM-C01-08 | Common-border conjecture: one-relation class counts depend only on common borders | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C01-05, EXP-C01-06, EXP-C01-07 |

## 3. Potentially novel ideas

Novelty means only that no equivalent was found in the sources searched (recorded per claim in `novelty_basis`). It is never a confirmed priority claim.

| Claim | Title | Verification | Novelty | Evidence |
|---|---|---|---|---|
| CLM-C01-08 | Common-border conjecture: one-relation class counts depend only on common borders | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C01-05, EXP-C01-06, EXP-C01-07 |

## 4. Rediscovered existing mathematics

| Claim | Title | Verification | Novelty | Evidence |
|---|---|---|---|---|
| CLM-C01-01 | Symbol counts are the complete invariant of the commutation congruence | PROVEN | REDISCOVERY | EXP-C01-01 |
| CLM-C01-02 | One symbol, one relation a^m = a^(m+p) gives exactly m+p classes (index m, period p) | PROVEN | REDISCOVERY | EXP-C01-02 |
| CLM-C01-03 | Several one-symbol relations have index min m_i and period gcd(n_i - m_i) | PROVEN | REDISCOVERY | EXP-C01-02 |
| CLM-C01-04 | Multiplication emerges as composition of substitutions; with two symbols it is non-commut… | PROVEN | REDISCOVERY | EXP-C01-03 |

## 5. Practical algorithmic results

_None yet._

## 6. Refuted hypotheses

| Claim | Title | Verification | Novelty | Evidence |
|---|---|---|---|---|
| CLM-C01-05 | H-C01-4: a single rearranging relation generates counting equivalence on long words (refu… | REFUTED | NOT ASSESSED | EXP-C01-04 |

## 7. Inconclusive

_None yet._

