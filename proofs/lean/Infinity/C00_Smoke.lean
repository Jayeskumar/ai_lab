import Mathlib.Data.Nat.Fib.Zeckendorf
/-! Smoke test for the proof pipeline (not a research result). -/
theorem smoke_fib : Nat.fib 10 = 55 := by decide
#print axioms smoke_fib
