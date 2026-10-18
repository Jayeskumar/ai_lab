import Mathlib.Logic.Relation
import Mathlib.Data.List.Count
import Mathlib.Tactic

/-!
# Cycle C04 — Derivation lengths, random descent and rewriting games

* `random_descent` (CLM-C04-05, abstract part): if every local peak `b ← a → c` of a relation is
  joinable by two derivations of the *same* length, then whenever `a` reaches a normal form `b`
  in `n` steps, every derivation from `a` has length `≤ n` and every derivation from `a` to a
  normal form has length exactly `n` and ends in `b` (van Oostrom's local criterion for random
  descent).
* `steps_length_unique` (CLM-C04-06, abstract part): a potential that changes by the same nonzero
  amount at every step forces all derivations between two given objects to have equal length.
* `inv_step`, `normal_iff_inv_zero`, `derivation_length_eq_inv`, `p_positions` (CLM-C04-04 and
  CLM-C04-08 for the rule `ab → ba`, encoded on `List Bool` with `a = true`, `b = false`): every
  step lowers the inversion count by exactly one, normal forms are the words without inversions,
  every complete derivation has exactly `inv w` steps, and in the rewriting game the
  P-positions (previous player wins) are exactly the words with an even inversion count.
-/

namespace Infinity.C04

section Abstract

variable {α : Type*} (R : α → α → Prop)

/-- `Steps R n a b`: `b` is reached from `a` in exactly `n` steps of `R`. -/
inductive Steps : ℕ → α → α → Prop
  | refl (a : α) : Steps 0 a a
  | cons {n : ℕ} {a b c : α} : R a b → Steps n b c → Steps (n + 1) a c

/-- `a` is a normal form: no step is possible. -/
def Normal (a : α) : Prop := ∀ b, ¬ R a b

/-- Local random descent: every local peak is joinable by derivations of equal length. -/
def LocalRD : Prop := ∀ a b c, R a b → R a c → ∃ d k, Steps R k b d ∧ Steps R k c d

variable {R}

theorem Steps.append {n m : ℕ} {a b c : α} (h1 : Steps R n a b) (h2 : Steps R m b c) :
    Steps R (n + m) a c := by
  induction h1 with
  | refl _ => simpa using h2
  | @cons k _ _ _ hab _ ih =>
    have := Steps.cons hab (ih h2)
    rwa [show k + 1 + m = k + m + 1 by omega]

theorem Steps.zero_eq {a b : α} (h : Steps R 0 a b) : a = b := by
  cases h
  rfl

/-- If all derivations from `a` are bounded, `a` reaches a normal form. -/
theorem exists_normal_of_bounded :
    ∀ (N : ℕ) (a : α), (∀ m c, Steps R m a c → m ≤ N) → ∃ k e, Steps R k a e ∧ Normal R e := by
  intro N
  induction N with
  | zero =>
    intro a hb
    refine ⟨0, a, Steps.refl a, fun b hab => ?_⟩
    have := hb 1 b (Steps.cons hab (Steps.refl b))
    omega
  | succ N ih =>
    intro a hb
    by_cases hn : Normal R a
    · exact ⟨0, a, Steps.refl a, hn⟩
    · simp only [Normal, not_forall, not_not] at hn
      obtain ⟨b, hab⟩ := hn
      obtain ⟨k, e, hk, he⟩ := ih b (fun m c hm => by
        have := hb (m + 1) c (Steps.cons hab hm); omega)
      exact ⟨k + 1, e, Steps.cons hab hk, he⟩

/-- **Random descent from the local criterion** (abstract part of CLM-C04-05). -/
theorem random_descent (hR : LocalRD R) :
    ∀ (n : ℕ) (a b : α), Steps R n a b → Normal R b →
      (∀ m c, Steps R m a c → m ≤ n) ∧ (∀ m c, Steps R m a c → Normal R c → m = n ∧ c = b) := by
  intro n
  induction n with
  | zero =>
    intro a b hab hb
    have hab' := hab.zero_eq
    subst hab'
    refine ⟨fun m c hm => ?_, fun m c hm _ => ?_⟩
    · cases hm with
      | refl => exact le_refl 0
      | cons h1 _ => exact absurd h1 (hb _)
    · cases hm with
      | refl => exact ⟨rfl, rfl⟩
      | cons h1 _ => exact absurd h1 (hb _)
  | succ n ih =>
    intro a b hab hb
    obtain ⟨a1, ha1, h1b⟩ : ∃ a1, R a a1 ∧ Steps R n a1 b := by
      cases hab with
      | cons h1 h2 => exact ⟨_, h1, h2⟩
    obtain ⟨B1, U1⟩ := ih a1 b h1b hb
    -- every one-step successor `a2` of `a` also reaches `b` in exactly `n` steps
    have key : ∀ a2, R a a2 → Steps R n a2 b := by
      intro a2 ha2
      obtain ⟨d, k, hd1, hd2⟩ := hR a a1 a2 ha1 ha2
      have bound : ∀ m c, Steps R m d c → m ≤ n - k := by
        intro m c hm
        have := B1 (k + m) c (hd1.append hm)
        omega
      obtain ⟨j, e, hj, he⟩ := exists_normal_of_bounded (n - k) d bound
      obtain ⟨hlen, heq⟩ := U1 (k + j) e (hd1.append hj) he
      subst heq
      have := hd2.append hj
      rwa [hlen] at this
    refine ⟨fun m c hm => ?_, fun m c hm hc => ?_⟩
    · cases hm with
      | refl => omega
      | cons h1 h2 =>
        have := (ih _ b (key _ h1) hb).1 _ c h2
        omega
    · cases hm with
      | refl => exact absurd ha1 (hc _)
      | cons h1 h2 =>
        obtain ⟨hm, hcb⟩ := (ih _ b (key _ h1) hb).2 _ c h2 hc
        exact ⟨by omega, hcb⟩

/-- A potential that changes by `δ` at every step changes by `n δ` along `n` steps. -/
theorem potential_steps (Φ : α → ℤ) (δ : ℤ) (hΦ : ∀ a b, R a b → Φ b = Φ a + δ)
    {n : ℕ} {a b : α} (h : Steps R n a b) : Φ b = Φ a + n * δ := by
  induction h with
  | refl _ => simp
  | cons hab _ ih =>
    rw [ih, hΦ _ _ hab]
    push_cast
    ring

/-- **All derivations between two given objects have the same length** if some potential changes
by the same nonzero amount at every step (abstract part of CLM-C04-06). -/
theorem steps_length_unique (Φ : α → ℤ) (δ : ℤ) (hδ : δ ≠ 0)
    (hΦ : ∀ a b, R a b → Φ b = Φ a + δ) {n m : ℕ} {a b : α}
    (h1 : Steps R n a b) (h2 : Steps R m a b) : n = m := by
  have e1 := potential_steps Φ δ hΦ h1
  have e2 := potential_steps Φ δ hΦ h2
  have : (n : ℤ) * δ = m * δ := by linarith
  exact_mod_cast mul_right_cancel₀ hδ this

end Abstract

section Swap

/-- One step of `ab → ba` on words over `{a, b}` (`a = true`, `b = false`). -/
def SwapStep (u v : List Bool) : Prop :=
  ∃ x y : List Bool, u = x ++ true :: false :: y ∧ v = x ++ false :: true :: y

/-- Number of inversions: pairs `a … b` (an `a` before a `b`). -/
def inv : List Bool → ℕ
  | [] => 0
  | true :: w => w.count false + inv w
  | false :: w => inv w

theorem inv_middle (x y : List Bool) :
    inv (x ++ true :: false :: y) = inv (x ++ false :: true :: y) + 1 := by
  induction x with
  | nil => simp [inv]; omega
  | cons c x ih =>
    cases c with
    | false => simpa [inv] using ih
    | true =>
      simp only [List.cons_append, inv, List.count_append, List.count_cons] at ih ⊢
      simp at ih ⊢
      omega

/-- **Every step of `ab → ba` lowers the inversion count by exactly one.** -/
theorem inv_step {u v : List Bool} (h : SwapStep u v) : inv u = inv v + 1 := by
  obtain ⟨x, y, rfl, rfl⟩ := h
  exact inv_middle x y

theorem swapStep_cons (c : Bool) {u v : List Bool} (h : SwapStep u v) :
    SwapStep (c :: u) (c :: v) := by
  obtain ⟨x, y, rfl, rfl⟩ := h
  exact ⟨c :: x, y, rfl, rfl⟩

theorem exists_step_of_inv_ne_zero : ∀ u : List Bool, inv u ≠ 0 → ∃ v, SwapStep u v
  | [], h => absurd rfl h
  | false :: w, h => by
    obtain ⟨v, hv⟩ := exists_step_of_inv_ne_zero w (by simpa [inv] using h)
    exact ⟨_, swapStep_cons false hv⟩
  | true :: [], h => absurd (by simp [inv]) h
  | true :: false :: w, _ => ⟨false :: true :: w, [], w, rfl, rfl⟩
  | true :: true :: w, h => by
    by_cases hw : inv (true :: w) = 0
    · exfalso
      simp only [inv, List.count_cons] at h hw
      simp at h hw
      omega
    · obtain ⟨v, hv⟩ := exists_step_of_inv_ne_zero (true :: w) hw
      exact ⟨_, swapStep_cons true hv⟩

/-- Normal forms of `ab → ba` are exactly the words without inversions. -/
theorem normal_iff_inv_zero (u : List Bool) : Normal SwapStep u ↔ inv u = 0 := by
  constructor
  · intro hn
    by_contra h
    obtain ⟨v, hv⟩ := exists_step_of_inv_ne_zero u h
    exact hn v hv
  · intro h v hv
    have := inv_step hv
    omega

/-- **Every complete derivation of `ab → ba` from `u` has exactly `inv u` steps.** -/
theorem derivation_length_eq_inv {n : ℕ} {u v : List Bool} (h : Steps SwapStep n u v)
    (hv : Normal SwapStep v) : n = inv u := by
  have e := potential_steps (fun w => (inv w : ℤ)) (-1)
    (fun a b hab => by have := inv_step hab; omega) h
  have h0 := (normal_iff_inv_zero v).1 hv
  simp only [h0, Nat.cast_zero] at e
  omega

/-- **P-positions of the rewriting game of `ab → ba`.** The words with an even inversion count
form the kernel of the game graph: every move from such a word leads to an odd count, and from
every odd count some move leads back to an even count; terminal words have count `0`. Since the
game terminates, this kernel is exactly the set of P-positions. -/
theorem p_positions :
    (∀ u v, SwapStep u v → Even (inv u) → ¬ Even (inv v)) ∧
    (∀ u, ¬ Even (inv u) → ∃ v, SwapStep u v ∧ Even (inv v)) := by
  constructor
  · intro u v h hu hv
    have := inv_step h
    rw [this] at hu
    exact (Nat.even_add_one.mp hu) hv
  · intro u hu
    have hne : inv u ≠ 0 := by rintro h; rw [h] at hu; exact hu ⟨0, rfl⟩
    obtain ⟨v, hv⟩ := exists_step_of_inv_ne_zero u hne
    refine ⟨v, hv, ?_⟩
    have := inv_step hv
    rw [this] at hu
    by_contra hve
    exact hu (Nat.even_add_one.mpr hve)

end Swap

section OneRule

variable {σ : Type*}

/-- One step of the single rule `l → r` on words over `σ`. -/
def RuleStep (l r : List σ) (u v : List σ) : Prop :=
  ∃ x y : List σ, u = x ++ l ++ y ∧ v = x ++ r ++ y

/-- `l` is unbordered: no nonempty proper suffix of `l` is also a prefix of `l`. -/
def Unbordered (l : List σ) : Prop :=
  ∀ p s t : List σ, l = p ++ s → l = s ++ t → p ≠ [] → s ≠ [] → False

/-- The case where the second redex starts `a` letters after the first one. -/
theorem overlap_case {l r : List σ} (hl : Unbordered l) (x y1 a y2 : List σ)
    (h : l ++ y1 = a ++ (l ++ y2)) :
    x ++ r ++ y1 = (x ++ a) ++ r ++ y2 ∨
      ∃ d, RuleStep l r (x ++ r ++ y1) d ∧ RuleStep l r ((x ++ a) ++ r ++ y2) d := by
  rcases List.append_eq_append_iff.mp h with ⟨e, he1, he2⟩ | ⟨c, hc1, hc2⟩
  · -- disjoint occurrences: a = l ++ e, y1 = e ++ l ++ y2
    subst he1 he2
    right
    exact ⟨x ++ r ++ e ++ r ++ y2, ⟨x ++ r ++ e, y2, by simp, by simp⟩, ⟨x, e ++ r ++ y2, by simp, by simp⟩⟩
  · -- overlapping occurrences: l = a ++ c and l ++ y2 = c ++ y1
    by_cases ha : a = []
    · subst ha
      simp only [List.nil_append] at hc1
      subst hc1
      have : y2 = y1 := List.append_cancel_left hc2
      subst this
      left
      simp
    by_cases hc : c = []
    · subst hc
      simp only [List.append_nil] at hc1
      subst hc1
      simp only [List.nil_append] at hc2
      subst hc2
      right
      exact ⟨x ++ r ++ r ++ y2, ⟨x ++ r, y2, by simp, by simp⟩, ⟨x, r ++ y2, by simp, by simp⟩⟩
    exfalso
    rcases List.append_eq_append_iff.mp hc2 with ⟨e, he1, _⟩ | ⟨t, ht1, _⟩
    · -- c = l ++ e is impossible: then |l| = |a| + |l| + |e| forces a = []
      have hlen := congrArg List.length hc1
      rw [he1] at hlen
      simp only [List.length_append] at hlen
      exact ha (List.eq_nil_of_length_eq_zero (by omega))
    · exact hl a c t hc1 ht1 ha hc

/-- **Diamond lemma**: for an unbordered left-hand side, two different one-step reducts of the
same word have a common one-step reduct. -/
theorem unbordered_diamond {l r : List σ} (hl : Unbordered l) {u v1 v2 : List σ}
    (h1 : RuleStep l r u v1) (h2 : RuleStep l r u v2) :
    v1 = v2 ∨ ∃ d, RuleStep l r v1 d ∧ RuleStep l r v2 d := by
  obtain ⟨x1, y1, rfl, rfl⟩ := h1
  obtain ⟨x2, y2, hu, rfl⟩ := h2
  have hu' : x1 ++ (l ++ y1) = x2 ++ (l ++ y2) := by simpa [List.append_assoc] using hu
  rcases List.append_eq_append_iff.mp hu' with ⟨a, ha, hy⟩ | ⟨c, hc, hy⟩
  · subst ha
    exact overlap_case hl x1 y1 a y2 hy
  · subst hc
    rcases overlap_case hl x2 y2 c y1 hy with h | ⟨d, hd1, hd2⟩
    · exact Or.inl h.symm
    · exact Or.inr ⟨d, hd2, hd1⟩

theorem unbordered_localRD {l r : List σ} (hl : Unbordered l) : LocalRD (RuleStep l r) := by
  intro a b c hab hac
  rcases unbordered_diamond hl hab hac with h | ⟨d, h1, h2⟩
  · subst h
    exact ⟨b, 0, Steps.refl b, Steps.refl b⟩
  · exact ⟨d, 1, Steps.cons h1 (Steps.refl d), Steps.cons h2 (Steps.refl d)⟩

/-- **CLM-C04-05 (formal).** A one-rule string rewriting system with an unbordered left-hand side
has random descent: if `u` reaches a normal form `v` in `n` steps, every derivation from `u` has
at most `n` steps and every derivation from `u` to a normal form has exactly `n` steps and ends
in `v`. -/
theorem unbordered_random_descent {l r : List σ} (hl : Unbordered l) :
    ∀ n u v, Steps (RuleStep l r) n u v → Normal (RuleStep l r) v →
      (∀ m w, Steps (RuleStep l r) m u w → m ≤ n) ∧
      (∀ m w, Steps (RuleStep l r) m u w → Normal (RuleStep l r) w → m = n ∧ w = v) :=
  random_descent (unbordered_localRD hl)

theorem ruleStep_length {l r u v : List σ} (h : RuleStep l r u v) :
    (v.length : ℤ) = u.length + ((r.length : ℤ) - l.length) := by
  obtain ⟨x, y, rfl, rfl⟩ := h
  simp only [List.length_append]
  push_cast
  ring

/-- **CLM-C04-06, length-changing case (formal).** If `|l| ≠ |r|`, all derivations between two
given words have the same number of steps. -/
theorem length_changing_unique {l r : List σ} (hlr : l.length ≠ r.length) {n m : ℕ}
    {u v : List σ} (h1 : Steps (RuleStep l r) n u v) (h2 : Steps (RuleStep l r) m u v) : n = m :=
  steps_length_unique (fun w => (w.length : ℤ)) ((r.length : ℤ) - l.length) (by omega)
    (fun _ _ h => ruleStep_length h) h1 h2

end OneRule

end Infinity.C04

#print axioms Infinity.C04.random_descent
#print axioms Infinity.C04.steps_length_unique
#print axioms Infinity.C04.inv_step
#print axioms Infinity.C04.normal_iff_inv_zero
#print axioms Infinity.C04.derivation_length_eq_inv
#print axioms Infinity.C04.p_positions
#print axioms Infinity.C04.unbordered_diamond
#print axioms Infinity.C04.unbordered_random_descent
#print axioms Infinity.C04.length_changing_unique
