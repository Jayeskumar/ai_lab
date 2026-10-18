import Mathlib.Data.Nat.Fib.Basic
import Mathlib.Algebra.BigOperators.Group.List
import Mathlib.Tactic

/-!
# Cycle C19 — The longest Zeckendorf game: the arithmetic core

Paper indexing `F 1 = 1, F 2 = 2, F 3 = 3, …` is `F i = Nat.fib (i + 1)`; Cusenza et al.'s weights are
`a i = F (i + 2) - i - 2`.  With the potential `Ψ c = Σ c_i a_i` every move of the Zeckendorf game changes
`Ψ` by a fixed amount:

* `dPsi_C1`, `dPsi_S2`, `dPsi_split` : combine-1 and every split raise `Ψ` by `1`;
* `dPsi_combine` : the combine `C i` (`F (i-1) ∧ F i → F (i+1)`, `i ≥ 2`) raises `Ψ` by `i`.

`length_identity` sums these over an arbitrary list of moves: the total change of `Ψ` equals the number
of moves plus `Σ (i - 1)` over the combines `C i`, `i ≥ 2` (CLM-C19-01; with `Ψ(start) = 0` and
`Ψ(end) = B(n)` this is `|G| = B(n) - Σ (i-1) MC_i`).  `weight_even`, `weight_odd` evaluate the combine
weights of the strategy game on a Fibonacci input (CLM-C19-03): `Σ (i-1)` over `i = j, j-2, …` is
`⌊j²/4⌋`.
-/

namespace Infinity.C19

/-- Paper-indexed Fibonacci numbers `F 1 = 1, F 2 = 2, F 3 = 3, F 4 = 5, …` (as integers). -/
def F (i : ℕ) : ℤ := (Nat.fib (i + 1) : ℤ)

/-- Cusenza et al.'s weights `a i = F (i+2) - i - 2`. -/
def a (i : ℕ) : ℤ := F (i + 2) - i - 2

theorem F_rec (i : ℕ) : F (i + 2) = F (i + 1) + F i := by
  unfold F
  rw [show i + 2 + 1 = (i + 1) + 2 by ring, Nat.fib_add_two]
  push_cast; ring

theorem a_one : a 1 = 0 := by decide

theorem dPsi_C1 : a 2 - 2 * a 1 = 1 := by decide

theorem dPsi_S2 : a 1 + a 3 - 2 * a 2 = 1 := by decide

/-- Splitting two copies of `F (i+3)` into `F (i+1)` and `F (i+4)` raises the potential by one. -/
theorem dPsi_split (i : ℕ) : a (i + 1) + a (i + 4) - 2 * a (i + 3) = 1 := by
  unfold a
  have h1 := F_rec (i + 3)   -- F (i+5) = F (i+4) + F (i+3)
  have h2 := F_rec (i + 4)   -- F (i+6) = F (i+5) + F (i+4)
  have h3 := F_rec (i + 1)   -- F (i+3) = F (i+2) + F (i+1)
  have h4 := F_rec (i + 2)   -- F (i+4) = F (i+3) + F (i+2)
  simp only [show i + 1 + 2 = i + 3 by ring, show i + 4 + 2 = i + 6 by ring, show i + 3 + 2 = i + 5 by ring,
    show i + 3 + 1 = i + 4 by ring, show i + 4 + 1 = i + 5 by ring, show i + 2 + 1 = i + 3 by ring,
    show i + 1 + 1 = i + 2 by ring] at *
  push_cast
  linear_combination h2 - h1 - h4 + h3

/-- The combine `F (i+1) ∧ F (i+2) → F (i+3)` (the move `C (i+2)`) raises the potential by `i + 2`. -/
theorem dPsi_combine (i : ℕ) : a (i + 3) - a (i + 2) - a (i + 1) = (i + 2 : ℤ) := by
  unfold a
  have h := F_rec (i + 3)
  simp only [show i + 3 + 2 = i + 5 by ring, show i + 2 + 2 = i + 4 by ring, show i + 1 + 2 = i + 3 by ring,
    show i + 3 + 1 = i + 4 by ring] at *
  push_cast
  linear_combination h

/-- The moves of the game, named by their paper index. -/
inductive Move
  | C1                    -- F1 ∧ F1 → F2
  | S2                    -- F2 ∧ F2 → F1 ∧ F3
  | S (i : ℕ)             -- F (i+3) ∧ F (i+3) → F (i+1) ∧ F (i+4)   (the split S_{i+3})
  | C (i : ℕ)             -- F (i+1) ∧ F (i+2) → F (i+3)              (the combine C_{i+2})

/-- Change of the potential under a move. -/
def dPsi : Move → ℤ
  | .C1 => a 2 - 2 * a 1
  | .S2 => a 1 + a 3 - 2 * a 2
  | .S i => a (i + 1) + a (i + 4) - 2 * a (i + 3)
  | .C i => a (i + 3) - a (i + 2) - a (i + 1)

/-- The excess weight `i - 1` of a combine `C_i` with `i ≥ 2`, and `0` for all other moves. -/
def excess : Move → ℤ
  | .C i => (i + 1 : ℤ)
  | _ => 0

theorem dPsi_eq (m : Move) : dPsi m = 1 + excess m := by
  cases m with
  | C1 => simp [dPsi, excess, dPsi_C1]
  | S2 => simp [dPsi, excess, dPsi_S2]
  | S i => simp [dPsi, excess, dPsi_split]
  | C i => simp only [dPsi, excess, dPsi_combine]; ring

/-- **CLM-C19-01 (arithmetic core).** Along any list of moves the potential changes by the number of
moves plus the total excess `Σ (i - 1)` of the combines `C_i`, `i ≥ 2`. -/
theorem length_identity (ms : List Move) :
    (ms.map dPsi).sum = ms.length + (ms.map excess).sum := by
  induction ms with
  | nil => simp
  | cons m ms ih =>
    simp only [List.map_cons, List.sum_cons, List.length_cons, ih, dPsi_eq]
    push_cast; ring

/-- **CLM-C19-03 (weights).** The combines `C_2, C_4, …, C_{2k}` have total excess `1 + 3 + … + (2k-1) = k²`
(`= ⌊j²/4⌋` for `j = 2k`). -/
theorem weight_even (k : ℕ) : (∑ t ∈ Finset.range k, (2 * t + 1 : ℤ)) = (k : ℤ) ^ 2 := by
  induction k with
  | zero => simp
  | succ k ih => rw [Finset.sum_range_succ, ih]; push_cast; ring

/-- The combines `C_3, C_5, …, C_{2k+1}` have total excess `2 + 4 + … + 2k = k (k + 1)`
(`= ⌊j²/4⌋` for `j = 2k + 1`). -/
theorem weight_odd (k : ℕ) : (∑ t ∈ Finset.range k, (2 * t + 2 : ℤ)) = (k : ℤ) * (k + 1) := by
  induction k with
  | zero => simp
  | succ k ih => rw [Finset.sum_range_succ, ih]; push_cast; ring

theorem quarter_square_even (k : ℕ) : (2 * k) * (2 * k) / 4 = k ^ 2 := by
  rw [show 2 * k * (2 * k) = 4 * k ^ 2 by ring]; omega

theorem quarter_square_odd (k : ℕ) : (2 * k + 1) * (2 * k + 1) / 4 = k * (k + 1) := by
  rw [show (2 * k + 1) * (2 * k + 1) = 4 * (k * (k + 1)) + 1 by ring]; omega

end Infinity.C19

#print axioms Infinity.C19.dPsi_split
#print axioms Infinity.C19.dPsi_combine
#print axioms Infinity.C19.length_identity
#print axioms Infinity.C19.weight_even
#print axioms Infinity.C19.weight_odd
#print axioms Infinity.C19.quarter_square_even
#print axioms Infinity.C19.quarter_square_odd
