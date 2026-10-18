import Mathlib.Data.Fin.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

/-!
# Cycle C06 — Successor-anchored magmas

Convention: elements `Fin N`, anchor `x ⋆ 0 = x + 1` (Laver's `p ⋆ 1 = p + 1` relabelled by
`p ↦ p - 1`).

* `laver3_anchored`, `laver3_left_distributive`: the Laver table `A₃` (computed by Laver's
  recursion in EXP-C06-01) is anchored and left-distributive (all 512 triples, by `decide`).
* `no_anchored_ld_three`: there is no anchored left-distributive magma on 3 elements
  (exhaustive over the 3⁶ entries outside the anchored column).
* `anchored_assoc_unique` (CLM-C06-02): for every `N ≥ 1`, the only associative operation on
  `ZMod N` with `x ⋆ 0 = x + 1` is `x ⋆ y = x + y + 1`.
-/

namespace Infinity.C06

/-- The Laver table `A₃` (0-based relabelling). -/
def laver3 : Fin 8 → Fin 8 → Fin 8 :=
  ![![1, 3, 5, 7, 1, 3, 5, 7], ![2, 3, 6, 7, 2, 3, 6, 7], ![3, 7, 3, 7, 3, 7, 3, 7],
    ![4, 5, 6, 7, 4, 5, 6, 7], ![5, 7, 5, 7, 5, 7, 5, 7], ![6, 7, 6, 7, 6, 7, 6, 7],
    ![7, 7, 7, 7, 7, 7, 7, 7], ![0, 1, 2, 3, 4, 5, 6, 7]]

theorem laver3_anchored : ∀ x : Fin 8, laver3 x 0 = x + 1 := by decide

set_option maxRecDepth 100000 in
theorem laver3_left_distributive :
    ∀ a b c : Fin 8, laver3 a (laver3 b c) = laver3 (laver3 a b) (laver3 a c) := by decide

/-- An anchored operation on `Fin 3` is determined by its 6 entries outside column 0. -/
def tbl (e : Fin 3 → Fin 2 → Fin 3) (x y : Fin 3) : Fin 3 :=
  if h : y = 0 then x + 1 else e x ⟨y.val - 1, by omega⟩

set_option maxRecDepth 100000 in
theorem no_anchored_ld_three :
    ∀ e : Fin 3 → Fin 2 → Fin 3,
      ¬ (∀ a b c : Fin 3, tbl e a (tbl e b c) = tbl e (tbl e a b) (tbl e a c)) := by
  decide

/-- **CLM-C06-02 (all N).** An associative operation on `ZMod N` (`N ≥ 1`) with `x ⋆ 0 = x + 1` is
`x ⋆ y = x + y + 1`. -/
theorem anchored_assoc_unique {N : ℕ} [NeZero N] (op : ZMod N → ZMod N → ZMod N)
    (anchor : ∀ x, op x 0 = x + 1) (assoc : ∀ x y z, op (op x y) z = op x (op y z)) :
    ∀ x y, op x y = x + y + 1 := by
  have step : ∀ x y, op x (y + 1) = op x y + 1 := by
    intro x y
    rw [← anchor y, ← assoc, anchor]
  have h : ∀ x (k : ℕ), op x (k : ZMod N) = x + k + 1 := by
    intro x k
    induction k with
    | zero => simp [anchor]
    | succ k ih => rw [Nat.cast_succ, step, ih]; ring
  intro x y
  have := h x y.val
  rwa [ZMod.natCast_zmod_val] at this

end Infinity.C06

#print axioms Infinity.C06.laver3_anchored
#print axioms Infinity.C06.laver3_left_distributive
#print axioms Infinity.C06.no_anchored_ld_three
#print axioms Infinity.C06.anchored_assoc_unique
