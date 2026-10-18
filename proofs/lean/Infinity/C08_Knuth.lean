import Mathlib.NumberTheory.Real.GoldenRatio
import Mathlib.Data.Nat.Fib.Zeckendorf
import Mathlib.Tactic

/-!
# Cycle C08 — Knuth's Fibonacci multiplication and all its shifts are associative

For `t : ℕ` the shifted Knuth product is
`circ t a b = Σ_{k ∈ Z(a)} Σ_{l ∈ Z(b)} F (k + l + t)`, where `Z(n) = Nat.zeckendorf n` is the
list of Zeckendorf indices of `n` (indices `≥ 2`, Mathlib's `Nat.fib` indexing). `t = 0` is
Knuth's Fibonacci multiplication (Knuth 1988); in the lab's `G`-indexing this is shift `s = t + 2`.

Proof (Arnoux-style, blueprint `proofs/paper/C08.md`, Theorem 1). Put `E x n = Σ_{k ∈ Z(n)} x ^ k`
for `x = φ, ψ`.
* `E_eq`: `E x n = n * x + sh n` with the integer "shadow" `sh n = Σ F (k - 1)`.
* `window`: `|E ψ n| < -ψ` (Zeckendorf indices form an increasing chain with gaps `≥ 2`,
  starting at `≥ 2`; the bound closes because `(-ψ) + (-ψ)^2 = 1`).
* `key`: `E x (circ t a b) = x ^ t * E x a * E x b` for `x = φ, ψ`: both sides have the
  form `P * x + (integer)`, and the two integers differ by less than `1`.
* `E_inj`: `n` is determined by `E φ n` and `E ψ n` because `φ ≠ ψ`.
Associativity and commutativity follow from the commutativity and associativity of `ℝ`.
-/

open Real
open scoped goldenRatio

namespace Infinity.C08

/-- Knuth's circle product with an extra shift `t` (`t = 0`: Knuth's Fibonacci multiplication). -/
def circ (t a b : ℕ) : ℕ :=
  ((Nat.zeckendorf a).map (fun k => ((Nat.zeckendorf b).map (fun l => Nat.fib (k + l + t))).sum)).sum

/-- The "shadow" of `n`: `Σ_{k ∈ Z(n)} F (k - 1)`. -/
def sh (n : ℕ) : ℕ := ((Nat.zeckendorf n).map (fun k => Nat.fib (k - 1))).sum

/-- The real "embedding" `Σ_{k ∈ Z(n)} x ^ k`. -/
noncomputable def E (x : ℝ) (n : ℕ) : ℝ := ((Nat.zeckendorf n).map (fun k => x ^ k)).sum

/-! ### Powers of `φ` and `ψ` in the basis `{x, 1}` -/

lemma phi_pow (k : ℕ) (hk : 1 ≤ k) : φ ^ k = (Nat.fib k : ℝ) * φ + Nat.fib (k - 1) := by
  have h := goldenRatio_mul_fib_succ_add_fib (k - 1)
  rw [Nat.sub_add_cancel hk] at h
  rw [← h]; ring

lemma psi_pow (k : ℕ) (hk : 1 ≤ k) : ψ ^ k = (Nat.fib k : ℝ) * ψ + Nat.fib (k - 1) := by
  have h := goldenConj_mul_fib_succ_add_fib (k - 1)
  rw [Nat.sub_add_cancel hk] at h
  rw [← h]; ring

/-! ### Zeckendorf indices -/

lemma chain_ge_two : ∀ l : List ℕ, (l ++ [0]).IsChain (fun a b => b + 2 ≤ a) → ∀ k ∈ l, 2 ≤ k
  | [], _, k, hk => by simp at hk
  | [a], h, k, hk => by
    have h' : 0 + 2 ≤ a := by simpa using h
    simp only [List.mem_singleton] at hk
    omega
  | a :: b :: l, h, k, hk => by
    have h' : b + 2 ≤ a ∧ ((b :: l) ++ [0]).IsChain (fun a b => b + 2 ≤ a) := by
      simpa using h
    have hb := chain_ge_two (b :: l) h'.2
    rcases List.mem_cons.mp hk with rfl | hk
    · have := hb b (by simp); omega
    · exact hb k hk

lemma zeck_ge_two (n : ℕ) : ∀ k ∈ Nat.zeckendorf n, 2 ≤ k :=
  chain_ge_two _ (Nat.isZeckendorfRep_zeckendorf n)

/-! ### Decomposition `Σ x ^ k = v * x + h` -/

lemma sum_pow_decomp (x : ℝ) (hx : ∀ k, 1 ≤ k → x ^ k = (Nat.fib k : ℝ) * x + Nat.fib (k - 1))
    (l : List ℕ) (hl : ∀ k ∈ l, 1 ≤ k) :
    (l.map (fun k => x ^ k)).sum =
      (((l.map Nat.fib).sum : ℕ) : ℝ) * x + (((l.map (fun k => Nat.fib (k - 1))).sum : ℕ) : ℝ) := by
  induction l with
  | nil => simp
  | cons a l ih =>
    simp only [List.map_cons, List.sum_cons, Nat.cast_add]
    rw [hx a (hl a (by simp)), ih (fun k hk => hl k (by simp [hk]))]
    ring

lemma E_eq (x : ℝ) (hx : ∀ k, 1 ≤ k → x ^ k = (Nat.fib k : ℝ) * x + Nat.fib (k - 1)) (n : ℕ) :
    E x n = (n : ℝ) * x + (sh n : ℝ) := by
  have h := sum_pow_decomp x hx (Nat.zeckendorf n)
    (fun k hk => le_trans (by norm_num) (zeck_ge_two n k hk))
  rw [Nat.sum_zeckendorf_fib] at h
  simpa [E, sh] using h

/-! ### The window lemma -/

lemma negPsi_pos : 0 < -ψ := by linarith [goldenConj_neg]

lemma negPsi_lt_one : -ψ < 1 := by linarith [neg_one_lt_goldenConj]

lemma negPsi_add_sq : -ψ + (-ψ) ^ 2 = 1 := by
  have := goldenConj_sq
  nlinarith

/-- Sums of `ψ ^ k` along an increasing chain with gaps `≥ 2` that starts after `m` are
bounded by `(-ψ) ^ (m + 1)` in absolute value. -/
lemma window_aux : ∀ (l : List ℕ) (m : ℕ), (m :: l).IsChain (fun a b => a + 2 ≤ b) →
    |(l.map (fun k => ψ ^ k)).sum| < (-ψ) ^ (m + 1)
  | [], m, _ => by simpa using pow_pos negPsi_pos (m + 1)
  | a :: l, m, h => by
    have h' : m + 2 ≤ a ∧ (a :: l).IsChain (fun a b => a + 2 ≤ b) := by simpa using h
    obtain ⟨hma, hrest⟩ := h'
    have ih := window_aux l a hrest
    simp only [List.map_cons, List.sum_cons]
    obtain ⟨j, rfl⟩ : ∃ j, a = j + 1 := ⟨a - 1, by omega⟩
    have hr0 := negPsi_pos
    have hr1 := negPsi_lt_one
    have habs : |ψ ^ (j + 1)| = (-ψ) ^ (j + 1) := by
      rw [abs_pow, abs_of_neg goldenConj_neg]
    have hsum : (-ψ) ^ (j + 1) + (-ψ) ^ (j + 1 + 1) = (-ψ) ^ j := by
      have e : (-ψ) ^ (j + 1) + (-ψ) ^ (j + 1 + 1) = (-ψ) ^ j * (-ψ + (-ψ) ^ 2) := by ring
      rw [e, negPsi_add_sq, mul_one]
    have hmono : (-ψ) ^ j ≤ (-ψ) ^ (m + 1) :=
      pow_le_pow_of_le_one hr0.le hr1.le (by omega)
    calc |ψ ^ (j + 1) + (l.map (fun k => ψ ^ k)).sum|
        ≤ |ψ ^ (j + 1)| + |(l.map (fun k => ψ ^ k)).sum| := abs_add_le _ _
      _ < (-ψ) ^ (j + 1) + (-ψ) ^ (j + 1 + 1) := by rw [habs]; linarith
      _ = (-ψ) ^ j := hsum
      _ ≤ (-ψ) ^ (m + 1) := hmono

/-- **Window lemma.** For every `n`, `|Σ_{k ∈ Z(n)} ψ ^ k| < -ψ = φ⁻¹`. -/
lemma window (n : ℕ) : |E ψ n| < -ψ := by
  have h := Nat.isZeckendorfRep_zeckendorf n
  have h2 : (0 :: (Nat.zeckendorf n).reverse).IsChain (fun a b => a + 2 ≤ b) := by
    have h3 : ((Nat.zeckendorf n) ++ [0]).reverse.IsChain (fun a b => a + 2 ≤ b) :=
      List.isChain_reverse.mpr h
    simpa using h3
  have h4 := window_aux _ 0 h2
  simpa [E, List.map_reverse, List.sum_reverse] using h4

/-! ### The twisted homomorphism -/

lemma sum_map_mul_const (l : List ℕ) (f : ℕ → ℝ) (c : ℝ) :
    (l.map (fun i => f i * c)).sum = (l.map f).sum * c := by
  induction l with
  | nil => simp
  | cons a l ih => simp [List.sum_cons, ih, add_mul]

lemma prod_sum (x : ℝ) (t : ℕ) (A B : List ℕ) :
    (A.map (fun k => (B.map (fun l => x ^ (k + l + t))).sum)).sum =
      x ^ t * (A.map (fun k => x ^ k)).sum * (B.map (fun l => x ^ l)).sum := by
  have inner : ∀ k, (B.map (fun l => x ^ (k + l + t))).sum = x ^ k * x ^ t * (B.map (fun l => x ^ l)).sum := by
    intro k
    have e : (B.map (fun l => x ^ (k + l + t))) = B.map (fun l => x ^ l * (x ^ k * x ^ t)) := by
      apply List.map_congr_left
      intro l _
      rw [pow_add, pow_add]; ring
    rw [e, sum_map_mul_const]; ring
  simp only [inner]
  rw [sum_map_mul_const (A) (fun k => x ^ k * x ^ t) ((B.map (fun l => x ^ l)).sum),
    sum_map_mul_const A (fun k => x ^ k) (x ^ t)]
  ring

lemma inner_decomp (x : ℝ) (hx : ∀ k, 1 ≤ k → x ^ k = (Nat.fib k : ℝ) * x + Nat.fib (k - 1))
    (t a : ℕ) (ha : 1 ≤ a) (B : List ℕ) :
    (B.map (fun l => x ^ (a + l + t))).sum =
      (((B.map (fun l => Nat.fib (a + l + t))).sum : ℕ) : ℝ) * x +
      (((B.map (fun l => Nat.fib (a + l + t - 1))).sum : ℕ) : ℝ) := by
  induction B with
  | nil => simp
  | cons b B ih =>
    simp only [List.map_cons, List.sum_cons, Nat.cast_add]
    rw [hx (a + b + t) (by omega), ih]
    ring

lemma double_decomp (x : ℝ) (hx : ∀ k, 1 ≤ k → x ^ k = (Nat.fib k : ℝ) * x + Nat.fib (k - 1))
    (t : ℕ) (A B : List ℕ) (hA : ∀ k ∈ A, 1 ≤ k) :
    (A.map (fun k => (B.map (fun l => x ^ (k + l + t))).sum)).sum =
      (((A.map (fun k => (B.map (fun l => Nat.fib (k + l + t))).sum)).sum : ℕ) : ℝ) * x +
      (((A.map (fun k => (B.map (fun l => Nat.fib (k + l + t - 1))).sum)).sum : ℕ) : ℝ) := by
  induction A with
  | nil => simp
  | cons a A ih =>
    simp only [List.map_cons, List.sum_cons, Nat.cast_add]
    rw [inner_decomp x hx t a (hA a (by simp)) B, ih (fun k hk => hA k (by simp [hk]))]
    ring

/-- **Twisted homomorphism.** `E x (a ∘_t b) = x ^ t * E x a * E x b` for `x = φ` and `x = ψ`. -/
theorem key (t a b : ℕ) :
    E φ (circ t a b) = φ ^ t * E φ a * E φ b ∧ E ψ (circ t a b) = ψ ^ t * E ψ a * E ψ b := by
  set P := circ t a b with hP
  set Q := ((Nat.zeckendorf a).map
    (fun k => ((Nat.zeckendorf b).map (fun l => Nat.fib (k + l + t - 1))).sum)).sum with hQdef
  have hA : ∀ k ∈ Nat.zeckendorf a, 1 ≤ k := fun k hk => le_trans (by norm_num) (zeck_ge_two a k hk)
  have hφ : φ ^ t * E φ a * E φ b = (P : ℝ) * φ + Q := by
    rw [E, E, ← prod_sum, double_decomp φ phi_pow t _ _ hA]
    rfl
  have hψ : ψ ^ t * E ψ a * E ψ b = (P : ℝ) * ψ + Q := by
    rw [E, E, ← prod_sum, double_decomp ψ psi_pow t _ _ hA]
    rfl
  -- the product of the two conjugates is small
  have hr0 := negPsi_pos
  have hr1 := negPsi_lt_one
  have wa := window a
  have wb := window b
  have hprod : |ψ ^ t * E ψ a * E ψ b| < (-ψ) ^ 2 := by
    rw [abs_mul, abs_mul, abs_pow, abs_of_neg goldenConj_neg]
    have ht : (-ψ) ^ t ≤ 1 := pow_le_one₀ hr0.le hr1.le
    have hab : |E ψ a| * |E ψ b| < (-ψ) * (-ψ) :=
      mul_lt_mul'' wa wb (abs_nonneg _) (abs_nonneg _)
    have hnn : 0 ≤ |E ψ a| * |E ψ b| := mul_nonneg (abs_nonneg _) (abs_nonneg _)
    calc (-ψ) ^ t * |E ψ a| * |E ψ b| = (-ψ) ^ t * (|E ψ a| * |E ψ b|) := by ring
      _ ≤ 1 * (|E ψ a| * |E ψ b|) := mul_le_mul_of_nonneg_right ht hnn
      _ < (-ψ) * (-ψ) := by linarith
      _ = (-ψ) ^ 2 := by ring
  -- integrality: Q is the shadow of P
  have hQ : Q = sh P := by
    have eP := E_eq ψ psi_pow P
    have wP := window P
    have hlt : |(Q : ℝ) - (sh P : ℝ)| < 1 := by
      have e : (Q : ℝ) - (sh P : ℝ) = ψ ^ t * E ψ a * E ψ b - E ψ P := by rw [hψ, eP]; ring
      rw [e]
      calc |ψ ^ t * E ψ a * E ψ b - E ψ P| ≤ |ψ ^ t * E ψ a * E ψ b| + |E ψ P| := abs_sub _ _
        _ < (-ψ) ^ 2 + (-ψ) := add_lt_add hprod wP
        _ = 1 := by linarith [negPsi_add_sq]
    have h1 : (Q : ℝ) < (sh P : ℝ) + 1 := by linarith [(abs_lt.mp hlt).2]
    have h2 : (sh P : ℝ) < (Q : ℝ) + 1 := by linarith [(abs_lt.mp hlt).1]
    have h1' : Q < sh P + 1 := by exact_mod_cast h1
    have h2' : sh P < Q + 1 := by exact_mod_cast h2
    omega
  constructor
  · rw [E_eq φ phi_pow P, hφ, hQ]
  · rw [E_eq ψ psi_pow P, hψ, hQ]

/-- `n` is determined by its two embeddings. -/
lemma E_inj {x y : ℕ} (h1 : E φ x = E φ y) (h2 : E ψ x = E ψ y) : x = y := by
  rw [E_eq φ phi_pow x, E_eq φ phi_pow y] at h1
  rw [E_eq ψ psi_pow x, E_eq ψ psi_pow y] at h2
  have h : ((x : ℝ) - y) * (φ - ψ) = 0 := by linear_combination h1 - h2
  have hne : φ - ψ ≠ 0 := by rw [goldenRatio_sub_goldenConj]; positivity
  have h3 := (mul_eq_zero.mp h).resolve_right hne
  exact_mod_cast sub_eq_zero.mp h3

/-- **Theorem (Knuth 1988 for `t = 0`; all shifts).** The shifted Knuth product is associative. -/
theorem circ_assoc (t a b c : ℕ) : circ t (circ t a b) c = circ t a (circ t b c) := by
  apply E_inj
  · rw [(key t (circ t a b) c).1, (key t a b).1, (key t a (circ t b c)).1, (key t b c).1]; ring
  · rw [(key t (circ t a b) c).2, (key t a b).2, (key t a (circ t b c)).2, (key t b c).2]; ring

/-- The shifted Knuth product is commutative. -/
theorem circ_comm (t a b : ℕ) : circ t a b = circ t b a := by
  apply E_inj
  · rw [(key t a b).1, (key t b a).1]; ring
  · rw [(key t a b).2, (key t b a).2]; ring

end Infinity.C08

#print axioms Infinity.C08.window
#print axioms Infinity.C08.key
#print axioms Infinity.C08.circ_assoc
#print axioms Infinity.C08.circ_comm
