# Historian novelty check: the spectrum of ETP law 501 (2026-10-20)

*Batch 1.2, for CLM-C05-22. Claim checked: "ETP equation 501, x = y◇(y◇(x◇(x◇y))), has finite models exactly of
the orders n ≡ 0, 1 (mod 4)", with the lab's proof (x□y := x◇(x◇y) is semi-symmetric with square translations;
the product of the signs of the translations of a finite semi-symmetric quasigroup is (−1)^(n(n−1)/2);
square roots of the translations of x□y = −x−y give the models) and a model of order 12 found by SAT. Written by
the Historian agent; saved to the repository by the Director, unchanged except for this header and the closing
note.*

**Bottom line:** (a), (b) and (d) are not stated in any source read. The general form of (c) is a classical
Latin-square theorem; the semi-symmetric case follows from it in one line but was found stated nowhere.

## Verdicts

**(a) The mod-4 restriction for 501: NOT FOUND.**
- B. Le Floch, *Spectra of equational laws* (versions of Jul 1, 10 and 14, 2025; §2.2 in the Jul 14 version):
  "501 x = y ⋄ (y ⋄ (x ⋄ (x ⋄ y))) has unknown spectrum containing 1,4,5,8,9. It implies that the operation
  x□y = x ⋄ (x ⋄ y) obeys law 14." The notes do not exclude 3, 6 or 7.
- `commentary/Equation501.md` (ETP repository; three commits by Le Floch, Jul 3, Jul 19 and Oct 5, 2025;
  unchanged at HEAD 1aec8a7, Sep 12, 2026): "The finite spectrum ... of this law is unknown."
- The only orders any source excludes: order 2 (the notes' list; Lean `FullSpectrum.lean`), and idempotent models
  of order ≡ 2 (mod 3) (B. Gunby-Mann, Jul 14, 2025).
- Closest precedents, for other laws: the notes prove "167 ... has spectrum {0, 1 mod 4}" by counting orbits
  ("n(n − 1) ≡ 0 mod 4"); on Zulip ("Order 3 Spectra", Jun 30, 2025) Le Floch hoped, for law 63, for "maybe
  eventually getting some mod 4 constraint on the magma size", with no result.

**(b) Models for every n ≡ 0, 1 (mod 4): NOT FOUND.**
- Known orders: 1, 4, 5, 8, 9 (the notes, by an automated prover) and 4 (`data/smallest_magma_examples.txt`).
- The notes use "the explicit model Z/mZ with x ◦ y = −x − y mod m" only as a model of law 14 (§4.2.3); for a
  different law, 72, they observe that "all left-multiplications Ly square to σ⁻¹". No source turns a law-14
  model into a model of 501 by taking square roots of its translations.

**(c) The product-of-signs identity: KNOWN in general form (classical); the semi-symmetric case is not stated
anywhere read, but follows immediately.**
- N. Francetić, S. Herke, I. M. Wanless, "Parity of sets of mutually orthogonal Latin squares",
  arXiv:1703.04764 (2017); J. Combin. Theory Ser. A 155 (2018) 67–99: "These three parities are related by
  πr + πc + πs ≡ (n choose 2) (mod 2). (1.1) This relation has been rediscovered numerous times. Different proofs
  have been published in [7, 10, 13, 22, 24]" — [13] J. C. M. Janssen, JCTA 69 (1995) 173–181; [24] P. Zappa,
  Boll. UMI 10-A (1996) 63–69; [7] Donovan–Grannell–Griggs–Lefevre, Graphs and Combinatorics 26 (2010);
  [10] Glynn (2010); [22] Wanless (2004).
- M. Kwan, K. Petrova, M. Sawhney, arXiv:2509.13125 (Sep 16, 2025): "it was proved by Janssen [34] and Zappa [58]
  that for any Latin square L of order n, we have Nrow(L) + Ncol(L) + Nsym(L) = f(n) (mod 2)", with f(n) = 0 for
  n ≡ 0, 1 (mod 4) and 1 otherwise; repeated in arXiv:2610.13487 (Oct 9, 2026).
- Corollary (the Historian's derivation): in a semi-symmetric Latin square the permutation of column b is
  L_b⁻¹ and that of symbol c is L_c, so the row, column and symbol parities are equal and (1.1) gives
  ∏ sgn L_x = (−1)^(n(n−1)/2). Francetić–Herke–Wanless use the same idea for group tables ("equiparity, because
  they are isotopic to all of their conjugates"). Not stated for semi-symmetric (Mendelsohn) quasigroups in any
  source read; the 2010 Donovan–Grannell–Griggs–Lefevre paper (abstract only: "constraints on the parity vector of
  a Latin square resulting from structural properties of the square", covering Steiner quasigroups) might.
- Suggested label: a classical corollary — cite Janssen, Zappa and Francetić–Herke–Wanless; the lab's proof via
  the order-3 map is one more proof of the special case.

**(d) A model of 501 of order 12: NOT FOUND.** No source mentions 501 at orders 10, 11 or 12; order 12 is no
product of known orders (3 is excluded); no source states non-existence at 3, 6, 7 or 10 (only 2).

**Consistency.** Every order the sources give for 501 is ≡ 0, 1 (mod 4). The ETP's order-4 model satisfies 501;
its □ satisfies law 14 and all four □-translations are even (the ◇-translations have signs −, −, +, −).

## Sources read

1. ETP repository, partial clone at 1aec8a7: history and all three versions of `commentary/Equation501.md`; a
   search for 501, its dual 3106, "semi-symmetric", "parity" and "mod 4" across all 771 commentary files,
   `paper/*.tex`, `blueprint/`, the text files in `data/`, `FullSpectrum.lean`, `SmallMagmas.lean`; PR #1463
   (Jul 21, 2026, unrelated).
2. GitHub issue and PR searches ("501", "spectrum", "semi-symmetric", "parity"): nothing on law 501.
3. Lean Zulip archive, stream Equational (frozen Feb 28, 2026): full-text search of 279 of 334 topic pages;
   "Order 3 Spectra" read in full.
4. Le Floch's notes (Jul 1, 10, 14, 2025): §2.2, §2.4, §4.2.3 and the counting lists; his `spectrum.json` has an
   empty entry for 501.
5. Gunby-Mann, "Spectra from clique decompositions of K_n" (Jul 14, 2025), in full.
6. ETP paper arXiv:2512.07087v2 (latest per the arXiv API) and the Sep 2026 site build: no mention of 501.
7. Le Floch, arXiv:2603.29909 and arXiv:2609.39872 (the latter treats 501 only as a semigroup law).
8. Parity of Latin squares: arXiv:1703.04764, 2509.13125, 2610.13487, 1610.06262, 1203.0223, 2012.15257;
   semisymmetric quasigroups: Kozlik, arXiv:2607.27872; Mendis–Wanless, arXiv:2603.23866 (no parity result).
9. arXiv API and web searches on semisymmetric quasigroups, Latin-square parity, parity of Mendelsohn and Steiner
   systems, law 501.

Not accessible: Zulip messages after Feb 28, 2026 (login); 55 archive topics with names starting with "." (404,
infrastructure topics); Janssen 1995 (ScienceDirect 403); the full text of Donovan–Grannell–Griggs–Lefevre 2010
(403; abstract only); Zappa 1996, Glynn 2010 and Wanless 2004 were not read.

## Director's note

Labels applied: CLM-C05-22 POTENTIALLY NOVEL for the spectrum (necessity, sufficiency and the order-12 model),
with the sign identity credited as a corollary of the Janssen–Zappa parity relation (1.1) for Latin squares.
ETP members may hold unpublished results; the novelty is relative to the sources listed.
