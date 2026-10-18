import Mathlib.Logic.Relation
import Mathlib.Data.List.Count
import Mathlib.Order.WellFounded
import Mathlib.Tactic

/-!
# Cycle C03 — Termination of one-rule string rewriting `0^p 1^q → 1^r 0^s`

Words are lists; over the binary alphabet we use `Bool` with `false = 0`, `true = 1`.

* `terminating_of_count_lt` (CLM-C03-01): a rule that strictly decreases the number of
  occurrences of some letter is terminating.
* `inv_append`, `terminating_swap` (CLM-C03-02, swap case): `0^p 1^q → 1^q 0^p` terminates —
  the number of (0,1)-inversions drops by `p*q` at every step.
* `not_terminating_of_loop` (CLM-C03-03): a self-embedding derivation `u →⁺ x u y` makes the
  system non-terminating.
* `loop_map` (CLM-C03-05, substitution lemma): a letter-to-word substitution that maps the
  rule `l → r` onto `l' → r'` maps loops of the first system to loops of the second.
* `not_terminating_double` (CLM-C03-03): if `r ≥ 2q` and `s ≥ 2p` (with `p, q ≥ 1`), the rule
  loops: `0^p 1^(2q) →² 1^r 0^(s-2p) (0^p 1^(2q)) 1^(r-2q) 0^s`.
* `not_terminating_0_11` (CLM-C03-04): the explicit four-step loop
  `001111 →⁴ 111 001111 00100` for `011 → 11100`, a rule with `r < 2q`.
-/

namespace Infinity.C03

open Relation

section General

variable {α : Type*}

/-- One rewrite step of the single rule `l → r`. -/
def Step (l r : List α) (u v : List α) : Prop := ∃ x y, u = x ++ l ++ y ∧ v = x ++ r ++ y

/-- `l → r` is terminating: the converse of the step relation is well-founded. -/
def Terminating (l r : List α) : Prop := WellFounded (fun v u => Step l r u v)

theorem terminating_of_count_lt [DecidableEq α] (l r : List α) (a : α)
    (h : r.count a < l.count a) : Terminating l r := by
  refine Subrelation.wf ?_ (measure fun w : List α => w.count a).wf
  intro v u hstep
  obtain ⟨x, y, hu, hv⟩ := hstep
  show v.count a < u.count a
  rw [hu, hv]
  simp only [List.count_append]
  omega

theorem step_context {l r u v : List α} (a b : List α) (h : Step l r u v) :
    Step l r (a ++ u ++ b) (a ++ v ++ b) := by
  obtain ⟨x, y, hu, hv⟩ := h
  exact ⟨a ++ x, y ++ b, by simp [hu], by simp [hv]⟩

theorem transGen_context {l r u v : List α} (a b : List α) (h : TransGen (Step l r) u v) :
    TransGen (Step l r) (a ++ u ++ b) (a ++ v ++ b) := by
  induction h with
  | single h => exact TransGen.single (step_context a b h)
  | tail _ h ih => exact TransGen.tail ih (step_context a b h)

/-- **CLM-C03-03 (certificates).** A self-embedding derivation proves non-termination. -/
theorem not_terminating_of_loop (l r u x y : List α)
    (h : TransGen (Step l r) u (x ++ u ++ y)) : ¬ Terminating l r := by
  intro hwf
  have hwf' : WellFounded (TransGen (fun v w => Step l r w v)) := hwf.transGen
  let S : Set (List α) := {w | ∃ a b, w = a ++ u ++ b}
  have hS : S.Nonempty := ⟨u, [], [], by simp⟩
  obtain ⟨m, ⟨a, b, rfl⟩, hmin⟩ := hwf'.has_min S hS
  have hstep : TransGen (Step l r) (a ++ u ++ b) (a ++ (x ++ u ++ y) ++ b) :=
    transGen_context a b h
  have hmem : a ++ (x ++ u ++ y) ++ b ∈ S := ⟨a ++ x, y ++ b, by simp⟩
  exact hmin _ hmem (transGen_swap.mpr hstep)

/-- **Substitution lemma.** A substitution `σ` (extended to words by `flatMap`) with
`σ l = l'`, `σ r = r'` maps steps of `l → r` to steps of `l' → r'`. -/
theorem step_map {β : Type*} (σ : α → List β) {l r u v : List α} (h : Step l r u v) :
    Step (l.flatMap σ) (r.flatMap σ) (u.flatMap σ) (v.flatMap σ) := by
  obtain ⟨x, y, hu, hv⟩ := h
  exact ⟨x.flatMap σ, y.flatMap σ, by simp [hu], by simp [hv]⟩

theorem loop_map {β : Type*} (σ : α → List β) {l r u x y : List α}
    (h : TransGen (Step l r) u (x ++ u ++ y)) :
    TransGen (Step (l.flatMap σ) (r.flatMap σ)) (u.flatMap σ)
      (x.flatMap σ ++ u.flatMap σ ++ y.flatMap σ) := by
  have key : ∀ {a b : List α}, TransGen (Step l r) a b →
      TransGen (Step (l.flatMap σ) (r.flatMap σ)) (a.flatMap σ) (b.flatMap σ) := by
    intro a b hab
    induction hab with
    | single h => exact TransGen.single (step_map σ h)
    | tail _ h ih => exact TransGen.tail ih (step_map σ h)
  simpa using key h

end General

section Binary

open List

/-- The rule `0^p 1^q → 1^r 0^s` over `Bool` (`false = 0`, `true = 1`). -/
def lhs (p q : ℕ) : List Bool := replicate p false ++ replicate q true
def rhs (r s : ℕ) : List Bool := replicate r true ++ replicate s false

/-- Number of pairs (a `0` before a `1`). -/
def inv : List Bool → ℕ
  | [] => 0
  | false :: w => w.count true + inv w
  | true :: w => inv w

theorem inv_append (u v : List Bool) :
    inv (u ++ v) = inv u + inv v + u.count false * v.count true := by
  induction u with
  | nil => simp [inv]
  | cons c u ih =>
    cases c with
    | false =>
      simp only [List.cons_append, inv, ih, List.count_append, List.count_cons]
      simp
      ring
    | true =>
      simp only [List.cons_append, inv, ih, List.count_cons]
      simp

theorem inv_replicate_false (n : ℕ) : inv (replicate n false) = 0 := by
  induction n with
  | zero => rfl
  | succ n ih => simp [replicate_succ, inv, ih, List.count_replicate]

theorem inv_replicate_true (n : ℕ) : inv (replicate n true) = 0 := by
  induction n with
  | zero => rfl
  | succ n ih => simp [replicate_succ, inv, ih]

theorem inv_three (x m y : List Bool) :
    inv (x ++ m ++ y) = inv x + inv m + inv y + x.count false * m.count true
      + x.count false * y.count true + m.count false * y.count true := by
  rw [inv_append, inv_append, List.count_append]
  ring

/-- **CLM-C03-02 (swap case).** `0^p 1^q → 1^q 0^p` terminates for `p, q ≥ 1`. -/
theorem terminating_swap (p q : ℕ) (hp : 0 < p) (hq : 0 < q) :
    Terminating (lhs p q) (rhs q p) := by
  refine Subrelation.wf ?_ (measure inv).wf
  intro v u hstep
  obtain ⟨x, y, hu, hv⟩ := hstep
  show inv v < inv u
  have il : inv (lhs p q) = p * q := by
    simp [lhs, inv_append, inv_replicate_false, inv_replicate_true]
  have ir : inv (rhs q p) = 0 := by
    simp [rhs, inv_append, inv_replicate_false, inv_replicate_true, List.count_replicate]
  have c1 : (lhs p q).count true = q := by simp [lhs, List.count_replicate]
  have c2 : (lhs p q).count false = p := by simp [lhs, List.count_replicate]
  have c3 : (rhs q p).count true = q := by simp [rhs, List.count_replicate]
  have c4 : (rhs q p).count false = p := by simp [rhs, List.count_replicate]
  rw [hu, hv, inv_three, inv_three, il, ir, c1, c2, c3, c4]
  have : 0 < p * q := Nat.mul_pos hp hq
  omega

/-- **CLM-C03-03 (general loop).** If `r ≥ 2q`, `s ≥ 2p`, `p, q ≥ 1`, the rule loops. -/
theorem not_terminating_double (p q r s : ℕ) (hp : 0 < p) (_hq : 0 < q)
    (hr : 2 * q ≤ r) (hs : 2 * p ≤ s) : ¬ Terminating (lhs p q) (rhs r s) := by
  have hs1 : replicate s false = replicate (s - p) false ++ replicate p false := by
    rw [← List.replicate_add]; congr 1; omega
  have hs2 : replicate (s - p) false = replicate (s - 2 * p) false ++ replicate p false := by
    rw [← List.replicate_add]; congr 1; omega
  have hr2 : replicate r true = replicate (2 * q) true ++ replicate (r - 2 * q) true := by
    rw [← List.replicate_add]; congr 1; omega
  have hq2 : replicate (2 * q) true = replicate q true ++ replicate q true := by
    rw [← List.replicate_add]; congr 1; omega
  apply not_terminating_of_loop (lhs p q) (rhs r s)
    (replicate p false ++ replicate (2 * q) true)
    (replicate r true ++ replicate (s - 2 * p) false)
    (replicate (r - 2 * q) true ++ replicate s false)
  have step1 : Step (lhs p q) (rhs r s) (replicate p false ++ replicate (2 * q) true)
      (replicate r true ++ replicate s false ++ replicate q true) := by
    refine ⟨[], replicate q true, ?_, ?_⟩
    · rw [hq2, lhs]; simp only [List.nil_append, List.append_assoc]
    · rw [rhs]; simp only [List.nil_append]
  have step2 : Step (lhs p q) (rhs r s) (replicate r true ++ replicate s false ++ replicate q true)
      (replicate r true ++ replicate (s - 2 * p) false ++ (replicate p false ++ replicate (2 * q) true)
        ++ (replicate (r - 2 * q) true ++ replicate s false)) := by
    refine ⟨replicate r true ++ replicate (s - p) false, [], ?_, ?_⟩
    · rw [lhs]; conv_lhs => rw [hs1]
      simp only [List.append_assoc, List.append_nil]
    · rw [rhs, hs2, List.append_nil]
      simp only [List.append_assoc]
      congr 3
      rw [hr2, List.append_assoc]
  exact TransGen.tail (TransGen.single step1) step2

/-- **CLM-C03-04.** `011 → 11100` (p = 1, q = 2, r = 3 < 2q, s = 2) is non-terminating:
`001111 → 01110011 → 0111011100 → 011111100100 → 11100111100100 = 111 · 001111 · 00100`. -/
theorem not_terminating_0_11 : ¬ Terminating (lhs 1 2) (rhs 3 2) := by
  apply not_terminating_of_loop (lhs 1 2) (rhs 3 2) [false, false, true, true, true, true]
    [true, true, true] [false, false, true, false, false]
  have s1 : Step (lhs 1 2) (rhs 3 2) [false, false, true, true, true, true]
      [false, true, true, true, false, false, true, true] :=
    ⟨[false], [true, true], by decide, by decide⟩
  have s2 : Step (lhs 1 2) (rhs 3 2) [false, true, true, true, false, false, true, true]
      [false, true, true, true, false, true, true, true, false, false] :=
    ⟨[false, true, true, true, false], [], by decide, by decide⟩
  have s3 : Step (lhs 1 2) (rhs 3 2) [false, true, true, true, false, true, true, true, false, false]
      [false, true, true, true, true, true, true, false, false, true, false, false] :=
    ⟨[false, true, true, true], [true, false, false], by decide, by decide⟩
  have s4 : Step (lhs 1 2) (rhs 3 2)
      [false, true, true, true, true, true, true, false, false, true, false, false]
      ([true, true, true] ++ [false, false, true, true, true, true] ++ [false, false, true, false, false]) :=
    ⟨[], [true, true, true, true, false, false, true, false, false], by decide, by decide⟩
  exact TransGen.tail (TransGen.tail (TransGen.tail (TransGen.single s1) s2) s3) s4

end Binary

end Infinity.C03

#print axioms Infinity.C03.terminating_of_count_lt
#print axioms Infinity.C03.terminating_swap
#print axioms Infinity.C03.not_terminating_of_loop
#print axioms Infinity.C03.loop_map
#print axioms Infinity.C03.not_terminating_double
#print axioms Infinity.C03.not_terminating_0_11
