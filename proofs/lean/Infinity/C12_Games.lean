import Mathlib.Data.Set.Basic
import Mathlib.Data.Nat.ModEq
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Tactic

/-!
# Cycle C12 — Relational one-heap games: Grundy functions by characterisation

A Grundy function is characterised by the *mex equations*: `g n` is the least natural number
not among the values of `g` on the options of `n`. We formalise this characterisation and
prove closed forms by exhibiting functions that satisfy it.

* `IsGrundy.unique`: Grundy functions are unique when every option is smaller.
* `residue_grundy` (CLM-C12-06): if no element of the move set `S` is divisible by `q` and
  `1, …, q-1 ∈ S`, the subtraction game `S` has Grundy function `n % q`.
* `power_of_two_grundy` (CLM-C12-06): subtract-a-power-of-2 has Grundy function `n % 3`.
* `split_parity` (CLM-C12-07): in any take-and-break game in which a heap splits into two
  nonempty heaps, and every heap `n ≥ 2` has at least one allowed split, `g n = (n+1) % 2`
  for `n ≥ 1` (value 1 for even heaps, 0 for odd heaps).
* `g03_P_positions` (CLM-C12-03): in the game "subtract a divisor `d` of `n` with
  `1 < d < n`", the P-positions (Grundy value 0) are exactly `0`, the odd numbers and the
  powers `2^(2j+1)`.
-/

namespace Infinity.C12

/-- `v` is the minimum excluded value of `A`. -/
def IsMex (A : Set ℕ) (v : ℕ) : Prop := v ∉ A ∧ ∀ w < v, w ∈ A

theorem IsMex.unique {A : Set ℕ} {v w : ℕ} (hv : IsMex A v) (hw : IsMex A w) : v = w := by
  rcases lt_trichotomy v w with h | h | h
  · exact absurd (hw.2 v h) hv.1
  · exact h
  · exact absurd (hv.2 w h) hw.1

/-- `g` satisfies the mex equations of the one-heap game with options `opts`. -/
def IsGrundy (opts : ℕ → Set ℕ) (g : ℕ → ℕ) : Prop := ∀ n, IsMex (g '' opts n) (g n)

/-- Uniqueness of Grundy functions for well-founded (decreasing) option relations. -/
theorem IsGrundy.unique {opts : ℕ → Set ℕ} (hwf : ∀ n, ∀ m ∈ opts n, m < n) {g h : ℕ → ℕ}
    (hg : IsGrundy opts g) (hh : IsGrundy opts h) : g = h := by
  funext n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    have himg : g '' opts n = h '' opts n := by
      ext v
      constructor
      · rintro ⟨m, hm, rfl⟩
        exact ⟨m, hm, (ih m (hwf n m hm)).symm⟩
      · rintro ⟨m, hm, rfl⟩
        exact ⟨m, hm, ih m (hwf n m hm)⟩
    exact (hg n).unique (by rw [himg]; exact hh n)

/-! ### Subtraction games -/

/-- Options of the subtraction game with move set `S`. -/
def subOpts (S : Set ℕ) (n : ℕ) : Set ℕ := {m | ∃ s ∈ S, s ≤ n ∧ m = n - s}

theorem subOpts_lt {S : Set ℕ} (hS : ∀ s ∈ S, 0 < s) (n : ℕ) : ∀ m ∈ subOpts S n, m < n := by
  rintro m ⟨s, hs, hsn, rfl⟩
  have := hS s hs
  omega

/-- **Residue lemma.** If `q > 0`, no move is divisible by `q`, and every `1 ≤ r < q` is a
move, then `n % q` satisfies the mex equations of the subtraction game. -/
theorem residue_grundy (q : ℕ) (hq : 0 < q) (S : Set ℕ)
    (hS0 : ∀ s ∈ S, s % q ≠ 0) (hS1 : ∀ r, 1 ≤ r → r < q → r ∈ S) :
    IsGrundy (subOpts S) (fun n => n % q) := by
  intro n
  constructor
  · rintro ⟨m, ⟨s, hs, hsn, rfl⟩, heq⟩
    apply hS0 s hs
    -- (n - s) ≡ n [MOD q] forces q ∣ s
    have h1 : (n - s) ≡ n [MOD q] := heq
    have h2 : (n - s) + s ≡ n + s [MOD q] := Nat.ModEq.add_right s h1
    rw [Nat.sub_add_cancel hsn] at h2
    have h3 : n + 0 ≡ n + s [MOD q] := by simpa using h2
    have h4 : 0 ≡ s [MOD q] := Nat.ModEq.add_left_cancel' n h3
    exact (Nat.modEq_zero_iff_dvd.mp h4.symm) |> Nat.mod_eq_zero_of_dvd
  · intro w hw
    have hw' : w < n % q := hw
    have hr : n % q < q := Nat.mod_lt n hq
    have hle : n % q ≤ n := Nat.mod_le n q
    have hdm := Nat.div_add_mod n q
    refine ⟨n - (n % q - w), ⟨n % q - w, hS1 _ (by omega) (by omega), by omega, rfl⟩, ?_⟩
    show (n - (n % q - w)) % q = w
    have e : n - (n % q - w) = w + q * (n / q) := by omega
    rw [e, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt (by omega)]

/-- The move set "powers of two". -/
def powersOfTwo : Set ℕ := {s | ∃ i : ℕ, s = 2 ^ i}

/-- **Subtract-a-power-of-two.** Every Grundy function of this game is `n % 3`. -/
theorem power_of_two_grundy (g : ℕ → ℕ) (hg : IsGrundy (subOpts powersOfTwo) g) :
    ∀ n, g n = n % 3 := by
  have hpos : ∀ s ∈ powersOfTwo, 0 < s := by
    rintro s ⟨i, rfl⟩
    exact pow_pos (by norm_num) i
  have hres : IsGrundy (subOpts powersOfTwo) (fun n => n % 3) := by
    apply residue_grundy 3 (by norm_num)
    · rintro s ⟨i, rfl⟩ h
      have h3 : 3 ∣ 2 ^ i := Nat.dvd_of_mod_eq_zero h
      have : 3 ∣ 2 := Nat.prime_three.dvd_of_dvd_pow h3
      omega
    · intro r h1 h2
      interval_cases r
      · exact ⟨0, by norm_num⟩
      · exact ⟨1, by norm_num⟩
  intro n
  exact congrFun (IsGrundy.unique (subOpts_lt hpos) hg hres) n

/-! ### Splitting (take-and-break) games -/

/-- Option values of the splitting game: `g a ^^^ g b` for allowed splits `a + b = n`. -/
def splitVals (allowed : ℕ → ℕ → Prop) (g : ℕ → ℕ) (n : ℕ) : Set ℕ :=
  {v | ∃ a b, 1 ≤ a ∧ 1 ≤ b ∧ a + b = n ∧ allowed a b ∧ v = g a ^^^ g b}

/-- **Splitting parity theorem.** If every heap `n ≥ 2` has an allowed split into two
nonempty heaps, any Grundy function of the splitting game equals `(n + 1) % 2` on `n ≥ 1`. -/
theorem split_parity (allowed : ℕ → ℕ → Prop)
    (hall : ∀ n, 2 ≤ n → ∃ a b, 1 ≤ a ∧ 1 ≤ b ∧ a + b = n ∧ allowed a b)
    (g : ℕ → ℕ) (hg : ∀ n, IsMex (splitVals allowed g n) (g n)) :
    ∀ n, 1 ≤ n → g n = (n + 1) % 2 := by
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro hn
    -- every option value equals the parity value of n
    have hopt : ∀ v ∈ splitVals allowed g n, v = n % 2 := by
      rintro v ⟨a, b, ha, hb, hab, -, rfl⟩
      rw [ih a (by omega) ha, ih b (by omega) hb]
      rcases Nat.mod_two_eq_zero_or_one a with h | h <;>
        rcases Nat.mod_two_eq_zero_or_one b with h' | h' <;>
        · have : n % 2 = (a + b) % 2 := by rw [hab]
          rw [Nat.add_mod] at this
          have e1 : (a + 1) % 2 = 1 - a % 2 := by omega
          have e2 : (b + 1) % 2 = 1 - b % 2 := by omega
          rw [e1, e2, h, h'] at *
          simp_all
    by_cases h1 : n = 1
    · subst h1
      have hempty : ∀ v, v ∉ splitVals allowed g 1 := by
        rintro v ⟨a, b, ha, hb, hab, -⟩
        omega
      have hm : IsMex (splitVals allowed g 1) 0 := ⟨hempty 0, fun w hw => absurd hw (by omega)⟩
      rw [(hg 1).unique hm]
    · obtain ⟨a, b, ha, hb, hab, hallow⟩ := hall n (by omega)
      have hmem : g a ^^^ g b ∈ splitVals allowed g n := ⟨a, b, ha, hb, hab, hallow, rfl⟩
      have hval : g a ^^^ g b = n % 2 := hopt _ hmem
      have hm : IsMex (splitVals allowed g n) ((n + 1) % 2) := by
        constructor
        · intro hin
          have := hopt _ hin
          omega
        · intro w hw
          have : w = n % 2 := by omega
          rw [this, ← hval]
          exact hmem
      exact (hg n).unique hm

/-! ### P-positions -/

/-- `P` is the set of P-positions (the player to move loses) of the game with options `opts`. -/
def IsPSet (opts : ℕ → Set ℕ) (P : Set ℕ) : Prop := ∀ n, n ∈ P ↔ ∀ m ∈ opts n, m ∉ P

theorem IsPSet.unique {opts : ℕ → Set ℕ} (hwf : ∀ n, ∀ m ∈ opts n, m < n) {P Q : Set ℕ}
    (hP : IsPSet opts P) (hQ : IsPSet opts Q) : P = Q := by
  ext n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    rw [hP n, hQ n]
    constructor
    · intro h m hm hmQ
      exact h m hm ((ih m (hwf n m hm)).mpr hmQ)
    · intro h m hm hmP
      exact h m hm ((ih m (hwf n m hm)).mp hmP)

/-- The zero set of a Grundy function is the set of P-positions. -/
theorem IsGrundy.zero_pset {opts : ℕ → Set ℕ} {g : ℕ → ℕ} (hg : IsGrundy opts g) :
    IsPSet opts {n | g n = 0} := by
  intro n
  simp only [Set.mem_ofPred_eq]
  constructor
  · intro h0 m hm hm0
    exact (hg n).1 ⟨m, hm, by rw [hm0, h0]⟩
  · intro h
    by_contra hne
    obtain ⟨m, hm, hm0⟩ := (hg n).2 0 (Nat.pos_of_ne_zero hne)
    exact h m hm hm0

/-! ### G03: subtract a non-trivial proper divisor -/

/-- Options of G03: subtract a divisor `d` of `n` with `1 < d < n`. -/
def g03Opts (n : ℕ) : Set ℕ := {m | ∃ d, d ∣ n ∧ 1 < d ∧ d < n ∧ m = n - d}

/-- Candidate P-positions of G03: `0`, the odd numbers and the powers `2^(2j+1)`. -/
def g03P : Set ℕ := {n | n = 0 ∨ n % 2 = 1 ∨ ∃ j, n = 2 ^ (2 * j + 1)}

theorem g03_lt : ∀ n, ∀ m ∈ g03Opts n, m < n := by
  rintro n m ⟨d, -, hd1, hdn, rfl⟩
  omega

lemma odd_dvd_two_pow {d k : ℕ} (hd : d ∣ 2 ^ k) (hodd : d % 2 = 1) : d = 1 :=
  (Nat.Coprime.pow_right k (Nat.coprime_two_right.mpr (Nat.odd_iff.mpr hodd))).eq_one_of_dvd hd

lemma not_two_pow_add_two_pow_lt {a b c : ℕ} (hlt : a < b) (h : 2 ^ a + 2 ^ b = 2 ^ c) : False := by
  have hfac : 2 ^ a * (1 + 2 ^ (b - a)) = 2 ^ c := by
    rw [mul_add, mul_one, ← pow_add, Nat.add_sub_cancel' hlt.le]
    exact h
  have hdvd : (1 + 2 ^ (b - a)) ∣ 2 ^ c := ⟨2 ^ a, by rw [← hfac]; ring⟩
  have h2 : 2 ∣ 2 ^ (b - a) := dvd_pow_self 2 (by omega)
  have hodd : (1 + 2 ^ (b - a)) % 2 = 1 := by omega
  have h1 := odd_dvd_two_pow hdvd hodd
  have : 0 < 2 ^ (b - a) := pow_pos (by norm_num) _
  omega

lemma two_pow_add_two_pow {a b c : ℕ} (h : 2 ^ a + 2 ^ b = 2 ^ c) : a = b := by
  rcases lt_trichotomy a b with hab | hab | hab
  · exact (not_two_pow_add_two_pow_lt hab h).elim
  · exact hab
  · exact (not_two_pow_add_two_pow_lt hab (by rw [add_comm]; exact h)).elim

lemma g03_odd_no_P_option {n m : ℕ} (hodd : n % 2 = 1) (hm : m ∈ g03Opts n) : m ∉ g03P := by
  obtain ⟨d, hdn, hd1, hdlt, rfl⟩ := hm
  have hdodd : d % 2 = 1 := by
    by_contra h
    have h2d : 2 ∣ d := by omega
    have : 2 ∣ n := dvd_trans h2d hdn
    omega
  rintro (h0 | hodd' | ⟨j, hj⟩)
  · omega
  · omega
  · have hsub : d ∣ n - d := Nat.dvd_sub hdn (dvd_refl d)
    rw [hj] at hsub
    have := odd_dvd_two_pow hsub hdodd
    omega

lemma g03_pow_no_P_option {j m : ℕ} (hm : m ∈ g03Opts (2 ^ (2 * j + 1))) : m ∉ g03P := by
  obtain ⟨d, hdn, hd1, hdlt, rfl⟩ := hm
  obtain ⟨i, hi, rfl⟩ := (Nat.dvd_prime_pow Nat.prime_two).mp hdn
  have hi1 : 1 ≤ i := by
    rcases Nat.eq_zero_or_pos i with h | h
    · subst h; simp at hd1
    · exact h
  have h2i : 2 ∣ 2 ^ i := dvd_pow_self 2 (by omega)
  have h2n : 2 ∣ 2 ^ (2 * j + 1) := dvd_pow_self 2 (by omega)
  rintro (h0 | hodd | ⟨j', hj'⟩)
  · omega
  · omega
  · have hsum : 2 ^ i + 2 ^ (2 * j' + 1) = 2 ^ (2 * j + 1) := by omega
    have hij := two_pow_add_two_pow hsum
    subst hij
    have h2 : 2 ^ (2 * j' + 1 + 1) = 2 ^ (2 * j + 1) := by rw [pow_succ]; omega
    have := Nat.pow_right_injective (le_refl 2) h2
    omega

lemma g03_even_has_P_option {n : ℕ} (hn0 : n ≠ 0) (hev : n % 2 = 0)
    (hnot : ¬ ∃ j, n = 2 ^ (2 * j + 1)) : ∃ m ∈ g03Opts n, m ∈ g03P := by
  obtain ⟨a, m, hm, hnm⟩ := Nat.exists_eq_two_pow_mul_odd hn0
  have hm1 : m % 2 = 1 := Nat.odd_iff.mp hm
  have ha : 1 ≤ a := by
    rcases Nat.eq_zero_or_pos a with h | h
    · subst h
      simp at hnm
      omega
    · exact h
  have hpa : 2 ≤ 2 ^ a := by
    calc 2 = 2 ^ 1 := by norm_num
      _ ≤ 2 ^ a := Nat.pow_le_pow_right (by norm_num) ha
  by_cases hmone : m = 1
  · subst hmone
    rw [mul_one] at hnm
    have ha_even : a % 2 = 0 := by
      by_contra hodd
      exact hnot ⟨a / 2, by rw [hnm]; congr 1; omega⟩
    obtain ⟨e, he⟩ : ∃ e, a = e + 1 := ⟨a - 1, by omega⟩
    have hpow : 2 ^ a = 2 * 2 ^ e := by rw [he, pow_succ]; ring
    have hpe : 1 ≤ 2 ^ e := Nat.one_le_two_pow
    refine ⟨2 ^ e, ⟨2 ^ e, ?_, ?_, ?_, ?_⟩, Or.inr (Or.inr ⟨e / 2, ?_⟩)⟩
    · rw [hnm, hpow]; exact dvd_mul_left _ _
    · have he1 : 1 ≤ e := by omega
      have : 2 ≤ 2 ^ e := by
        calc 2 = 2 ^ 1 := by norm_num
          _ ≤ 2 ^ e := Nat.pow_le_pow_right (by norm_num) he1
      omega
    · omega
    · omega
    · congr 1; omega
  · have hm3 : 3 ≤ m := by omega
    refine ⟨n - m, ⟨m, ?_, by omega, ?_, rfl⟩, Or.inr (Or.inl ?_)⟩
    · rw [hnm]; exact dvd_mul_left _ _
    · rw [hnm]; nlinarith
    · have hodd : Odd ((2 ^ a - 1) * m) := by
        apply Nat.odd_mul.mpr
        refine ⟨Nat.odd_iff.mpr ?_, hm⟩
        have : 2 ∣ 2 ^ a := dvd_pow_self 2 (by omega)
        omega
      rw [Nat.sub_one_mul, ← hnm] at hodd
      exact Nat.odd_iff.mp hodd

/-- The P-positions of G03 are exactly `0`, the odd numbers and the powers `2^(2j+1)`. -/
theorem g03_pset : IsPSet g03Opts g03P := by
  intro n
  constructor
  · intro hn m hm hmP
    rcases hn with h0 | hodd | ⟨j, rfl⟩
    · obtain ⟨d, -, -, hd, -⟩ := hm
      omega
    · exact g03_odd_no_P_option hodd hm hmP
    · exact g03_pow_no_P_option hm hmP
  · intro h
    by_contra hnP
    simp only [g03P, Set.mem_ofPred_eq, not_or] at hnP
    obtain ⟨hn0, hnodd, hnpow⟩ := hnP
    obtain ⟨m, hm, hmP⟩ := g03_even_has_P_option hn0 (by omega) hnpow
    exact h m hm hmP

/-- **CLM-C12-03.** For every Grundy function of G03, `g n = 0` iff `n = 0`, `n` is odd, or
`n = 2^(2j+1)`. -/
theorem g03_P_positions (g : ℕ → ℕ) (hg : IsGrundy g03Opts g) (n : ℕ) :
    g n = 0 ↔ (n = 0 ∨ n % 2 = 1 ∨ ∃ j, n = 2 ^ (2 * j + 1)) := by
  have h : {n | g n = 0} = g03P := IsPSet.unique g03_lt hg.zero_pset g03_pset
  exact Set.ext_iff.mp h n

end Infinity.C12

#print axioms Infinity.C12.IsGrundy.unique
#print axioms Infinity.C12.residue_grundy
#print axioms Infinity.C12.power_of_two_grundy
#print axioms Infinity.C12.split_parity
#print axioms Infinity.C12.g03_P_positions
