import Mathlib.Data.Fin.Basic
import Mathlib.Tactic

/-!
# Cycle C17 — The forced anchored table (CLM-C17-05, uniqueness for every `N`)

Written proof: `proofs/paper/C17.md`, Observation 4, paragraph "Uniqueness for every N".

Elements are `Fin N` with `N ≥ 1` (`[NeZero N]`) and the modular addition of `Fin N`, so `x + 1`
means `x + 1 (mod N)`.  The hypotheses are

* the anchor `x ⋆ 0 = x + 1` for all `x`, and
* the instances `x ⋆ (y + 1) = (x ⋆ y) ⋆ (x + 1)` of left-distributivity at `z = 0`
  **without wrap-around**: all `x` and all `y` with `y ≤ N - 2`, written `y.val + 1 < N`
  (for `N = 1` there is no such `y`).

Results (all for every `N ≥ 1`):

* `row_last` (CLM-C17-05 (a)): row `N - 1` is the identity, `(N - 1) ⋆ y = y`.
* `row_gt` ((b)): for `x < N - 1` every entry of row `x` is `> x` (as natural numbers).
* `forced_unique` ((c)): two operations satisfying the hypotheses are equal, i.e. the instances with
  `y ≤ N - 2` force at most one table.
* `full_instance_iff`: the forced table satisfies the full instance (including the wrap-around
  `y = N - 1`) iff the wrap-around equations `x + 1 = (x ⋆ (N - 1)) ⋆ (x + 1)` hold.
* `forced_exists` (the existence half of "Laver's recursion has a unique solution for every `N`",
  the parenthetical remark of Observation 4): an operation satisfying the hypotheses exists for
  every `N ≥ 1`. It is built by the downward recursion of the written proof (`lav`).
* `forced_existsUnique`: both together.

Not covered here: for which `N` the wrap-around equations hold (the open converse "only powers of 2"),
and the identification of the forced table with Laver's table `A_n` for `N = 2ⁿ`, which therefore
satisfies the full instance (Laver's theorem; for `A₃` see `C06_Laver.lean`).
-/

namespace Infinity.C17

section FinN

variable {N : ℕ} [NeZero N]

/-- If `y + 1` does not wrap around, its value is `y.val + 1`. -/
theorem val_add_one {y : Fin N} (h : y.val + 1 < N) : (y + 1).val = y.val + 1 := by
  rw [Fin.val_add, Fin.val_one', Nat.mod_eq_of_lt (show 1 < N by omega), Nat.mod_eq_of_lt h]

/-- `(N - 1) + 1 = 0` in `Fin N`. -/
theorem add_one_eq_zero {x : Fin N} (h : x.val = N - 1) : x + 1 = 0 := by
  have hN : 0 < N := Nat.pos_of_ne_zero (NeZero.ne N)
  ext
  rw [Fin.val_add, Fin.val_one', Fin.val_zero]
  rcases Nat.lt_or_ge 1 N with h1 | h1
  · rw [Nat.mod_eq_of_lt h1, h, Nat.sub_add_cancel hN, Nat.mod_self]
  · have : N = 1 := by omega
    subst this
    exact Nat.mod_one _

/-- Induction along a row: `P 0` and `P y → P (y + 1)` for `y ≤ N - 2` give `P y` for all `y`. -/
theorem row_induction {P : Fin N → Prop} (h0 : P 0)
    (hs : ∀ y : Fin N, y.val + 1 < N → P y → P (y + 1)) : ∀ y, P y := by
  suffices h : ∀ k (hk : k < N), P ⟨k, hk⟩ from fun y => h y.val y.isLt
  intro k
  induction k with
  | zero =>
    intro hk
    have e : (⟨0, hk⟩ : Fin N) = 0 := by ext; simp
    rw [e]; exact h0
  | succ k ih =>
    intro hk
    have hk' : k < N := by omega
    have e : (⟨k + 1, hk⟩ : Fin N) = (⟨k, hk'⟩ : Fin N) + 1 := by
      ext; rw [val_add_one (by simpa using hk)]
    rw [e]
    exact hs _ (by simpa using hk) (ih hk')

section Forced

variable (op : Fin N → Fin N → Fin N) (anchor : ∀ x, op x 0 = x + 1)
  (step : ∀ x y : Fin N, y.val + 1 < N → op x (y + 1) = op (op x y) (x + 1))
include anchor step

/-- **CLM-C17-05 (a).** Under the anchor and the instances `y ≤ N - 2`, row `N - 1` is the
identity: `(N - 1) ⋆ y = y` for all `y`. -/
theorem row_last : ∀ x y : Fin N, x.val = N - 1 → op x y = y := by
  intro x y hx
  have hx1 : x + 1 = 0 := add_one_eq_zero hx
  refine row_induction (P := fun y => op x y = y) ?_ ?_ y
  · rw [anchor, hx1]
  · intro y hy ih
    rw [step x y hy, ih, hx1, anchor]

/-- **CLM-C17-05 (b).** For `x < N - 1` every entry of row `x` exceeds `x` (as natural numbers). -/
theorem row_gt : ∀ x y : Fin N, x.val < N - 1 → x.val < (op x y).val := by
  -- strong downward induction on `x`, i.e. strong induction on `d = N - 1 - x`
  suffices h : ∀ d, ∀ x : Fin N, N - 1 - x.val = d → ∀ y, x.val < N - 1 → x.val < (op x y).val from
    fun x y hx => h _ x rfl y hx
  intro d
  induction d using Nat.strong_induction_on with
  | _ d ih =>
    intro x hd y hx
    have hx1 : (x + 1).val = x.val + 1 := val_add_one (by omega)
    refine row_induction (P := fun y => x.val < (op x y).val) ?_ ?_ y
    · rw [anchor, hx1]; omega
    · intro y hy ihy
      rw [step x y hy]
      by_cases hv : (op x y).val = N - 1
      · rw [row_last op anchor step _ _ hv, hx1]; omega
      · have hvlt : (op x y).val < N - 1 := by have := (op x y).isLt; omega
        have := ih (N - 1 - (op x y).val) (by omega) (op x y) rfl (x + 1) hvlt
        omega

/-- **The wrap-around instance.** Under the hypotheses, the full instance
`x ⋆ (y + 1) = (x ⋆ y) ⋆ (x + 1)` (all `y`, including `y = N - 1`) holds iff the wrap-around equations
`x + 1 = (x ⋆ (N - 1)) ⋆ (x + 1)` hold for all `x`. -/
theorem full_instance_iff :
    (∀ x y : Fin N, op x (y + 1) = op (op x y) (x + 1)) ↔
      ∀ x y : Fin N, y.val = N - 1 → x + 1 = op (op x y) (x + 1) := by
  constructor
  · intro h x y hy
    have := h x y
    rwa [add_one_eq_zero hy, anchor] at this
  · intro h x y
    by_cases hy : y.val + 1 < N
    · exact step x y hy
    · have hy' : y.val = N - 1 := by have := y.isLt; omega
      rw [add_one_eq_zero hy', anchor]
      exact h x y hy'

end Forced

/-- **CLM-C17-05 (c), uniqueness for every `N`.** Two operations on `Fin N` that both satisfy the anchor
`x ⋆ 0 = x + 1` and the instances `x ⋆ (y + 1) = (x ⋆ y) ⋆ (x + 1)` for `y ≤ N - 2` are equal. -/
theorem forced_unique (op₁ op₂ : Fin N → Fin N → Fin N)
    (anchor₁ : ∀ x, op₁ x 0 = x + 1)
    (step₁ : ∀ x y : Fin N, y.val + 1 < N → op₁ x (y + 1) = op₁ (op₁ x y) (x + 1))
    (anchor₂ : ∀ x, op₂ x 0 = x + 1)
    (step₂ : ∀ x y : Fin N, y.val + 1 < N → op₂ x (y + 1) = op₂ (op₂ x y) (x + 1)) :
    op₁ = op₂ := by
  suffices h : ∀ d, ∀ x : Fin N, N - 1 - x.val = d → ∀ y, op₁ x y = op₂ x y by
    funext x y; exact h _ x rfl y
  intro d
  induction d using Nat.strong_induction_on with
  | _ d ih =>
    intro x hd y
    by_cases hxl : x.val = N - 1
    · rw [row_last op₁ anchor₁ step₁ x y hxl, row_last op₂ anchor₂ step₂ x y hxl]
    have hx : x.val < N - 1 := by have := x.isLt; omega
    refine row_induction (P := fun y => op₁ x y = op₂ x y) ?_ ?_ y
    · rw [anchor₁, anchor₂]
    · intro y hy ihy
      rw [step₁ x y hy, step₂ x y hy, ihy]
      have hv := row_gt op₂ anchor₂ step₂ x y hx
      exact ih (N - 1 - (op₂ x y).val) (by have := (op₂ x y).isLt; omega) _ rfl _

end FinN

/-! ### Existence: the downward recursion (Laver's recursion without wrap-around) -/

section Existence

variable {N : ℕ}

/-- The forced table on natural numbers, by the recursion of the written proof: row `N - 1` (and
anything above) is the identity; for `x < N - 1`, `x ⋆ 0 = x + 1` and `x ⋆ (y + 1) = v ⋆ (x + 1)` with
`v = x ⋆ y`, a row that is already defined because `v > x` (the fallback value `0` is never used,
`lav_spec`). -/
def lav (N : ℕ) (x y : ℕ) : ℕ :=
  if x + 1 < N then
    match y with
    | 0 => x + 1
    | y + 1 =>
      if h : x < lav N x y then lav N (lav N x y) (x + 1) else 0
  else y
termination_by (N - x, y)
decreasing_by
  · exact Prod.Lex.right _ (Nat.lt_succ_self y)
  · exact Prod.Lex.left _ _ (by omega)

theorem lav_top {x : ℕ} (y : ℕ) (hx : ¬ x + 1 < N) : lav N x y = y := by
  rw [lav.eq_def]; simp [hx]

theorem lav_zero {x : ℕ} (hx : x + 1 < N) : lav N x 0 = x + 1 := by
  rw [lav.eq_def]; simp [hx]

theorem lav_succ {x : ℕ} (y : ℕ) (hx : x + 1 < N) (hlt : x < lav N x y) :
    lav N x (y + 1) = lav N (lav N x y) (x + 1) := by
  conv_lhs => rw [lav.eq_def]
  simp [hx, hlt]

/-- The invariant of the recursion: for `x < N - 1` and `y < N`, `x < x ⋆ y < N`. -/
theorem lav_spec : ∀ x y : ℕ, x + 1 < N → y < N → x < lav N x y ∧ lav N x y < N := by
  suffices h : ∀ d, ∀ x : ℕ, N - 1 - x = d → x + 1 < N → ∀ y, y < N → x < lav N x y ∧ lav N x y < N by
    intro x y hx hy; exact h _ x rfl hx y hy
  intro d
  induction d using Nat.strong_induction_on with
  | _ d ih =>
    intro x hd hx y
    induction y with
    | zero => intro _; rw [lav_zero hx]; omega
    | succ y ihy =>
      intro hy
      obtain ⟨h1, h2⟩ := ihy (by omega)
      rw [lav_succ y hx h1]
      by_cases hv : lav N x y + 1 < N
      · have := ih (N - 1 - lav N x y) (by omega) (lav N x y) rfl hv (x + 1) (by omega)
        omega
      · rw [lav_top _ hv]; omega

theorem lav_lt (x y : ℕ) (hy : y < N) : lav N x y < N := by
  by_cases h : x + 1 < N
  · exact (lav_spec x y h hy).2
  · rw [lav_top y h]; exact hy

variable [NeZero N]

/-- The forced table as an operation on `Fin N`. -/
def forcedOp (N : ℕ) [NeZero N] (x y : Fin N) : Fin N :=
  ⟨lav N x.val y.val, lav_lt x.val y.val y.isLt⟩

/-- **Existence (Observation 4, "Laver's recursion has a solution for every `N`").** The forced table
satisfies the anchor and every instance with `y ≤ N - 2`. -/
theorem forced_exists :
    (∀ x : Fin N, forcedOp N x 0 = x + 1) ∧
    ∀ x y : Fin N, y.val + 1 < N →
      forcedOp N x (y + 1) = forcedOp N (forcedOp N x y) (x + 1) := by
  constructor
  · intro x
    ext
    simp only [forcedOp, Fin.val_zero]
    by_cases hx : x.val + 1 < N
    · rw [lav_zero hx, val_add_one hx]
    · rw [lav_top 0 hx, add_one_eq_zero (show x.val = N - 1 by have := x.isLt; omega), Fin.val_zero]
  · intro x y hy
    ext
    simp only [forcedOp]
    rw [val_add_one hy]
    by_cases hx : x.val + 1 < N
    · rw [val_add_one hx]
      exact lav_succ y.val hx (lav_spec x.val y.val hx y.isLt).1
    · have hx' : x.val = N - 1 := by have := x.isLt; omega
      rw [lav_top _ hx, lav_top _ hx, add_one_eq_zero hx', Fin.val_zero]
      exact (lav_zero hy).symm

/-- **CLM-C17-05 with existence.** For every `N ≥ 1` there is exactly one operation on `Fin N` satisfying
the anchor and the instances `x ⋆ (y + 1) = (x ⋆ y) ⋆ (x + 1)` for `y ≤ N - 2`. -/
theorem forced_existsUnique :
    ∃! op : Fin N → Fin N → Fin N, (∀ x, op x 0 = x + 1) ∧
      ∀ x y : Fin N, y.val + 1 < N → op x (y + 1) = op (op x y) (x + 1) :=
  ⟨forcedOp N, forced_exists, fun op h =>
    forced_unique op (forcedOp N) h.1 h.2 forced_exists.1 forced_exists.2⟩

end Existence

end Infinity.C17

#print axioms Infinity.C17.row_last
#print axioms Infinity.C17.row_gt
#print axioms Infinity.C17.full_instance_iff
#print axioms Infinity.C17.forced_unique
#print axioms Infinity.C17.forced_exists
#print axioms Infinity.C17.forced_existsUnique
