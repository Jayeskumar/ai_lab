import Mathlib

/-!
# Cycle C05, batch 1.2 — laws `x = y ◇ (S ◇ y)` have only quasigroup models

If a finite magma satisfies `x = y ◇ (s(x, y) ◇ y)` for some binary term operation `s`, then

* every left translation `z ↦ y ◇ z` is a bijection (the law makes it onto), and
* every right translation `z ↦ z ◇ y` is a bijection: for `x = y ◇ w` the law gives
  `y ◇ (s(x, y) ◇ y) = y ◇ w`, hence `s(x, y) ◇ y = w` by injectivity of the left translation.

So the Cayley table is a Latin square. This justifies the "Latin columns" constraint of EXP-C05-09 for the ETP
laws 1076, 1083, 1110, 1279, 1286 and 1313 (proofs/paper/C05.md, Lemma 7 generalised), each instantiated below.
For a law `x = y ◇ T` of any other shape only the left translations are known to be bijective
(`left_mul_bijective_of_law'`).
-/

namespace Infinity.C05.Quasigroup

variable {α : Type*} [Finite α]

/-- Left translations are bijective for any law `x = y ◇ t(x, y)`. -/
theorem left_mul_bijective_of_law' (op : α → α → α) (t : α → α → α) (h : ∀ x y, op y (t x y) = x)
    (y : α) : Function.Bijective (op y) := by
  have hsurj : Function.Surjective (op y) := fun x => ⟨t x y, h x y⟩
  exact ⟨Finite.injective_iff_surjective.mpr hsurj, hsurj⟩

/-- Right translations are bijective for any law `x = y ◇ (s(x, y) ◇ y)`. -/
theorem right_mul_bijective_of_law (op : α → α → α) (s : α → α → α)
    (h : ∀ x y, op y (op (s x y) y) = x) (y : α) : Function.Bijective (fun z => op z y) := by
  have hl := left_mul_bijective_of_law' op (fun x y => op (s x y) y) h y
  have hsurj : Function.Surjective (fun z => op z y) := by
    intro w
    refine ⟨s (op y w) y, ?_⟩
    apply hl.1
    exact h (op y w) y
  exact ⟨Finite.injective_iff_surjective.mpr hsurj, hsurj⟩

/-- The six open ETP laws of the form `x = y ◇ (S ◇ y)`; in each, `S` is given as a function of `x, y`. -/
def Law1076 (op : α → α → α) : Prop := ∀ x y, op y (op (op x (op x y)) y) = x
def Law1083 (op : α → α → α) : Prop := ∀ x y, op y (op (op x (op y x)) y) = x
def Law1110 (op : α → α → α) : Prop := ∀ x y, op y (op (op y (op x x)) y) = x
def Law1279 (op : α → α → α) : Prop := ∀ x y, op y (op (op (op x x) y) y) = x
def Law1286 (op : α → α → α) : Prop := ∀ x y, op y (op (op (op x y) x) y) = x
def Law1313' (op : α → α → α) : Prop := ∀ x y, op y (op (op (op y x) x) y) = x

theorem law1076_right_bijective {op : α → α → α} (h : Law1076 op) (y : α) :
    Function.Bijective (fun z => op z y) :=
  right_mul_bijective_of_law op (fun x y => op x (op x y)) h y

theorem law1083_right_bijective {op : α → α → α} (h : Law1083 op) (y : α) :
    Function.Bijective (fun z => op z y) :=
  right_mul_bijective_of_law op (fun x y => op x (op y x)) h y

theorem law1110_right_bijective {op : α → α → α} (h : Law1110 op) (y : α) :
    Function.Bijective (fun z => op z y) :=
  right_mul_bijective_of_law op (fun x y => op y (op x x)) h y

theorem law1279_right_bijective {op : α → α → α} (h : Law1279 op) (y : α) :
    Function.Bijective (fun z => op z y) :=
  right_mul_bijective_of_law op (fun x y => op (op x x) y) h y

theorem law1286_right_bijective {op : α → α → α} (h : Law1286 op) (y : α) :
    Function.Bijective (fun z => op z y) :=
  right_mul_bijective_of_law op (fun x y => op (op x y) x) h y

theorem law1313_right_bijective' {op : α → α → α} (h : Law1313' op) (y : α) :
    Function.Bijective (fun z => op z y) :=
  right_mul_bijective_of_law op (fun x y => op (op y x) x) h y

end Infinity.C05.Quasigroup

#print axioms Infinity.C05.Quasigroup.left_mul_bijective_of_law'
#print axioms Infinity.C05.Quasigroup.right_mul_bijective_of_law
#print axioms Infinity.C05.Quasigroup.law1076_right_bijective
#print axioms Infinity.C05.Quasigroup.law1083_right_bijective
#print axioms Infinity.C05.Quasigroup.law1110_right_bijective
#print axioms Infinity.C05.Quasigroup.law1279_right_bijective
#print axioms Infinity.C05.Quasigroup.law1286_right_bijective
#print axioms Infinity.C05.Quasigroup.law1313_right_bijective'
