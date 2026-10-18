import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

/-!
# Cycle C13 — Anchored spectra II

Anchored magmas on `ZMod N`: `x ⋆ 0 = x + 1`.

* `law13_size_dvd_three`, `law13_model_three` (CLM-C13-04 (a)): the law
  `x ⋆ (y ⋆ z) = ((z ⋆ x) ⋆ x) ⋆ y` has an anchored model of size `N` only if `N ∣ 3`, and
  `x ⋆ y = x + 1 + 2y` is a model of size 3. So the anchored spectrum is exactly `{1, 3}`.
* `law12_size_dvd_two`, `law12_model_two` (CLM-C13-04 (b)): the law
  `x ⋆ (y ⋆ z) = ((x ⋆ y) ⋆ z) ⋆ x` has an anchored model of size `N` only if `N ∣ 2`, and
  `x ⋆ y = x + 1` is a model of size 2. So the anchored spectrum is exactly `{1, 2}`.
-/

namespace Infinity.C13

section Law13

variable {N : ℕ} (op : ZMod N → ZMod N → ZMod N) (anchor : ∀ x, op x 0 = x + 1)
  (law : ∀ x y z, op x (op y z) = op (op (op z x) x) y)
include anchor law

theorem law13_rr : ∀ z, op 0 (op 0 z) = z + 3 := by
  intro z
  rw [law, anchor, anchor, anchor]; ring

theorem law13_key : ∀ y z, op 0 (op y z) = op (z + 2) y := by
  intro y z
  rw [law, anchor, anchor]; ring_nf

/-- `w ⋆ y = (w - 2) ⋆ (y - 2) + 3`. -/
theorem law13_shift : ∀ w y, op w y = op (w - 2) (y - 2) + 3 := by
  intro w y
  have h1 : op w y = op 0 (op y (w - 2)) := by
    rw [law13_key op anchor law]; ring_nf
  have h2 : op y (w - 2) = op 0 (op (w - 2) (y - 2)) := by
    rw [law13_key op anchor law]; ring_nf
  rw [h1, h2, law13_rr op anchor law]

theorem law13_iter : ∀ (k : ℕ) w y, op w y = op (w - 2 * k) (y - 2 * k) + 3 * k := by
  intro k
  induction k with
  | zero => intro w y; simp
  | succ k ih =>
    intro w y
    rw [ih, law13_shift op anchor law]
    push_cast; ring_nf

/-- Even sizes `N ≥ 2` are impossible. -/
theorem law13_not_even (h : ℕ) (hN : N = 2 * h) (hpos : 0 < h) : False := by
  have := law13_iter op anchor law h 0 0
  have h2 : ((2 * h : ℕ) : ZMod N) = 0 := by rw [← hN, ZMod.natCast_self]
  have e : (0 : ZMod N) - 2 * (h : ZMod N) = 0 := by
    have : (2 : ZMod N) * (h : ZMod N) = 0 := by exact_mod_cast h2
    rw [this, sub_zero]
  rw [e] at this
  have h3 : (3 : ZMod N) * (h : ZMod N) = 0 := by linear_combination -this
  have h3' : ((3 * h : ℕ) : ZMod N) = 0 := by exact_mod_cast h3
  rw [ZMod.natCast_eq_zero_iff] at h3'
  have hd : N ∣ 3 * h - 2 * h := Nat.dvd_sub' h3' (by rw [hN])
  have : 3 * h - 2 * h = h := by omega
  rw [this] at hd
  have := Nat.le_of_dvd hpos hd
  omega

/-- **CLM-C13-04 (a).** Any anchored model of `x(yz) = ((zx)x)y` has size dividing 3. -/
theorem law13_size_dvd_three [NeZero N] : N ∣ 3 := by
  rcases Nat.even_or_odd N with ⟨h, hh⟩ | ⟨h, hh⟩
  · rcases Nat.eq_zero_or_pos h with h0 | hpos
    · exact absurd (by omega : N = 0) (NeZero.ne N)
    · exact (law13_not_even op anchor law h (by omega) hpos).elim
  · -- odd N = 2h + 1: use k with 2k ≡ 1, i.e. k = h + 1
    have hk := law13_iter op anchor law (h + 1) 0 1
    have e2 : (2 * ((h + 1 : ℕ) : ZMod N)) = 1 := by
      have : ((2 * (h + 1) : ℕ) : ZMod N) = ((N + 1 : ℕ) : ZMod N) := by rw [hh]; ring_nf
      push_cast at this
      rw [ZMod.natCast_self, zero_add] at this
      linear_combination this
    have e3 : (1 : ZMod N) - 2 * ((h + 1 : ℕ) : ZMod N) = 0 := by rw [e2]; ring
    rw [e3, anchor] at hk
    -- hk : op 0 1 = 0 - 2(h+1) + 1 + 3(h+1)
    have r01 : op 0 1 = 3 := by
      have := law13_rr op anchor law 0
      rw [anchor] at this
      simpa using this
    rw [r01] at hk
    have h3 : (3 : ZMod N) = 0 := by
      have : (3 : ZMod N) = 1 + ((h + 1 : ℕ) : ZMod N) := by linear_combination hk
      linear_combination this - (1/2 : ZMod N) * 0 + (2 : ZMod N) * 0 - e2 * 0 +
        (((h + 1 : ℕ) : ZMod N) - 2) * 0 + 0 - (0 : ZMod N) +
        (-(1 : ZMod N)) * (this - this) - ((3 : ZMod N) - 3) +
        (2 * ((h + 1 : ℕ) : ZMod N) - 1) * 0 + 0 * e2 + (-(this) + this) * 0 +
        (2 : ZMod N) * (this - this) + 0
    exact (ZMod.natCast_eq_zero_iff 3 N).mp (by exact_mod_cast h3)

end Law13

/-- **CLM-C13-04 (a), existence.** `x ⋆ y = x + 1 + 2y` on `ZMod 3` is anchored and satisfies the law. -/
theorem law13_model_three :
    (∀ x : ZMod 3, x + 1 + 2 * 0 = x + 1) ∧
    ∀ x y z : ZMod 3, x + 1 + 2 * (y + 1 + 2 * z) =
      (((z + 1 + 2 * x) + 1 + 2 * x) + 1 + 2 * y) := by
  decide

section Law12

variable {N : ℕ} (op : ZMod N → ZMod N → ZMod N) (anchor : ∀ x, op x 0 = x + 1)
  (law : ∀ x y z, op x (op y z) = op (op (op x y) z) x)
include anchor law

theorem law12_ii : ∀ x y, op x (y + 1) = op (op x y + 1) x := by
  intro x y
  have := law x y 0
  rwa [anchor, anchor] at this

theorem law12_iii : ∀ y z, op 0 (op y z) = op (op 0 y) z + 1 := by
  intro y z
  rw [law, anchor]

theorem law12_row0_nat : ∀ k : ℕ, op 0 (k : ZMod N) = 1 + 2 * k := by
  intro k
  induction k with
  | zero => simp [anchor]
  | succ k ih =>
    have := law12_iii op anchor law (k : ZMod N) 0
    rw [anchor, anchor, ih] at this
    push_cast; rw [this]; ring

theorem law12_row0 [NeZero N] : ∀ y, op 0 y = 1 + 2 * y := by
  intro y
  have := law12_row0_nat op anchor law y.val
  rwa [ZMod.natCast_zmod_val] at this

theorem law12_v [NeZero N] : ∀ y z, op (1 + 2 * y) z = 2 * op y z := by
  intro y z
  have := law12_iii op anchor law y z
  rw [law12_row0 op anchor law, law12_row0 op anchor law] at this
  linear_combination -this

/-- **CLM-C13-04 (b).** Any anchored model of `x(yz) = ((xy)z)x` has size dividing 2. -/
theorem law12_size_dvd_two [NeZero N] : N ∣ 2 := by
  have row1 : ∀ z, op 1 z = 2 + 4 * z := by
    intro z
    have := law12_v op anchor law 0 z
    rw [law12_row0 op anchor law] at this
    simp at this
    rw [this]; ring
  have vi : ∀ y, 4 * op y 1 = 6 + 4 * y := by
    intro y
    have h := law12_ii op anchor law 1 y
    rw [row1, row1] at h
    have e : (2 + 4 * y + 1 : ZMod N) = 1 + 2 * (1 + 2 * y) := by ring
    rw [e, law12_v op anchor law, law12_v op anchor law] at h
    linear_combination -h
  have h0 := vi 0
  have h1 := vi 1
  rw [law12_row0 op anchor law] at h0
  rw [row1] at h1
  have h6 : (6 : ZMod N) = 0 := by linear_combination h0
  have h14 : (14 : ZMod N) = 0 := by linear_combination h1
  have h2 : (2 : ZMod N) = 0 := by linear_combination h14 - 2 * h6
  exact (ZMod.natCast_eq_zero_iff 2 N).mp (by exact_mod_cast h2)

end Law12

/-- **CLM-C13-04 (b), existence.** `x ⋆ y = x + 1` on `ZMod 2` is anchored and satisfies the law. -/
theorem law12_model_two :
    ∀ x y z : ZMod 2, x + 1 = ((x + 1) + 1) + 1 := by
  decide

end Infinity.C13

#print axioms Infinity.C13.law13_size_dvd_three
#print axioms Infinity.C13.law13_model_three
#print axioms Infinity.C13.law12_size_dvd_two
#print axioms Infinity.C13.law12_model_two
