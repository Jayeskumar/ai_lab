import Mathlib.Data.List.Infix
import Mathlib.Tactic

/-!
# Cycle C11 — Pattern-terminated codes are prefix-free

`T_p` uses as codewords the binary words in which the pattern `p` occurs for the first time
at the very end: `p` is a suffix of `w`, and no proper prefix of `w` has `p` as a suffix.

* `prefix_free`: no codeword of `T_p` is a proper prefix of another (CLM-C11-01).
* `unique_parse_head`: hence the first codeword of any concatenation is determined, the key
  step for unique decodability of streams.
-/

namespace Infinity.C11

/-- `w` is a codeword of the pattern-terminated code `T_p`. -/
def IsCodeword (p w : List Bool) : Prop :=
  p <:+ w ∧ ∀ v, v <+: w → v ≠ w → ¬ p <:+ v

/-- **Prefix-freeness.** If a codeword `v` is a prefix of a codeword `w`, they are equal. -/
theorem prefix_free (p v w : List Bool) (hv : IsCodeword p v) (hw : IsCodeword p w)
    (h : v <+: w) : v = w := by
  by_contra hne
  exact hw.2 v h hne hv.1

/-- If two concatenations of codewords agree, their first codewords agree. -/
theorem unique_parse_head (p v w s t : List Bool) (hv : IsCodeword p v) (hw : IsCodeword p w)
    (h : v ++ s = w ++ t) : v = w := by
  rcases List.prefix_or_prefix_of_prefix (List.prefix_append v s) (h ▸ List.prefix_append w t)
    with hvw | hwv
  · exact prefix_free p v w hv hw hvw
  · exact (prefix_free p w v hw hv hwv).symm

end Infinity.C11

#print axioms Infinity.C11.prefix_free
#print axioms Infinity.C11.unique_parse_head
