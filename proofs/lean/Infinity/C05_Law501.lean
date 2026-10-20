import Mathlib

/-!
# Cycle C05 — finite models of ETP law 501 have order `≡ 0, 1 (mod 4)`

ETP equation 501 is `x = y ◇ (y ◇ (x ◇ (x ◇ y)))`.

* `law501_card_mod_four` (CLM-C05-22, necessity half of Theorem 14 of proofs/paper/C05.md): every
  finite magma satisfying law 501 has order `n ≡ 0` or `1 (mod 4)`.
* `sign_prodComm` : for every finite type `α` of cardinality `n`, the coordinate swap
  `(x, y) ↦ (y, x)` of `α × α` has sign `(-1) ^ (n (n - 1) / 2)`.
* `E501_order4_law`, `E501_order5_law` : models of orders 4 and 5, certified by `decide`, so both
  residues are attained.

Proof of `law501_card_mod_four` (a sign argument on `α × α`). Put `x □ y := x ◇ (x ◇ y)`.

1. The law has the form `x = y ◇ t(x, y)`, so each left translation `L_y = (y ◇ ·)` is onto, hence a
   permutation of the finite carrier (`law501_left_bijective`). The left translation of `□` at `y` is
   the square `L_y * L_y`, so its sign is `1`.
2. The law says exactly that `□` is semi-symmetric (ETP law 14): `y □ (x □ y) = x` (`box_semisymm`).
   Hence also `(x □ y) □ x = y` (`box_semisymm'`: apply law 14 at `(y, x □ y)`). So the right
   translation `R_y = (· □ y)` is a permutation with inverse `(y □ ·) = L_y * L_y` (`boxRight_inv`),
   and `sign R_y = 1` (`sign_boxRight`).
3. `Φ (x, y) = (y, x □ y)` satisfies `Φ² (x, y) = (x □ y, x)` and `Φ³ = 1` (`phi_cube`), so
   `sign Φ = 1` (`sign_phi`).
4. `Φ = τ * P` (`phi_eq`) with `τ (x, y) = (y, x)` (`Equiv.prodComm`) and `P (x, y) = (R_y x, y)`
   (`Equiv.prodCongrLeft`). By `Equiv.Perm.sign_prodCongrLeft`, `sign P = ∏ y, sign R_y = 1`, hence
   `sign τ = 1` (`sign_prodComm_eq_one`).
5. `τ` is an involution whose fixed points are the `n` diagonal pairs (`fixedPointsProdCommEquiv`), so
   `Equiv.Perm.sign_of_pow_two_eq_one` gives `sign τ = (-1) ^ ((n * n - n) / 2)` (`sign_prodComm`).
   Hence `(n * n - n) / 2` is even, i.e. `n ≡ 0, 1 (mod 4)` (`mod_four_of_even_half`).
-/

namespace Infinity.C05

section Law501

variable {α : Type*}

/-- ETP equation 501: `x = y ◇ (y ◇ (x ◇ (x ◇ y)))`. -/
def Law501 (op : α → α → α) : Prop := ∀ x y, op y (op y (op x (op x y))) = x

/-- The derived operation `x □ y = x ◇ (x ◇ y)`. -/
def box (op : α → α → α) (x y : α) : α := op x (op x y)

/-- Law 501 says that `□` is semi-symmetric (ETP law 14): `y □ (x □ y) = x`. -/
theorem box_semisymm {op : α → α → α} (h : Law501 op) (x y : α) : box op y (box op x y) = x :=
  h x y

/-- The companion identity of a semi-symmetric operation: `(x □ y) □ x = y`. -/
theorem box_semisymm' {op : α → α → α} (h : Law501 op) (x y : α) : box op (box op x y) x = y := by
  have h1 := box_semisymm h y (box op x y)
  rwa [box_semisymm h x y] at h1

/-- The right translation `R_y = (· □ y)` as a permutation; its inverse is `(y □ ·)`. -/
def boxRight {op : α → α → α} (h : Law501 op) (y : α) : Equiv.Perm α where
  toFun x := box op x y
  invFun x := box op y x
  left_inv x := box_semisymm h x y
  right_inv x := box_semisymm' h y x

/-- The map `Φ (x, y) = (y, x □ y)` on `α × α`. -/
def phiFun (op : α → α → α) (p : α × α) : α × α := (p.2, box op p.1 p.2)

theorem phiFun_three {op : α → α → α} (h : Law501 op) (p : α × α) :
    phiFun op (phiFun op (phiFun op p)) = p := by
  obtain ⟨x, y⟩ := p
  simp only [phiFun, box_semisymm h, box_semisymm' h]

/-- `Φ` as a permutation of `α × α`; its inverse is `Φ²`. -/
def phi {op : α → α → α} (h : Law501 op) : Equiv.Perm (α × α) where
  toFun := phiFun op
  invFun p := phiFun op (phiFun op p)
  left_inv := phiFun_three h
  right_inv := phiFun_three h

theorem phi_cube {op : α → α → α} (h : Law501 op) : phi h * phi h * phi h = 1 :=
  Equiv.ext (phiFun_three h)

/-- `Φ = τ * P` with `τ (x, y) = (y, x)` and `P (x, y) = (x □ y, y)`. -/
theorem phi_eq {op : α → α → α} (h : Law501 op) :
    phi h = (Equiv.prodComm α α : Equiv.Perm (α × α)) * Equiv.prodCongrLeft (boxRight h) :=
  Equiv.ext fun _ => rfl

end Law501

section LeftTranslations

variable {α : Type*} [Finite α]

/-- Each left translation `L_y = (y ◇ ·)` of a finite model of law 501 is a bijection. -/
theorem law501_left_bijective {op : α → α → α} (h : Law501 op) (y : α) :
    Function.Bijective (op y) := by
  have hsurj : Function.Surjective (op y) := fun x => ⟨_, h x y⟩
  exact ⟨Finite.injective_iff_surjective.mpr hsurj, hsurj⟩

/-- The left translation `L_y = (y ◇ ·)` as a permutation. -/
noncomputable def leftPerm {op : α → α → α} (h : Law501 op) (y : α) : Equiv.Perm α :=
  Equiv.ofBijective (op y) (law501_left_bijective h y)

/-- `R_y⁻¹ = (y □ ·) = L_y * L_y`. -/
theorem boxRight_inv {op : α → α → α} (h : Law501 op) (y : α) :
    (boxRight h y)⁻¹ = leftPerm h y * leftPerm h y :=
  Equiv.ext fun _ => rfl

end LeftTranslations

section Swap

variable (α : Type*)

theorem prodComm_sq : (Equiv.prodComm α α : Equiv.Perm (α × α)) ^ 2 = 1 :=
  Equiv.ext fun _ => rfl

/-- The fixed points of the coordinate swap `(x, y) ↦ (y, x)` are the diagonal pairs. -/
def fixedPointsProdCommEquiv :
    Function.fixedPoints (Equiv.prodComm α α : Equiv.Perm (α × α)) ≃ α where
  toFun p := p.1.1
  invFun x := ⟨(x, x), rfl⟩
  left_inv := by
    rintro ⟨⟨a, b⟩, hab⟩
    have hba : (b, a) = (a, b) := hab
    obtain rfl : b = a := congrArg Prod.fst hba
    rfl
  right_inv _ := rfl

variable [Fintype α] [DecidableEq α]

/-- The coordinate swap of `α × α` has sign `(-1) ^ (n (n - 1) / 2)`, where `n = |α|`. -/
theorem sign_prodComm :
    Equiv.Perm.sign (Equiv.prodComm α α : Equiv.Perm (α × α)) =
      (-1) ^ ((Fintype.card α * Fintype.card α - Fintype.card α) / 2) := by
  rw [Equiv.Perm.sign_of_pow_two_eq_one (prodComm_sq α), Fintype.card_prod,
    Fintype.card_congr (fixedPointsProdCommEquiv α)]

end Swap

/-- If `n (n - 1) / 2` is even then `n ≡ 0, 1 (mod 4)`. -/
theorem mod_four_of_even_half {n : ℕ} (h : Even ((n * n - n) / 2)) : n % 4 = 0 ∨ n % 4 = 1 := by
  obtain ⟨k, hk⟩ := h
  have hle : n ≤ n * n := Nat.le_mul_self n
  have hmod : n * n % 4 = (n % 4) * (n % 4) % 4 := Nat.mul_mod _ _ _
  have hlt : n % 4 < 4 := Nat.mod_lt _ (by norm_num)
  interval_cases hr : n % 4 <;> omega

section Sign

variable {α : Type*} [Fintype α] [DecidableEq α]

theorem sign_boxRight {op : α → α → α} (h : Law501 op) (y : α) :
    Equiv.Perm.sign (boxRight h y) = 1 := by
  rw [← Equiv.Perm.sign_inv, boxRight_inv h y, map_mul, Int.units_mul_self]

theorem sign_phi {op : α → α → α} (h : Law501 op) : Equiv.Perm.sign (phi h) = 1 := by
  have h3 := congrArg Equiv.Perm.sign (phi_cube h)
  rw [map_mul, map_mul, map_one] at h3
  rcases Int.units_eq_one_or (Equiv.Perm.sign (phi h)) with h1 | h1
  · exact h1
  · rw [h1] at h3
    exact absurd h3 (by decide)

/-- In a finite model of law 501 the coordinate swap of `α × α` is an even permutation. -/
theorem sign_prodComm_eq_one {op : α → α → α} (h : Law501 op) :
    Equiv.Perm.sign (Equiv.prodComm α α : Equiv.Perm (α × α)) = 1 := by
  have h1 := sign_phi h
  rw [phi_eq h, map_mul, Equiv.Perm.sign_prodCongrLeft] at h1
  simpa only [sign_boxRight h, Finset.prod_const_one, mul_one] using h1

/-- **CLM-C05-22 (necessity).** A finite magma satisfying `x = y ◇ (y ◇ (x ◇ (x ◇ y)))` (ETP law 501)
has order `≡ 0` or `1 (mod 4)`. -/
theorem law501_card_mod_four {op : α → α → α} (h : Law501 op) :
    Fintype.card α % 4 = 0 ∨ Fintype.card α % 4 = 1 := by
  have h1 := sign_prodComm_eq_one h
  rw [sign_prodComm, neg_one_pow_eq_one_iff_even (by decide)] at h1
  exact mod_four_of_even_half h1

-- The same statement with the law written out.
example (op : α → α → α) (h : ∀ x y, op y (op y (op x (op x y))) = x) :
    Fintype.card α % 4 = 0 ∨ Fintype.card α % 4 = 1 :=
  law501_card_mod_four h

end Sign

section Tables

/-- A 4-element model of law 501: `x ◇ y = ω² x + ω y` over `𝔽₄ = {0, 1, ω, ω²}`, with the elements
coded as `0, 1, 2, 3` (`ω = 2`, `ω² = 3`; addition is XOR of the 2-bit codes). -/
def E501_order4 : Fin 4 → Fin 4 → Fin 4 := fun a b =>
  ![![0, 2, 3, 1], ![3, 1, 0, 2], ![1, 3, 2, 0], ![2, 0, 1, 3]] a b

theorem E501_order4_law : Law501 E501_order4 := by
  unfold Law501
  decide

/-- A 5-element model of law 501: `x ◇ y = 3x + 2y` over `ZMod 5`. -/
theorem E501_order5_law : Law501 (fun x y : ZMod 5 => 3 * x + 2 * y) := by
  unfold Law501
  decide

end Tables

end Infinity.C05

#print axioms Infinity.C05.box_semisymm
#print axioms Infinity.C05.box_semisymm'
#print axioms Infinity.C05.phiFun_three
#print axioms Infinity.C05.phi_cube
#print axioms Infinity.C05.phi_eq
#print axioms Infinity.C05.law501_left_bijective
#print axioms Infinity.C05.boxRight_inv
#print axioms Infinity.C05.prodComm_sq
#print axioms Infinity.C05.sign_prodComm
#print axioms Infinity.C05.mod_four_of_even_half
#print axioms Infinity.C05.sign_boxRight
#print axioms Infinity.C05.sign_phi
#print axioms Infinity.C05.sign_prodComm_eq_one
#print axioms Infinity.C05.law501_card_mod_four
#print axioms Infinity.C05.E501_order4_law
#print axioms Infinity.C05.E501_order5_law
