import Mathlib

/-!
# Cycle C17, batch 1.1 — CLM-C17-08: the row-period argument, machine-checked

Written by the Skeptic in its review of batch 1.1 (reviews/skeptic_batch1.1.md, section 1; original at
reviews/skeptic_checks/batch1.1/C17_RowPeriod.lean) and moved here unchanged except for the namespace.

Independent check of the Historian's argument (reviews/historian_C11_C20.md, "The CLM-C17-05 question",
item 4), in the 0-based convention of the lab (`x ⋆ 0 = x + 1`, `x ⋆ (y + 1) = (x ⋆ y) ⋆ (x + 1)`).

Main result (`only_powers_of_two`, `full_instance_iff_pow_two`): **assuming Laver's theorem** in the form
"for every `j` there is an anchored operation on `Fin (2 ^ j)` satisfying the full instance", an anchored
operation on `Fin N` (`N ≥ 1`) satisfying the full instance exists iff `N` is a power of `2`.
Laver's theorem enters only as the explicit hypothesis `laver`, and only at `2 ^ (k + 1)`, `k = v₂(N)`.

The argument, for `N = 2^k · (odd ≥ 3)`, `m = 2^k`, `B = 2m`, `s = N - B` (`m ∣ s`, `s ≥ 1`):

* `Forced` collects the facts of the forced table used below (values `< N`, anchor, the instances
  `y ≤ N - 2`, row `N - 1` is the identity, row `x ≤ N - 2` has entries `> x`); `forced_natOp` derives
  them from the hypotheses of `C17_ForcedTable.lean` (the Fin lemmas are copied from that file).
* `Forced.shift`, `Forced.mod_period`: a row restarts after it reaches the top `N - 1`, so it is
  periodic with period `y₀ + 1` (`y₀` the first top); `Forced.period_dvd`: if moreover `x ⋆ (N-1) = N-1`,
  the period divides `N`; `Forced.top_of_wrap`: the wrap-around at `x` forces `x ⋆ (N-1) = N-1`.
* `Forced.mod_half`: in a forced table of order `2^(k+1)` satisfying the wrap-around, every row
  `u ≤ 2^(k+1) - 2` depends only on the column mod `2^k` (its period is a power of 2 below `2^(k+1)`).
* `shift_copy` (the Historian's (i)): rows `s, …, N - 2` of `F_N` are `s + F_B(x - s, y mod m)`.
* `row_below` ((ii)): row `s - 1` of `F_N` is `y ↦ s + (y mod B)`.
* `wrap_fails` ((iii)): hence `(s-1) ⋆ (N-1) = N - m - 1` and the wrap-around fails at `x = s - 1`.
-/

namespace Infinity.C17.RowPeriod

/-! ## Part 1: the argument for functions on ℕ -/

/-- The properties of the forced table of order `N` (0-based) used in the argument. -/
structure Forced (N : ℕ) (f : ℕ → ℕ → ℕ) : Prop where
  lt : ∀ x y, x < N → y < N → f x y < N
  zero : ∀ x, x + 1 < N → f x 0 = x + 1
  step : ∀ x y, x + 1 < N → y + 1 < N → f x (y + 1) = f (f x y) (x + 1)
  last : ∀ y, y < N → f (N - 1) y = y
  gt : ∀ x y, x + 1 < N → y < N → x < f x y

section Rows

variable {N : ℕ} {f : ℕ → ℕ → ℕ}

/-- A row restarts after it reaches the top element `N - 1`. -/
theorem Forced.restart (hf : Forced N f) {x y : ℕ} (hx : x + 1 < N) (hy : y + 1 < N)
    (htop : f x y = N - 1) : f x (y + 1) = x + 1 := by
  rw [hf.step x y hx hy, htop, hf.last (x + 1) hx]

/-- After the top element at `y₀`, the row repeats from its start. -/
theorem Forced.shift (hf : Forced N f) {x y₀ : ℕ} (hx : x + 1 < N) (htop : f x y₀ = N - 1) :
    ∀ j, y₀ + 1 + j < N → f x (y₀ + 1 + j) = f x j := by
  intro j
  induction j with
  | zero =>
    intro h
    rw [Nat.add_zero, hf.restart hx (by omega) htop, hf.zero x hx]
  | succ j ih =>
    intro h
    rw [show y₀ + 1 + (j + 1) = (y₀ + 1 + j) + 1 by omega, hf.step x _ hx (by omega),
      ih (by omega), ← hf.step x j hx (by omega)]

/-- Rows are periodic: once `f x y₀ = N - 1`, `f x y = f x (y % (y₀ + 1))`. -/
theorem Forced.mod_period (hf : Forced N f) {x y₀ : ℕ} (hx : x + 1 < N) (htop : f x y₀ = N - 1) :
    ∀ y, y < N → f x y = f x (y % (y₀ + 1)) := by
  intro y
  induction y using Nat.strong_induction_on with
  | _ y ih =>
    intro hy
    rcases Nat.lt_or_ge y (y₀ + 1) with h | h
    · rw [Nat.mod_eq_of_lt h]
    · have h1 := hf.shift hx htop (y - (y₀ + 1)) (by omega)
      rw [show y₀ + 1 + (y - (y₀ + 1)) = y by omega] at h1
      rw [h1, ih _ (by omega) (by omega), ← Nat.mod_eq_sub_mod h]

/-- Below the top, a row increases strictly. -/
theorem Forced.lt_succ (hf : Forced N f) {x y : ℕ} (hx : x + 1 < N) (hy : y + 1 < N)
    (hv : f x y + 1 < N) : f x y < f x (y + 1) := by
  rw [hf.step x y hx hy]
  exact hf.gt _ _ hv hx

/-- Every row `x ≤ N - 2` reaches the top element, at a column `y ≤ N - 2 - x`. -/
theorem Forced.exists_top (hf : Forced N f) {x : ℕ} (hx : x + 1 < N) :
    ∃ y, y + x + 2 ≤ N ∧ f x y = N - 1 := by
  by_contra hcon
  simp only [not_exists, not_and] at hcon
  have key : ∀ y, y + x + 2 ≤ N → x + 1 + y ≤ f x y := by
    intro y
    induction y with
    | zero => intro _; have := hf.zero x hx; omega
    | succ y ih =>
      intro hy
      have h1 := ih (by omega)
      have h2 : f x y < N := hf.lt x y (by omega) (by omega)
      have h3 : f x y ≠ N - 1 := hcon y (by omega)
      have h4 := hf.lt_succ hx (by omega) (by omega : f x y + 1 < N)
      omega
  have h5 := key (N - x - 2) (by omega)
  have h6 : f x (N - x - 2) < N := hf.lt x _ (by omega) (by omega)
  exact hcon (N - x - 2) (by omega) (by omega)

/-- If `x ⋆ (N - 1) = N - 1`, the period of row `x` (one more than its first top) divides `N`. -/
theorem Forced.period_dvd (hf : Forced N f) {x : ℕ} (hx : x + 1 < N) (hlast : f x (N - 1) = N - 1) :
    ∃ y₀, y₀ + x + 2 ≤ N ∧ f x y₀ = N - 1 ∧ (y₀ + 1) ∣ N := by
  classical
  have hex := hf.exists_top hx
  obtain ⟨y₀, hy₀, hmin⟩ : ∃ y₀, (y₀ + x + 2 ≤ N ∧ f x y₀ = N - 1) ∧
      ∀ z, z < y₀ → ¬ (z + x + 2 ≤ N ∧ f x z = N - 1) :=
    ⟨Nat.find hex, Nat.find_spec hex, fun z hz => Nat.find_min hex hz⟩
  refine ⟨y₀, hy₀.1, hy₀.2, ?_⟩
  have hmod := hf.mod_period hx hy₀.2 (N - 1) (by omega)
  rw [hlast] at hmod
  have hr : (N - 1) % (y₀ + 1) < y₀ + 1 := Nat.mod_lt _ (by omega)
  have hr' : (N - 1) % (y₀ + 1) = y₀ := by
    by_contra hne
    exact hmin ((N - 1) % (y₀ + 1)) (by omega) ⟨by omega, hmod.symm⟩
  have h := Nat.div_add_mod (N - 1) (y₀ + 1)
  rw [hr'] at h
  exact ⟨(N - 1) / (y₀ + 1) + 1, by rw [Nat.mul_add, Nat.mul_one]; omega⟩

/-- The wrap-around equation at `x` forces `x ⋆ (N - 1) = N - 1`. -/
theorem Forced.top_of_wrap (hf : Forced N f) {x : ℕ} (hx : x + 1 < N)
    (hw : f (f x (N - 1)) (x + 1) = x + 1) : f x (N - 1) = N - 1 := by
  by_contra hne
  have hv : f x (N - 1) < N := hf.lt x _ (by omega) (by omega)
  have h1 : x < f x (N - 1) := hf.gt x _ hx (by omega)
  have h2 := hf.gt (f x (N - 1)) (x + 1) (by omega) hx
  omega

end Rows

/-- **Laver's periodicity, used at `B = 2^(k+1)`.** If a forced table of order `2^(k+1)` satisfies the
wrap-around equations, each of its rows `u ≤ 2^(k+1) - 2` depends only on the column modulo `2^k`. -/
theorem Forced.mod_half {k : ℕ} {g : ℕ → ℕ → ℕ} (hg : Forced (2 ^ (k + 1)) g)
    (hw : ∀ u, u + 1 < 2 ^ (k + 1) → g (g u (2 ^ (k + 1) - 1)) (u + 1) = u + 1) :
    ∀ u y, u + 1 < 2 ^ (k + 1) → y < 2 ^ (k + 1) → g u y = g u (y % 2 ^ k) := by
  intro u y hu hy
  obtain ⟨y₀, hy₀, htop, hdvd⟩ := hg.period_dvd hu (hg.top_of_wrap hu (hw u hu))
  have hlt : y₀ + 1 < 2 ^ (k + 1) := by omega
  obtain ⟨j, hj, hj'⟩ := (Nat.dvd_prime_pow Nat.prime_two).mp hdvd
  have hjk : j ≤ k := by
    by_contra h
    have : j = k + 1 := by omega
    rw [this] at hj'
    omega
  have hdvd' : (y₀ + 1) ∣ 2 ^ k := by
    rw [hj']
    exact Nat.pow_dvd_pow 2 hjk
  have hpk : 2 ^ k < 2 ^ (k + 1) := by
    rw [pow_succ]
    have := Nat.one_le_two_pow (n := k)
    omega
  rw [hg.mod_period hu htop y hy, hg.mod_period hu htop (y % 2 ^ k)
    (lt_trans (Nat.mod_lt _ (by positivity)) hpk), Nat.mod_mod_of_dvd _ hdvd']

section Block

variable {N m s B : ℕ} {f g : ℕ → ℕ → ℕ}

/-- **The Historian's (i).** Rows `s, …, N - 2` of `F_N` are shifted copies of rows of `F_B`:
`F_N(x, y) = s + F_B(x - s, y mod m)`, for `N = s + B`, `B = 2m`, `m ∣ s`, provided the rows of `F_B` below
its top depend only on the column mod `m`. -/
theorem shift_copy (hB : B = 2 * m) (hm : 0 < m) (hf : Forced N f) (hg : Forced B g)
    (hper : ∀ u y, u + 1 < B → y < B → g u y = g u (y % m)) (hN : N = s + B) (hs : m ∣ s) :
    ∀ x y, s ≤ x → x + 1 < N → y < N → f x y = s + g (x - s) (y % m) := by
  suffices H : ∀ d x, N - x = d → ∀ y, s ≤ x → x + 1 < N → y < N →
      f x y = s + g (x - s) (y % m) by
    intro x y; exact H _ x rfl y
  intro d
  induction d using Nat.strong_induction_on with
  | _ d ihd =>
    intro x hd y hsx hx
    induction y with
    | zero =>
      intro _
      rw [Nat.zero_mod, hf.zero x hx, hg.zero (x - s) (by omega)]
      omega
    | succ y ihy =>
      intro hy
      have IH := ihy (by omega)
      have hrm : y % m < m := Nat.mod_lt _ hm
      have huB : x - s + 1 < B := by omega
      have hrB : y % m + 1 < B := by omega
      -- the right-hand side: one step of the recursion in `F_B`
      have hR : g (x - s) ((y + 1) % m) = g (g (x - s) (y % m)) (x - s + 1) := by
        rw [← Nat.mod_add_mod y m 1, ← hper (x - s) (y % m + 1) huB hrB,
          hg.step (x - s) (y % m) huB hrB]
      rw [hR, hf.step x y hx (by omega), IH]
      have hv : g (x - s) (y % m) < B := hg.lt _ _ (by omega) (by omega)
      rcases Nat.lt_or_ge (g (x - s) (y % m) + 1) B with h | h
      · -- below the top: the row `s + g (x - s) (y % m) > x` is already a shifted copy
        have hgt : x - s < g (x - s) (y % m) := hg.gt _ _ huB (by omega)
        have hw := ihd (N - (s + g (x - s) (y % m))) (by omega) (s + g (x - s) (y % m)) rfl (x + 1)
          (by omega) (by omega) (by omega)
        rw [hw, Nat.add_sub_cancel_left, hper (g (x - s) (y % m)) (x - s + 1) h huB]
        obtain ⟨t, rfl⟩ := hs
        rw [show x + 1 = (x - m * t + 1) + m * t by omega, Nat.add_mul_mod_self_left]
      · -- the top element: row `N - 1` of `F_N` and row `B - 1` of `F_B` are identities
        have htop : g (x - s) (y % m) = B - 1 := by omega
        rw [htop, hg.last (x - s + 1) huB, show s + (B - 1) = N - 1 by omega, hf.last (x + 1) hx]
        omega

/-- **The Historian's (ii).** Row `s - 1` of `F_N` is `y ↦ s + (y mod B)`; its period is `B`. -/
theorem row_below (hB : B = 2 * m) (hm : 0 < m) (hf : Forced N f) (hg : Forced B g)
    (hper : ∀ u y, u + 1 < B → y < B → g u y = g u (y % m)) (hN : N = s + B) (hs : m ∣ s)
    (hs1 : 1 ≤ s) : ∀ y, y < N → f (s - 1) y = s + y % B := by
  have hcopy := shift_copy hB hm hf hg hper hN hs
  intro y
  induction y with
  | zero =>
    intro _
    rw [hf.zero (s - 1) (by omega), Nat.zero_mod]
    omega
  | succ y ih =>
    intro hy
    rw [hf.step (s - 1) y (by omega) hy, ih (by omega), show s - 1 + 1 = s by omega]
    have hyB : y % B < B := Nat.mod_lt _ (by omega)
    rcases Nat.lt_or_ge (y % B + 1) B with h | h
    · have e : (y + 1) % B = y % B + 1 := by
        rw [← Nat.mod_add_mod y B 1, Nat.mod_eq_of_lt h]
      rw [hcopy (s + y % B) s (by omega) (by omega) (by omega), Nat.add_sub_cancel_left, e]
      obtain ⟨t, rfl⟩ := hs
      rw [Nat.mul_mod_right, hg.zero _ h]
    · have e : y % B = B - 1 := by omega
      have e' : (y + 1) % B = 0 := by
        rw [← Nat.mod_add_mod y B 1, e, show B - 1 + 1 = B by omega, Nat.mod_self]
      rw [e, show s + (B - 1) = N - 1 by omega, hf.last s (by omega), e']
      omega

/-- **The Historian's (iii).** For `N ≡ m (mod 2m)` with `N > 2m`, the wrap-around equation fails at
`x = s - 1` (`s = N - B`): `(x ⋆ (N - 1)) ⋆ (x + 1) ≠ x + 1`. -/
theorem wrap_fails (hB : B = 2 * m) (hm : 0 < m) (hf : Forced N f) (hg : Forced B g)
    (hper : ∀ u y, u + 1 < B → y < B → g u y = g u (y % m)) (hNmod : N % B = m) (hNgt : B < N) :
    f (f (N - B - 1) (N - 1)) (N - B) ≠ N - B := by
  obtain ⟨q, hq⟩ : ∃ q, N = B * q + m := ⟨N / B, by have := Nat.div_add_mod N B; omega⟩
  have hq0 : q ≠ 0 := by
    rintro rfl
    rw [Nat.mul_zero, Nat.zero_add] at hq
    omega
  obtain ⟨q', rfl⟩ : ∃ q', q = q' + 1 := ⟨q - 1, by omega⟩
  have hN' : N = m * (2 * q' + 1) + 2 * m := by rw [hq, hB]; ring
  have hsplit : m * (2 * q' + 1) = m * (2 * q') + m := by ring
  have hs : m ∣ N - B := ⟨2 * q' + 1, by omega⟩
  have hs1 : 1 ≤ N - B := by omega
  have hrow := row_below hB hm hf hg hper (show N = (N - B) + B by omega) hs hs1 (N - 1) (by omega)
  have hmod : (N - 1) % B = m - 1 := by
    rw [show N - 1 = (m - 1) + B * (q' + 1) by omega, Nat.add_mul_mod_self_left,
      Nat.mod_eq_of_lt (by omega)]
  rw [hrow, hmod]
  intro h
  have := hf.gt (N - B + (m - 1)) (N - B) (by omega) (by omega)
  omega

end Block

/-! ## Part 2: the bridge to the formulation of `C17_ForcedTable.lean` (`Fin N`)

The five lemmas `val_add_one`, `add_one_eq_zero`, `row_induction`, `row_last`, `row_gt` are copied from
`proofs/lean/Infinity/C17_ForcedTable.lean` (namespace `Infinity.C17`), so that this file only imports
Mathlib. -/

section FinN

variable {N : ℕ} [NeZero N]

theorem val_add_one {y : Fin N} (h : y.val + 1 < N) : (y + 1).val = y.val + 1 := by
  rw [Fin.val_add, Fin.val_one', Nat.mod_eq_of_lt (show 1 < N by omega), Nat.mod_eq_of_lt h]

theorem add_one_eq_zero {x : Fin N} (h : x.val = N - 1) : x + 1 = 0 := by
  have hN : 0 < N := Nat.pos_of_ne_zero (NeZero.ne N)
  ext
  rw [Fin.val_add, Fin.val_one', Fin.val_zero]
  rcases Nat.lt_or_ge 1 N with h1 | h1
  · rw [Nat.mod_eq_of_lt h1, h, Nat.sub_add_cancel hN, Nat.mod_self]
  · have : N = 1 := by omega
    subst this
    exact Nat.mod_one _

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

section Op

variable (op : Fin N → Fin N → Fin N) (anchor : ∀ x, op x 0 = x + 1)
  (step : ∀ x y : Fin N, y.val + 1 < N → op x (y + 1) = op (op x y) (x + 1))
include anchor step

theorem row_last : ∀ x y : Fin N, x.val = N - 1 → op x y = y := by
  intro x y hx
  have hx1 : x + 1 = 0 := add_one_eq_zero hx
  refine row_induction (P := fun y => op x y = y) ?_ ?_ y
  · rw [anchor, hx1]
  · intro y hy ih
    rw [step x y hy, ih, hx1, anchor]

theorem row_gt : ∀ x y : Fin N, x.val < N - 1 → x.val < (op x y).val := by
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

end Op

/-- An operation on `Fin N` as a function on `ℕ` (`0` outside the square). -/
def natOp (op : Fin N → Fin N → Fin N) (x y : ℕ) : ℕ :=
  if h : x < N ∧ y < N then (op ⟨x, h.1⟩ ⟨y, h.2⟩).val else 0

omit [NeZero N] in
theorem natOp_eq (op : Fin N → Fin N → Fin N) (x y : Fin N) :
    natOp op x.val y.val = (op x y).val := by
  simp [natOp, x.isLt, y.isLt]

/-- The hypotheses of `C17_ForcedTable.lean` give the properties `Forced`. -/
theorem forced_natOp (op : Fin N → Fin N → Fin N) (anchor : ∀ x, op x 0 = x + 1)
    (step : ∀ x y : Fin N, y.val + 1 < N → op x (y + 1) = op (op x y) (x + 1)) :
    Forced N (natOp op) where
  lt := by
    intro x y hx hy
    have := natOp_eq op ⟨x, hx⟩ ⟨y, hy⟩
    simp only at this
    rw [this]
    exact (op _ _).isLt
  zero := by
    intro x hx
    have h := natOp_eq op ⟨x, by omega⟩ 0
    rw [Fin.val_zero] at h
    rw [h, anchor, val_add_one (by simpa using hx)]
  step := by
    intro x y hx hy
    have e1 := natOp_eq op ⟨x, by omega⟩ ⟨y + 1, hy⟩
    have e2 := natOp_eq op ⟨x, by omega⟩ ⟨y, by omega⟩
    have hyy : (⟨y + 1, hy⟩ : Fin N) = (⟨y, by omega⟩ : Fin N) + 1 := by
      ext; rw [val_add_one (by simpa using hy)]
    have hxx : ((⟨x, by omega⟩ : Fin N) + 1).val = x + 1 := val_add_one (by simpa using hx)
    have e3 := natOp_eq op (op ⟨x, by omega⟩ ⟨y, by omega⟩) ((⟨x, by omega⟩ : Fin N) + 1)
    simp only at e1 e2
    rw [e1, hyy, step _ _ (by simpa using hy), ← e3, hxx, e2]
  last := by
    intro y hy
    have hN : 0 < N := Nat.pos_of_ne_zero (NeZero.ne N)
    have h := natOp_eq op ⟨N - 1, by omega⟩ ⟨y, hy⟩
    simp only at h
    rw [h, row_last op anchor step _ _ rfl]
  gt := by
    intro x y hx hy
    have h := natOp_eq op ⟨x, by omega⟩ ⟨y, hy⟩
    simp only at h
    rw [h]
    exact row_gt op anchor step ⟨x, by omega⟩ ⟨y, hy⟩ (by simp; omega)

/-- The full instance gives the wrap-around equations of `natOp op`. -/
theorem wrap_natOp (op : Fin N → Fin N → Fin N) (anchor : ∀ x, op x 0 = x + 1)
    (full : ∀ x y : Fin N, op x (y + 1) = op (op x y) (x + 1)) :
    ∀ x, x + 1 < N → natOp op (natOp op x (N - 1)) (x + 1) = x + 1 := by
  intro x hx
  have hN : 0 < N := Nat.pos_of_ne_zero (NeZero.ne N)
  have e1 := natOp_eq op ⟨x, by omega⟩ ⟨N - 1, by omega⟩
  simp only at e1
  have hxx : ((⟨x, by omega⟩ : Fin N) + 1).val = x + 1 := val_add_one (by simpa using hx)
  have e2 := natOp_eq op (op ⟨x, by omega⟩ ⟨N - 1, by omega⟩) ((⟨x, by omega⟩ : Fin N) + 1)
  rw [hxx] at e2
  have hw := full ⟨x, by omega⟩ ⟨N - 1, by omega⟩
  rw [add_one_eq_zero (by simp), anchor] at hw
  rw [e1, e2, ← hw, hxx]

end FinN

/-- **CLM-C17-08, "only if", from Laver's theorem.** If for every `j` some anchored operation on
`Fin (2 ^ j)` satisfies the full instance (Laver's theorem), then an anchored operation on `Fin N`
satisfying the full instance exists only if `N` is a power of `2`. -/
theorem only_powers_of_two
    (laver : ∀ j : ℕ, ∃ op : Fin (2 ^ j) → Fin (2 ^ j) → Fin (2 ^ j),
      (∀ x, op x 0 = x + 1) ∧ ∀ x y, op x (y + 1) = op (op x y) (x + 1))
    (N : ℕ) [NeZero N] (op : Fin N → Fin N → Fin N) (anchor : ∀ x, op x 0 = x + 1)
    (full : ∀ x y, op x (y + 1) = op (op x y) (x + 1)) : ∃ j, N = 2 ^ j := by
  by_contra hnot
  simp only [not_exists] at hnot
  obtain ⟨k, n', hodd, hN⟩ := Nat.exists_eq_two_pow_mul_odd (NeZero.ne N)
  obtain ⟨t, rfl⟩ := hodd
  have ht : t ≠ 0 := by
    rintro rfl
    exact hnot k (by rw [hN]; ring)
  obtain ⟨m, hm⟩ : ∃ m, m = 2 ^ k := ⟨_, rfl⟩
  have hm0 : 0 < m := by rw [hm]; positivity
  have hB : 2 ^ (k + 1) = 2 * m := by rw [hm, pow_succ]; ring
  obtain ⟨g, ganchor, gfull⟩ := laver (k + 1)
  obtain ⟨G, hG⟩ : ∃ G : ℕ → ℕ → ℕ, G = natOp g := ⟨_, rfl⟩
  have hg : Forced (2 ^ (k + 1)) G := by rw [hG]; exact forced_natOp g ganchor (fun x y _ => gfull x y)
  have hgw : ∀ x, x + 1 < 2 ^ (k + 1) → G (G x (2 ^ (k + 1) - 1)) (x + 1) = x + 1 := by
    rw [hG]; exact wrap_natOp g ganchor gfull
  have hf := forced_natOp op anchor (fun x y _ => full x y)
  have hfw := wrap_natOp op anchor full
  have hper := Forced.mod_half hg hgw
  rw [← hm, hB] at hper
  rw [hB] at hg
  have hN' : N = m + 2 * m * t := by rw [hN, ← hm]; ring
  have hNmod : N % (2 * m) = m := by
    rw [hN', Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt (by omega)]
  have hle : 2 * m ≤ 2 * m * t := Nat.le_mul_of_pos_right _ (by omega)
  have hNgt : 2 * m < N := by omega
  have key := wrap_fails rfl hm0 hf hg hper hNmod hNgt
  have hw := hfw (N - 2 * m - 1) (by omega)
  rw [show N - 2 * m - 1 + 1 = N - 2 * m by omega] at hw
  exact key hw

/-- **CLM-C17-08 from Laver's theorem.** Under the same hypothesis, for every `N ≥ 1` an anchored
operation on `Fin N` satisfying the full instance (wrap-around included) exists iff `N` is a power of 2. -/
theorem full_instance_iff_pow_two
    (laver : ∀ j : ℕ, ∃ op : Fin (2 ^ j) → Fin (2 ^ j) → Fin (2 ^ j),
      (∀ x, op x 0 = x + 1) ∧ ∀ x y, op x (y + 1) = op (op x y) (x + 1))
    (N : ℕ) [NeZero N] :
    (∃ op : Fin N → Fin N → Fin N, (∀ x, op x 0 = x + 1) ∧ ∀ x y, op x (y + 1) = op (op x y) (x + 1))
      ↔ ∃ j, N = 2 ^ j := by
  constructor
  · rintro ⟨op, anchor, full⟩
    exact only_powers_of_two laver N op anchor full
  · rintro ⟨j, rfl⟩
    exact laver j

end Infinity.C17.RowPeriod

#print axioms Infinity.C17.RowPeriod.wrap_fails
#print axioms Infinity.C17.RowPeriod.only_powers_of_two
#print axioms Infinity.C17.RowPeriod.full_instance_iff_pow_two
