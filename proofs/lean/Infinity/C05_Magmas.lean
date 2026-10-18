import Mathlib.Data.Sym.Card
import Mathlib.GroupTheory.Perm.Cycle.Type
import Mathlib.Tactic

/-!
# Cycle C05 — Spectra of single-identity magma varieties

* `law167_card_mod_four` (CLM-C05-04, necessity half): every finite magma satisfying
  `(y*x)*(x*y) = x` (ETP equation 167) has order `n ≡ 0, 1 (mod 4)`.
  Proof: `{x, y} ↦ {x*y, y*x}` is a fixed-point-free involution on the unordered pairs of
  distinct elements, so `n.choose 2` is even.
* `left_mul_bijective_of_law` : if a finite magma satisfies `x = y * s(x, y)` for some binary
  term operation `s`, every left translation is a bijection (rows of the Cayley table are
  permutations) — the implied constraint used soundly in EXP-C05-03.
* Small certified tables (by `decide`): models of law 167 of orders 4 and 5, and the absence
  of models of law 167 and of law 66 `x = y*(x*(y*y))` of order 2.
-/

namespace Infinity.C05

section Law167

variable {α : Type*} [Fintype α] [DecidableEq α]

/-- ETP equation 167: `x = (y*x)*(x*y)`. -/
def Law167 (op : α → α → α) : Prop := ∀ x y, op (op y x) (op x y) = x

/-- The induced map on unordered pairs, `{a, b} ↦ {a*b, b*a}`. -/
def pairMap (op : α → α → α) : Sym2 α → Sym2 α :=
  Sym2.lift ⟨fun a b => s(op a b, op b a), fun _ _ => Sym2.eq_swap⟩

omit [Fintype α] [DecidableEq α] in
theorem pairMap_mk (op : α → α → α) (a b : α) : pairMap op s(a, b) = s(op a b, op b a) := rfl

omit [Fintype α] [DecidableEq α] in
theorem pairMap_involutive {op : α → α → α} (h : Law167 op) : Function.Involutive (pairMap op) := by
  intro p
  induction p using Sym2.ind with
  | _ a b =>
    rw [pairMap_mk, pairMap_mk, h b a, h a b, Sym2.eq_swap]

omit [Fintype α] [DecidableEq α] in
theorem pairMap_not_diag {op : α → α → α} (h : Law167 op) {p : Sym2 α} (hp : ¬ p.IsDiag) :
    ¬ (pairMap op p).IsDiag := by
  intro hd
  apply hp
  have hinv := pairMap_involutive h p
  induction p using Sym2.ind with
  | _ a b =>
    rw [pairMap_mk] at hd hinv
    rw [Sym2.mk_isDiag_iff] at hd ⊢
    rw [hd, pairMap_mk, Sym2.eq_iff] at hinv
    rcases hinv with ⟨h1, h2⟩ | ⟨h1, h2⟩
    · exact h1.symm.trans h2
    · exact h2.symm.trans h1

omit [Fintype α] [DecidableEq α] in
theorem pairMap_no_fixed {op : α → α → α} (h : Law167 op) {p : Sym2 α} (hp : ¬ p.IsDiag) :
    pairMap op p ≠ p := by
  induction p using Sym2.ind with
  | _ a b =>
    rw [Sym2.mk_isDiag_iff] at hp
    rw [pairMap_mk, Ne, Sym2.eq_iff]
    rintro (⟨h1, h2⟩ | ⟨h1, h2⟩)
    · -- a*b = a and b*a = b: the law gives (b*a)*(a*b) = b*a = b, but it must be a
      have := h a b
      rw [h2, h1, h2] at this
      exact hp this.symm
    · -- a*b = b and b*a = a: the law gives (b*a)*(a*b) = a*b = b, but it must be a
      have := h a b
      rw [h2, h1, h1] at this
      exact hp this.symm

/-- The involution restricted to non-diagonal unordered pairs. -/
def offMap {op : α → α → α} (h : Law167 op) : Function.End { p : Sym2 α // ¬ p.IsDiag } :=
  fun p => ⟨pairMap op p.1, pairMap_not_diag h p.2⟩

theorem choose_two_even {op : α → α → α} (h : Law167 op) : (Fintype.card α).choose 2 % 2 = 0 := by
  have hsq : (offMap h) ^ 2 ^ 1 = 1 := by
    funext p
    apply Subtype.ext
    show pairMap op (pairMap op p.1) = p.1
    exact pairMap_involutive h p.1
  have : Fact (Nat.Prime 2) := ⟨Nat.prime_two⟩
  have hmod := Equiv.Perm.card_fixedPoints_modEq (p := 2) (n := 1) hsq
  have hempty : IsEmpty (Function.fixedPoints (offMap h)) :=
    ⟨fun ⟨p, hp⟩ => pairMap_no_fixed h p.2 (congrArg Subtype.val hp)⟩
  simp only [Fintype.card_eq_zero] at hmod
  rw [Sym2.card_subtype_not_diag] at hmod
  simpa [Nat.ModEq] using hmod

/-- **CLM-C05-04 (necessity).** A finite magma satisfying `(y*x)*(x*y) = x` has order
`≡ 0` or `1 (mod 4)`. -/
theorem law167_card_mod_four {op : α → α → α} (h : Law167 op) :
    Fintype.card α % 4 = 0 ∨ Fintype.card α % 4 = 1 := by
  have he := choose_two_even h
  set n := Fintype.card α
  rw [Nat.choose_two_right] at he
  have h4 : n * (n - 1) % 4 = 0 := by
    have h2 : 2 ∣ n * (n - 1) := (Nat.even_mul_pred_self n).two_dvd
    obtain ⟨k, hk⟩ := h2
    rw [hk, Nat.mul_div_cancel_left _ (by norm_num)] at he
    omega
  have hm : n * (n - 1) % 4 = (n % 4) * ((n - 1) % 4) % 4 := Nat.mul_mod _ _ _
  have hlt : n % 4 < 4 := Nat.mod_lt _ (by norm_num)
  rcases Nat.eq_zero_or_pos n with h0 | hpos
  · left; rw [h0]
  · have hsub : (n - 1) % 4 = (n % 4 + 3) % 4 := by omega
    rw [hsub] at hm
    interval_cases hr : n % 4 <;> simp_all

end Law167

section LeftTranslations

variable {α : Type*} [Finite α]

/-- If `x = y * s x y` holds identically in a finite magma, all left translations are
bijective (each row of the Cayley table is a permutation). -/
theorem left_mul_bijective_of_law (op : α → α → α) (s : α → α → α)
    (h : ∀ x y, op y (s x y) = x) (y : α) : Function.Bijective (op y) := by
  have hsurj : Function.Surjective (op y) := fun x => ⟨s x y, h x y⟩
  exact ⟨Finite.injective_iff_surjective.mpr hsurj, hsurj⟩

end LeftTranslations

section Tables

/-- A 4-element model of law 167, found by SAT (EXP-C05-01) and certified here. -/
def T4 : Fin 4 → Fin 4 → Fin 4 := fun a b =>
  ![![0, 3, 1, 0], ![0, 2, 2, 2], ![2, 0, 1, 3], ![1, 3, 1, 3]] a b

theorem T4_law167 : ∀ x y : Fin 4, T4 (T4 y x) (T4 x y) = x := by decide

/-- A 5-element model of law 167 (SAT, EXP-C05-01), certified. -/
def T5 : Fin 5 → Fin 5 → Fin 5 := fun a b =>
  ![![3, 2, 3, 2, 1], ![3, 2, 0, 0, 4], ![1, 3, 1, 1, 3], ![1, 2, 0, 0, 4], ![4, 0, 4, 2, 4]] a b

theorem T5_law167 : ∀ x y : Fin 5, T5 (T5 y x) (T5 x y) = x := by decide

/-- The 4-element model is not a quasigroup: row 1 repeats the value 2. -/
theorem T4_not_latin : T4 1 1 = T4 1 2 := by decide

/-- No 2-element magma satisfies law 167 (exhaustive over all 16 tables). -/
theorem no_law167_order2 : ∀ op : Fin 2 → Fin 2 → Fin 2, ¬ ∀ x y, op (op y x) (op x y) = x := by
  decide

/-- No 2-element magma satisfies ETP law 66, `x = y*(x*(y*y))` (Mendelsohn law). -/
theorem no_law66_order2 : ∀ op : Fin 2 → Fin 2 → Fin 2, ¬ ∀ x y, op y (op x (op y y)) = x := by
  decide


/-- NAND on `Fin 2` satisfies `x = (y*x)*(x*(y*y))`: an order-2 model (EXP-C05-05). -/
def nand2 : Fin 2 → Fin 2 → Fin 2 := fun a b => ![![1, 1], ![1, 0]] a b

theorem nand2_law : ∀ x y : Fin 2, nand2 (nand2 y x) (nand2 x (nand2 y y)) = x := by decide

/-- **CLM-C05-06 (refutation of H-C05-A at order 2).** No affine operation
`x*y = a x + b y + c` over `ZMod 2` satisfies `x = (y*x)*(x*(y*y))`. -/
theorem no_affine_model_mod2 : ∀ a b c : ZMod 2, ¬ ∀ x y : ZMod 2,
    a * (a * y + b * x + c) + b * (a * x + b * (a * y + b * y + c) + c) + c = x := by decide

end Tables

end Infinity.C05

#print axioms Infinity.C05.law167_card_mod_four
#print axioms Infinity.C05.left_mul_bijective_of_law
#print axioms Infinity.C05.T4_law167
#print axioms Infinity.C05.T5_law167
#print axioms Infinity.C05.T4_not_latin
#print axioms Infinity.C05.no_law167_order2
#print axioms Infinity.C05.no_law66_order2
#print axioms Infinity.C05.nand2_law
#print axioms Infinity.C05.no_affine_model_mod2
