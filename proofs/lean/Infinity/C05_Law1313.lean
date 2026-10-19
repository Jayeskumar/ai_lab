import Mathlib

/-!
# Cycle C05, batch 1.1 — finite models of ETP law 1313 are quasigroups

ETP equation 1313 is `x = y ◇ (((y ◇ x) ◇ x) ◇ y)`. In a finite magma satisfying it,

* every left translation `z ↦ y ◇ z` is a bijection (the law has the form `x = y ◇ s(x, y)`), and
* every right translation `z ↦ z ◇ y` is a bijection: for `x = y ◇ w` the law gives
  `y ◇ (((y ◇ x) ◇ x) ◇ y) = y ◇ w`, so `((y ◇ x) ◇ x) ◇ y = w` by injectivity of the left translation.

So the Cayley table is a Latin square — the implied "Latin columns" constraint used soundly in EXP-C05-08
(proofs/paper/C05.md, Lemma 7).
-/

namespace Infinity.C05

variable {α : Type*} [Finite α]

/-- ETP equation 1313: `x = y ◇ (((y ◇ x) ◇ x) ◇ y)`. -/
def Law1313 (op : α → α → α) : Prop := ∀ x y, op y (op (op (op y x) x) y) = x

theorem law1313_left_bijective {op : α → α → α} (h : Law1313 op) (y : α) :
    Function.Bijective (op y) := by
  have hsurj : Function.Surjective (op y) := fun x => ⟨_, h x y⟩
  exact ⟨Finite.injective_iff_surjective.mpr hsurj, hsurj⟩

theorem law1313_right_bijective {op : α → α → α} (h : Law1313 op) (y : α) :
    Function.Bijective (fun z => op z y) := by
  have hsurj : Function.Surjective (fun z => op z y) := by
    intro w
    refine ⟨op (op y (op y w)) (op y w), ?_⟩
    apply (law1313_left_bijective h y).1
    exact h (op y w) y
  exact ⟨Finite.injective_iff_surjective.mpr hsurj, hsurj⟩

omit [Finite α] in
/-- The right projection `x ◇ y = y` is not a model of law 1313 on a type with two distinct elements, so a model
of order at least 2 has a row that is not the identity. -/
theorem law1313_not_right_projection {a b : α} (hab : a ≠ b) : ¬ Law1313 (fun _ y : α => y) := by
  intro h
  exact hab (h a b).symm

/-- ETP equation 677: `x = y ◇ (x ◇ ((y ◇ x) ◇ y))`; the right projection is not a model either. -/
def Law677 (op : α → α → α) : Prop := ∀ x y, op y (op x (op (op y x) y)) = x

theorem law677_left_bijective {op : α → α → α} (h : Law677 op) (y : α) :
    Function.Bijective (op y) := by
  have hsurj : Function.Surjective (op y) := fun x => ⟨_, h x y⟩
  exact ⟨Finite.injective_iff_surjective.mpr hsurj, hsurj⟩

omit [Finite α] in
theorem law677_not_right_projection {a b : α} (hab : a ≠ b) : ¬ Law677 (fun _ y : α => y) := by
  intro h
  exact hab (h a b).symm

end Infinity.C05

#print axioms Infinity.C05.law1313_left_bijective
#print axioms Infinity.C05.law1313_right_bijective
#print axioms Infinity.C05.law1313_not_right_projection
#print axioms Infinity.C05.law677_left_bijective
#print axioms Infinity.C05.law677_not_right_projection
