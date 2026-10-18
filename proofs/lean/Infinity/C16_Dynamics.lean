import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

/-!
# Cycle C16 — Fibonacci dynamics in finite magmas

For a binary operation `op : M → M → M` the recurrence `x_{k+1} = op x_k x_{k-1}` is the iteration of the
*pair map* `(a, b) ↦ (b, op b a)`.

* `pairMap_injective_iff` (CLM-C16-01): the pair map is injective iff every left translation `op b` is
  injective (the q-ary form of Golomb's nonsingularity criterion); `pairMap_bijective_iff` for finite `M`.
* `mirrorMap_eq` (CLM-C16-01): the mirror recurrence `x_{k+1} = op x_{k-1} x_k` is the forward recurrence
  of the opposite operation.
* `pairMap_fixed_iff` (CLM-C16-11): the fixed points of the pair map are exactly the pairs `(a, a)` with
  `op a a = a`.
* `top_two_cycle` (used for CLM-C16-15): if `t` is a left identity and a right absorbing element
  (as the top element of a Laver table), then `(t, c)` and `(c, t)` form a 2-cycle.
* `anchored_fibonacci` (CLM-C16-12): in the anchored associative magma `x * y = x + y + 1` on `ZMod N`,
  the shifted sequence `x_k + 1` satisfies the Fibonacci recurrence.
-/

namespace Infinity.C16

variable {M : Type*} (op : M → M → M)

/-- The pair map of the recurrence `x_{k+1} = op x_k x_{k-1}`: `(x_{k-1}, x_k) ↦ (x_k, x_{k+1})`. -/
def pairMap (p : M × M) : M × M := (p.2, op p.2 p.1)

/-- The pair map of the mirror recurrence `x_{k+1} = op x_{k-1} x_k`. -/
def mirrorMap (p : M × M) : M × M := (p.2, op p.1 p.2)

/-- **CLM-C16-01.** The pair map is injective iff every left translation `a ↦ op b a` is injective. -/
theorem pairMap_injective_iff :
    Function.Injective (pairMap op) ↔ ∀ b, Function.Injective (op b) := by
  constructor
  · intro h b a a' haa
    have : pairMap op (a, b) = pairMap op (a', b) := by
      simp [pairMap, haa]
    have := h this
    simpa using congrArg Prod.fst this
  · intro h p q hpq
    obtain ⟨a, b⟩ := p
    obtain ⟨a', b'⟩ := q
    simp only [pairMap, Prod.mk.injEq] at hpq
    obtain ⟨hb, hab⟩ := hpq
    subst hb
    have := h b hab
    simp [this]

/-- For finite `M`, the pair map is a permutation iff every left translation is a permutation. -/
theorem pairMap_bijective_iff [Finite M] :
    Function.Bijective (pairMap op) ↔ ∀ b, Function.Bijective (op b) := by
  constructor
  · intro h b
    exact Finite.injective_iff_bijective.mp ((pairMap_injective_iff op).mp h.1 b)
  · intro h
    exact Finite.injective_iff_bijective.mp
      ((pairMap_injective_iff op).mpr fun b => (h b).1)

/-- **CLM-C16-01.** The mirror recurrence is the forward recurrence of the opposite operation. -/
theorem mirrorMap_eq : mirrorMap op = pairMap (fun x y => op y x) := by
  funext p
  rfl

/-- **CLM-C16-11.** Fixed points of the pair map are exactly the idempotent diagonal pairs. -/
theorem pairMap_fixed_iff (a b : M) : pairMap op (a, b) = (a, b) ↔ a = b ∧ op a a = a := by
  simp only [pairMap, Prod.mk.injEq]
  constructor
  · rintro ⟨h1, h2⟩
    subst h1
    exact ⟨rfl, h2⟩
  · rintro ⟨h1, h2⟩
    subst h1
    exact ⟨rfl, h2⟩

/-- If `t` is a left identity (`op t y = y`) and right absorbing (`op x t = t`), the pairs `(t, c)` and
`(c, t)` are exchanged by the pair map (the 2-cycles of the Laver tables, CLM-C16-15). -/
theorem top_two_cycle (t : M) (hl : ∀ y, op t y = y) (hr : ∀ x, op x t = t) (c : M) :
    pairMap op (t, c) = (c, t) ∧ pairMap op (c, t) = (t, c) := by
  simp [pairMap, hl, hr]

/-- **CLM-C16-12.** In the anchored associative magma `x * y = x + y + 1` on `ZMod N`, every solution of
`x_{k+2} = x_{k+1} * x_k` is a shifted Fibonacci sequence: `y_k = x_k + 1` satisfies `y_{k+2} = y_{k+1} + y_k`. -/
theorem anchored_fibonacci {N : ℕ} (s : ℕ → ZMod N) (h : ∀ k, s (k + 2) = s (k + 1) + s k + 1) :
    ∀ k, s (k + 2) + 1 = (s (k + 1) + 1) + (s k + 1) := by
  intro k
  rw [h k]
  ring

end Infinity.C16

#print axioms Infinity.C16.pairMap_injective_iff
#print axioms Infinity.C16.pairMap_bijective_iff
#print axioms Infinity.C16.mirrorMap_eq
#print axioms Infinity.C16.pairMap_fixed_iff
#print axioms Infinity.C16.top_two_cycle
#print axioms Infinity.C16.anchored_fibonacci
