import Mathlib.RingTheory.Polynomial.GaussLemma
import Mathlib.Algebra.Polynomial.Reverse
import Mathlib.RingTheory.PrincipalIdealDomain
import Mathlib.Basic.Real.Basic
import Mathlib.Tactic

/-!
# Cycle C02 — Exchange systems: uniqueness of emergent positional representations

A carry rule `m[k] → Σ_j b_j [k+j]` has the *carry polynomial* `P(X) = Σ_j b_j X^j - m`; its
positive root `r` is the emergent base, and a stable configuration (at most `m - 1` tokens
per level) is a digit string `c` with value `Σ_k c_k r^k = aeval r c`.

* `exists_large_coeff`: every nonzero multiple of a polynomial with constant term `-m` has a
  coefficient of absolute value `≥ m` (trailing-coefficient argument).
* `digits_unique` (CLM-C02-07): if `P` is primitive and irreducible over `ℚ`, two digit strings
  with digits in `[0, m)` and equal value at a real root `r` of `P` are equal.
-/

open Polynomial

namespace Infinity.C02

theorem exists_large_coeff (P Q : ℤ[X]) (m : ℤ) (hP0 : P.coeff 0 = -m) (hm : 0 < m)
    (hQ : Q ≠ 0) : ∃ k, m ≤ |(P * Q).coeff k| := by
  refine ⟨(P * Q).natTrailingDegree, ?_⟩
  have hP : P.coeff 0 ≠ 0 := by rw [hP0]; omega
  have h1 : (P * Q).coeff (P * Q).natTrailingDegree = (P * Q).trailingCoeff := rfl
  rw [h1, trailingCoeff_mul, trailingCoeff_eq_coeff_zero hP, hP0]
  have hq : Q.trailingCoeff ≠ 0 := trailingCoeff_nonzero_iff_nonzero.mpr hQ
  have h2 : 1 ≤ |Q.trailingCoeff| := Int.one_le_abs hq
  rw [abs_mul, abs_neg, abs_of_pos hm]
  nlinarith

/-- **CLM-C02-07.** Uniqueness of representations in the emergent base of a carry rule whose
carry polynomial is primitive and irreducible over `ℚ`. -/
theorem digits_unique (P : ℤ[X]) (m : ℤ) (hm : 0 < m) (hP0 : P.coeff 0 = -m)
    (hprim : P.IsPrimitive) (hirr : Irreducible (P.map (Int.castRingHom ℚ)))
    (r : ℝ) (hr : aeval r P = 0) (c d : ℤ[X])
    (hc : ∀ k, 0 ≤ c.coeff k ∧ c.coeff k < m) (hd : ∀ k, 0 ≤ d.coeff k ∧ d.coeff k < m)
    (hval : aeval r c = aeval r d) : c = d := by
  by_contra hne
  have hΔne : c - d ≠ 0 := sub_ne_zero.mpr hne
  have hΔr : aeval r (c - d) = 0 := by simp [hval]
  -- over ℚ, the irreducible `P` must divide `c - d` (otherwise they are coprime, and a
  -- Bézout identity evaluated at the common root `r` gives `0 = 1`)
  have hdivQ : P.map (Int.castRingHom ℚ) ∣ (c - d).map (Int.castRingHom ℚ) := by
    by_contra hnd
    obtain ⟨a, b, hab⟩ := (hirr.coprime_iff_not_dvd).mpr hnd
    have h := congrArg (aeval r) hab
    have e1 : aeval r (P.map (Int.castRingHom ℚ)) = 0 := by
      rw [show (Int.castRingHom ℚ) = algebraMap ℤ ℚ from rfl, aeval_map_algebraMap]; exact hr
    have e2 : aeval r ((c - d).map (Int.castRingHom ℚ)) = 0 := by
      rw [show (Int.castRingHom ℚ) = algebraMap ℤ ℚ from rfl, aeval_map_algebraMap]; exact hΔr
    rw [map_add, map_mul, map_mul, e1, e2, mul_zero, mul_zero, add_zero, map_one] at h
    exact zero_ne_one h
  -- Gauss's lemma: divisibility descends to ℤ[X]
  have hdivZ : P ∣ c - d := (IsPrimitive.Int.dvd_iff_map_cast_dvd_map_cast P (c - d) hprim).mpr hdivQ
  obtain ⟨Q, hQ⟩ := hdivZ
  have hQne : Q ≠ 0 := by
    rintro rfl
    exact hΔne (by simpa using hQ)
  obtain ⟨k, hk⟩ := exists_large_coeff P Q m hP0 hm hQne
  rw [← hQ, coeff_sub] at hk
  have := hc k
  have := hd k
  have : |c.coeff k - d.coeff k| < m := by rw [abs_lt]; constructor <;> linarith
  linarith

end Infinity.C02

#print axioms Infinity.C02.exists_large_coeff
#print axioms Infinity.C02.digits_unique
