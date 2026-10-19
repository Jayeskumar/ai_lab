# Formal verification, batch 1.1 — notes

Four new Lean 4 + Mathlib files (Lean v4.35.0, the project's Mathlib). Each file imports only Mathlib,
is self-contained, and ends with `#print axioms` for every main theorem. No existing file was edited and
`proofs/lean_results.json` was **not** regenerated (that needs the lab's checker, which this batch did not
run).

| Target | Claim | File | Status | Compile (wall, warm cache) |
|---|---|---|---|---|
| T1 | CLM-C17-05 | `Infinity/C17_ForcedTable.lean` | done, plus existence | 5.4 s |
| T2 | CLM-C13-01 | `Infinity/C13_AffineStructure.lean` | done: (a), (b), (c), (f) as asked, and also (d), (e) | 6.1 s |
| T3 | CLM-C19-15 (core of Thms 7, 8) | `Infinity/C19_DeficitBound.lean` | done (arithmetic core only, as asked) | 5.8 s |
| T4 | CLM-C10-07 | `Infinity/C10_SkewBinary.lean` | done: counting part, plus the link to canonical skew binary | 7.1 s |

Command: `cd proofs/lean && PATH=$HOME/.elan/bin:$PATH lake env lean Infinity/<File>.lean`. Every file
exits 0 with no errors and no warnings. **Axioms:** every main theorem depends only on
`[propext, Classical.choice, Quot.sound]` or a subset of it (`[propext, Quot.sound]` for, e.g.,
`row_last`, `row_gt`, `full_instance_iff`, `forced_unique`, `affine_anchored`, `length_B`, `count_B`).
The files contain no `sorry`, `admit`, `native_decide`, `axiom`, `unsafe`, `implemented_by` or `set_option`.
(The first compile after a cold start can take minutes of wall time while Mathlib's .olean files are
read from disk. CPU time is a few seconds.)

---

## T1 — CLM-C17-05, the forced anchored table (`Infinity.C17`)

Setting: `{N : ℕ} [NeZero N]` (i.e. N ≥ 1), elements `Fin N` with modular `+`. The two hypotheses, used in
every theorem below:

```lean
(anchor : ∀ x, op x 0 = x + 1)
(step   : ∀ x y : Fin N, y.val + 1 < N → op x (y + 1) = op (op x y) (x + 1))
```

Here `y.val + 1 < N` is the paper's `y ≤ N − 2` (no wrap-around). It is vacuous for N = 1.

Main statements (`op`, `anchor` and `step` are section variables as above):

```lean
theorem row_last : ∀ x y : Fin N, x.val = N - 1 → op x y = y                          -- (a)
theorem row_gt   : ∀ x y : Fin N, x.val < N - 1 → x.val < (op x y).val               -- (b)
theorem forced_unique (op₁ op₂ : Fin N → Fin N → Fin N) (anchor₁ …) (step₁ …) (anchor₂ …) (step₂ …) :
    op₁ = op₂                                                                          -- (c)
theorem full_instance_iff :
    (∀ x y : Fin N, op x (y + 1) = op (op x y) (x + 1)) ↔
      ∀ x y : Fin N, y.val = N - 1 → x + 1 = op (op x y) (x + 1)
theorem forced_exists : (∀ x : Fin N, forcedOp N x 0 = x + 1) ∧
    ∀ x y : Fin N, y.val + 1 < N → forcedOp N x (y + 1) = forcedOp N (forcedOp N x y) (x + 1)
theorem forced_existsUnique : ∃! op : Fin N → Fin N → Fin N, (∀ x, op x 0 = x + 1) ∧
    ∀ x y : Fin N, y.val + 1 < N → op x (y + 1) = op (op x y) (x + 1)
```

**Covered:** (a), (b) and (c) exactly as in the paragraph "Uniqueness for every N", for every N ≥ 1.
Also covered: the sentence "it is a model of the full instance iff the wrap-around equations hold"
(`full_instance_iff`), and existence of the forced table for every N (`forced_exists`, built by the
downward recursion `lav`). Existence is the "has a solution for every N" half of the parenthetical remark
in Observation 4. Helpers: `val_add_one`, `add_one_eq_zero`, `row_induction`, `lav_spec`.

**Not covered:** for which N the wrap-around equations hold (the open converse "only powers of 2"), and
the identification of the forced table with Laver's table `A_n` for N = 2ⁿ together with Laver's theorem
that it is left-distributive. `C06_Laver.lean` checks `A₃` only.

---

## T2 — CLM-C13-01, structure of affine spectra (`Infinity.C13`)

Polynomials are `ℤ[X]`, evaluated at `a : ZMod N` by `Polynomial.aeval a f`.
`Aff (S : Set ℤ[X]) : Set ℕ := {N | 1 ≤ N ∧ ∃ a : ZMod N, ∀ f ∈ S, aeval a f = 0}`.

**(a)**

```lean
theorem affine_anchored {N : ℕ} (op : ZMod N → ZMod N → ZMod N) (α β γ : ZMod N)
    (hop : ∀ x y, op x y = α * x + β * y + γ) (anchor : ∀ x, op x 0 = x + 1) :
    α = 1 ∧ γ = 1 ∧ ∀ x y, op x y = x + β * y + 1
```

This holds for every N with no hypothesis. For N = 1 it is trivial, because `ZMod 1` has one element.
`affine_table_anchored` is the converse.

**(b)** This is now a theorem, not a definition. Terms `Term V` (variables in a `Fintype V`) evaluate as
`Term.eval op ρ`. `Term.coeffP v t` and `Term.constP t` are the paper's `C_t[v]` and `D_t`.
`sysLaw s t = {C_s[v] − C_t[v] : v} ∪ {D_s − D_t}` and `sysLaws E = ⋃_{e ∈ E} sysLaw e.1 e.2`.
`affModels E` is the set of N ≥ 1 for which some table `x + a·y + 1` on `ZMod N` satisfies every law of
`E` under every assignment.

```lean
theorem Term.eval_affine … : t.eval (fun x y => x + a * y + 1) ρ = ∑ v, aeval a (t.coeffP v) * ρ v + aeval a t.constP
theorem law_holds_affine_iff (s t : Term V) (a : ZMod N) :
    (∀ ρ : V → ZMod N, s.eval (fun x y => x + a * y + 1) ρ = t.eval (fun x y => x + a * y + 1) ρ) ↔
      ∀ f ∈ sysLaw s t, aeval a f = 0
theorem affModels_eq (E : Set (Term V × Term V)) : affModels E = Aff (sysLaws E)
```

**(c)**

```lean
theorem aff_of_dvd {S : Set ℤ[X]} {N d : ℕ} (hN : N ∈ Aff S) (hd : d ∣ N) : d ∈ Aff S
theorem aff_mul_of_coprime {S : Set ℤ[X]} {N M : ℕ} (hN : N ∈ Aff S) (hM : M ∈ Aff S)
    (hco : Nat.Coprime N M) : N * M ∈ Aff S                       -- via ZMod.chineseRemainder
theorem mem_aff_iff_primePow {S : Set ℤ[X]} {N : ℕ} (hN : N ≠ 0) :
    N ∈ Aff S ↔ ∀ p ∈ N.primeFactors, p ^ N.factorization p ∈ Aff S   -- the "hence" sentence
```

Also `aff_one : 1 ∈ Aff S`.

**(d)** (not requested; done)

```lean
theorem aff_structure_of_no_common_factor (S : Finset ℤ[X])
    (hS : ∀ g : ℚ[X], (∀ f ∈ S, g ∣ f.map (Int.castRingHom ℚ)) → g.degree ≤ 0) :
    (Aff (S : Set ℤ[X])).Finite ∧ ∃ L ∈ Aff (S : Set ℤ[X]), (∀ N ∈ Aff (S : Set ℤ[X]), N ≤ L) ∧
      (∀ N, N ∈ Aff (S : Set ℤ[X]) ↔ N ∣ L) ∧
      ∀ (R : ℤ) (u : ℤ[X] → ℤ[X]), ∑ f ∈ S, u f * f = C R → (L : ℤ) ∣ R
```

`hS` says "no common factor of positive degree in ℚ[a]". It implies S ≠ ∅, since otherwise `X` would be a
common factor. The ingredients are also stated separately:

- `exists_int_mem_ideal`: Bézout in ℚ[X] and clearing denominators give R ≠ 0 with `Σ u f * f = C R`.
- `dvd_of_mem_aff`: every N ∈ Aff S divides such an R.
- `aff_finite`: Aff S is finite.
- `aff_lcm`: Aff S is closed under lcm.
- `aff_eq_divisors`: any finite Aff S is the set of divisors of its maximum.
- `aff_eq_divisors_of_ideal`.

**(e)** (not requested; done)

```lean
theorem aff_infinite {S : Set ℤ[X]} {G : ℚ[X]} (hG : 0 < G.degree)
    (hdvd : ∀ f ∈ S, G ∣ f.map (Int.castRingHom ℚ)) : (Aff S).Infinite
theorem aff_empty : Aff (∅ : Set ℤ[X]) = {N | 1 ≤ N}
```

The proof differs from the paper's. The paper uses Schur's theorem to get infinitely many *primes*. Here,
Gauss's lemma (`IsPrimitive.Int.dvd_iff_map_cast_dvd_map_cast`) turns G into a primitive integer
polynomial dividing every f in ℤ[X]. Then N = |G(k)| is unbounded (`Polynomial.abs_tendsto_atTop`), and
k is a root of G modulo |G(k)|. This gives infinitely many N, which is all that (e) states. The integer
version is `aff_infinite_of_dvd`.

**(f)**

```lean
theorem aff_of_root {S : Set ℤ[X]} {G : ℤ[X]} (hG : ∀ f ∈ S, G ∣ f) {N : ℕ} (hN : 1 ≤ N)
    (a : ZMod N) (ha : aeval a G = 0) : N ∈ Aff S                                  -- first sentence
theorem primePow_root_iff (S : Finset ℤ[X]) (G : ℤ[X]) (h u : ℤ[X] → ℤ[X])
    (hfac : ∀ f ∈ S, f = G * h f) (R' : ℤ) (hsum : ∑ f ∈ S, u f * h f = C R')
    {p : ℕ} (hp : p.Prime) (hpR : ¬ (p : ℤ) ∣ R') (e : ℕ) :
    (∃ a : ZMod (p ^ e), ∀ f ∈ S, aeval a f = 0) ↔ ∃ a : ZMod (p ^ e), aeval a G = 0
theorem primePow_root_iff_of_mem_span (S : Set ℤ[X]) (G : ℤ[X]) (h : ℤ[X] → ℤ[X])
    (hfac : ∀ f ∈ S, f = G * h f) (R' : ℤ) (hR' : C R' ∈ Ideal.span (h '' S))
    {p : ℕ} (hp : p.Prime) (hpR : ¬ (p : ℤ) ∣ R') (e : ℕ) : (same conclusion)
theorem primePow_mem_aff_iff_of_coprime_cofactors (S : Finset ℤ[X]) (G : ℤ[X]) (h : ℤ[X] → ℤ[X])
    (hfac : ∀ f ∈ S, f = G * h f)
    (hcof : ∀ g : ℚ[X], (∀ f ∈ S, g ∣ (h f).map (Int.castRingHom ℚ)) → g.degree ≤ 0) :
    ∃ R' : ℤ, R' ≠ 0 ∧ C R' ∈ Ideal.span (h '' (S : Set ℤ[X])) ∧
      ∀ p : ℕ, p.Prime → ¬ (p : ℤ) ∣ R' → ∀ e : ℕ,
        (p ^ e ∈ Aff (S : Set ℤ[X]) ↔ ∃ a : ZMod (p ^ e), aeval a G = 0)
```

`primePow_mem_aff_iff` restates `primePow_root_iff` in terms of `Aff`. The Lean statements are slightly
stronger than the English:

- G is any integer polynomial with `f = G * h f`; it need not be the primitive part of the ℚ-gcd.
- R′ ≠ 0 is not assumed, since it follows from p ∤ R′.
- e = 0 is allowed; both sides are then trivially true.
- The last theorem also proves the parenthetical "(it exists, since the h_f have no common factor over ℚ)".

**Not covered in T2:**

- The remark in (d) that a non-zero resultant of two polynomials lies in the ideal.
- In (f), the construction of G′ as the primitive part of the ℚ-gcd, and the fact that its cofactors have
  no common factor over ℚ. G and h are hypotheses, and the coprimality of the cofactors is the hypothesis
  `hcof`.
- The link between laws and polynomials is made only by (b). Parts (c)–(f) are stated for sets of
  polynomials.

---

## T3 — CLM-C19-15, arithmetic core of the deficit bound (`Infinity.C19`)

Indexing: the paper's F_i is `Nat.fib (i+1)`. A chip on level k is worth `fib (k+2)`. The chip weight is
a_{k+1} = `fib (k+4) − k − 3`, which equals `Infinity.C19.a (k+1)` of `C19_Zeckendorf.lean`.
φ = `Real.goldenRatio` and ψ = `Real.goldenConj`.

```lean
theorem weight_identity (k : ℕ) :
    (Nat.fib (k + 4) : ℝ) = φ ^ 2 * Nat.fib (k + 2) + ψ ^ (k + 2)                       -- (i)
theorem deficit_bound (T t : ℕ) (z ℓ : ℕ → ℕ) (hz : ∀ k, z k ≤ 1) (hℓ : ∀ k, ℓ k ≤ 1)
    (hℓt : ∀ k, t < k → ℓ k = 0)
    (hval : ∑ k ∈ range (T + 1), Nat.fib (k + 2) * z k = ∑ k ∈ range (T + 1), Nat.fib (k + 2) * ℓ k) :
    ∑ k ∈ range (T + 1), ((Nat.fib (k + 4) : ℝ) - k - 3) * ((z k : ℝ) - ℓ k)
      ≤ 1 + ((t : ℝ) + 1) * (t + 6) / 2                                                -- (ii)
theorem deficit_bound_int … :   -- same hypotheses, integer weights, exact quotient
    ∑ k ∈ range (T + 1), ((Nat.fib (k + 4) : ℤ) - k - 3) * ((z k : ℤ) - ℓ k) ≤ 1 + (((t + 1) * (t + 6) / 2 : ℕ) : ℤ)
```

Helpers:

- `weight_eq`
- `abs_goldenConj_sq_add` : |ψ|² + |ψ| = 1
- `geom_abs_goldenConj` : Σ_{k≤T} |ψ|^{k+2} = 1 − |ψ|^{T+1}
- `geom_abs_goldenConj_le_one`
- `sum_lazy_le`
- `sum_range_add_three` : Σ_{k≤t} (k+3) = (t+1)(t+6)/2
- `two_dvd_succ_mul_add_six`

**Covered:** (i), and (ii) as specified. The requested hypothesis "z k = ℓ k = 0 for k > T" is not needed,
because all sums are truncated at T, so the theorem is stated without it. Neither z nor ℓ needs to be a
Zeckendorf or lazy string: any 0/1 strings of equal value will do. With z = Zeckendorf(n), ℓ = lazy(n)
and T at least both top levels, the left side is B(n) − Ψ(lazy(n)).

**Not covered** (as the target allows; stated in the file's docstring). Nothing about games is
formalised:

- That the split phase ends at lazy(n) (Theorem 2).
- L(n) ≥ Ψ(lazy(n)) and Ψ(Zeckendorf(n)) = B(n), and hence D(n) ≤ B(n) − Ψ(lazy(n)) and the
  game-length bound of Theorem 7.
- The asymptotic L(n) = φ²n − O(log² n).

---

## T4 — CLM-C10-07, skew binary counting (`Infinity.C10`)

**Part 1, the words.** `B 0 = [0]`, `B (k+1) = B k ++ B k ++ [1]`, and
`S k N := ((B k).take N).count 1`.

```lean
theorem length_B (k : ℕ) : (B k).length = 2 ^ (k + 1) - 1
theorem count_B (k : ℕ) : (B k).count 1 = 2 ^ k - 1
theorem prefix_bound (k N : ℕ) (hN : N ≤ (B k).length) : |(S k N : ℚ) - N / 2| ≤ (k + 1) / 2
```

Also: `B_le_one` (all letters are 0 or 1), `prefix_bound_nat` (the same bound in ℕ, as
2S ≤ N + k + 1 ∧ N ≤ 2S + k + 1), `count_B_eq`, and `deficit_full` (D(M_k) = −1/2).

**Part 2, the link to canonical skew binary.** This part was optional; it is done.

- Representations are little-endian lists of a fixed length K. `val` uses weights w_i = 2^{i+1} − 1.
- `Canon l` means the digits are 0, 1 or 2 and only the lowest nonzero digit may be 2.
- `chi l = 1` iff 2 ∈ l.
- `changes l m` is the number of differing positions.
- `repK K n` is n increments applied to the all-zero list.

```lean
theorem canon_existsUnique (K n : ℕ) (hn : n < w K) : ∃! l : List ℕ, l.length = K ∧ Canon l ∧ val l = n
theorem increment_cost (l m : List ℕ) (hl : Canon l) (hm : Canon m) (hlen : l.length = m.length)
    (hv : val m = val l + 1) : changes l m = 1 + chi l ∧ changes l m ≤ 2
theorem chi_word : ∀ K, (List.range (w K)).map (fun n => chi (repK K n)) = B K
theorem totalCost_eq (K N : ℕ) (hN : N < w K) : totalCost K N = N + S K N
theorem totalCost_bound (K N : ℕ) (hN : N < w K) : |(totalCost K N : ℚ) - 3 * N / 2| ≤ (K + 1) / 2
theorem average_cost (N : ℕ) (hN : 0 < N) :
    |(totalCost (Nat.log 2 (N + 1)) N : ℚ) / N - 3 / 2| ≤ (Nat.log 2 (N + 1) + 1) / (2 * N)
```

Here `totalCost K N = Σ_{n<N} changes (repK K n) (repK K (n+1))`. Further theorems:

- `inc_spec`, `val_inc`, `changes_inc` : the increment rule of part (i).
- `canon_unique` : uniqueness of canonical representations. The paper cites this from the literature; here
  it is proved.
- `decomp_low`, `decomp_high`, `decomp_top`, `repK_last` : the decomposition in part (ii).
- `totalCost_succ` : the cost does not depend on K once N < w_K.

**Covered:** all of Theorem 6:

- every increment changes at most 2 digits;
- the χ-word is B_k;
- the prefix bound;
- the average over 0 ≤ n < N is 3/2 + O(log N / N), with the explicit constant above.

**Conventions to note:**

- Representations have a fixed number of digits K. Higher digits are 0 and never change, so counting
  changed positions below K is the paper's cost.
- The definition of `inc` is the paper's rule written recursively. The cost and average theorems do not
  depend on it: `increment_cost` is stated for any two canonical lists, and the representation of n + 1
  is unique by `canon_unique`.

**Not covered:** nothing in Theorem 6 that I am aware of. The O(·) statement is given as an explicit
inequality, not as an asymptotic formula.
