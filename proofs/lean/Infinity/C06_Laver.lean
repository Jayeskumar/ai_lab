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
* `anchored_rd_unique` (CLM-C06-03): the only right-distributive anchored operation is `x ⋆ y = x + 1`.
* `odd_law_even_impossible`, `odd_law_formula`, `odd_law_model` (CLM-C06-06): the law
  `(x ⋆ y) ⋆ z = x ⋆ ((y ⋆ z) ⋆ z)` has an anchored model on `ZMod N` iff `N` is odd, and then
  `2 · (x ⋆ y - x - 1) = y`, i.e. `x ⋆ y = x + 1 + y/2`.
* `centralizer_eq`, `comp_eq`, `id_eq` and `leftPerm_assoc`, `leftPerm_comm`, `leftPerm_one_mul`,
  `leftPerm_mul_one` (CLM-C06-08): a pairwise commuting family of maps `f m` with `f m e = m` is
  closed under composition and contains the identity; hence `a · b := (a - 1) ⋆ b` turns an anchored
  left-permutable magma into a commutative monoid with identity `0`.
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

/-- **CLM-C06-03.** An anchored right-distributive operation on `ZMod N` is `x ⋆ y = x + 1`. -/
theorem anchored_rd_unique {N : ℕ} [NeZero N] (op : ZMod N → ZMod N → ZMod N)
    (anchor : ∀ x, op x 0 = x + 1) (rd : ∀ x y z, op (op x y) z = op (op x z) (op y z)) :
    ∀ x y, op x y = x + 1 := by
  have step : ∀ x y, op (x + 1) (y + 1) = op x y + 1 := by
    intro x y
    have := rd x y 0
    rw [anchor, anchor, anchor] at this
    exact this.symm
  have h : ∀ a (k : ℕ), op (a + k) (k : ZMod N) = a + 1 + k := by
    intro a k
    induction k with
    | zero => simp [anchor]
    | succ k ih =>
      rw [Nat.cast_succ, ← add_assoc, step, ih]; ring
  intro x y
  have := h (x - y) y.val
  rw [ZMod.natCast_zmod_val] at this
  rw [show x - y + y = x by ring] at this
  rw [this]; ring

section OddLaw

variable {N : ℕ} (op : ZMod N → ZMod N → ZMod N)

/-- The `z = 0` instance of the odd law: `x ⋆ (y + 2) = x ⋆ y + 1`. -/
theorem odd_law_step (anchor : ∀ x, op x 0 = x + 1)
    (law : ∀ x y z, op (op x y) z = op x (op (op y z) z)) :
    ∀ x y, op x (y + 2) = op x y + 1 := by
  intro x y
  have := law x y 0
  rw [anchor, anchor, anchor] at this
  rw [show y + 1 + 1 = y + 2 by ring] at this
  exact this.symm

theorem odd_law_even_steps (anchor : ∀ x, op x 0 = x + 1)
    (law : ∀ x y z, op (op x y) z = op x (op (op y z) z)) :
    ∀ x (k : ℕ), op x ((2 * k : ℕ) : ZMod N) = x + 1 + k := by
  intro x k
  induction k with
  | zero => simp [anchor]
  | succ k ih =>
    have e : ((2 * (k + 1) : ℕ) : ZMod N) = ((2 * k : ℕ) : ZMod N) + 2 := by push_cast; ring
    rw [e, odd_law_step op anchor law, ih]; push_cast; ring

/-- **CLM-C06-06 (no even sizes).** For even `N ≥ 2` the odd law has no anchored model. -/
theorem odd_law_even_impossible [NeZero N] (hN : 2 ≤ N) (heven : 2 ∣ N)
    (anchor : ∀ x, op x 0 = x + 1)
    (law : ∀ x y z, op (op x y) z = op x (op (op y z) z)) : False := by
  obtain ⟨h, rfl⟩ := heven
  have := odd_law_even_steps op anchor law 0 h
  rw [ZMod.natCast_self, anchor] at this
  have hz : ((h : ℕ) : ZMod (2 * h)) = 0 := by linear_combination -this
  rw [ZMod.natCast_eq_zero_iff] at hz
  have := Nat.le_of_dvd (by omega) hz
  omega

/-- **CLM-C06-06 (the formula).** In any anchored model of the odd law, `2 · (x ⋆ y - x - 1) = y`.
For odd `N`, where `2` is a unit, this determines the operation: `x ⋆ y = x + 1 + y / 2`. -/
theorem odd_law_formula [NeZero N] (hodd : N % 2 = 1) (anchor : ∀ x, op x 0 = x + 1)
    (law : ∀ x y z, op (op x y) z = op x (op (op y z) z)) :
    ∀ x y, 2 * (op x y - x - 1) = y := by
  intro x y
  have key := odd_law_even_steps op anchor law x (y.val * ((N + 1) / 2))
  have hcast : ((2 * (y.val * ((N + 1) / 2)) : ℕ) : ZMod N) = y := by
    have : 2 * (y.val * ((N + 1) / 2)) = y.val + y.val * N := by
      have h2 : 2 * ((N + 1) / 2) = N + 1 := by omega
      calc 2 * (y.val * ((N + 1) / 2)) = y.val * (2 * ((N + 1) / 2)) := by ring
        _ = y.val + y.val * N := by rw [h2]; ring
    rw [this]; push_cast
    rw [ZMod.natCast_self, ZMod.natCast_zmod_val]; ring
  rw [hcast] at key
  have h2K : (2 : ZMod N) * ((y.val * ((N + 1) / 2) : ℕ) : ZMod N) = y := by
    calc (2 : ZMod N) * ((y.val * ((N + 1) / 2) : ℕ) : ZMod N)
        = ((2 * (y.val * ((N + 1) / 2)) : ℕ) : ZMod N) := by simp only [Nat.cast_mul, Nat.cast_ofNat]
      _ = y := hcast
  rw [key]
  linear_combination h2K

/-- **CLM-C06-06 (existence).** For odd `N`, `x ⋆ y = x + 1 + h·y` with `h = (N + 1)/2` is an
anchored model of the odd law. -/
theorem odd_law_model (hodd : N % 2 = 1) :
    let h : ZMod N := ((N + 1) / 2 : ℕ)
    (∀ x : ZMod N, x + 1 + h * 0 = x + 1) ∧
    ∀ x y z : ZMod N, (x + 1 + h * y) + 1 + h * z = x + 1 + h * ((y + 1 + h * z) + 1 + h * z) := by
  intro h
  have h2 : (2 : ZMod N) * h = 1 := by
    have : 2 * ((N + 1) / 2) = N + 1 := by omega
    show (2 : ZMod N) * (((N + 1) / 2 : ℕ) : ZMod N) = 1
    have e : ((2 * ((N + 1) / 2) : ℕ) : ZMod N) = ((N + 1 : ℕ) : ZMod N) := by rw [this]
    push_cast at e
    rw [e, ZMod.natCast_self, zero_add]
  refine ⟨fun x => by ring, fun x y z => ?_⟩
  linear_combination (-(1 + h * z)) * h2

end OddLaw

section LeftPermutable

variable {M : Type*} (e : M) (f : M → M → M)

/-- In a pairwise commuting family `f m` with `f m e = m`, every map `g` commuting with the whole
family is the member `f (g e)`: the family is its own centraliser. -/
theorem centralizer_eq (hval : ∀ m, f m e = m) (hcomm : ∀ a b x, f a (f b x) = f b (f a x))
    (g : M → M) (hg : ∀ c x, g (f c x) = f c (g x)) : ∀ m, g m = f (g e) m := by
  intro m
  calc g m = g (f m e) := by rw [hval]
    _ = f m (g e) := hg m e
    _ = f m (f (g e) e) := by rw [hval]
    _ = f (g e) (f m e) := hcomm m (g e) e
    _ = f (g e) m := by rw [hval]

theorem comp_eq (hval : ∀ m, f m e = m) (hcomm : ∀ a b x, f a (f b x) = f b (f a x)) :
    ∀ a b x, f a (f b x) = f (f a b) x := by
  intro a b x
  have := centralizer_eq e f hval hcomm (fun y => f a (f b y))
    (fun c y => by rw [hcomm b c, hcomm a c]) x
  simpa [hval] using this

theorem id_eq (hval : ∀ m, f m e = m) (hcomm : ∀ a b x, f a (f b x) = f b (f a x)) :
    ∀ x, f e x = x := by
  intro x
  have := centralizer_eq e f hval hcomm id (fun c y => rfl) x
  simpa using this.symm

end LeftPermutable

section AnchoredLeftPermutable

variable {N : ℕ} (op : ZMod N → ZMod N → ZMod N) (anchor : ∀ x, op x 0 = x + 1)
  (lp : ∀ x y z, op x (op y z) = op y (op x z))
include anchor lp

omit lp in
private theorem lp_val : ∀ m : ZMod N, op (m - 1) 0 = m := by intro m; rw [anchor]; ring

omit anchor in
private theorem lp_comm : ∀ a b x : ZMod N, op (a - 1) (op (b - 1) x) = op (b - 1) (op (a - 1) x) :=
  fun _ _ _ => lp _ _ _

/-- **CLM-C06-08.** `a · b := (a - 1) ⋆ b` is associative. -/
theorem leftPerm_assoc : ∀ a b c : ZMod N,
    op (op (a - 1) b - 1) c = op (a - 1) (op (b - 1) c) := by
  intro a b c
  exact (comp_eq (0 : ZMod N) (fun m z => op (m - 1) z) (lp_val op anchor) (lp_comm op lp)
    a b c).symm

/-- **CLM-C06-08.** `a · b := (a - 1) ⋆ b` is commutative. -/
theorem leftPerm_comm : ∀ a b : ZMod N, op (a - 1) b = op (b - 1) a := by
  intro a b
  have h1 := lp_val op anchor b
  have h2 := lp_val op anchor a
  calc op (a - 1) b = op (a - 1) (op (b - 1) 0) := by rw [h1]
    _ = op (b - 1) (op (a - 1) 0) := lp _ _ _
    _ = op (b - 1) a := by rw [h2]

/-- **CLM-C06-08.** `0` is a two-sided identity for `a · b := (a - 1) ⋆ b`. -/
theorem leftPerm_one_mul : ∀ b : ZMod N, op (0 - 1) b = b :=
  id_eq (0 : ZMod N) (fun m z => op (m - 1) z) (lp_val op anchor) (lp_comm op lp)

omit lp in
theorem leftPerm_mul_one : ∀ a : ZMod N, op (a - 1) 0 = a := lp_val op anchor

end AnchoredLeftPermutable

end Infinity.C06

#print axioms Infinity.C06.laver3_anchored
#print axioms Infinity.C06.laver3_left_distributive
#print axioms Infinity.C06.no_anchored_ld_three
#print axioms Infinity.C06.anchored_assoc_unique
#print axioms Infinity.C06.anchored_rd_unique
#print axioms Infinity.C06.odd_law_even_impossible
#print axioms Infinity.C06.odd_law_formula
#print axioms Infinity.C06.odd_law_model
#print axioms Infinity.C06.leftPerm_assoc
#print axioms Infinity.C06.leftPerm_comm
#print axioms Infinity.C06.leftPerm_one_mul
#print axioms Infinity.C06.leftPerm_mul_one
