# Foundational Systems of Project Infinity

This document fixes the *object-level* assumptions of every research branch.
It is versioned; changes are recorded in the research journal.

## 0. Object level versus meta level (an honest caveat)

The research prompt asks us to start from minimal assumptions: logical
consistency, distinguishable objects, equality/inequality and explicit
transformation rules. We honour this **at the object level**: inside each
system below, no numbers, coordinates, arithmetic operations or algebraic
laws are assumed unless the system's axioms introduce them.

At the **meta level** (when we *prove* things about a system) we use ordinary
mathematics: classical logic, induction over finite constructions, and set
theory as formalised in Lean 4's type theory with Mathlib. This is
unavoidable — even "a word is a finite string" presupposes finiteness — and
we state it explicitly so that no result is mistaken for a derivation of
arithmetic from nothing. When a cycle says that a concept "emerges", it means:
the concept is *definable* from the system's primitives and is *forced* (up to
isomorphism) by them, as shown by a meta-level proof.

Verification vocabulary used everywhere: PROVEN (valid proof checked — by
Lean, or by a written proof that survived independent skeptic review),
COMPUTATIONALLY SUPPORTED, CONJECTURE, REFUTED, INCONCLUSIVE; novelty labels
REDISCOVERY, POTENTIALLY NOVEL, NOT ASSESSED.

---

## System A — Objects and transformations without numbers

**Primitives.** A finite set Σ of pairwise distinguishable symbols; an empty
object ε; juxtaposition (concatenation) of objects.

**Objects.** Words: ε, every symbol, and the juxtaposition of two words.

**Axioms (free monoid).**
- A1 (associativity of juxtaposition) (uv)w = u(vw); hence brackets are omitted.
- A2 (empty object) εu = u = uε.
- A3 (freeness) Two words are equal iff they are both ε, or they have equal
  first symbols and equal remainders. (Equivalently: cancellation plus
  "equidivisibility"; a word has a unique factorisation into symbols.)

**Transformations.** A *rewriting system* is a finite set R of rules ℓ → r
(ℓ, r words). One step: xℓy →_R xry. A derivation is a chain of steps.
The *equational* version ↔*_R is the smallest congruence containing R.

**Number-free notions.** normal form (no rule applies); termination (no
infinite derivation); confluence (diverging derivations rejoin); invariant (a
map f on words with f(u) = f(v) whenever u →_R v); complete invariant
(f(u) = f(v) iff u ↔*_R v).

**Consistency requirement.** A1–A3 have a model (finite sequences over Σ),
hence are consistent. A congruence is *non-trivial* iff at least two words
are inequivalent; this is checked per rewriting system (it can fail, e.g.
a = ε, b = ε collapses everything).

**Status of numbers.** Numbers are not primitive. They may be used only as
*names* for invariant classes after a cycle has shown that the classes form a
structure isomorphic to the one being named (cycle C01).

---

## System B — Objects with invented composition rules

**Primitives.** A carrier S of distinguishable objects; one binary operation
∗ : S × S → S (closure is part of the definition: a *magma*); equality.

**Laws.** An identity is an equation s = t between terms built from
variables and ∗; a magma *satisfies* it if it holds for every assignment of
the variables. A *variety* is the class of magmas satisfying a set of laws.

**Not assumed.** associativity, commutativity, identity elements, inverses,
idempotence, distributivity, cancellation. Each is a *candidate law* to be
tested, never a default.

**Variants.** (i) partial operations (closure fails; recorded explicitly);
(ii) *successor-anchored magmas*: a magma (S, ∗) with a distinguished element
g and a cyclic permutation σ of S such that x ∗ g = σ(x) for all x.

**Consistency requirement.** Every set of identities is satisfied by the
one-element magma, so consistency is automatic; the meaningful question is
*non-trivial* consistency, measured by the **spectrum** — the set of sizes n
for which an n-element model exists. A law whose spectrum is {1} is
"collapsing".

---

## System C — Alternative representations of quantities

**Prerequisite.** System C may use the natural numbers N because cycle C01
derives them in System A as the complete invariant of commutation (the free
monoid on one symbol). Until C01 is PROVEN, System C results are conditional.

**Representation system.** A triple (D, A, val): a digit alphabet D, a set
A ⊆ D* of admissible strings, and a valuation val : A → N. It is *complete*
if val is onto and *unambiguous* if val is one-to-one.

**Positional systems with weights.** A strictly increasing weight sequence
G_0 = 1 < G_1 < … ; val(d_k…d_0) = Σ d_i G_i; admissibility is either
"greedy" (the representation produced by repeatedly subtracting the largest
weight) or a combinatorial condition (e.g. no two adjacent 1s).

**Operations.** Successor, comparison, addition, and *invented* operations
defined on digit strings (e.g. digit-position convolution, "circle"
products); each operation is profiled for closure, associativity,
commutativity, identity, inverses, distributivity, cost.

**Consistency requirement.** val must be well defined on A; completeness and
unambiguity are proved per system, never assumed.

---

## System D — Structures based on relationships rather than magnitude

**Primitives.** Objects together with one or more *relations*; only relational
structure matters, i.e. every notion must be invariant under isomorphism.

**D1 Games.** A position is determined by its set of options; the option
relation must be well-founded (no infinite play). Derived notions: outcome
(the player to move wins/loses), game sum (move in exactly one component),
and the *minimum excluded* (mex) value, defined using only the well-order of
"nim heaps" ∗0, ∗1, … where ∗n is the position whose options are exactly
∗0, …, ∗(n−1) — a purely relational definition.

**D2 Graphs as quantities.** Objects are finite simple graphs up to
isomorphism; operations are graph constructions (disjoint union, products);
"magnitudes" are isomorphism-invariant maps compatible with the operations.

**Consistency requirement.** Models exist (finite games, finite graphs).
Well-foundedness of options is required for games and checked by
construction (every move decreases a finite structure).

---

## System E — Local-rule dynamics over invented algebras (independent system)

**Primitives.** A finite magma (S, ∗) from System B and a one-dimensional
array of cells (the cyclic order Z/N or the line Z).

**Dynamics.** A configuration assigns an element of S to every cell; one
synchronous step replaces x_i by x_i ∗ x_{i+1}.

**Axioms.** locality (a cell's next state depends only on a bounded
neighbourhood), uniformity (the same rule everywhere), synchrony.

**Questions.** How do the algebraic laws of ∗ (associativity, idempotence,
quasigroup property, …) control the dynamics (periodicity, predictability,
compressibility, speed of simulation)?

**Consistency requirement.** The dynamics is a well-defined total map on
configurations for every magma.

Further independent systems (E2, …) are added to this file when created.
