import Mathlib.Tactic

/-!
# Cycle C18 — e-transformations of quasigroups

`eT op l u` is Markovski's e-transformation of the list `u` with leader `l`:
`b₀ = l * a₀`, `bᵢ = bᵢ₋₁ * aᵢ`.

* `eT_length`: it preserves length.
* `eT_injective` (CLM-C18-01): if every left translation `y ↦ x * y` is injective (left cancellation), then
  `eT op l` is injective — an e-transformation never creates collisions among strings.
* `eT_ne_of_ne` (CLM-C18-02): with right cancellation, two runs started in different states over the same input
  differ at every position — a difference, once created, persists to the end of the string.
* `eT_append`, `eT_tail_factors` (CLM-C18-03, the tail-information bound): the outputs on a suffix `s` depend on the
  prefix `p` only through the single state reached after `p`; so for a fixed suffix there are at most `|α|`
  possible tails.
-/

namespace Infinity.C18

variable {α : Type*} (op : α → α → α)

/-- The e-transformation with leader `l`. -/
def eT : α → List α → List α
  | _, [] => []
  | l, a :: as => op l a :: eT (op l a) as

/-- The state after processing a list (the last output, or the leader for the empty list). -/
def st (l : α) (p : List α) : α := p.foldl op l

@[simp] theorem eT_nil (l : α) : eT op l [] = [] := rfl

@[simp] theorem eT_cons (l a : α) (as : List α) : eT op l (a :: as) = op l a :: eT op (op l a) as := rfl

theorem eT_length (l : α) (u : List α) : (eT op l u).length = u.length := by
  induction u generalizing l with
  | nil => rfl
  | cons a as ih => simp [ih]

/-- **CLM-C18-01.** Left cancellation makes every e-transformation injective. -/
theorem eT_injective (hl : ∀ x, Function.Injective (op x)) (l : α) : Function.Injective (eT op l) := by
  intro u v h
  induction u generalizing l v with
  | nil =>
    cases v with
    | nil => rfl
    | cons b bs => simp at h
  | cons a as ih =>
    cases v with
    | nil => simp at h
    | cons b bs =>
      simp only [eT_cons, List.cons.injEq] at h
      obtain ⟨h1, h2⟩ := h
      have hab : a = b := hl l h1
      subst hab
      rw [ih (op l a) h2]

/-- **CLM-C18-02.** With right cancellation, runs from different states over the same input differ everywhere. -/
theorem eT_ne_of_ne (hr : ∀ y, Function.Injective (fun x => op x y)) :
    ∀ (s : List α) (b b' : α), b ≠ b' →
      ∀ i (h : i < s.length), (eT op b s)[i]'(by rw [eT_length]; exact h) ≠
        (eT op b' s)[i]'(by rw [eT_length]; exact h) := by
  intro s
  induction s with
  | nil => intro b b' _ i h; simp at h
  | cons c cs ih =>
    intro b b' hbb i hi
    have hne : op b c ≠ op b' c := fun e => hbb (hr c e)
    cases i with
    | zero => simpa using hne
    | succ j =>
      have hj : j < cs.length := by simpa using hi
      simpa using ih (op b c) (op b' c) hne j hj

/-- Splitting the input splits the output, with the state after the prefix as the new leader. -/
theorem eT_append (l : α) (p s : List α) : eT op l (p ++ s) = eT op l p ++ eT op (st op l p) s := by
  induction p generalizing l with
  | nil => rfl
  | cons a as ih => simp [st, ih (op l a)]

/-- **CLM-C18-03 (tail-information bound).** For a fixed suffix `s`, the outputs on `s` are a function of the
single state reached after the prefix: at most `|α|` different tails, whatever the prefix. -/
theorem eT_tail_factors (l : α) (s : List α) :
    ∀ p : List α, (eT op l (p ++ s)).drop p.length = eT op (st op l p) s := by
  intro p
  rw [eT_append]
  have : (eT op l p).length = p.length := eT_length op l p
  rw [← this, List.drop_left]

end Infinity.C18

#print axioms Infinity.C18.eT_length
#print axioms Infinity.C18.eT_injective
#print axioms Infinity.C18.eT_ne_of_ne
#print axioms Infinity.C18.eT_append
#print axioms Infinity.C18.eT_tail_factors
