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


section Frontier

/-! Models establishing spectrum memberships beyond those stated in the ETP notes
(EXP-C05-03/04); each law check is decided by the kernel. -/

/-- A model of ETP law 467, `x = y(x(x(yy)))`, of order 9 (SAT, EXP-C05-03/04). -/
def E467_order9 : Fin 9 → Fin 9 → Fin 9 := fun a b => ![![1, 6, 2, 8, 0, 3, 4, 5, 7], ![5, 2, 0, 4, 6, 1, 7, 3, 8], ![6, 7, 8, 5, 4, 0, 3, 2, 1], ![2, 8, 4, 3, 7, 6, 1, 0, 5], ![4, 3, 1, 6, 5, 8, 2, 7, 0], ![8, 5, 3, 0, 1, 7, 6, 4, 2], ![7, 1, 5, 2, 3, 4, 0, 8, 6], ![0, 4, 7, 1, 8, 2, 5, 6, 3], ![3, 0, 6, 7, 2, 5, 8, 1, 4]] a b

theorem E467_order9_law : ∀ x y : Fin 9, (E467_order9 y (E467_order9 x (E467_order9 x (E467_order9 y y)))) = x := by decide

/-- A model of ETP law 677, `x = y(x((yx)y))`, of order 5 (SAT, EXP-C05-03/04). -/
def E677_order5 : Fin 5 → Fin 5 → Fin 5 := fun a b => ![![0, 3, 4, 1, 2], ![4, 1, 3, 2, 0], ![1, 0, 2, 4, 3], ![2, 4, 0, 3, 1], ![3, 2, 1, 0, 4]] a b

theorem E677_order5_law : ∀ x y : Fin 5, (E677_order5 y (E677_order5 x (E677_order5 (E677_order5 y x) y))) = x := by decide

/-- A model of ETP law 677, `x = y(x((yx)y))`, of order 7 (SAT, EXP-C05-03/04). -/
def E677_order7 : Fin 7 → Fin 7 → Fin 7 := fun a b => ![![0, 1, 2, 3, 4, 5, 6], ![6, 2, 3, 4, 5, 0, 1], ![4, 0, 6, 1, 2, 3, 5], ![1, 3, 4, 5, 0, 6, 2], ![5, 6, 1, 2, 3, 4, 0], ![2, 4, 5, 0, 6, 1, 3], ![3, 5, 0, 6, 1, 2, 4]] a b

theorem E677_order7_law : ∀ x y : Fin 7, (E677_order7 y (E677_order7 x (E677_order7 (E677_order7 y x) y))) = x := by decide

/-- A model of ETP law 677, `x = y(x((yx)y))`, of order 9 (SAT, EXP-C05-03/04). -/
def E677_order9 : Fin 9 → Fin 9 → Fin 9 := fun a b => ![![1, 3, 0, 8, 5, 7, 6, 2, 4], ![7, 5, 1, 6, 4, 0, 2, 8, 3], ![8, 7, 2, 4, 0, 6, 3, 5, 1], ![5, 8, 3, 0, 6, 4, 1, 7, 2], ![3, 2, 4, 7, 8, 5, 0, 1, 6], ![4, 6, 5, 1, 2, 3, 7, 0, 8], ![2, 1, 6, 5, 7, 8, 4, 3, 0], ![0, 4, 7, 2, 3, 1, 8, 6, 5], ![6, 0, 8, 3, 1, 2, 5, 4, 7]] a b

theorem E677_order9_law : ∀ x y : Fin 9, (E677_order9 y (E677_order9 x (E677_order9 (E677_order9 y x) y))) = x := by decide

/-- A model of ETP law 883, `x = y((xy)(yy))`, of order 10 (SAT, EXP-C05-03/04). -/
def E883_order10 : Fin 10 → Fin 10 → Fin 10 := fun a b => ![![0, 8, 1, 4, 6, 3, 5, 2, 7, 9], ![3, 7, 5, 0, 8, 2, 9, 1, 4, 6], ![5, 3, 8, 7, 0, 9, 1, 6, 2, 4], ![2, 4, 9, 6, 7, 1, 3, 5, 0, 8], ![1, 9, 6, 2, 5, 4, 8, 0, 3, 7], ![7, 0, 3, 8, 4, 5, 2, 9, 6, 1], ![8, 5, 0, 3, 1, 7, 6, 4, 9, 2], ![6, 1, 4, 9, 2, 8, 0, 7, 5, 3], ![4, 6, 2, 1, 9, 0, 7, 3, 8, 5], ![9, 2, 7, 5, 3, 6, 4, 8, 1, 0]] a b

theorem E883_order10_law : ∀ x y : Fin 10, (E883_order10 y (E883_order10 (E883_order10 x y) (E883_order10 y y))) = x := by decide

/-- A model of ETP law 1286, `x = y(((xy)x)y)`, of order 9 (SAT, EXP-C05-03/04). -/
def E1286_order9 : Fin 9 → Fin 9 → Fin 9 := fun a b => ![![0, 2, 8, 7, 3, 1, 4, 5, 6], ![6, 1, 4, 2, 8, 7, 3, 0, 5], ![4, 5, 2, 6, 7, 0, 1, 8, 3], ![1, 8, 5, 3, 6, 4, 0, 2, 7], ![5, 7, 3, 1, 4, 2, 8, 6, 0], ![8, 6, 7, 0, 1, 5, 2, 3, 4], ![7, 4, 0, 8, 5, 3, 6, 1, 2], ![2, 3, 6, 4, 0, 8, 5, 7, 1], ![3, 0, 1, 5, 2, 6, 7, 4, 8]] a b

theorem E1286_order9_law : ∀ x y : Fin 9, (E1286_order9 y (E1286_order9 (E1286_order9 (E1286_order9 x y) x) y)) = x := by decide

/-- A model of ETP law 1313, `x = y(((yx)x)y)`, of order 9 (SAT, EXP-C05-03/04). -/
def E1313_order9 : Fin 9 → Fin 9 → Fin 9 := fun a b => ![![1, 7, 6, 4, 8, 2, 5, 0, 3], ![3, 4, 0, 2, 6, 7, 1, 8, 5], ![0, 1, 2, 3, 4, 5, 6, 7, 8], ![7, 0, 5, 8, 3, 6, 2, 1, 4], ![4, 8, 1, 6, 5, 0, 7, 3, 2], ![6, 5, 4, 1, 7, 3, 8, 2, 0], ![8, 3, 7, 5, 2, 1, 0, 4, 6], ![5, 2, 8, 7, 0, 4, 3, 6, 1], ![2, 6, 3, 0, 1, 8, 4, 5, 7]] a b

theorem E1313_order9_law : ∀ x y : Fin 9, (E1313_order9 y (E1313_order9 (E1313_order9 (E1313_order9 y x) x) y)) = x := by decide

/-- A model of ETP law 1516, `x = (yy)(x(xy))`, of order 9 (SAT, EXP-C05-03/04). -/
def E1516_order9 : Fin 9 → Fin 9 → Fin 9 := fun a b => ![![1, 3, 0, 4, 6, 5, 8, 2, 7], ![4, 5, 1, 0, 2, 7, 6, 8, 3], ![8, 0, 2, 6, 7, 1, 5, 3, 4], ![5, 2, 3, 7, 4, 8, 1, 0, 6], ![0, 7, 4, 1, 8, 3, 2, 6, 5], ![7, 8, 5, 3, 0, 6, 4, 1, 2], ![2, 4, 6, 8, 5, 0, 3, 7, 1], ![3, 6, 7, 5, 1, 2, 0, 4, 8], ![6, 1, 8, 2, 3, 4, 7, 5, 0]] a b

theorem E1516_order9_law : ∀ x y : Fin 9, (E1516_order9 (E1516_order9 y y) (E1516_order9 x (E1516_order9 x y))) = x := by decide

/-- A model of ETP law 1719, `x = (yy)((xx)y)`, of order 10 (SAT, EXP-C05-03/04). -/
def E1719_order10 : Fin 10 → Fin 10 → Fin 10 := fun a b => ![![0, 9, 1, 8, 2, 4, 6, 3, 5, 7], ![1, 7, 2, 9, 4, 8, 5, 0, 6, 3], ![6, 1, 5, 2, 3, 9, 0, 7, 4, 8], ![3, 8, 7, 4, 6, 0, 9, 2, 1, 5], ![7, 3, 6, 1, 8, 2, 4, 5, 0, 9], ![4, 0, 9, 5, 1, 6, 3, 8, 7, 2], ![8, 5, 3, 7, 0, 1, 2, 4, 9, 6], ![2, 6, 4, 3, 7, 5, 1, 9, 8, 0], ![5, 2, 0, 6, 9, 7, 8, 1, 3, 4], ![9, 4, 8, 0, 5, 3, 7, 6, 2, 1]] a b

theorem E1719_order10_law : ∀ x y : Fin 10, (E1719_order10 (E1719_order10 y y) (E1719_order10 (E1719_order10 x x) y)) = x := by decide

end Frontier

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
#print axioms Infinity.C05.E467_order9_law
#print axioms Infinity.C05.E677_order5_law
#print axioms Infinity.C05.E677_order7_law
#print axioms Infinity.C05.E677_order9_law
#print axioms Infinity.C05.E883_order10_law
#print axioms Infinity.C05.E1286_order9_law
#print axioms Infinity.C05.E1313_order9_law
#print axioms Infinity.C05.E1516_order9_law
#print axioms Infinity.C05.E1719_order10_law
