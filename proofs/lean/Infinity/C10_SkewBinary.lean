import Mathlib.Data.List.Basic
import Mathlib.Tactic

/-!
# Cycle C10 — Skew binary counting (CLM-C10-07)

Written proof: `proofs/paper/C10.md`, Theorem 6.

**Part 1: the 0/1 words `B_k`** (Theorem 6 (ii), the counting).  `B_0 = 0`, `B_{k+1} = B_k B_k 1`;
for `N ≤ |B_k|`, `S_k(N)` is the number of ones among the first `N` letters of `B_k`.

* `length_B` : `|B_k| = 2^(k+1) - 1`;
* `count_B` : `B_k` contains exactly `2^k - 1` ones; `B_le_one` : every letter is `0` or `1`;
* `prefix_bound` : `|S_k(N) - N/2| ≤ (k + 1)/2` for every `N ≤ |B_k|` (in `ℚ`);
  `prefix_bound_nat` is the same statement as two inequalities in `ℕ`;
* `count_B_eq`, `deficit_full` : `S_k(|B_k|) = 2^k - 1`, so `D(M_k) = S(M_k) - M_k/2 = -1/2`.

**Part 2: canonical skew binary** (Theorem 6 (i), and the link between `B_k` and skew binary).
Representations are little-endian digit lists `[d_0, …, d_{K-1}]` of a fixed length `K` (all higher
digits are `0`), with value `Σ d_i w_i`, `w_i = 2^(i+1) - 1`; *canonical* (`Canon`) means digits
`0, 1, 2`, only the lowest nonzero digit possibly a `2`.  `χ(l) = 1` iff `l` contains a `2`;
`changes l m` counts the positions where `l` and `m` differ.

* `canon_unique`, `canon_existsUnique` : every `n < w_K = 2^(K+1) - 1` has exactly one canonical `K`-digit
  representation, namely `repK K n` (`n` increments from `0 … 0`). The paper takes this uniqueness from
  the literature (Myers 1983, Okasaki 1998); here it is proved.
* `inc_spec`, `val_inc`, `changes_inc` : the increment rule of the proof, part (i).
* `increment_cost` : the canonical representations of `n` and `n + 1` differ in exactly `1 + χ(n)`
  positions, hence in at most `2` (stated for any two canonical lists of equal length whose values
  differ by one, so it does not depend on how `inc` is defined).
* `chi_word` : `χ(0) χ(1) … χ(M_K - 1) = B_K` (`M_K = w_K`): the decomposition of part (ii).
* `totalCost_eq`, `totalCost_bound`, `average_cost` : for `N < w_K` the increments `n → n + 1`,
  `0 ≤ n < N`, change `N + S_K(N)` digits in total, which is within `(K + 1)/2` of `3N/2`; with
  `K = ⌊log₂ (N + 1)⌋` digits, `|cost/N - 3/2| ≤ (⌊log₂ (N + 1)⌋ + 1)/(2N)`, i.e. the average is
  `3/2 + O(log N / N)`.
* `totalCost_succ` : the total cost does not depend on the number of digits `K` once `N < w_K`.
-/

namespace Infinity.C10

/-- The words `B_0 = 0`, `B_{k+1} = B_k B_k 1`. -/
def B : ℕ → List ℕ
  | 0 => [0]
  | k + 1 => B k ++ B k ++ [1]

/-- Every letter of `B_k` is `0` or `1`. -/
theorem B_le_one : ∀ k, ∀ x ∈ B k, x ≤ 1 := by
  intro k
  induction k with
  | zero => simp [B]
  | succ k ih =>
    intro x hx
    simp only [B, List.mem_append, List.mem_singleton] at hx
    rcases hx with (hx | hx) | hx
    · exact ih x hx
    · exact ih x hx
    · omega

theorem length_B_add_one (k : ℕ) : (B k).length + 1 = 2 ^ (k + 1) := by
  induction k with
  | zero => simp [B]
  | succ k ih =>
    simp only [B, List.length_append, List.length_singleton]
    rw [pow_succ]
    omega

/-- **CLM-C10-07, length.** `|B_k| = 2^(k+1) - 1`. -/
theorem length_B (k : ℕ) : (B k).length = 2 ^ (k + 1) - 1 := by
  have := length_B_add_one k
  omega

theorem count_B_add_one (k : ℕ) : (B k).count 1 + 1 = 2 ^ k := by
  induction k with
  | zero => simp [B]
  | succ k ih =>
    simp only [B, List.count_append, List.count_singleton_self]
    rw [pow_succ]
    omega

/-- **CLM-C10-07, number of ones.** `B_k` contains exactly `2^k - 1` ones. -/
theorem count_B (k : ℕ) : (B k).count 1 = 2 ^ k - 1 := by
  have := count_B_add_one k
  omega

/-- `S_k(N)`: the number of ones among the first `N` letters of `B_k`. -/
def S (k N : ℕ) : ℕ := ((B k).take N).count 1

/-- **CLM-C10-07, prefix bound (natural-number form).** For `N ≤ |B_k|`: `|2 S_k(N) - N| ≤ k + 1`. -/
theorem prefix_bound_nat (k : ℕ) :
    ∀ N ≤ (B k).length, 2 * S k N ≤ N + (k + 1) ∧ N ≤ 2 * S k N + (k + 1) := by
  induction k with
  | zero =>
    intro N hN
    simp only [B, List.length_singleton] at hN
    interval_cases N <;> simp [S, B]
  | succ k ih =>
    intro N hN
    have hL := length_B_add_one k
    have hC := count_B_add_one k
    rw [pow_succ] at hL
    set L := (B k).length with hLdef
    set P := 2 ^ k
    have hlen : (B (k + 1)).length = 2 * L + 1 := by
      simp only [B, List.length_append, List.length_singleton]; omega
    rw [hlen] at hN
    -- decompose the prefix along `B_{k+1} = B_k ++ B_k ++ [1]`
    have hS : S (k + 1) N = S k N + S k (N - L) + ([1].take (N - 2 * L)).count 1 := by
      have e : N - (L + L) = N - 2 * L := by omega
      simp only [S, B, List.take_append, List.count_append, List.length_append, ← hLdef, e]
    rcases Nat.lt_or_ge L N with hNL | hNL
    · -- `N > L`: the whole first copy of `B_k` is included
      have h1 : S k N = P - 1 := by
        simp only [S]; rw [List.take_of_length_le (by omega), count_B]
      rcases Nat.lt_or_ge (2 * L) N with h2L | h2L
      · -- `N = 2L + 1`: the whole word
        have hN' : N = 2 * L + 1 := by omega
        have h2 : S k (N - L) = P - 1 := by
          simp only [S]; rw [List.take_of_length_le (by omega), count_B]
        have h3 : ([1].take (N - 2 * L)).count 1 = 1 := by
          rw [show N - 2 * L = 1 by omega]; simp
        rw [hS, h1, h2, h3]
        omega
      · -- `L < N ≤ 2L`: the first copy and a prefix of the second
        have h3 : ([1].take (N - 2 * L)).count 1 = 0 := by
          rw [show N - 2 * L = 0 by omega]; simp
        have := ih (N - L) (by omega)
        rw [hS, h1, h3]
        omega
    · -- `N ≤ L`: a prefix of the first copy of `B_k`
      have h2 : S k (N - L) = 0 := by
        simp only [S]; rw [show N - L = 0 by omega]; simp
      have h3 : ([1].take (N - 2 * L)).count 1 = 0 := by
        rw [show N - 2 * L = 0 by omega]; simp
      have := ih N hNL
      rw [hS, h2, h3]
      omega

/-- **CLM-C10-07, prefix bound.** For every `N ≤ |B_k| = 2^(k+1) - 1`, the number `S_k(N)` of ones among
the first `N` letters of `B_k` satisfies `|S_k(N) - N/2| ≤ (k + 1)/2`. -/
theorem prefix_bound (k N : ℕ) (hN : N ≤ (B k).length) :
    |(S k N : ℚ) - N / 2| ≤ (k + 1) / 2 := by
  obtain ⟨h1, h2⟩ := prefix_bound_nat k N hN
  have h1' : (2 * S k N : ℚ) ≤ N + (k + 1) := by exact_mod_cast h1
  have h2' : (N : ℚ) ≤ 2 * S k N + (k + 1) := by exact_mod_cast h2
  rw [abs_le]
  constructor <;> linarith

/-- `S_k(|B_k|) = 2^k - 1`. -/
theorem count_B_eq (k : ℕ) : S k (B k).length = 2 ^ k - 1 := by
  simp only [S, List.take_length, count_B]

/-- `D(M_k) = S(M_k) - M_k/2 = -1/2` for the full word (`M_k = 2^(k+1) - 1`). -/
theorem deficit_full (k : ℕ) : (S k (B k).length : ℚ) - ((B k).length : ℚ) / 2 = -1 / 2 := by
  have hL := length_B_add_one k
  have hC := count_B_add_one k
  rw [S, List.take_length]
  have hL' : ((B k).length : ℚ) + 1 = 2 * 2 ^ k := by
    rw [pow_succ] at hL; exact_mod_cast (by omega : (B k).length + 1 = 2 * 2 ^ k)
  have hC' : (((B k).count 1 : ℕ) : ℚ) + 1 = 2 ^ k := by exact_mod_cast hC
  linarith


/-! ### Canonical skew binary (Theorem 6 (i)) and the link `χ`-word `= B_k` -/

/-- Skew-binary weights `w_k = 2^(k+1) - 1`. `M_k = w_k` is also the number of values that are
representable with digits at positions `< k` (`canon_existsUnique`). -/
def w (k : ℕ) : ℕ := 2 ^ (k + 1) - 1

theorem w_zero : w 0 = 1 := rfl

theorem w_succ (k : ℕ) : w (k + 1) = 2 * w k + 1 := by
  unfold w
  rw [pow_succ 2 (k + 1)]
  have : 1 ≤ 2 ^ (k + 1) := Nat.one_le_two_pow
  omega

theorem w_pos (k : ℕ) : 0 < w k := by
  unfold w
  have : 2 ≤ 2 ^ (k + 1) := by
    calc 2 = 2 ^ 1 := rfl
      _ ≤ 2 ^ (k + 1) := Nat.pow_le_pow_right (by norm_num) (by omega)
  omega

theorem length_B_eq_w (k : ℕ) : (B k).length = w k := length_B k

/-- Value of a little-endian digit list whose first digit sits at position `k`. -/
def valFrom : ℕ → List ℕ → ℕ
  | _, [] => 0
  | k, d :: l => d * w k + valFrom (k + 1) l

/-- The value `Σ_i d_i w_i` of a little-endian digit list `[d_0, d_1, …]`. -/
def val (l : List ℕ) : ℕ := valFrom 0 l

/-- Canonical skew binary: all digits are `0`, `1` or `2`, and only the lowest nonzero digit may be a `2`.
(Recursively: zeros at the bottom are skipped; the first nonzero digit is `≤ 2`; all later digits are
`≤ 1`.) -/
def Canon : List ℕ → Prop
  | [] => True
  | 0 :: l => Canon l
  | (d + 1) :: l => d + 1 ≤ 2 ∧ ∀ x ∈ l, x ≤ 1

theorem canon_cons_zero (l : List ℕ) : Canon (0 :: l) ↔ Canon l := Iff.rfl

theorem canon_cons_succ (d : ℕ) (l : List ℕ) :
    Canon ((d + 1) :: l) ↔ d + 1 ≤ 2 ∧ ∀ x ∈ l, x ≤ 1 := Iff.rfl

/-- `χ(l) = 1` if the representation contains a `2`, else `0`. -/
def chi (l : List ℕ) : ℕ := if 2 ∈ l then 1 else 0

/-- The number of positions at which two digit lists of the same length differ. -/
def changes : List ℕ → List ℕ → ℕ
  | x :: l, y :: m => (if x = y then 0 else 1) + changes l m
  | _, _ => 0

/-- Add `1` to the lowest digit. -/
def bump : List ℕ → List ℕ
  | [] => []
  | d :: l => (d + 1) :: l

/-- The increment of Theorem 6 (i), on a fixed number of digits: if the representation contains a `2`
(for canonical input necessarily its lowest nonzero digit), that `2` becomes `0` and the next digit
grows by `1`; otherwise the digit at position `0` grows by `1`. A carry out of the top position is
dropped; this only happens at the largest `K`-digit value `maxK K`, excluded wherever it matters.
The results below that matter (`increment_cost`, `chi_word`, …) do not depend on this definition: by
`canon_unique` the successor representation is determined by its value. -/
def inc : List ℕ → List ℕ
  | [] => []
  | 0 :: l => if 2 ∈ l then 0 :: inc l else 1 :: l
  | 1 :: l => 2 :: l
  | 2 :: l => 0 :: bump l
  | (d + 3) :: l => (d + 3) :: l

/-- The largest canonical `K`-digit representation: `[]` for `K = 0`, else `0 … 0 2`. -/
def maxK : ℕ → List ℕ
  | 0 => []
  | K + 1 => List.replicate K 0 ++ [2]

/-- `repK K n`: `n` increments applied to `0 … 0` (`K` digits); by `repK_spec` and `canon_unique` it is
the canonical skew-binary representation of `n` with `K` digits, for `n < w K`. -/
def repK (K n : ℕ) : List ℕ := inc^[n] (List.replicate K 0)

/-! #### Basic facts -/

theorem length_bump (l : List ℕ) : (bump l).length = l.length := by
  cases l <;> rfl

theorem length_inc : ∀ l : List ℕ, (inc l).length = l.length
  | [] => rfl
  | 0 :: l => by
    by_cases h : 2 ∈ l
    · simp only [inc, h, ↓reduceIte, List.length_cons, length_inc l]
    · simp only [inc, h, ↓reduceIte, List.length_cons]
  | 1 :: l => rfl
  | 2 :: l => by simp only [inc, List.length_cons, length_bump]
  | (d + 3) :: l => rfl

theorem length_maxK (K : ℕ) : (maxK K).length = K := by
  cases K <;> simp [maxK]

theorem repK_zero (K : ℕ) : repK K 0 = List.replicate K 0 := rfl

theorem repK_succ (K n : ℕ) : repK K (n + 1) = inc (repK K n) :=
  Function.iterate_succ_apply' _ _ _

theorem length_repK (K n : ℕ) : (repK K n).length = K := by
  induction n with
  | zero => simp [repK_zero]
  | succ n ih => rw [repK_succ, length_inc, ih]

theorem canon_replicate (K : ℕ) : Canon (List.replicate K 0) := by
  induction K with
  | zero => trivial
  | succ K ih => rw [List.replicate_succ]; exact ih

theorem canon_le_one_of_two_notMem : ∀ l : List ℕ, Canon l → 2 ∉ l → ∀ x ∈ l, x ≤ 1
  | [] => by simp
  | 0 :: l => by
    intro hc h2 x hx
    simp only [List.mem_cons] at hx h2
    rcases hx with rfl | hx
    · omega
    · exact canon_le_one_of_two_notMem l hc (fun h => h2 (Or.inr h)) x hx
  | (d + 1) :: l => by
    rintro ⟨hd, hl⟩ h2 x hx
    simp only [List.mem_cons] at hx h2
    rcases hx with rfl | hx
    · omega
    · exact hl x hx

theorem valFrom_replicate (K : ℕ) : ∀ k, valFrom k (List.replicate K 0) = 0 := by
  induction K with
  | zero => intro k; rfl
  | succ K ih => intro k; rw [List.replicate_succ, valFrom, ih]; simp

theorem valFrom_append (c : ℕ) : ∀ (l : List ℕ) (k : ℕ),
    valFrom k (l ++ [c]) = valFrom k l + c * w (k + l.length)
  | [], k => by simp [valFrom]
  | d :: l, k => by
    rw [List.cons_append, valFrom, valFrom, valFrom_append c l (k + 1), List.length_cons]
    rw [show k + 1 + l.length = k + (l.length + 1) by omega]
    ring

theorem val_maxK (K : ℕ) : val (maxK K) + 1 = w K := by
  cases K with
  | zero => rfl
  | succ K =>
    simp only [val, maxK, valFrom_append, valFrom_replicate, List.length_replicate, zero_add, w_succ]

/-- `0 :: maxK (K + 1) = maxK (K + 2)`. -/
theorem cons_zero_maxK (K : ℕ) : 0 :: maxK (K + 1) = maxK (K + 2) := by
  simp [maxK, List.replicate_succ]

/-- If `0 :: l` is not maximal and `l` contains a `2`, then `l` is not maximal. -/
theorem ne_maxK_of_cons_zero {l : List ℕ} (h2 : 2 ∈ l) (h : 0 :: l ≠ maxK (0 :: l).length) :
    l ≠ maxK l.length := by
  intro hl
  apply h
  cases hlen : l.length with
  | zero => rw [List.length_eq_zero_iff.mp hlen] at h2; simp at h2
  | succ j =>
    rw [hlen] at hl
    rw [List.length_cons, hlen, hl, cons_zero_maxK]

/-! #### The increment: canonicity, value, cost -/

theorem valFrom_bump (k : ℕ) : ∀ l : List ℕ, l ≠ [] → valFrom k (bump l) = valFrom k l + w k
  | [], h => absurd rfl h
  | d :: l, _ => by simp only [bump, valFrom]; ring

/-- **Theorem 6 (i), the increment.** For a canonical `l` that is not the largest representation of its
length, `inc l` is canonical and, at any offset `k`, its value exceeds that of `l` by `1` if `l` contains a
`2`, and by `w k` (the weight of the lowest position) otherwise. In particular `val (inc l) = val l + 1`. -/
theorem inc_spec : ∀ l : List ℕ, Canon l → l ≠ maxK l.length →
    Canon (inc l) ∧ ∀ k, valFrom k (inc l) = valFrom k l + (if 2 ∈ l then 1 else w k)
  | [], _, h => absurd rfl h
  | 0 :: l, hc, hne => by
    by_cases h2 : 2 ∈ l
    · have hne' := ne_maxK_of_cons_zero h2 hne
      obtain ⟨hc', hv⟩ := inc_spec l hc hne'
      simp only [inc, h2, ↓reduceIte]
      refine ⟨hc', fun k => ?_⟩
      simp only [valFrom, hv (k + 1), h2, ↓reduceIte, List.mem_cons, or_true]
      ring
    · simp only [inc, h2, ↓reduceIte]
      refine ⟨(canon_cons_succ 0 l).mpr ⟨by norm_num, canon_le_one_of_two_notMem l hc h2⟩,
        fun k => ?_⟩
      have : ¬ (2 = 0 ∨ 2 ∈ l) := by simp [h2]
      simp only [valFrom, List.mem_cons, this, ↓reduceIte]
      ring
  | 1 :: l, ⟨_, hl⟩, _ => by
    have h2 : 2 ∉ l := fun h => by have := hl 2 h; omega
    refine ⟨(canon_cons_succ 1 l).mpr ⟨le_rfl, hl⟩, fun k => ?_⟩
    have : ¬ (2 = 1 ∨ 2 ∈ l) := by simp [h2]
    simp only [inc, valFrom, List.mem_cons, this, ↓reduceIte]
    ring
  | 2 :: l, ⟨_, hl⟩, hne => by
    have hl0 : l ≠ [] := by
      rintro rfl
      exact hne rfl
    obtain ⟨x, l', rfl⟩ := List.exists_cons_of_ne_nil hl0
    have hx : x ≤ 1 := hl x (List.mem_cons_self)
    refine ⟨(canon_cons_zero _).mpr ((canon_cons_succ x l').mpr
      ⟨by omega, fun y hy => hl y (List.mem_cons_of_mem x hy)⟩), fun k => ?_⟩
    simp only [inc, bump, valFrom, List.mem_cons, true_or, ↓reduceIte, w_succ]
    ring
  | (_ + 3) :: _, ⟨h, _⟩, _ => by omega

theorem val_inc (l : List ℕ) (hc : Canon l) (hne : l ≠ maxK l.length) : val (inc l) = val l + 1 := by
  have := (inc_spec l hc hne).2 0
  simp only [val, this, w_zero, ite_self]

theorem changes_self : ∀ l : List ℕ, changes l l = 0
  | [] => rfl
  | x :: l => by simp [changes, changes_self l]

theorem changes_bump : ∀ l : List ℕ, l ≠ [] → changes l (bump l) = 1
  | [], h => absurd rfl h
  | x :: l, _ => by simp [changes, bump, changes_self]

/-- **Theorem 6 (i), the cost of an increment.** For a canonical, non-maximal `l`, the increment changes
exactly `1 + χ(l)` digits. -/
theorem changes_inc : ∀ l : List ℕ, Canon l → l ≠ maxK l.length → changes l (inc l) = 1 + chi l
  | [], _, h => absurd rfl h
  | 0 :: l, hc, hne => by
    by_cases h2 : 2 ∈ l
    · have hne' := ne_maxK_of_cons_zero h2 hne
      have ih := changes_inc l hc hne'
      simp only [chi, h2, ↓reduceIte] at ih
      simp only [inc, h2, ↓reduceIte, changes, chi, List.mem_cons, or_true, ih]
    · simp [inc, h2, changes, chi, changes_self]
  | 1 :: l, ⟨_, hl⟩, _ => by
    have h2 : 2 ∉ l := fun h => by have := hl 2 h; omega
    have : ¬ (2 = 1 ∨ 2 ∈ l) := by simp [h2]
    simp only [inc, changes, chi, List.mem_cons, this, changes_self]
    rfl
  | 2 :: l, ⟨_, _⟩, hne => by
    have hl0 : l ≠ [] := by
      rintro rfl
      exact hne rfl
    simp [inc, changes, chi, changes_bump l hl0]
  | (_ + 3) :: _, ⟨h, _⟩, _ => by omega

/-! #### `repK K n` is the canonical representation of `n` -/

theorem repK_spec (K : ℕ) : ∀ n, n < w K → Canon (repK K n) ∧ val (repK K n) = n := by
  intro n
  induction n with
  | zero => intro _; exact ⟨canon_replicate K, valFrom_replicate K 0⟩
  | succ n ih =>
    intro hn
    obtain ⟨hc, hv⟩ := ih (by omega)
    have hne : repK K n ≠ maxK (repK K n).length := by
      rw [length_repK]
      intro h
      have := val_maxK K
      rw [← h, hv] at this
      omega
    rw [repK_succ]
    exact ⟨(inc_spec _ hc hne).1, by rw [val_inc _ hc hne, hv]⟩

theorem repK_ne_maxK {K n : ℕ} (hn : n + 1 < w K) : repK K n ≠ maxK (repK K n).length := by
  rw [length_repK]
  intro h
  have := val_maxK K
  rw [← h, (repK_spec K n (by omega)).2] at this
  omega

/-! #### Appending a top digit -/

theorem bump_append (c : ℕ) : ∀ l : List ℕ, l ≠ [] → bump (l ++ [c]) = bump l ++ [c]
  | [], h => absurd rfl h
  | _ :: _, _ => rfl

theorem inc_append (c : ℕ) (hc : c ≠ 2) : ∀ l : List ℕ, l ≠ maxK l.length →
    inc (l ++ [c]) = inc l ++ [c]
  | [], h => absurd rfl h
  | 0 :: l, hne => by
    have hiff : (2 ∈ l ++ [c]) ↔ 2 ∈ l := by
      simp only [List.mem_append, List.mem_singleton]
      constructor
      · rintro (h | h)
        · exact h
        · exact absurd h.symm hc
      · exact Or.inl
    by_cases h2 : 2 ∈ l
    · have hne' := ne_maxK_of_cons_zero h2 hne
      simp only [List.cons_append, inc, hiff.mpr h2, h2, ↓reduceIte, inc_append c hc l hne']
    · have h2' : 2 ∉ l ++ [c] := fun h => h2 (hiff.mp h)
      simp only [List.cons_append, inc, h2, h2', ↓reduceIte]
  | 1 :: l, _ => rfl
  | 2 :: l, hne => by
    have hl0 : l ≠ [] := by
      rintro rfl
      exact hne rfl
    simp only [List.cons_append, inc, bump_append c l hl0]
  | (d + 3) :: l, _ => rfl

theorem inc_maxK_append (c : ℕ) (hc : c ≤ 1) : ∀ K : ℕ,
    inc (maxK K ++ [c]) = List.replicate K 0 ++ [c + 1]
  | 0 => by
    interval_cases c <;> rfl
  | 1 => by
    simp [maxK, inc, bump]
  | K + 2 => by
    rw [← cons_zero_maxK, List.cons_append, inc]
    have h2 : 2 ∈ maxK (K + 1) ++ [c] := by simp [maxK]
    simp only [h2, ↓reduceIte, inc_maxK_append c hc (K + 1)]
    simp [List.replicate_succ]

/-- Values below `w K` keep their representation when a `K`-th digit `0` is added. -/
theorem decomp_low (K : ℕ) : ∀ n, n < w K → repK (K + 1) n = repK K n ++ [0] := by
  intro n
  induction n with
  | zero => intro _; rw [repK_zero, repK_zero, List.replicate_succ']
  | succ n ih =>
    intro hn
    rw [repK_succ, repK_succ, ih (by omega), inc_append 0 (by norm_num) _ (repK_ne_maxK hn)]

theorem decomp_high_aux (K : ℕ) (hlast : repK K (w K - 1) = maxK K) :
    ∀ m, m < w K → repK (K + 1) (w K + m) = repK K m ++ [1] := by
  have hw := w_pos K
  intro m
  induction m with
  | zero =>
    intro _
    have e : w K + 0 = (w K - 1) + 1 := by omega
    rw [e, repK_succ, decomp_low K (w K - 1) (by omega), hlast, inc_maxK_append 0 (by norm_num),
      repK_zero]
  | succ m ih =>
    intro hm
    rw [← Nat.add_assoc, repK_succ, ih (by omega), inc_append 1 (by norm_num) _ (repK_ne_maxK hm),
      repK_succ]

theorem decomp_top_aux (K : ℕ) (hlast : repK K (w K - 1) = maxK K) :
    repK (K + 1) (2 * w K) = maxK (K + 1) := by
  have hw := w_pos K
  rw [show 2 * w K = (w K + (w K - 1)) + 1 by omega, repK_succ,
    decomp_high_aux K hlast (w K - 1) (by omega), hlast, inc_maxK_append 1 le_rfl]
  rfl

/-- The last `K`-digit representation is `maxK K`. -/
theorem repK_last : ∀ K, repK K (w K - 1) = maxK K
  | 0 => rfl
  | K + 1 => by
    rw [w_succ, show 2 * w K + 1 - 1 = 2 * w K by omega]
    exact decomp_top_aux K (repK_last K)

/-- Values `w K + m` (`m < w K`) are `1` at position `K` on top of the representation of `m`. -/
theorem decomp_high (K : ℕ) : ∀ m, m < w K → repK (K + 1) (w K + m) = repK K m ++ [1] :=
  decomp_high_aux K (repK_last K)

/-- The value `2 w K` is the digit `2` at position `K`. -/
theorem decomp_top (K : ℕ) : repK (K + 1) (2 * w K) = maxK (K + 1) :=
  decomp_top_aux K (repK_last K)

/-! #### Uniqueness of canonical representations -/

theorem canon_of_append (c : ℕ) : ∀ l : List ℕ, Canon (l ++ [c]) → Canon l
  | [], _ => trivial
  | 0 :: l, h => canon_of_append c l h
  | (_ + 1) :: _, ⟨hd, hl⟩ => ⟨hd, fun x hx => hl x (List.mem_append_left _ hx)⟩

theorem le_two_of_canon_append (c : ℕ) : ∀ l : List ℕ, Canon (l ++ [c]) → c ≤ 2
  | [], h => by
    rcases c with _ | c
    · omega
    · exact h.1
  | 0 :: l, h => le_two_of_canon_append c l h
  | (d + 1) :: l, ⟨_, hl⟩ => by
    have := hl c (by simp)
    omega

theorem zero_of_canon_append_two : ∀ l : List ℕ, Canon (l ++ [2]) → ∀ x ∈ l, x = 0
  | [], _ => by simp
  | 0 :: l, h => by
    intro x hx
    simp only [List.mem_cons] at hx
    rcases hx with rfl | hx
    · rfl
    · exact zero_of_canon_append_two l h x hx
  | (d + 1) :: l, ⟨_, hl⟩ => by
    have := hl 2 (by simp)
    omega

/-- Every canonical list of length `K` is `repK K n` for some `n < w K`. -/
theorem canon_eq_repK : ∀ K (l : List ℕ), l.length = K → Canon l → ∃ n < w K, repK K n = l
  | 0, l, hl, _ => ⟨0, by rw [w_zero]; omega, by rw [List.length_eq_zero_iff.mp hl]; rfl⟩
  | K + 1, l, hl, hc => by
    rcases List.eq_nil_or_concat' l with rfl | ⟨l', c, rfl⟩
    · simp at hl
    have hl' : l'.length = K := by simpa using hl
    obtain ⟨n', hn', hrep⟩ := canon_eq_repK K l' hl' (canon_of_append c l' hc)
    have hc2 := le_two_of_canon_append c l' hc
    have hwK := w_succ K
    interval_cases c
    · exact ⟨n', by omega, by rw [decomp_low K n' hn', hrep]⟩
    · exact ⟨w K + n', by omega, by rw [decomp_high K n' hn', hrep]⟩
    · refine ⟨2 * w K, by omega, ?_⟩
      have hz : l' = List.replicate K 0 :=
        List.eq_replicate_iff.mpr ⟨hl', zero_of_canon_append_two l' hc⟩
      rw [decomp_top, hz]
      rfl

/-- A canonical `K`-digit list has value `< w K`. -/
theorem val_lt (l : List ℕ) (hc : Canon l) : val l < w l.length := by
  obtain ⟨n, hn, hrep⟩ := canon_eq_repK l.length l rfl hc
  have : val l = n := by rw [← (repK_spec _ n hn).2, hrep]
  rw [this]
  exact hn

/-- **Uniqueness of canonical skew-binary representations** (used without proof in the paper, citing
Myers 1983 and Okasaki 1998): two canonical digit lists of the same length and value are equal. -/
theorem canon_unique (l m : List ℕ) (hl : Canon l) (hm : Canon m) (hlen : l.length = m.length)
    (hv : val l = val m) : l = m := by
  obtain ⟨n, hn, hl'⟩ := canon_eq_repK l.length l rfl hl
  obtain ⟨n', hn', hm'⟩ := canon_eq_repK l.length m hlen.symm hm
  have e1 : val l = n := by rw [← (repK_spec _ n hn).2, hl']
  have e2 : val m = n' := by rw [← (repK_spec _ n' hn').2, hm']
  have e : n = n' := by omega
  rw [← hl', ← hm', e]

/-- **Existence and uniqueness.** Every `n < w K = 2^(K+1) - 1` has exactly one canonical `K`-digit
skew-binary representation, namely `repK K n`. -/
theorem canon_existsUnique (K n : ℕ) (hn : n < w K) :
    ∃! l : List ℕ, l.length = K ∧ Canon l ∧ val l = n :=
  ⟨repK K n, ⟨length_repK K n, repK_spec K n hn⟩, fun m ⟨hlen, hc, hv⟩ =>
    canon_unique m (repK K n) hc (repK_spec K n hn).1 (by rw [hlen, length_repK])
      (by rw [hv, (repK_spec K n hn).2])⟩

/-- **CLM-C10-07, the increment cost.** If `l` and `m` are the canonical representations (of the same
length) of `n` and `n + 1`, they differ in exactly `1 + χ(l)` positions; in particular in at most `2`. -/
theorem increment_cost (l m : List ℕ) (hl : Canon l) (hm : Canon m) (hlen : l.length = m.length)
    (hv : val m = val l + 1) : changes l m = 1 + chi l ∧ changes l m ≤ 2 := by
  have hlt := val_lt m hm
  have hne : l ≠ maxK l.length := by
    intro h
    have := val_maxK l.length
    rw [← h, hlen] at this
    omega
  have hmi : m = inc l :=
    canon_unique m (inc l) hm (inc_spec l hl hne).1 (by rw [length_inc, hlen])
      (by rw [hv, val_inc l hl hne])
  rw [hmi, changes_inc l hl hne]
  refine ⟨rfl, ?_⟩
  unfold chi
  split_ifs <;> omega

/-! #### The `χ`-word is `B_k`, and the average cost -/

theorem chi_append (l : List ℕ) {c : ℕ} (hc : c ≠ 2) : chi (l ++ [c]) = chi l := by
  have : (2 ∈ l ++ [c]) ↔ 2 ∈ l := by
    simp only [List.mem_append, List.mem_singleton]
    constructor
    · rintro (h | h)
      · exact h
      · exact absurd h.symm hc
    · exact Or.inl
  simp only [chi, this]

/-- **CLM-C10-07, the `χ`-word.** `χ(0) χ(1) … χ(M_k - 1) = B_k`, where `χ(n) = 1` iff the canonical
representation of `n` contains a `2`. -/
theorem chi_word : ∀ K, (List.range (w K)).map (fun n => chi (repK K n)) = B K
  | 0 => rfl
  | K + 1 => by
    rw [w_succ, show 2 * w K + 1 = (w K + w K) + 1 by ring, List.range_succ, List.range_add,
      List.map_append, List.map_append, List.map_map]
    have h1 : (List.range (w K)).map (fun n => chi (repK (K + 1) n)) = B K := by
      rw [← chi_word K]
      refine List.map_congr_left (fun n hn => ?_)
      rw [decomp_low K n (List.mem_range.mp hn), chi_append _ (by norm_num)]
    have h2 : (List.range (w K)).map ((fun n => chi (repK (K + 1) n)) ∘ (fun x => w K + x)) = B K := by
      rw [← chi_word K]
      refine List.map_congr_left (fun n hn => ?_)
      simp only [Function.comp]
      rw [decomp_high K n (List.mem_range.mp hn), chi_append _ (by norm_num)]
    have h3 : chi (repK (K + 1) (w K + w K)) = 1 := by
      rw [← two_mul, decomp_top]
      simp [chi, maxK]
    rw [h1, h2, List.map_singleton, h3]
    rfl

theorem count_one_eq_sum : ∀ l : List ℕ, (∀ x ∈ l, x ≤ 1) → l.count 1 = l.sum
  | [], _ => rfl
  | x :: l, h => by
    have hx := h x (by simp)
    have ih := count_one_eq_sum l (fun y hy => h y (by simp [hy]))
    rw [List.count_cons, List.sum_cons, ih]
    interval_cases x
    · simp
    · simp only [beq_self_eq_true, ↓reduceIte]; omega

theorem list_sum_range (g : ℕ → ℕ) : ∀ N, ((List.range N).map g).sum = ∑ n ∈ Finset.range N, g n
  | 0 => rfl
  | N + 1 => by rw [List.sum_range_succ, Finset.sum_range_succ, list_sum_range g N]

/-- `S_K(N) = χ(0) + … + χ(N - 1)` for `N ≤ M_K`. -/
theorem S_eq_sum_chi (K N : ℕ) (hN : N ≤ w K) : S K N = ∑ n ∈ Finset.range N, chi (repK K n) := by
  rw [S, ← chi_word K, ← List.map_take, List.take_range, Nat.min_eq_left hN, ← list_sum_range]
  refine count_one_eq_sum _ (fun x hx => ?_)
  obtain ⟨n, _, rfl⟩ := List.mem_map.mp hx
  unfold chi
  split_ifs <;> omega

/-- The total number of digit changes of the increments `n → n + 1`, `0 ≤ n < N`, in `K`-digit
canonical skew binary. -/
def totalCost (K N : ℕ) : ℕ := ∑ n ∈ Finset.range N, changes (repK K n) (repK K (n + 1))

/-- **CLM-C10-07, the total cost.** For `N < w K`: `totalCost K N = N + S_K(N)`. -/
theorem totalCost_eq (K N : ℕ) (hN : N < w K) : totalCost K N = N + S K N := by
  rw [S_eq_sum_chi K N (by omega), totalCost]
  have : ∀ n ∈ Finset.range N, changes (repK K n) (repK K (n + 1)) = 1 + chi (repK K n) := by
    intro n hn
    have hn' := Finset.mem_range.mp hn
    rw [repK_succ]
    exact changes_inc _ (repK_spec K n (by omega)).1 (repK_ne_maxK (by omega))
  rw [Finset.sum_congr rfl this, Finset.sum_add_distrib]
  simp

/-- **CLM-C10-07, the average (explicit form).** For `N < w K = 2^(K+1) - 1`,
`|totalCost K N - 3N/2| ≤ (K + 1)/2`. -/
theorem totalCost_bound (K N : ℕ) (hN : N < w K) :
    |(totalCost K N : ℚ) - 3 * N / 2| ≤ (K + 1) / 2 := by
  have h := prefix_bound K N (by rw [length_B_eq_w]; omega)
  rw [totalCost_eq K N hN]
  push_cast
  rw [show ((N : ℚ) + S K N - 3 * N / 2) = (S K N : ℚ) - N / 2 by ring]
  exact h

/-- **CLM-C10-07, the average `3/2 + O(log N / N)`.** With `K = ⌊log₂ (N + 1)⌋` digits (enough for all
values `≤ N`), the average number of changed digits over the increments `n → n + 1`, `0 ≤ n < N`,
differs from `3/2` by at most `(⌊log₂ (N + 1)⌋ + 1)/(2N)`. -/
theorem average_cost (N : ℕ) (hN : 0 < N) :
    |(totalCost (Nat.log 2 (N + 1)) N : ℚ) / N - 3 / 2| ≤ (Nat.log 2 (N + 1) + 1) / (2 * N) := by
  set K := Nat.log 2 (N + 1)
  have hK : N < w K := by
    have : N + 1 < 2 ^ (K + 1) := Nat.lt_pow_succ_log_self (b := 2) (by norm_num) (N + 1)
    unfold w
    omega
  have h := totalCost_bound K N hK
  have hNq : (0 : ℚ) < N := by exact_mod_cast hN
  rw [show (totalCost K N : ℚ) / N - 3 / 2 = ((totalCost K N : ℚ) - 3 * N / 2) / N by
    field_simp]
  rw [abs_div, abs_of_pos hNq, div_le_div_iff₀ hNq (by positivity)]
  nlinarith [abs_nonneg ((totalCost K N : ℚ) - 3 * N / 2)]

theorem changes_append (c : ℕ) : ∀ l m : List ℕ, l.length = m.length →
    changes (l ++ [c]) (m ++ [c]) = changes l m
  | [], [], _ => by simp [changes]
  | x :: l, y :: m, h => by
    simp only [List.cons_append, changes, changes_append c l m (by simpa using h)]
  | [], _ :: _, h => by simp at h
  | _ :: _, [], h => by simp at h

/-- The cost does not depend on the number of digits, once it is large enough. -/
theorem totalCost_succ (K N : ℕ) (hN : N < w K) : totalCost (K + 1) N = totalCost K N := by
  refine Finset.sum_congr rfl (fun n hn => ?_)
  have hn' := Finset.mem_range.mp hn
  rw [decomp_low K n (by omega), decomp_low K (n + 1) (by omega),
    changes_append 0 _ _ (by rw [length_repK, length_repK])]

end Infinity.C10

#print axioms Infinity.C10.B_le_one
#print axioms Infinity.C10.length_B
#print axioms Infinity.C10.count_B
#print axioms Infinity.C10.prefix_bound_nat
#print axioms Infinity.C10.prefix_bound
#print axioms Infinity.C10.count_B_eq
#print axioms Infinity.C10.deficit_full
#print axioms Infinity.C10.inc_spec
#print axioms Infinity.C10.val_inc
#print axioms Infinity.C10.changes_inc
#print axioms Infinity.C10.repK_spec
#print axioms Infinity.C10.canon_unique
#print axioms Infinity.C10.canon_existsUnique
#print axioms Infinity.C10.increment_cost
#print axioms Infinity.C10.chi_word
#print axioms Infinity.C10.totalCost_eq
#print axioms Infinity.C10.totalCost_bound
#print axioms Infinity.C10.average_cost
#print axioms Infinity.C10.totalCost_succ
