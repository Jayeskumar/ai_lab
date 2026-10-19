import Mathlib.NumberTheory.Real.GoldenRatio
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic

/-!
# Cycle C19 — The deficit bound `D(n) ≤ 1 + (t + 1)(t + 6)/2`: the arithmetic core

Written proof: `proofs/paper/C19.md`, Theorem 7 (CLM-C19-14, the move bound) and Theorem 8
(CLM-C19-15, the deficit bound).

**This file formalises only the arithmetic core of these theorems; no game is formalised.**

Indexing: Mathlib's `Nat.fib` has `fib 0 = 0, fib 1 = 1, fib 2 = 1, …`; the paper's `F_i` is
`fib (i + 1)`, a chip on level `k` is worth `F_{k+1} = fib (k + 2)`, and the chip weight is
`a_{k+1} = F_{k+3} - k - 3 = fib (k + 4) - k - 3` (the weight `Infinity.C19.a (k + 1)` of
`C19_Zeckendorf.lean`). `φ = Real.goldenRatio`, `ψ = Real.goldenConj = -1/φ`.

* `weight_identity` ((i)): `fib (k + 4) = φ² · fib (k + 2) + ψ^(k+2)` in `ℝ`, i.e.
  `a_{k+1} = φ² F_{k+1} + ψ^(k+2) - k - 3`.
* `geom_abs_goldenConj` : `Σ_{k ≤ T} |ψ|^(k+2) = 1 - |ψ|^(T+1) ≤ 1` (the finite form of
  `Σ_{k ≥ 0} |ψ|^(k+2) = ψ²/(1 - |ψ|) = 1`).
* `sum_lazy_le`, `sum_range_add_three` : `Σ_{k ≤ T} (k + 3) ℓ_k ≤ Σ_{k ≤ t} (k + 3) = (t + 1)(t + 6)/2`
  for a 0/1 string `ℓ` vanishing above `t`.
* `deficit_bound` ((ii)): for 0/1 digit strings `z, ℓ` (all values `≤ 1`) with `ℓ_k = 0` for `k > t`
  and equal values `Σ_{k ≤ T} F_{k+1} z_k = Σ_{k ≤ T} F_{k+1} ℓ_k`,
  `Σ_{k ≤ T} a_{k+1} (z_k - ℓ_k) ≤ 1 + (t + 1)(t + 6)/2` (in `ℝ`).
  With `z = Zeckendorf(n)`, `ℓ = lazy(n)` and `T` above both top levels the left side is
  `B(n) - Ψ(lazy(n))`, which is the inequality used in Theorems 7 and 8.
* `deficit_bound_int` : the same bound for the integer weights, with the exact natural-number
  quotient `(t + 1)(t + 6)/2`.

Not covered (still written proofs only): that the split phase ends at `lazy(n)` (Theorem 2), the game
facts `L(n) ≥ Ψ(lazy(n))` and `Ψ(Zeckendorf(n)) = B(n)`, hence the inequality `D(n) ≤ B(n) - Ψ(lazy n)`
itself, and the asymptotic `L(n) = φ² n - O(log² n)`.  The hypotheses of `deficit_bound` are weaker
than those of the application: `z` need not be a Zeckendorf string nor `ℓ` a lazy one, and `z, ℓ` need
not vanish above `T` (the sums are simply truncated at `T`).
-/

open Finset
open scoped goldenRatio

namespace Infinity.C19

/-- **CLM-C19-15 (i), the weight identity.** `F_{k+3} = φ² F_{k+1} + ψ^(k+2)`, i.e.
`fib (k + 4) = φ² · fib (k + 2) + ψ^(k+2)`. -/
theorem weight_identity (k : ℕ) :
    (Nat.fib (k + 4) : ℝ) = φ ^ 2 * Nat.fib (k + 2) + ψ ^ (k + 2) := by
  have h1 : (Nat.fib (k + 4) : ℝ) - φ * Nat.fib (k + 3) = ψ ^ (k + 3) :=
    Real.fib_succ_sub_goldenRatio_mul_fib (k + 3)
  have h2 : (Nat.fib (k + 3) : ℝ) - φ * Nat.fib (k + 2) = ψ ^ (k + 2) :=
    Real.fib_succ_sub_goldenRatio_mul_fib (k + 2)
  have h3 : φ + ψ = 1 := Real.goldenRatio_add_goldenConj
  linear_combination h1 + φ * h2 + ψ ^ (k + 2) * h3

/-- The chip weight in the form used in the proof: `a_{k+1} = φ² F_{k+1} + ψ^(k+2) - k - 3`. -/
theorem weight_eq (k : ℕ) :
    (Nat.fib (k + 4) : ℝ) - k - 3 = φ ^ 2 * Nat.fib (k + 2) + ψ ^ (k + 2) - (k + 3) := by
  rw [weight_identity]; ring

/-- `|ψ| = -ψ` and `|ψ|² + |ψ| = 1`. -/
theorem abs_goldenConj_sq_add : |ψ| ^ 2 + |ψ| = 1 := by
  rw [abs_of_neg Real.goldenConj_neg, neg_sq, Real.goldenConj_sq]; ring

/-- `Σ_{k ≤ T} |ψ|^(k+2) = 1 - |ψ|^(T+1)`. -/
theorem geom_abs_goldenConj (T : ℕ) :
    ∑ k ∈ range (T + 1), |ψ| ^ (k + 2) = 1 - |ψ| ^ (T + 1) := by
  have h := abs_goldenConj_sq_add
  induction T with
  | zero => simp only [zero_add, range_one, sum_singleton, pow_one]; linarith
  | succ T ih =>
    rw [sum_range_succ, ih]
    linear_combination (|ψ| ^ (T + 1)) * h

/-- `Σ_{k ≤ T} |ψ|^(k+2) ≤ 1`. -/
theorem geom_abs_goldenConj_le_one (T : ℕ) : ∑ k ∈ range (T + 1), |ψ| ^ (k + 2) ≤ 1 := by
  rw [geom_abs_goldenConj]
  have : 0 ≤ |ψ| ^ (T + 1) := pow_nonneg (abs_nonneg _) _
  linarith

/-- `Σ_{k ≤ t} (k + 3) = (t + 1)(t + 6)/2`. -/
theorem sum_range_add_three (t : ℕ) :
    ∑ k ∈ range (t + 1), ((k : ℝ) + 3) = ((t : ℝ) + 1) * (t + 6) / 2 := by
  induction t with
  | zero => simp; norm_num
  | succ t ih => rw [sum_range_succ, ih]; push_cast; ring

/-- For a 0/1 string `ℓ` vanishing above `t`: `Σ_{k ≤ T} (k + 3) ℓ_k ≤ Σ_{k ≤ t} (k + 3)`. -/
theorem sum_lazy_le (T t : ℕ) (ℓ : ℕ → ℕ) (hℓ : ∀ k, ℓ k ≤ 1) (hℓt : ∀ k, t < k → ℓ k = 0) :
    ∑ k ∈ range (T + 1), (k + 3) * ℓ k ≤ ∑ k ∈ range (t + 1), (k + 3) := by
  calc ∑ k ∈ range (T + 1), (k + 3) * ℓ k
      ≤ ∑ k ∈ range (T + 1), (if k ≤ t then k + 3 else 0) := by
        refine sum_le_sum (fun k _ => ?_)
        split_ifs with h
        · calc (k + 3) * ℓ k ≤ (k + 3) * 1 := Nat.mul_le_mul_left _ (hℓ k)
            _ = k + 3 := mul_one _
        · rw [hℓt k (by omega), mul_zero]
    _ = ∑ k ∈ (range (T + 1)).filter (· ≤ t), (k + 3) := by rw [sum_filter]
    _ ≤ ∑ k ∈ range (t + 1), (k + 3) := by
        refine sum_le_sum_of_subset (fun k hk => ?_)
        simp only [mem_filter, mem_range] at hk ⊢
        omega

/-- **CLM-C19-15 (ii), the arithmetic core of Theorems 7 and 8.** Let `z, ℓ : ℕ → ℕ` be digit strings
with all digits `≤ 1`, `ℓ_k = 0` for `k > t`, and the same value
`Σ_{k ≤ T} F_{k+1} z_k = Σ_{k ≤ T} F_{k+1} ℓ_k` (`F_{k+1} = fib (k + 2)`). Then
`Σ_{k ≤ T} a_{k+1} (z_k - ℓ_k) ≤ 1 + (t + 1)(t + 6)/2` with `a_{k+1} = fib (k + 4) - k - 3`.
(For `z = Zeckendorf(n)`, `ℓ = lazy(n)` the left side is `B(n) - Ψ(lazy n)`; the game-theoretic steps
that turn this into `D(n) ≤ 1 + (t + 1)(t + 6)/2` are not formalised.) -/
theorem deficit_bound (T t : ℕ) (z ℓ : ℕ → ℕ) (hz : ∀ k, z k ≤ 1) (hℓ : ∀ k, ℓ k ≤ 1)
    (hℓt : ∀ k, t < k → ℓ k = 0)
    (hval : ∑ k ∈ range (T + 1), Nat.fib (k + 2) * z k = ∑ k ∈ range (T + 1), Nat.fib (k + 2) * ℓ k) :
    ∑ k ∈ range (T + 1), ((Nat.fib (k + 4) : ℝ) - k - 3) * ((z k : ℝ) - ℓ k)
      ≤ 1 + ((t : ℝ) + 1) * (t + 6) / 2 := by
  set R := range (T + 1)
  -- the values agree, also in `ℝ`
  have hval' : ∑ k ∈ R, (Nat.fib (k + 2) : ℝ) * z k = ∑ k ∈ R, (Nat.fib (k + 2) : ℝ) * ℓ k := by
    exact_mod_cast hval
  -- split off the `φ²` part
  have hsplit : ∑ k ∈ R, ((Nat.fib (k + 4) : ℝ) - k - 3) * ((z k : ℝ) - ℓ k)
      = φ ^ 2 * (∑ k ∈ R, (Nat.fib (k + 2) : ℝ) * z k - ∑ k ∈ R, (Nat.fib (k + 2) : ℝ) * ℓ k)
        + ∑ k ∈ R, (ψ ^ (k + 2) * ((z k : ℝ) - ℓ k) - ((k : ℝ) + 3) * ((z k : ℝ) - ℓ k)) := by
    rw [← sum_sub_distrib, mul_sum, ← sum_add_distrib]
    refine sum_congr rfl (fun k _ => ?_)
    rw [weight_eq]; ring
  -- termwise bound of the remaining part
  have hterm : ∀ k ∈ R, ψ ^ (k + 2) * ((z k : ℝ) - ℓ k) - ((k : ℝ) + 3) * ((z k : ℝ) - ℓ k)
      ≤ |ψ| ^ (k + 2) + ((k : ℝ) + 3) * ℓ k := by
    intro k _
    have hz0 : (0 : ℝ) ≤ z k := Nat.cast_nonneg _
    have hz1 : (z k : ℝ) ≤ 1 := by exact_mod_cast hz k
    have hl0 : (0 : ℝ) ≤ ℓ k := Nat.cast_nonneg _
    have hl1 : (ℓ k : ℝ) ≤ 1 := by exact_mod_cast hℓ k
    have habs : |(z k : ℝ) - ℓ k| ≤ 1 := abs_sub_le_iff.mpr ⟨by linarith, by linarith⟩
    have h1 : ψ ^ (k + 2) * ((z k : ℝ) - ℓ k) ≤ |ψ| ^ (k + 2) := by
      calc ψ ^ (k + 2) * ((z k : ℝ) - ℓ k) ≤ |ψ ^ (k + 2) * ((z k : ℝ) - ℓ k)| := le_abs_self _
        _ = |ψ| ^ (k + 2) * |(z k : ℝ) - ℓ k| := by rw [abs_mul, abs_pow]
        _ ≤ |ψ| ^ (k + 2) * 1 :=
          mul_le_mul_of_nonneg_left habs (pow_nonneg (abs_nonneg _) _)
        _ = |ψ| ^ (k + 2) := mul_one _
    have h2 : -(((k : ℝ) + 3) * ((z k : ℝ) - ℓ k)) ≤ ((k : ℝ) + 3) * ℓ k := by
      have : (0 : ℝ) ≤ ((k : ℝ) + 3) * z k := mul_nonneg (by positivity) hz0
      linarith
    linarith
  -- the `(k + 3) ℓ_k` part
  have hlazy : ∑ k ∈ R, ((k : ℝ) + 3) * ℓ k ≤ ((t : ℝ) + 1) * (t + 6) / 2 := by
    rw [← sum_range_add_three t]
    have := sum_lazy_le T t ℓ hℓ hℓt
    exact_mod_cast this
  calc ∑ k ∈ R, ((Nat.fib (k + 4) : ℝ) - k - 3) * ((z k : ℝ) - ℓ k)
      = ∑ k ∈ R, (ψ ^ (k + 2) * ((z k : ℝ) - ℓ k) - ((k : ℝ) + 3) * ((z k : ℝ) - ℓ k)) := by
        rw [hsplit, hval', sub_self, mul_zero, zero_add]
    _ ≤ ∑ k ∈ R, (|ψ| ^ (k + 2) + ((k : ℝ) + 3) * ℓ k) := sum_le_sum hterm
    _ = ∑ k ∈ R, |ψ| ^ (k + 2) + ∑ k ∈ R, ((k : ℝ) + 3) * ℓ k := sum_add_distrib
    _ ≤ 1 + ((t : ℝ) + 1) * (t + 6) / 2 := add_le_add (geom_abs_goldenConj_le_one T) hlazy

/-- `(t + 1)(t + 6)` is even. -/
theorem two_dvd_succ_mul_add_six (t : ℕ) : 2 ∣ (t + 1) * (t + 6) := by
  rcases Nat.even_or_odd t with ⟨m, rfl⟩ | ⟨m, rfl⟩
  · exact ⟨(m + m + 1) * (m + 3), by ring⟩
  · exact ⟨(m + 1) * (2 * m + 7), by ring⟩

/-- **CLM-C19-15 (ii), integer form.** Under the hypotheses of `deficit_bound`, with the integer chip
weights `a_{k+1} = fib (k + 4) - k - 3`: `Σ_{k ≤ T} a_{k+1} (z_k - ℓ_k) ≤ 1 + (t + 1)(t + 6)/2`, where the
quotient `(t + 1)(t + 6)/2` is exact. -/
theorem deficit_bound_int (T t : ℕ) (z ℓ : ℕ → ℕ) (hz : ∀ k, z k ≤ 1) (hℓ : ∀ k, ℓ k ≤ 1)
    (hℓt : ∀ k, t < k → ℓ k = 0)
    (hval : ∑ k ∈ range (T + 1), Nat.fib (k + 2) * z k = ∑ k ∈ range (T + 1), Nat.fib (k + 2) * ℓ k) :
    ∑ k ∈ range (T + 1), ((Nat.fib (k + 4) : ℤ) - k - 3) * ((z k : ℤ) - ℓ k)
      ≤ 1 + (((t + 1) * (t + 6) / 2 : ℕ) : ℤ) := by
  have hreal := deficit_bound T t z ℓ hz hℓ hℓt hval
  obtain ⟨m, hm⟩ := two_dvd_succ_mul_add_six t
  have hq : (t + 1) * (t + 6) / 2 = m := by rw [hm]; omega
  rw [hq]
  have hm' : (m : ℝ) = ((t : ℝ) + 1) * (t + 6) / 2 := by
    have := congrArg (Nat.cast : ℕ → ℝ) hm
    push_cast at this
    linarith
  have : ((∑ k ∈ range (T + 1), ((Nat.fib (k + 4) : ℤ) - k - 3) * ((z k : ℤ) - ℓ k) : ℤ) : ℝ)
      ≤ ((1 + (m : ℤ) : ℤ) : ℝ) := by
    push_cast
    rw [hm']
    exact hreal
  exact_mod_cast this

end Infinity.C19

#print axioms Infinity.C19.weight_identity
#print axioms Infinity.C19.geom_abs_goldenConj
#print axioms Infinity.C19.sum_lazy_le
#print axioms Infinity.C19.sum_range_add_three
#print axioms Infinity.C19.deficit_bound
#print axioms Infinity.C19.deficit_bound_int
