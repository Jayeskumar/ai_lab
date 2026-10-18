import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Tactic

/-!
# Cycle C15 — Magma cellular automata

The automaton of a binary operation `*` updates a row by `c'ᵢ = cᵢ * cᵢ₊₁`. Its `t`-step local map
`F t x` (the value of cell `0` after `t` steps, as a function of the row `x : ℕ → M`) satisfies
`F 0 x = x 0` and `F (t+1) x = F t x * F t (x ∘ succ)`.

* `ca_comm_binomial` (CLM-C15-01, commutative case): in a commutative monoid,
  `F t x = ∏_{k ≤ t} (x k) ^ (t choose k)` — Pascal's triangle in the exponents.
* `ca_step_shift`: the defining recursion also holds when the first step is peeled off at the end
  (`F (t+1) x = F t (fun i => x i * x (i+1))`), i.e. the local maps compose like the global map.
-/

namespace Infinity.C15

variable {M : Type*}

/-- The `t`-step local map of the automaton `c'ᵢ = cᵢ * cᵢ₊₁`, read at cell `0`. -/
def F [Mul M] : ℕ → (ℕ → M) → M
  | 0, x => x 0
  | t + 1, x => F t x * F t (fun i => x (i + 1))

/-- Peeling off the first step instead of the last one: `F (t+1) x = F t (x')` with `x'` the row after
one step. -/
theorem ca_step_shift [Mul M] : ∀ (t : ℕ) (x : ℕ → M), F (t + 1) x = F t (fun i => x i * x (i + 1))
  | 0, x => rfl
  | t + 1, x => by
    show F (t + 1) x * F (t + 1) (fun i => x (i + 1)) = F (t + 1) (fun i => x i * x (i + 1))
    rw [ca_step_shift t x, ca_step_shift t (fun i => x (i + 1))]
    rfl

/-- **CLM-C15-01 (commutative case).** In a commutative monoid the light cone is Pascal's triangle:
`F t x = ∏_{k=0}^{t} (x k) ^ (t.choose k)`. -/
theorem ca_comm_binomial [CommMonoid M] :
    ∀ (t : ℕ) (x : ℕ → M), F t x = ∏ k ∈ Finset.range (t + 1), x k ^ (t.choose k) := by
  intro t
  induction t with
  | zero => intro x; simp [F]
  | succ t ih =>
    intro x
    show F t x * F t (fun i => x (i + 1)) = _
    rw [ih x, ih (fun i => x (i + 1))]
    -- right-hand side: peel off k = 0, use Pascal's rule and split the product
    rw [Finset.prod_range_succ' (fun k => x k ^ ((t + 1).choose k)) (t + 1)]
    simp only [Nat.choose_succ_succ, pow_add, Finset.prod_mul_distrib, Nat.choose_zero_right, pow_one]
    -- left factor: peel off k = 0 as well; the extra top term of the shifted product is x (t+1) ^ 0
    rw [Finset.prod_range_succ' (fun k => x k ^ (t.choose k)) t,
      Finset.prod_range_succ (fun k => x (k + 1) ^ (t.choose (k + 1))) t]
    simp only [Nat.choose_zero_right, pow_one, Nat.choose_succ_self, pow_zero, mul_one]
    ac_rfl

end Infinity.C15

#print axioms Infinity.C15.ca_step_shift
#print axioms Infinity.C15.ca_comm_binomial
