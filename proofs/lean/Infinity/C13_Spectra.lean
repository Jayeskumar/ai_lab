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
* `translation_form` (core of CLM-C13-02): if `x ⋆ σ(y) = x ⋆ y + 1` for some map `σ`, the anchored operation is
  `x ⋆ y = x + 1 + κ(y)` with `κ` a bijection fixing 0.
* `linear_of_shift`: `κ(y + c) = κ(y) + 1` with `κ 0 = 0` forces `c` to be a unit and `κ` to be linear.
* `golden_law_models`, `golden_law_model_of_root` (C06 Theorem 6, CLM-C06-07): models of
  `(xy)z = x(y(zz))` ↔ roots of `a² + a = 1`.
* `T1`, `w_family_models`, `w_family_model_of_root` (CLM-C13-03): for every one-variable term `W`, the anchored
  models of `(xy)z = x(y W(z))` are exactly the affine tables `x + 1 + a·y` with `a · c_W(a) = 1`.
* `cube_law_no_two`, `cubeOp_model` (CLM-C13-05): `x = x(x(xx))` has anchored models of every size except 2,
  so anchored spectra are not always closed under divisors.
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
    rw [ih w y, law13_shift op anchor law (w - 2 * k) (y - 2 * k)]
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
  have hd : N ∣ 3 * h - 2 * h := Nat.dvd_sub h3' (by rw [hN])
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
  · -- odd N = 2h + 1: use k = h + 1, for which 2k ≡ 1
    have hk := law13_iter op anchor law (h + 1) 0 1
    push_cast at hk
    have e2 : (2 : ZMod N) * ((h : ZMod N) + 1) = 1 := by
      have hn : 2 * (h + 1) = N + 1 := by omega
      have := congrArg (fun n : ℕ => (n : ZMod N)) hn
      push_cast at this
      rw [ZMod.natCast_self, zero_add] at this
      exact this
    have e3 : (1 : ZMod N) - 2 * ((h : ZMod N) + 1) = 0 := by rw [e2]; ring
    rw [e3, anchor] at hk
    have r01 : op 0 1 = 3 := by
      have := law13_rr op anchor law 0
      rw [anchor] at this
      simpa using this
    rw [r01] at hk
    have hK : (h : ZMod N) + 1 = 2 := by linear_combination -hk
    have h3 : (3 : ZMod N) = 0 := by linear_combination -2 * hK + e2
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
    ∀ x _y _z : ZMod 2, x + 1 = ((x + 1) + 1) + 1 := by
  decide

section Rigidity

variable {N : ℕ} [NeZero N]

/-- **Translation form (core of CLM-C13-02).** If some map `σ` satisfies `x ⋆ σ(y) = x ⋆ y + 1`, every anchored
operation is a translation table `x ⋆ y = x + 1 + κ(y)` with `κ` a bijection fixing `0`. -/
theorem translation_form (op : ZMod N → ZMod N → ZMod N) (anchor : ∀ x, op x 0 = x + 1)
    (σ : ZMod N → ZMod N) (hσ : ∀ x y, op x (σ y) = op x y + 1) :
    ∃ κ : ZMod N → ZMod N, κ 0 = 0 ∧ Function.Bijective κ ∧ ∀ x y, op x y = x + 1 + κ y := by
  have iter : ∀ (k : ℕ) x, op x (σ^[k] 0) = x + 1 + k := by
    intro k
    induction k with
    | zero => intro x; simp [anchor]
    | succ k ih =>
      intro x
      rw [Function.iterate_succ_apply', hσ, ih]; push_cast; ring
  let f : ZMod N → ZMod N := fun k => σ^[k.val] 0
  have hf : ∀ x k, op x (f k) = x + 1 + k := by
    intro x k
    have := iter k.val x
    rwa [ZMod.natCast_zmod_val] at this
  have finj : Function.Injective f := by
    intro k k' h
    have h1 := hf 0 k
    have h2 := hf 0 k'
    rw [h] at h1
    rw [h1] at h2
    linear_combination h2
  have fbij : Function.Bijective f := (Finite.injective_iff_bijective).mp finj
  let e := Equiv.ofBijective f fbij
  refine ⟨e.symm, ?_, e.symm.bijective, ?_⟩
  · have : f 0 = 0 := by simp [f]
    rw [Equiv.symm_apply_eq]
    exact this.symm
  · intro x y
    have := hf x (e.symm y)
    have hy : f (e.symm y) = y := e.apply_symm_apply y
    rw [hy] at this
    exact this

/-- **CLM-C13-02 (Theorem 2), machine-checked.** For any binary function `V` (in particular any term in `y, z`), every
anchored model of `(x ⋆ y) ⋆ z = x ⋆ V(y, z)` is a translation table `x ⋆ y = x + 1 + κ(y)`. -/
theorem right_normed_translation (op : ZMod N → ZMod N → ZMod N) (anchor : ∀ x, op x 0 = x + 1)
    (V : ZMod N → ZMod N → ZMod N) (law : ∀ x y z, op (op x y) z = op x (V y z)) :
    ∃ κ : ZMod N → ZMod N, κ 0 = 0 ∧ Function.Bijective κ ∧ ∀ x y, op x y = x + 1 + κ y := by
  apply translation_form op anchor (fun y => V y 0)
  intro x y
  have := law x y 0
  rw [anchor] at this
  exact this.symm

/-- **Linearity (core of CLM-C13-03).** If `κ 0 = 0` and `κ (y + c) = κ y + 1` for all `y`, then `c` is a unit and
`κ y = a * y` with `a * c = 1`. -/
theorem linear_of_shift (κ : ZMod N → ZMod N) (h0 : κ 0 = 0) (c : ZMod N)
    (hc : ∀ y, κ (y + c) = κ y + 1) : ∃ a : ZMod N, a * c = 1 ∧ ∀ y, κ y = a * y := by
  have hnat : ∀ j : ℕ, κ ((j : ZMod N) * c) = j := by
    intro j
    induction j with
    | zero => simp [h0]
    | succ j ih =>
      have := hc ((j : ZMod N) * c)
      rw [ih] at this
      push_cast
      rw [add_mul, one_mul, this]
  have ht : ∀ t : ZMod N, κ (t * c) = t := by
    intro t
    have := hnat t.val
    rwa [ZMod.natCast_zmod_val] at this
  have inj : Function.Injective (fun t : ZMod N => t * c) := by
    intro t t' h
    have := congrArg κ h
    simp only at this
    rwa [ht, ht] at this
  obtain ⟨a, ha⟩ := (Finite.injective_iff_surjective.mp inj) 1
  have ha' : a * c = 1 := ha
  refine ⟨a, ha', fun y => ?_⟩
  have : y = (a * y) * c := by
    calc y = y * (a * c) := by rw [ha', mul_one]
      _ = (a * y) * c := by ring
  conv_lhs => rw [this]
  exact ht (a * y)

/-- **The golden law (C06 Theorem 6, CLM-C06-07), machine-checked.** The anchored models of
`(x ⋆ y) ⋆ z = x ⋆ (y ⋆ (z ⋆ z))` are exactly the tables `x ⋆ y = x + 1 + a·y` with `a² + a = 1`. -/
theorem golden_law_models (op : ZMod N → ZMod N → ZMod N) (anchor : ∀ x, op x 0 = x + 1)
    (law : ∀ x y z, op (op x y) z = op x (op y (op z z))) :
    ∃ a : ZMod N, a ^ 2 + a = 1 ∧ ∀ x y, op x y = x + 1 + a * y := by
  -- z = 0 gives x ⋆ (y ⋆ 1) = x ⋆ y + 1
  have hσ : ∀ x y, op x (op y 1) = op x y + 1 := by
    intro x y
    have := law x y 0
    rw [anchor, anchor] at this
    simpa using this.symm
  obtain ⟨κ, hκ0, -, hform⟩ := translation_form op anchor (fun y => op y 1) hσ
  -- the law in terms of κ
  have hlaw : ∀ y z, κ (y + 1 + κ (z + 1 + κ z)) = κ y + κ z + 1 := by
    intro y z
    have := law 0 y z
    rw [hform 0 y, hform (0 + 1 + κ y) z, hform y (op z z), hform z z, hform 0] at this
    linear_combination -this
  -- z = 0: κ (y + c) = κ y + 1 with c = 1 + κ 1
  have hshift : ∀ y, κ (y + (1 + κ 1)) = κ y + 1 := by
    intro y
    have := hlaw y 0
    rw [hκ0] at this
    simpa [add_assoc] using this
  obtain ⟨a, hac, hlin⟩ := linear_of_shift κ hκ0 (1 + κ 1) hshift
  have hk1 : κ 1 = a := by rw [hlin]; ring
  refine ⟨a, ?_, fun x y => by rw [hform, hlin]⟩
  rw [hk1] at hac
  linear_combination hac

omit [NeZero N] in
/-- Converse: every root `a` of `a² + a = 1` gives an anchored model of the golden law. -/
theorem golden_law_model_of_root (a : ZMod N) (ha : a ^ 2 + a = 1) :
    ∀ x y z : ZMod N, (x + 1 + a * y) + 1 + a * z =
      x + 1 + a * (y + 1 + a * (z + 1 + a * z)) := by
  intro x y z
  linear_combination (-(1 + a * z)) * ha

/-! ### The W-family (CLM-C13-03) -/

/-- Binary trees with all leaves labelled by the single variable `z`. -/
inductive T1 where
  | leaf : T1
  | node : T1 → T1 → T1

namespace T1

/-- Value of the one-variable term at `z` in the magma `op`. -/
def eval {N : ℕ} (op : ZMod N → ZMod N → ZMod N) (z : ZMod N) : T1 → ZMod N
  | leaf => z
  | node u v => op (u.eval op z) (v.eval op z)

/-- `c_W(a) = Σ_leaves a^(right depth)`. -/
def cpoly {N : ℕ} (a : ZMod N) : T1 → ZMod N
  | leaf => 1
  | node u v => u.cpoly a + a * v.cpoly a

/-- The constant term `d_W(a)` of the affine evaluation. -/
def dpoly {N : ℕ} (a : ZMod N) : T1 → ZMod N
  | leaf => 0
  | node u v => u.dpoly a + a * v.dpoly a + 1

theorem eval_affine {N : ℕ} (a : ZMod N) (W : T1) (z : ZMod N) :
    W.eval (fun x y => x + 1 + a * y) z = W.cpoly a * z + W.dpoly a := by
  induction W with
  | leaf => simp [eval, cpoly, dpoly]
  | node u v ihu ihv => simp only [eval, cpoly, dpoly, ihu, ihv]; ring

theorem cpoly_eq {N : ℕ} (a : ZMod N) (W : T1) : W.cpoly a = a * W.dpoly a + 1 := by
  induction W with
  | leaf => simp [cpoly, dpoly]
  | node u v ihu ihv => simp only [cpoly, dpoly, ihu, ihv]; ring

end T1

/-- **CLM-C13-03 (Theorem 3), machine-checked.** For every one-variable term `W`, every anchored model of
`(x ⋆ y) ⋆ z = x ⋆ (y ⋆ W(z))` is affine, `x ⋆ y = x + 1 + a·y`, with `a · c_W(a) = 1`. -/
theorem w_family_models (W : T1) (op : ZMod N → ZMod N → ZMod N) (anchor : ∀ x, op x 0 = x + 1)
    (law : ∀ x y z, op (op x y) z = op x (op y (W.eval op z))) :
    ∃ a : ZMod N, a * W.cpoly a = 1 ∧ ∀ x y, op x y = x + 1 + a * y := by
  set w0 := W.eval op 0 with hw0
  have hσ : ∀ x y, op x (op y w0) = op x y + 1 := by
    intro x y
    have := law x y 0
    rw [anchor] at this
    exact this.symm
  obtain ⟨κ, hκ0, -, hform⟩ := translation_form op anchor (fun y => op y w0) hσ
  have hshift : ∀ y, κ (y + (1 + κ w0)) = κ y + 1 := by
    intro y
    have := law 0 y 0
    rw [hform (op 0 y) 0, hform 0 y, hform y w0, hform 0 (y + 1 + κ w0), hκ0] at this
    rw [show y + (1 + κ w0) = y + 1 + κ w0 by ring]
    linear_combination -this
  obtain ⟨a, hac, hlin⟩ := linear_of_shift κ hκ0 (1 + κ w0) hshift
  have haff : ∀ x y, op x y = x + 1 + a * y := fun x y => by rw [hform, hlin]
  have hop : op = fun x y => x + 1 + a * y := by funext x y; exact haff x y
  refine ⟨a, ?_, haff⟩
  have h00 := law 0 0 0
  rw [hop] at h00
  simp only at h00
  rw [T1.eval_affine] at h00
  rw [T1.cpoly_eq]
  linear_combination -h00

/-- Converse of `w_family_models`: every `a` with `a · c_W(a) = 1` gives an anchored model. -/
theorem w_family_model_of_root {N : ℕ} (W : T1) (a : ZMod N) (ha : a * W.cpoly a = 1) :
    ∀ x y z : ZMod N, (x + 1 + a * y) + 1 + a * z =
      x + 1 + a * (y + 1 + a * W.eval (fun u v => u + 1 + a * v) z) := by
  intro x y z
  rw [T1.eval_affine]
  have hc := T1.cpoly_eq a W
  linear_combination (-1 - a * z) * ha + a * hc

end Rigidity

/-! ### A spectrum that is not closed under divisors (CLM-C13-05) -/

/-- **CLM-C13-05 (no model of size 2).** No anchored operation on `ZMod 2` satisfies `x = x ⋆ (x ⋆ (x ⋆ x))`. -/
theorem cube_law_no_two (op : ZMod 2 → ZMod 2 → ZMod 2) (anchor : ∀ x, op x 0 = x + 1) :
    ¬ ∀ x, op x (op x (op x x)) = x := by
  intro law
  have h0 := law 0
  have a0 : op 0 0 = 1 := by rw [anchor]; rfl
  rw [a0] at h0
  have : ∀ v : ZMod 2, v = 0 ∨ v = 1 := by decide
  rcases this (op 0 1) with h | h
  · rw [h, a0] at h0; exact absurd h0 (by decide)
  · rw [h, h] at h0; exact absurd h0 (by decide)

/-- The explicit model used for every size `N ≥ 3`. -/
def cubeOp {N : ℕ} (x y : ZMod N) : ZMod N :=
  if y = 0 then x + 1 else if x = 0 then (if y = 1 then 2 else 0) else (if y = x then x else 0)

/-- **CLM-C13-05 (models of every size N ≥ 3).** `cubeOp` is anchored and satisfies `x = x ⋆ (x ⋆ (x ⋆ x))`.
Together with `cube_law_no_two` the anchored spectrum of this law is `ℕ ∖ {2}`: it contains 4 but not 2. -/
theorem cubeOp_model {N : ℕ} (hN : 3 ≤ N) :
    (∀ x : ZMod N, cubeOp x 0 = x + 1) ∧ ∀ x : ZMod N, cubeOp x (cubeOp x (cubeOp x x)) = x := by
  haveI : NeZero N := ⟨by omega⟩
  have h1 : (1 : ZMod N) ≠ 0 := by
    intro h
    have := (ZMod.natCast_eq_zero_iff 1 N).mp (by exact_mod_cast h)
    have := Nat.le_of_dvd (by norm_num) this
    omega
  have h2 : (2 : ZMod N) ≠ 0 := by
    intro h
    have := (ZMod.natCast_eq_zero_iff 2 N).mp (by exact_mod_cast h)
    have := Nat.le_of_dvd (by norm_num) this
    omega
  have h21 : (2 : ZMod N) ≠ 1 := by
    intro h
    have h' : (1 : ZMod N) = 0 := by linear_combination h
    exact h1 h'
  refine ⟨fun x => by simp [cubeOp], fun x => ?_⟩
  by_cases hx : x = 0
  · subst hx
    simp [cubeOp, h1, h2, h21]
  · simp [cubeOp, hx]

end Infinity.C13

#print axioms Infinity.C13.law13_size_dvd_three
#print axioms Infinity.C13.law13_model_three
#print axioms Infinity.C13.law12_size_dvd_two
#print axioms Infinity.C13.law12_model_two
#print axioms Infinity.C13.translation_form
#print axioms Infinity.C13.linear_of_shift
#print axioms Infinity.C13.golden_law_models
#print axioms Infinity.C13.golden_law_model_of_root
#print axioms Infinity.C13.w_family_models
#print axioms Infinity.C13.w_family_model_of_root
#print axioms Infinity.C13.right_normed_translation
#print axioms Infinity.C13.cube_law_no_two
#print axioms Infinity.C13.cubeOp_model
