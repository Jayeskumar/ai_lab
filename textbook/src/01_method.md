# How the laboratory works

## Minimal assumptions, stated twice

Each research branch begins from a *foundational system* whose object-level
axioms are written down explicitly (repository file
`research/systems/SYSTEMS.md`):

* **System A** — words over distinguishable symbols, juxtaposition, rewriting
  rules; no numbers.
* **System B** — a carrier with one invented binary operation; no algebraic
  law is assumed, every law is a hypothesis to be tested.
* **System C** — representations of quantities (digit strings with a
  valuation), admissible only after System A has *derived* counting.
* **System D** — structures defined by relations only (game options, graphs).
* **System E** — local-rule dynamics over invented algebras.

The *meta level* — the mathematics we use to prove things about these
systems — is ordinary mathematics (formally, Lean's type theory with
Mathlib). When we say that a concept "emerges", we mean that it is definable
from the system's primitives and forced by them up to isomorphism, as shown
by a meta-level proof.

## A research cycle

Every cycle runs ten steps, and the cycle report in the repository is
organised by them:

1. generate hypotheses — including at least one *bold* hypothesis that might
   fail;
2. state them precisely;
3. design experiments that could falsify them;
4. implement the experiments (deterministic, seeded scripts);
5. execute them (results are hashed; re-running checks the hash);
6. analyse the results;
7. attempt proofs or find counterexamples;
8. compare with the literature (OEIS and web searches; references recorded);
9. look for applications, with baselines and honest negatives;
10. document everything in the journal and the database.

## Kinds of proof

**Lean proofs.** Statements are formalised in Lean 4 with Mathlib; a file
counts as verified only if it compiles with no `sorry` and `#print axioms`
reports only `propext`, `Classical.choice` and `Quot.sound`.

**Computer-assisted proofs.** Some results are proved by finite certificates
that a program checks: a completed rewriting system whose convergence is
re-verified independently, an automaton whose count sequence obeys a
recurrence of bounded order, a recurring window of a monotone map. For these
the book states the *trust base* — the program code — and the cross-checks
used to guard against implementation errors.

**Written proofs** are complete arguments reviewed by the lab's Skeptic, who
works independently from the authors and tries to break every claim.

## Novelty

The Historian searches the OEIS (all integer sequences we produce are looked
up, and the cached answers are kept in the repository) and the literature.
Matches are *read*, not counted: in Chapter 9 a sequence agreed with an OEIS
entry for 24 terms and then diverged; the agreement had a simple explanation
and was recorded as a coincidence.
