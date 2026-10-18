import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Combinatorics.SimpleGraph.Maps
import Mathlib.Tactic

/-!
# Cycle C14 — the 256 local graph products

A *local product* of simple graphs decides adjacency of `(g, h)` and `(g', h')` from the pair of
relations `(rel G g g', rel H h h')`, each relation being `E` (equal), `A` (adjacent) or `N`
(distinct, non-adjacent).

* `rel_lprod`: the relation of two vertices of `G * H` is `phi S (rel G ..) (rel H ..)`.
* `assoc_iso` (CLM-C14-01, "if"): if `phi` is associative on relations, the canonical map
  `((g, h), k) ↦ (g, (h, k))` is a graph isomorphism `(G * H) * K ≃g G * (H * K)` for ALL graphs.
* `assoc_of_P3` (CLM-C14-01, "only if"): if the canonical map is an isomorphism for
  `G = H = K = P₃` (the path on three vertices), then `phi` is associative on relations.
* `assoc_codes`, `comm_assoc_codes` (CLM-C14-02): exactly 20 of the 256 products are associative,
  10 of them commutative (kernel computation with `decide`).
* `character_codes`, `xor_character` (CLM-C14-04, relation level): exactly six products admit a
  `{-1,0,1}`-valued multiplicative character `c (phi S r s) = c r * c s` with `c A ≠ c N`; for the
  symmetric-difference product it is `c = (1, -1, 1)` (the sign pattern of `J - 2A`).
-/

namespace Infinity.C14

/-- The three relations between two vertices of a simple graph. -/
inductive Rel3 | E | A | N
  deriving DecidableEq, Repr

open Rel3

instance : Fintype Rel3 := ⟨{E, A, N}, fun x => by cases x <;> simp⟩

/-- A local product: which relation pairs produce adjacency (the value at `(E, E)` is ignored). -/
abbrev Prod3 := Rel3 → Rel3 → Bool

/-- The relation of a product pair, given the relations in the two factors. -/
def phi (S : Prod3) : Rel3 → Rel3 → Rel3
  | E, E => E
  | r, s => if S r s then A else N

lemma phi_eq_E_iff (S : Prod3) (r s : Rel3) : phi S r s = E ↔ r = E ∧ s = E := by
  cases r <;> cases s <;> simp [phi] <;> split_ifs <;> simp

lemma eq_of_ne_E {x y : Rel3} (hx : x ≠ E) (hy : y ≠ E) (h : x = A ↔ y = A) : x = y := by
  cases x <;> cases y <;> simp_all

section Graphs

open Classical

variable {U V W : Type*}

/-- Relation of two vertices of a simple graph. -/
noncomputable def rel (G : SimpleGraph V) (a b : V) : Rel3 :=
  if a = b then E else if G.Adj a b then A else N

lemma rel_self (G : SimpleGraph V) (a : V) : rel G a a = E := by simp [rel]

lemma rel_symm (G : SimpleGraph V) (a b : V) : rel G a b = rel G b a := by
  unfold rel
  by_cases h : a = b
  · subst h; rfl
  · have h' : b ≠ a := fun e => h e.symm
    simp [h, h', G.adj_comm]

lemma rel_eq_A (G : SimpleGraph V) (a b : V) : rel G a b = A ↔ G.Adj a b := by
  unfold rel
  split_ifs with h1 h2
  · subst h1; simp
  · simp [h2]
  · simp [h2]

lemma rel_eq_E (G : SimpleGraph V) (a b : V) : rel G a b = E ↔ a = b := by
  unfold rel
  split_ifs with h1 h2 <;> simp_all

/-- The local product with cell set `S`. -/
noncomputable def lprod (S : Prod3) (G : SimpleGraph V) (H : SimpleGraph W) : SimpleGraph (V × W) where
  Adj p q := phi S (rel G p.1 q.1) (rel H p.2 q.2) = A
  symm := ⟨fun p q h => by simpa [rel_symm G q.1 p.1, rel_symm H q.2 p.2] using h⟩
  loopless := ⟨fun p h => by simp [rel_self, phi] at h⟩

lemma rel_lprod (S : Prod3) (G : SimpleGraph V) (H : SimpleGraph W) (p q : V × W) :
    rel (lprod S G H) p q = phi S (rel G p.1 q.1) (rel H p.2 q.2) := by
  by_cases hpq : p = q
  · subst hpq
    simp [rel_self, phi]
  · have hne : phi S (rel G p.1 q.1) (rel H p.2 q.2) ≠ E := by
      rw [Ne, phi_eq_E_iff, rel_eq_E, rel_eq_E]
      exact fun h => hpq (Prod.ext h.1 h.2)
    have hrel : rel (lprod S G H) p q ≠ E := by rw [Ne, rel_eq_E]; exact hpq
    apply eq_of_ne_E hrel hne
    rw [rel_eq_A]
    rfl

/-- Relation-level associativity of a local product. -/
def AssocRel (S : Prod3) : Prop := ∀ r₁ r₂ r₃ : Rel3, phi S (phi S r₁ r₂) r₃ = phi S r₁ (phi S r₂ r₃)

/-- CLM-C14-01 ("if"): relation-level associativity makes the canonical map an isomorphism. -/
noncomputable def assoc_iso (S : Prod3) (hS : AssocRel S)
    (G : SimpleGraph U) (H : SimpleGraph V) (K : SimpleGraph W) :
    lprod S (lprod S G H) K ≃g lprod S G (lprod S H K) where
  toEquiv := Equiv.prodAssoc U V W
  map_rel_iff' := by
    intro p q
    show phi S (rel G _ _) (rel (lprod S H K) _ _) = A ↔ phi S (rel (lprod S G H) _ _) (rel K _ _) = A
    rw [rel_lprod, rel_lprod]
    simp only [Equiv.prodAssoc_apply]
    rw [hS]

/-- CLM-C14-01 ("if"), as a theorem: the products are isomorphic via the canonical map. -/
theorem assoc_iso_nonempty (S : Prod3) (hS : AssocRel S)
    (G : SimpleGraph U) (H : SimpleGraph V) (K : SimpleGraph W) :
    Nonempty (lprod S (lprod S G H) K ≃g lprod S G (lprod S H K)) :=
  ⟨assoc_iso S hS G H K⟩

/-- The path `0 - 1 - 2`. -/
def P3 : SimpleGraph (Fin 3) := SimpleGraph.fromRel fun a b => a.val + 1 = b.val

/-- A pair of vertices of `P3` realising each relation. -/
def pick : Rel3 → Fin 3 × Fin 3
  | E => (0, 0)
  | A => (0, 1)
  | N => (0, 2)

lemma rel_pick (r : Rel3) : rel P3 (pick r).1 (pick r).2 = r := by
  cases r <;> simp [rel, pick, P3, SimpleGraph.fromRel_adj]

/-- CLM-C14-01 ("only if"): `P3 * P3 * P3` already detects every failure of associativity. -/
theorem assoc_of_P3 (S : Prod3)
    (h : ∀ p q : (Fin 3 × Fin 3) × Fin 3,
      (lprod S P3 (lprod S P3 P3)).Adj (Equiv.prodAssoc _ _ _ p) (Equiv.prodAssoc _ _ _ q) ↔
        (lprod S (lprod S P3 P3) P3).Adj p q) : AssocRel S := by
  intro r₁ r₂ r₃
  have key := h (((pick r₁).1, (pick r₂).1), (pick r₃).1) (((pick r₁).2, (pick r₂).2), (pick r₃).2)
  change phi S (rel P3 _ _) (rel (lprod S P3 P3) _ _) = A ↔
      phi S (rel (lprod S P3 P3) _ _) (rel P3 _ _) = A at key
  rw [rel_lprod, rel_lprod] at key
  simp only [Equiv.prodAssoc_apply, rel_pick] at key
  by_cases hE : r₁ = E ∧ r₂ = E ∧ r₃ = E
  · obtain ⟨rfl, rfl, rfl⟩ := hE
    rfl
  · apply eq_of_ne_E
    · rw [Ne, phi_eq_E_iff, phi_eq_E_iff]; tauto
    · rw [Ne, phi_eq_E_iff, phi_eq_E_iff]; tauto
    · exact key.symm

end Graphs

/-! ### The finite classification -/

/-- Cell index of a relation pair (the eight cells other than `(E, E)`; `(E, E)` gets index 8). -/
def cellIdx : Rel3 → Rel3 → ℕ
  | E, A => 0 | E, N => 1 | A, E => 2 | A, A => 3 | A, N => 4 | N, E => 5 | N, A => 6 | N, N => 7
  | E, E => 8

/-- The product with code `c` (bit `i` of `c` ↔ cell `i`, same order as `systems/graph_products.py`). -/
def ofCode (c : ℕ) : Prod3 := fun r s => c.testBit (cellIdx r s)

instance (S : Prod3) : Decidable (AssocRel S) := by unfold AssocRel; infer_instance

/-- Relation-level commutativity: `S` is symmetric off the diagonal. -/
def CommRel (S : Prod3) : Prop := ∀ r s : Rel3, phi S r s = phi S s r

instance (S : Prod3) : Decidable (CommRel S) := by unfold CommRel; infer_instance

set_option maxRecDepth 100000 in
/-- CLM-C14-02: exactly these 20 of the 256 local products are associative. -/
theorem assoc_codes :
    (List.range 256).filter (fun c => decide (AssocRel (ofCode c))) =
      [0, 1, 4, 5, 8, 13, 28, 29, 31, 73, 77, 85, 93, 109, 127, 141, 221, 223, 253, 255] := by
  decide

set_option maxRecDepth 100000 in
/-- CLM-C14-02: exactly ten associative products are commutative. -/
theorem comm_assoc_codes :
    (List.range 256).filter (fun c => decide (AssocRel (ofCode c) ∧ CommRel (ofCode c))) =
      [0, 5, 8, 13, 85, 93, 127, 141, 221, 255] := by
  decide

/-- A `{-1, 0, 1}`-valued candidate character `(c E, c A, c N)`. -/
def charOf (x y z : ℤ) : Rel3 → ℤ
  | E => x | A => y | N => z

/-- Relation-level multiplicative character (the entrywise content of `M(G * H) = M(G) ⊗ M(H)`). -/
def IsChar (S : Prod3) (c : Rel3 → ℤ) : Prop := c A ≠ c N ∧ ∀ r s : Rel3, c (phi S r s) = c r * c s

instance (S : Prod3) (c : Rel3 → ℤ) : Decidable (IsChar S c) := by unfold IsChar; infer_instance

/-- All 27 candidates with values in `{-1, 0, 1}`. -/
def candidates : List (Rel3 → ℤ) :=
  [-1, 0, 1].flatMap fun x => [-1, 0, 1].flatMap fun y => [-1, 0, 1].map fun z => charOf x y z

set_option maxRecDepth 100000 in
/-- CLM-C14-04 (relation level, values in {-1,0,1}): exactly six products admit a character:
direct (8), strong (13), symmetric difference (85), co-normal (93), the complement-dual of the
direct product (127) and `EA AE AA NN` (141). -/
theorem character_codes :
    (List.range 256).filter (fun c => candidates.any fun χ => decide (IsChar (ofCode c) χ)) =
      [8, 13, 85, 93, 127, 141] := by
  decide

/-- The symmetric-difference (XOR) product has the character `(1, -1, 1)`: the sign of a relation
multiplies, i.e. `S(G ⊕ H) + I = (S(G) + I) ⊗ (S(H) + I)` entrywise. -/
theorem xor_character : IsChar (ofCode 85) (charOf 1 (-1) 1) := by decide

end Infinity.C14

#print axioms Infinity.C14.rel_lprod
#print axioms Infinity.C14.assoc_iso
#print axioms Infinity.C14.assoc_iso_nonempty
#print axioms Infinity.C14.assoc_of_P3
#print axioms Infinity.C14.assoc_codes
#print axioms Infinity.C14.comm_assoc_codes
#print axioms Infinity.C14.character_codes
#print axioms Infinity.C14.xor_character
