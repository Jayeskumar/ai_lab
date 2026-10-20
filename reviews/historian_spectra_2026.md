# Historian report: finite spectra of 15 ETP laws, state of the sources on 2026-10-20

Historian (novelty analyst), independent of the researchers. Scope: what the literature and the Equational
Theories Project (ETP) public material say about the orders n of finite models of laws 467, 501, 670, 677, 704,
883, 907, 1076, 1083, 1110, 1279, 1286, 1313, 1516, 1719 (ETP numbering, x = t). Main focus: orders 8-12 (677 and
1313: 11-14), and whether anything is newer than B. Le Floch's July 2025 notes.

Method. Web search; arXiv API; the public Lean Zulip archive (leanprover-community.github.io/archive, frozen on
2026-02-28); ETP repository files through raw.githubusercontent.com, directory listings through Software
Heritage (snapshot of 2026-09-16, `main` at commit 1aec8a7 of 2026-09-12), GitHub web pages through WebFetch; the
eq677 model database. Downloads went to `/tmp/claude-0/-home-user-ai-lab/5e93bf16-791a-5608-a61f-d865140bf384/scratchpad/historian3/<name>/` and
were treated as data. The source models were re-checked by
`reviews/historian_checks/spectra/check_sources.py` (section 7; under a second of CPU). No git commands.
Process slip: one download (`archive_root.html`, the archive home page) first landed in the repository root because
I gave curl a relative output path. The Director moved it into the scratchpad. No other file was written outside
`reviews/historian_spectra_2026.md` and `reviews/historian_checks/spectra/`.

Conventions. "IN" means a model of that order exists and "OUT" means none exists. Le Floch's phrase "unknown
spectrum starting with a, b, ..." is read, as the lab already reads it, as "the smallest members are a, b, ...", so
unlisted orders below the last listed one are OUT. This is an interpretation, marked "(s.w.)" below. The notes'
explicit lists ("the 31 laws ... have no model of size 2", "the 14 laws ... none of size 3") are cited as N-list.
"Newer" means later than the July 14, 2025 version of the notes.

---------------------------------------------------------------------------------------------------------------

## 1. Answer in brief

1. **No newer version of Le Floch's notes exists in any place I could reach.** The newest is still the July 14,
   2025 upload; three versions exist: July 1, July 10 and July 14, 2025. Their per-law sentences for the 15 laws
   are identical in the July 10 and July 14 versions. The planned paper on spectra is still unpublished. Le Floch
   on GitHub issue #1052 (Nov 7, 2025): "I will write a paper on various questions around the spectrum, with
   whomever is interested." The ETP referee response (round 2, `paper/referee reports/response.tex`) still has
   `\todo` under "Cite the article in preparation in which the results on spectra of laws of higher orders will be
   reported". Le Floch's 2026 arXiv papers (2603.29909, 2609.39872) never use the word "spectrum".
2. **The ETP GitHub repository has no spectrum table or data file.** It has only Lean proofs that the 15 laws are
   not full-spectrum: no model of size 2 for 14 of them, none of size 3 for 883. It also has per-equation
   commentary files, last edited Jul-Dec 2025. All 15 say the finite spectrum is "unknown", and several add
   structural facts (section 6).
3. **The ETP paper's spectrum section (§9) is unchanged** between arXiv v2 (Dec 16, 2025) and the project-site build
   of Sep 12, 2026. It still treats only full spectra and "deferred" detailed spectra. The appendices contain no
   spectra. The paper does contain law-specific size facts in other sections: §5.1 and Example 5.2 (1286: smallest
   model 7, a model of order 11), §7.3.1 (677: Mace4 exhausts size 8 and finds a model of size 9) and Tables 3-4
   (677).
4. **No 2025-2026 arXiv paper states spectra of these laws.** I searched the arXiv API and the abstracts and full
   texts of the ETP follow-up papers (section 8).
5. **Law 677 is the only one with substantial newer material.** The Zulip topic "FINITE: 677 -> 255" (631
   messages, Dec 2024 - Feb 2026) and the community model database `memoryleak47/eq677` give the following.
   - IN up to 20: 1, 5, 7, 9, 11, 13, 16, 19.
   - OUT: 2, 3, 4, 6 (Dec 7, 2024), 8 (Dec 7, 2024; ETP paper) and **10** ("There are no models whatsoever of 677
     in size 10 (39h in Mace4)", J. Brox, Jan 12, 2025).
   - A complete "general model search up to n=11" (R. Schneider, Nov 2025).
   - Le Floch, Jan 8, 2026: "the known spectrum ≤100 is now: 1, 5, 7, 9, 11, 13, 16, 19, 21, 25, ...".
   - **Orders 12 and 14 of 677 are open in every source.** On Jan 8, 2026 the participants said the only known
     non-existence technique is exhaustive search.
6. **Older sources that the July 2025 notes do not reflect** state facts the lab currently counts as new:
   - 677: orders 2-10 (Zulip, Dec 2024 - Jan 2025).
   - **1516: models of orders 8 and 9, none of order 10 (with a stated caveat), a linear model of order 11** (Zulip,
     Nov 4-5, 2024).
   - 1286: beyond the notes' "starting with 1, 7" (confirmed by Mace4 on Nov 5, 2024), a linear model of order 11
     (ETP paper, Example 5.2; commentary).
7. **A contemporaneous note the lab has not read:** B. Gunby-Mann, "Spectra from clique decompositions of K_n"
   (Zulip upload, July 14, 2025, the same day as the last notes).
   - It proves with Wilson's existence theorem for pairwise balanced designs that **467, 670, 704, 883, 1076, 1110,
     1279, 1313, 1516** (and 63, 667, 1489) contain every sufficiently large order.
   - It gives explicit idempotent orders: 670: 11, 16, 29; 1076: 16, 47; 1313: 5, 16, 19; the laws that reduce to
     63/73/118/125: 8, 11.
   - It shows 501, 1083 and 1719 have no idempotent model of order ≡ 2 (mod 3).
   - It shows 677's idempotent linear models live exactly at prime powers q ≡ 0, 1 (mod 5).

**For the lab's targets:** no source decides any of the pairs targeted by EXP-C05-09 and EXP-C05-10 (section 4.2).
Decisions there are new relative to everything I read. 1313 at 8 and 10 (CLM-C05-13) are also not stated anywhere.

---------------------------------------------------------------------------------------------------------------

## 2. Summary table (all orders)

Source codes:
- **N** = Le Floch notes (Jul 1, 10 and 14, 2025; identical for these laws apart from 467's Gaussian-integer
  sentence, which was added on Jul 10); N-list = the notes' lists of laws without models of size 2 or 3.
- **GM** = Gunby-Mann clique note (Jul 14, 2025).
- **Z677**, **Z1516**, **ZIS** (Implication Statistics), **ZAP** (Austin pairs) = Zulip topics.
- **P** = ETP paper (arXiv v2, Dec 16, 2025; same text in the Sep 12, 2026 site build).
- **C** = ETP commentary files.
- **L** = ETP Lean `FullSpectrum.lean` / `Generated/FullSpectrum.lean`.
- **DB** = eq677 model database.
- **BP** = ETP blueprint, chapter 677.

"All large" = every sufficiently large n is in the spectrum (GM, through Wilson's theorem; the bound is not
effective).

| Law | Orders IN (stated or directly implied) | Orders OUT | Sources | Newer than Jul 14, 2025? |
|---|---|---|---|---|
| 467 | 1, 5, 7, 8 (N); every odd k²+l² with k, l of different parity, i.e. 5, 9, 13, 17, 25, ... (N, Jul 10/14); 8, 11 (GM, idempotent models reduce to 63); all large (GM) | 2 (N-list, L); 3, 4, 6 (s.w.) | N, GM, C, L | only C (structural; "unknown") |
| 501 | 1, 4, 5, 8, 9 (N) | 2 (N-list, L). Idempotent models: none of order ≡ 2 mod 3 (GM) | N, GM, C, L | only C |
| 670 | 1, 4, 5 (N); 11, 16, 29 (GM, idempotent linear); all large (GM) | 2 (N-list, L); 3 (s.w.); 6, 7 (N) | N, GM, C, L | only C |
| 677 | 1, 5, 7, 9, 11, 13, 16, 19 (≤ 20; Z677, P, DB); ≤ 100 also 21, 25, 29, 31, 35, 37, 41, 43, 45, 49, 55, 57, 61, 63, 65, 67, 69, 71, 73, 76, 77, 79, 80, 81, 83 (DB only), 85, 89, 91, 93, 95, 96, 97, 99 (Z677 Jan 8 and 15, 2026); all prime powers q ≡ 0, 1 mod 5 (GM); all large n ≡ 0, 1 mod 5 (GM); n ≡ 1, 5 mod 20 by gluing (Z677) | 2, 3, 4, 6 (Z677 Dec 7, 2024; 2 also N-list, L); 8 (Z677 Dec 7, 2024; P §7.3.1); 10 (Z677 Jan 12, 2025); no other ≤ 11 (complete search, Z677 Nov 2025 + DB) | Z677, P, DB, GM, BP, C, N, L | **yes** (Z677 Sep 2025-Feb 2026, P, DB) |
| 704 | 1, 5, 7, 8 (N); 8, 11 (GM, via 73); all large (GM) | 2 (N-list, L); 3, 4, 6 (s.w.); 9 (N) | N, GM, C, L | only C |
| 883 | every n ≡ 1, 2 mod 3, i.e. 1, 2, 4, 5, 7, 8, 10, 11, 13, 14, ... (N); all large (GM) | 3 (N-list; L, Generated/FullSpectrum.lean) | N, GM, C, L | only C |
| 907 | 1, 3, 7, 9, 13 (N) | 2, 4, 5, 6 (N; 2 also L) | N, GM, C, L | only C |
| 1076 | 1, 5 (N); 16, 47 (GM); 65 (C; ZAP), 169 (ZAP); all large (GM) | 2 (N-list, L); 3, 4 (s.w.); 6, 7 (N) | N, GM, C, ZAP, L | only C (structural: finite models are idempotent quasigroups) |
| 1083 | 1, 3, 4, 7, 8, 9 (N); 12 = 3·4 by direct product (implied; the notes state multiplicativity) | 2 (N-list, L). Idempotent models: none ≡ 2 mod 3 (GM) | N, GM, C, L | only C |
| 1110 | 1, 4, 5, 7, 8, 9 (N); 8, 11 (GM, via 125); 25 (C); all large (GM) | 2 (N-list, L); 3, 6 (s.w.) | N, GM, C, L | only C |
| 1279 | 1, 5, 7, 8 (N); 8, 11 (GM, via 118); all large (GM) | 2 (N-list, L); 3, 4, 6 (s.w.); 9 (N) | N, GM, C, L | only C |
| 1286 | 1, 7 (N; P §5.1; ZIS); 11 (P Example 5.2; C) | 2 (N-list, L); 3-6 (s.w.; ZIS Mace4 Nov 5, 2024; P §5.1 "smallest non-trivial finite model was of size 7") | N, P, ZIS, C, GM, L | P (Dec 2025), but its facts date from Oct-Nov 2024 |
| 1313 | 1, 5, 7 (N); 5, 16, 19 (GM, idempotent linear); all large (GM) | 2 (N-list, L); 3, 4, 6 (s.w.) | N, GM, C, L | only C |
| 1516 | 1, 5, 7, 8 (N); 7, 8, 9, 11 (Z1516, Nov 4-5, 2024); 8, 11 (GM, via 63); 35 (C); all large (GM) | 2 (N-list, L); 3, 4, 6 (s.w.); **10** (Z1516, with a caveat: "might have had a bug") | N, Z1516, GM, C, L | only C |
| 1719 | every n ≡ 0, 1 mod 3, and 5, 8 (N): 1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, ... | 2 (N-list, L). Idempotent models: none ≡ 2 mod 3 (GM) | N, GM, C, L | only C |

---------------------------------------------------------------------------------------------------------------

## 3. Orders 8-12, and 677 / 1313 at 11-14

A dash (—) means that no source I read says anything about that order.

| Law | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|
| 467 | IN (N) | IN (N: ℤ[i]/(3)) | — | IN (GM)¹ | — |
| 501 | IN (N) | IN (N) | — | — | — |
| 670 | — | — | — | IN (GM) | — |
| 704 | IN (N) | OUT (N) | — | IN (GM)¹ | — |
| 883 | IN (N) | — | IN (N) | IN (N) | — |
| 907 | — | IN (N) | — | — | — |
| 1076 | — | — | — | — | — |
| 1083 | IN (N) | IN (N) | — | — | IN (3·4, product) |
| 1110 | IN (N) | IN (N) | — | IN (GM)¹ | — |
| 1279 | IN (N) | OUT (N) | — | IN (GM)¹ | — |
| 1286 | — | — | — | IN (P Ex. 5.2; C) | — |
| 1516 | IN (N; Z1516) | IN (Z1516, Nov 5, 2024) | OUT? (Z1516, caveated) | IN (Z1516; GM¹) | — |
| 1719 (not asked) | IN (N) | IN (N) | IN (N) | — | IN (N) |

| Law | 11 | 12 | 13 | 14 |
|---|---|---|---|---|
| 677 | IN (Z677 Dec 5, 2024, four linear models mod 11; GM; P Table 4; DB, 4 models) | — (open; Table 4's undefined "special" class has none) | IN (Z677 Dec 5, 2024, linear mod 13; P Table 4; DB, 1 model) | — (open; no "special" model either) |
| 1313 | — | — | — (the lab's own EXP-C05-07 has a linear model) | — |

¹ GM: "For those laws that reduce to the Dupont law 63, its parastrophical equivalent 73, or one of their finite
equivalents (up to duality) such as 118 or 125, we simply note that fact instead (all of these are saturated by
the set {8, 11})". Here "saturated by S" means S lies in the idempotent spectrum. Check: an idempotent linear model
x◇y = (1−b)x + by over ℤ/11 exists for each of 467, 704, 883, 1110, 1279, 1516 (section 7).

---------------------------------------------------------------------------------------------------------------

## 4. Consequences for the lab

### 4.1 Claims of cycle C05 against the sources

| Claim | Fact | Prior source found | Suggested label |
|---|---|---|---|
| CLM-C05-07 | 677 has models of orders 5, 7, 9 | 5: T. Tao, Z677 Dec 5, 2024 (2x−y on ℤ/5). 7: I. Tencer, Z677 Dec 5, 2024 (linear models mod 7) and D. McNeil, Dec 7, 2024 ("two non-iso order 7 677s"). 9: J. Brox, Z677 Dec 9, 2024 (explicit table, re-checked) and ETP paper v2 §7.3.1 ("to find a model of size 9 in 16s") | **REDISCOVERY** for 677 |
| CLM-C05-07 | 1516 has a model of order 9 | A. Livne Bar-on, Z1516 Nov 5, 2024 (explicit table, re-checked) | **REDISCOVERY** |
| CLM-C05-07 | 1286 and 1313 have models of order 9 | none found | stays POTENTIALLY NOVEL (relative to these sources) |
| CLM-C05-08 | 677 has no models of orders 3, 4, 6 | I. Tencer, Z677 Dec 7, 2024: "There are no 677 models of size 2, 3, 4, and 6." | **REDISCOVERY** for 677 |
| CLM-C05-08 | 501 none of 6, 7; 883 none of 6; 1076 none of 8; 1083 none of 5, 6 | none found | stays POTENTIALLY NOVEL |
| CLM-C05-09 (refuted) | order-16 models of 677 and 1313 | 677: BP ("a field of size 16"), Z677 Nov 21, 2025 ("16 (two)"), GM (q = 16 ≡ 1 mod 5). 1313: GM ("Splits over F16") | the refuting facts were already known |
| CLM-C05-10 | linear models over GF(q), q ≤ 128 | partly known: 677 prime-field linear models up to 499 (Z677 Dec 5, 2024) and linear sizes up to 100 (Z677 Nov 21, 2025); 670 at 11, 16, 29, 1076 at 16, 47, 1313 at 5, 16, 19 (GM); 1286 at 7, 11 (P, C); 1516 at 5, 7, 11 (Z1516); 467 Gaussian-integer models (N); 1110 parametric families (C) | NOT ASSESSED → partly REDISCOVERY; the complete table for all 15 laws was not found anywhere |
| CLM-C05-11 | 677 has no model of order 8 | J. Brox, Z677 Dec 7, 2024 (Mace4, 41 min); ETP paper §7.3.1 | REDISCOVERY (already labelled) |
| CLM-C05-12 | 677 has no model of order 10; its orders ≤ 10 are exactly 1, 5, 7, 9 | J. Brox, Z677 Jan 12, 2025: "There are no models whatsoever of 677 in size 10 (39h in Mace4)." R. Schneider, Z677 Nov 21, 2025: a complete "general model search up to n=11" | **REDISCOVERY**; the lab adds the first independently checkable certificate (DRAT) |
| CLM-C05-13 | 1313 has no model of order 8 or 10 | none found | stays POTENTIALLY NOVEL |
| CLM-C05-14 | non-right-cancellative finite models of 677 exist; models of order ≤ 10 are quasigroups | consistent with the sources. The smallest known non-right-cancellative model is now order **55** (Le Floch, Z677 Nov 22, 2025, edit; D. Renshaw, Feb 4, 2026). Kocsis, Z677 Mar 4, 2025: "computer searches found none" small. Every DB model of order ≤ 11 is a Latin square (section 7) | add the citations |

The same corrections apply to the C05 README frontier table ("677 ... 5, 7, 9 (notes give no sizes)") and to
`textbook/src/06_magma_laws.md`:
- Theorem 6.4 (677 at 5, 7, 9; 1516 at 9) is "POTENTIALLY NOVEL relative to the ETP notes" there; these memberships
  are rediscoveries.
- Theorem 6.5: its 677 gaps (3, 4, 6) are rediscoveries.
- Theorem 6.11: 677 at order 10 is a rediscovery too, with a new certificate. 1313 at 8 and 10 stays unmatched.

### 4.2 The targets of the running experiments

The EXP-C05-09 targets are 467/10, 501/10, 670/10, 704/10, 907/10, 1076/10, 1083/10, 1110/10, 1279/10, 1286/10,
883/9, 1076/9, 670/8, 907/8 and 1286/8. The EXP-C05-10 targets are 1313/14, 1076/12, 1110/12, 1279/12, 1286/12,
1313/12, 1110/13, 1279/13, 1076/11 and 1313/11.
- **No source states membership or non-membership for any of these pairs.** The closest items follow.
  - 1076 at 9: M. Bolan, ZAP Dec 2, 2024: "1076 just doesn't seem to have many small models (I have found no
    nonlinear ones so far, Mace 4 is currently checking order 9)". No result was reported later.
  - GM's asymptotic theorem covers 1076, 1110, 1279, 1313, 670, 704, 467, 883 only beyond an ineffective bound.
- The controls agree with the sources: 704/9 and 1279/9 are OUT ("no 9", N); 1083/12 is IN by product.
- Not targeted, but open or nearly open in the sources: **1516 at 10** (the caveated Zulip "no"), 1516 at 12,
  1719 at 11, 677 at 12 and 14.

---------------------------------------------------------------------------------------------------------------

## 5. Per-law notes (verbatim quotes)

URLs used below:
- N(Jul 14): https://leanprover.zulipchat.com/user_uploads/3121/jrBQt8qmSzvI3w359L3p-LVR/spectrum.pdf
- N(Jul 10): https://leanprover.zulipchat.com/user_uploads/3121/apvdoKH3jwd1mrnPxZcvlXL_/spectrum.pdf
- N(Jul 1): https://leanprover.zulipchat.com/user_uploads/3121/2kbrfArXGBOH-Ko9D13RqRkq/spectrum.pdf
- GM: https://leanprover.zulipchat.com/user_uploads/3121/Ln5Nhztwtnfftwo3eIviWsJV/Two-variable-Clique-Decompositions.pdf
  (announced in "Order 3 Spectra", msg 528581357)
- Z677: https://leanprover-community.github.io/archive/stream/458659-Equational/topic/FINITE.3A.20677.20-.3E.20255.html
  (append `#<msg id>`; the original is https://leanprover.zulipchat.com/#narrow/channel/458659-Equational/topic/FINITE.3A.20677.20-.3E.20255/near/<msg id>)
- Z1516: https://leanprover-community.github.io/archive/stream/458659-Equational/topic/1516.20-.3E.20255.html
- C: https://raw.githubusercontent.com/teorth/equational_theories/main/commentary/Equation<n>.md
- P: https://arxiv.org/pdf/2512.07087v2 and https://teorth.github.io/equational_theories/paper.pdf

Common to all 15 laws:
- N (Jul 14, §1.1): "The 31 laws {2, 63, 66, 73, 115, 118, 125, 167, 168, 467, 474, 501, 670, 677, 704, 873, 880,
  907, 1076, 1083, 1110, 1279, 1286, 1313, 1480, 1486, 1489, 1516, 1685, 1692, 1719} have no model of size 2. The 14
  laws {481, 546, 556, 667, 695, 883, 887, 895, 898, 1323, 1483, 1485, 1496, 1526} have models of size 2 but none of
  size 3."
- L: `theorem not_full_spectrum_card2_2var : NotFullSpectrum [66, 73, 118, 167, 467, 474, 501, 670, 677, 704, 873,
  907, 1076, 1083, 1110, 1279, 1286, 1313, 1489, 1516, 1685, 1692, 1719]` (no model of size 2) and
  `theorem not_full_spectrum_Equation883` (`use 3`, no model of size 3).
  Files: https://raw.githubusercontent.com/teorth/equational_theories/main/equational_theories/FullSpectrum.lean and
  `.../Generated/FullSpectrum.lean`.
- C: each of the 15 commentary files says "The finite spectrum of (cardinalities of finite magmas satisfying) this
  law is unknown" and links to "Order 3 Spectra".
- `spectrum.json` (Le Floch, Jul 1, 2025,
  https://leanprover.zulipchat.com/user_uploads/3121/rhtlgrHH1Qio18T61MZeJE-T/spectrum.json) has `"spec": ""` for
  all 15 laws. It records nothing for them.
- `data/smallest_magma.txt` (ETP repository) gives the smallest non-trivial model size: 467 5, 501 4, 670 4, 677 5,
  704 5, 883 2, 907 3, 1076 5, 1083 3, 1110 4, 1279 5, 1286 7, 1313 5, 1516 5, 1719 3. These agree with N.
- GM (Zulip, Jul 14, 2025, msg 528581357): "Using the clique decomposition technique, we can show that 63, 467, 667,
  670, 704, 883, 1076, 1110, 1279, 1313, 1489, and 1516 have asymptotically full spectrum (idempotent spectrum,
  even, as those are the only magmas that this technique produces). Out of the remaining 8 laws, 115, 501, 873,
  1083, and 1719 do not have asymptotically full idempotent spectrum; in fact, their idempotent spectrum contains no
  n≡2 (mod 3) due to being 'downstream' from Law 14 ... The remaining three two-variable laws, 677 (of course),
  907, and 1286, have modular barriers to idempotent linear models, but it's not clear that those barriers exist
  for nonlinear models".
  - Method (PDF): Proposition 1 glues idempotent models along an edge-decomposition of K_n into cliques. Corollary 2
    applies Wilson's theorem [R. Wilson, JCTA 18 (1975) 71-79].
  - The PDF's text breaks off at "The equation 907, x = y ◇ ((y ◇ x) ◇ (x ◇ y))". The page ends there and page 3
    holds only the references.

### 467: x = y(x(x(yy)))
- N (Jul 10/14): "467 x = y ⋄ (x ⋄ (x ⋄ (y ⋄ y))) has unknown spectrum starting with 1, 5, 7, 8. It is the Dupont law
  twisted by the squaring map. The spectrum contains at least all odd integers that are sums of two squares k²+l²
  (with k, l of different parities), as the quotient ℤ[i]/(k+il)ℤ[i] equipped with the operation x ⋄ y =
  −((k²+l²+1)/2)(1+i)x + iy obeys this law. It has other linear models which are harder to describe. It likely has
  non-linear models too." The Jul 1 version lacks the Gaussian-integer sentence.
- GM table: "467 ... Idempotent models reduce to 63". For 63: "Saturating Set {8, 11} ... Splits over F8; 5 is a
  root mod 11". N (Jul 14, §2.3, on 63): "Idempotent models (x ⋄ x = x) have sizes 1, 5, 7, 8, 11, ...".
- C (Equation467.md): "Finite magmas satisfying this law are left quasigroups (left multiplications are bijective),
  the squaring and cubing maps S: x ↦ x◇x and B: x ↦ x◇(x◇x) are inverse bijections, and law 2847 holds. In
  addition, the operation defined by x◆y = x◇(x◇y) satisfies law 1722 ... The left division operation ...
  satisfies law 437 ... thus the two laws are parastrophically equivalent for left quasigroups."
- Nothing newer than July 2025 about orders 8-12. 10 and 12 are unaddressed.

### 501: x = y(y(x(xy)))
- N: "501 ... has unknown spectrum containing 1,4,5,8,9. It implies that the operation x□y = x ⋄ (x ⋄ y) obeys law
  14."
- GM §3.1: 501 is among the laws whose "idempotent spectrum does not contain any n ≡ 2 (mod 3)". So any model of
  order 8 or 11 is non-idempotent.
- C: "This law implies that all left multiplications are bijective. The left division operation ... satisfies the
  same law ... x ◆ y = x ◇ (x ◇ y) satisfies the semi-symmetric quasigroup law 14".
- Nothing newer about 8-12. 10, 11 and 12 are unaddressed.

### 670: x = y(x((xy)y))
- N: "670 ... has unknown spectrum starting with 1, 4, 5, not 6 nor 7".
- GM table: "670 ... ILP −b⁴ + 2b³ − b + 1, Saturating Set {11, 16, 29}, Splits over F16, 6 is a root mod 11, 3 is
  a root mod 29". So 11 is IN (re-checked: (1−b)x + bx with b = 6 over ℤ/11 satisfies 670).
- C: "Finite magmas satisfying this law are left quasigroups".
- Nothing newer. 8, 9, 10 and 12 are unaddressed in the sources. The lab has 9 from GF(9).

### 677: x = y(x((yx)y))
- N: "677 ... has unknown spectrum. It is the source of the famous last surviving implication." No sizes.
- Zulip, Dec 2024 - Mar 2025 (older than the notes, but not in them):
  - T. Tao, Dec 5, 2024, msg 486373274: "The smallest non-trivial model is of order 5; this particular example is
    x⋄y=2x−y on ℤ/5ℤ." He also gives the two types of linear models (from P. Nielsen): "Type 1: β is negative a
    primitive 5th root of unity ... and α = 1−β ... Type 2: β is a root of x⁴+x³+2x²+2x+1 and α=−β³−β−1".
  - I. Tencer, Dec 5, 2024, msg 486395178: "Here are all the linear models up to order 500 in ℤ/pℤ, p prime: no
    candidates for 2, no candidates for 3, modulus: 5, a: 2, b: 4, modulus: 7, a: 4, b: 1, modulus: 7, a: 4, b: 3,
    modulus: 11, a: 10, b: 2 ... modulus: 13, a: 9, b: 11, no candidates for 17 ... no candidates for 23, no
    candidates for 29".
  - I. Tencer, Dec 7, 2024, msg 486683966: "There are no 677 models of size 2, 3, 4, and 6."
  - J. Brox, Dec 7, 2024, msg 486711939: "Mace4 has been able to check in 41min that 677 has NO models of size 8."
    D. McNeil, msg 486714519: "There are definitely two non-iso order 7 677s (with and without constant squares)."
  - J. Brox, Dec 9, 2024, msg 486936665: "A model of 677 of size 9, found in 32.5h by Mace4 (it also satisfies
    255)", with a table that I re-checked.
  - J. Brox, Jan 10, 2025, msg 492948727: "There is only one model of 677 in size 9 (the linear one). ... I'm
    searching for all models of sizes 10,11 now".
  - **J. Brox, Jan 12, 2025, msg 493229385: "There are no models whatsoever of 677 in size 10 (39h in Mace4)."**
  - J. Brox, Mar 12, 2025, msg 505103036: "We have exhausted: 677 anti 255: size 11 (57 days)." This is about
    counterexamples to 255 only.
- Zulip, Sep 2025 - Feb 2026 (newer):
  - J. Hyun, Sep 25 and Oct 30, 2025, msgs 541356883, 547914401: SAT runs on "+677 −255 magmas of size 12 to 16"
    never terminated ("no sign of termination even for size 12").
  - R. Schneider, Nov 21, 2025, msgs 558558568 and 558558838: "It's a general DPLL-based search, so it should find
    all models -- not idempotent by construction"; "The 'general model search' works til size 11 (which you can
    clear in 3h)."
  - R. Schneider, msg 558760706: the database is "built using: linear/affine models modulus n up to n=50;
    matrix/affine models modulus sqrt(n) up to n=50; a general search up to n=11; a translation invariant search up
    to n=37; a semi translation invariant search up to n=31".
  - M. Bolan, msg 558558444: "There are linear models of order 41, but order 21 is even a new ORDER."
  - B. Le Floch, Nov 21, 2025, msg 558759563: "Up to size 100, there are linear magmas of sizes 5, 7 (two), 9, 11
    (four), 13, 16 (two), 19 (two), 25 (several), 31 (six), 35 (two), 37 (two), 41 (four), 43 (four), 45, 49
    (several), 55 (four), 61 (four), 63 (two), 65, 67 (two), 71 (four), 73 (two), 77 (eight), 80 (two), 81
    (several), 91 (two), 95 (two), 97 (two), 99 (four)."
  - B. Le Floch, Nov 21, 2025, msg 558700555: the size-21 model "is just the projective plane over the finite field
    F4, with each projective line carrying the idempotent magma of size 5". Also: "In that spectrum discussion it
    allowed us to conclude IIRC that the spectrum of E677 contains all integers above some (unknown) value."
    **Caution:** this recollection is not supported by the written argument. GM's note says only "all sufficiently
    large n ≡ 0, 1 (mod 5)", and idempotent linear models exist only at q ≡ 0, 1 (mod 5).
  - B. Le Floch, Nov 28, 2025, msg 560767814: Steiner designs "S(2,5,n) exists exactly for n≡1,5 mod 20 (citing
    Hanini, 1961)". Gluing the 5-element idempotent model along such a design gives models of these orders. Also:
    "one of size 51 (which would be new in the spectrum of 677) ... is equivalent to a long-standing open problem of
    constructing three pairwise-orthogonal Latin squares of size 10."
  - **B. Le Floch, Jan 8, 2026, msg 566939908: "I think the known spectrum ≤100 is now: 1, 5, 7, 9, 11, 13, 16, 19,
    21, 25, 29, 31, 35, 37, 41, 43, 45, 49, 55, 61, 63, 65, 67, 71, 73, 76, 77, 79, 80, 81, 85, 89, 91, 95, 96, 97,
    99."**
    - Later additions: 69 (B. Reinke, Jan 15, 2026, msg 568263276), 57 and 93 (Le Floch, msg 568323398).
    - The same day, msg 567001135: "Do we have any technique to show non-existence for certain sizes?" B. Reinke,
      msg 567004975: "I guess so far we only have the technique to have an exhaustive search return nothing".
  - Non-right-cancellative models: Le Floch, Nov 22, 2025, msg 558778716: "a non-right-cancellative model with 77
    elements ... EDIT: Down to a 55-element model". D. Renshaw, Feb 4, 2026, msg 571795518: such magmas "having
    sizes 55, 77, 121, 143, 155, and 176".
- ETP paper (v2 and Sep 2026):
  - §7.3.1: "for E677 models, Mace4 is able to exhaust size 8 in 1.5s, and to find a model of size 9 in 16s".
  - Table 3: "Time to find one model of E677 of size 9 and to exhaust the same size".
  - Table 4: "certain special E677 models" (LaTeX label `table:Schneider`; the class is not defined in the text).
    One model is found at sizes 9, 11, 13, 16, 19, with "—" at 10, 12, 14, 15, 17, 18, and the class is exhausted up
    to 19. **This says nothing about general models at 12 or 14.**
  - Problem 8.1: E677 ⊨fin E255 is open.
- BP: "Suppose M is a field that admits a primitive cube root of unity ω as well as a primitive fifth root of unity
  ζ (for instance, M could be a field of size 16)"; with G = F31 this gives a 496-element non-right-cancellative
  model.
- GM §3.2: "has ILP g(b) = b⁴ − b³ + b² − b + 1, which has roots in F_q for prime power q if and only if q ≡ 0, 1
  (mod 5) ... so using the techniques here we may only show that all sufficiently large n ≡ 0, 1 (mod 5) are in the
  idempotent spectrum of 677."
- DB (https://dwrensha.github.io/eq677/index.html and raw `db/<n>/<k>`, retrieved Oct 20, 2026):
  - Sizes with models: 1, 5 (1), 7 (2), 9 (1), 11 (4), 13 (1), 16 (2), 19 (2), 21 (4), 25 (48), 29, 31, 35, 37,
    41, 43, 45, 49, 55, 61, 63, 65, 67, 71, 73, 77, 80, 81, 83, 85, 89, 91, 95, 97, 99, 496.
  - Probing `db/n/0` for n = 2..30 returns models only at 5, 7, 9, 11, 13, 16, 19, 21, 25, 29.
  - All re-checked models satisfy 677 and are Latin squares; the order-83 model is idempotent.
  - The database lists found models only. Only n ≤ 11 was searched completely.
- **Newer than July 2025: yes, for 11 and 13 (IN) and for 12 and 14 (still open).** 10 (OUT) dates from Jan 2025.
  It was re-confirmed implicitly by the complete search to 11 (Nov 2025).

### 704: x = y(y((xx)y))
- N: "704 ... has unknown spectrum starting with 1, 5, 7, 8 and no 9. It is a twist of law 73 by the squaring map."
- GM table: "704 ... Idempotent models reduce to 73", saturated by {8, 11}.
- C: "It implies that left multiplications are surjective and the squaring map is injective."
- Nothing newer. 10 and 12 are unaddressed.

### 883: x = y((xy)(yy))
- N: "883 ... (and 1323, 1526) has unknown spectrum containing {1, 2 mod 3}. It is obeyed by semi-symmetric loops
  and idempotent magmas obeying law 73 (parastrophically equivalent to the Dupont law). The size 7 model is such an
  idempotent magma."
- GM table: "883 ... Idempotent models reduce to 118".
- C (Equation883.md): "For finite magmas, or for quasigroups, law 1323, law 1526, and law 2744 are equivalent." Law
  2744 is the dual of 883, so 883 has the finite spectrum of 1323 and 1526.
- Nothing newer. 9 and 12 are unaddressed (8, 10 and 11 are in N's {1, 2 mod 3}).

### 907: x = y((yx)(xy))
- N: "907 ... has unknown spectrum containing 1, 3, 7, 9, 13, and not 2, 4, 5, 6. Models tend to either have a left
  identity or to be commutative and idempotent."
- GM §3.2: 907 has a "modular barrier" to idempotent linear models; the text breaks off.
- C: "This law implies that left multiplications are surjective."
- Nothing newer. 8, 10, 11 and 12 are unaddressed.

### 1076: x = y((x(xy))y)
- N: "1076 ... has unknown spectrum starting with 1, 5, and not having 6 nor 7."
- GM table: "1076 ... ILP −b⁴ + b³ + b² − b + 1, {16, 47}, Splits over F16, 3 is a root mod 47."
- C (last edited Dec 4, 2025): "Finite magmas are quasigroups: both left and right multiplications are bijective.
  In addition, for finite magmas this law implies that the magma operation is idempotent, but not for infinite
  magmas. The free magma with one single generator for this law is infinite, but has no finite quotient other than
  the singleton." It also mentions "a 65-element quasigroup obtained by a cohomological construction".
- ZAP (Nov-Dec 2024): an order 13² = 169 counterexample, reduced to order 65. M. Bolan, Dec 2, 2024, msg 485536350:
  "1076 just doesn't seem to have many small models (I have found no nonlinear ones so far, Mace 4 is currently
  checking order 9)". No result followed.
- Nothing newer about 8-12, and no source addresses 8-12 at all.

### 1083: x = y((x(yx))y)
- N: "1083 ... has unknown spectrum containing 1,3,4,7,8,9. It implies that x□y = x ⋄ (y ⋄ x) obeys law 14."
- GM §3.1: the idempotent spectrum contains no n ≡ 2 (mod 3).
- C: "This law implies that left multiplications are surjective and right multiplications are injective."
- Nothing newer. 10 and 11 are unaddressed; 12 = 3·4 is IN by product.

### 1110: x = y((y(xx))y)
- N: "1110 ... has unknown spectrum starting with 1, 4, 5, 7, 8, 9. It is a twist of law 73 by the squaring map."
- GM table: "Idempotent models reduce to 125", saturated by {8, 11}.
- C: "Finite models of this equation are quasigroups ..., and the squaring map S is bijective ... Models include the
  linear translation-invariant model x ◇ y = x + a(y-x) where a(1-a)² = 1, or the linear model x ◇ y = ϕx - y where
  ϕ² = ϕ + 1." The second family exists over F11 because 5 is a square mod 11, giving another source for 11 ∈ Spec.
  **Transcription caveat (my check):** the first family fails as written, (1−a)x + ay. Over ℤ/p for p = 5, 11, 17,
  19, 23, 37, 43 it holds only with the roles swapped, x ◇ y = ax + (1−a)y = y + a(x−y). The two forms have the same
  root primes (a ↔ 1−a), so the orders they give are unaffected. ϕx − y checks out at every prime tested.
  C also mentions a 25-element quasigroup from a magma extension of ℤ/5ℤ.
- Nothing newer about 8-12. 10 and 12 are unaddressed (and 13, a target of EXP-C05-10).

### 1279: x = y(((xx)y)y)
- N: "1279 ... has unknown spectrum starting with 1, 5, 7, 8 and no 9. It is (dual to) a twist of law 73 by the
  squaring map."
- GM table: "Idempotent models reduce to 118", saturated by {8, 11}.
- C: "It implies that left multiplications are surjective and that S is injective. In a quasigroup this law implies
  that S is bijective."
- Nothing newer. 10 and 12 are unaddressed (and 13).

### 1286: x = y(((xy)x)y)
- N: "1286 ... has unknown spectrum starting with 1, 7."
- ZIS, A. Livne Bar-on, Nov 5, 2024, msg 480795569: "Checked with Mace4, equation 1286 doesn't have models with
  sizes 2-6, the smallest non-trivial model is of order 7"
  (https://leanprover-community.github.io/archive/stream/458659-Equational/topic/Implication.20Statistics.html).
- P (v2, §5.1): "there is always a model of size 2 ≤ n ≤ 5, with the lone exception of E1286 (and its dual E2301),
  for which the smallest non-trivial finite model was of size 7". Example 5.2: the variety "{(a, b) : 1 = ba³ + bab,
  0 = a + ba²b + b²} ... for instance when M = ℤ/pℤ and (p, a, b) = (11, 1, 7)." So 11 is IN (re-checked).
- C (corrected by T. Tao, Aug 19, 2025): "(p,a,b) = (11,1,7)" and "The parameter choice (p,a,b) = (7,6,2) is known to
  give the smallest model".
- GM: modular barrier to idempotent linear models.
- The ETP paper is newer, but its 1286 facts date from 2024. 8, 9, 10 and 12 are unaddressed in the sources (the
  lab has 9).

### 1313: x = y(((yx)x)y)
- N: "1313 ... has unknown spectrum starting with 1, 5, 7."
- GM table: "1313 ... ILP −b⁴ + 3b³ − 2b² + 1, {5, 16, 19}, Splits over F16, 4 is a root mod 5 and 19." Re-checked
  for 5 and 19.
- C: "This law implies that left multiplications are surjective."
- Nothing newer. **No source addresses 8-14.** CLM-C05-13 (8 and 10 OUT) and the 11-14 targets are not in any
  source.

### 1516: x = (yy)(x(xy))
- N: "1516 ... has unknown spectrum starting with 1, 5, 7, 8. It is the Dupont law twisted by the squaring map."
- Z1516 (Oct-Nov 2024, older than the notes and not reflected in them):
  - T. Tao, Oct 23, 2024, msg 478524073: "The smallest non-trivial finite magma is of order 5 ... x⋄y=3x+3y on ℤ/5ℤ
    ... Another linear model is x⋄y=4x+y on ℤ/7ℤ."
  - T. Tao, Oct 24, 2024, msg 478616617: "All finite 1516 models have surjective squaring map."
  - A. Jiang, Nov 4, 2024, msg 480474436: "there's a size 8 model of form (a,b,c) * (d,e,f) =
    (a+b+e,d+e+f+a+c,e+f+b) everything mod 2" (re-checked).
  - A. Livne Bar-on, Nov 4, 2024, msg 480530878: "the three linear models of order 7 ... 4x + y ... 4x + 5y ...
    6x + 2y".
  - **A. Livne Bar-on, Nov 5, 2024, msg 480658028:** "I asked Mace4 for non-idemponent models of order 9, and got
    this one" (table, re-checked). Also: "Order 8 had only idempotent models" (table, re-checked). And: "**There
    were no 1516 magmas of order 10 (this is a merge of results of 2 long runs and I might have had a bug). Order 11
    has a single linear model 7x+5y which is idempotent**, and Mace4 is having a lot of trouble finding a
    non-idempotent model, but hadn't ruled it out yet."
- GM table: "Idempotent models reduce to 63", saturated by {8, 11}.
- C: "This law implies law 255 in linear models, translation-invariant models, and finite magmas"; "a 35-element
  quasigroup" (cohomological); "In quasigroups, this law implies that the squaring map S is bijective".
- Nothing newer than July 2025 about 8-12, but the 2024 thread settles 8, 9 and 11 (IN) and claims 10 OUT.
  **1516 at 10 deserves a certified decision.** 12 is unaddressed.

### 1719: x = (yy)((xx)y)
- N: "1719 ... has unknown spectrum containing {0, 1 mod 3} ∪ {5, 8}, possibly [1, +∞) \ {2}? Indeed, it is obeyed by
  Mendelsohn quasigroups so the spectrum contains {0, 1 mod 3} \ {6}, and magmas of size 5, 6, 8 are easily found by
  an ATP."
- GM §3.1: the idempotent spectrum contains no n ≡ 2 (mod 3).
- C: "A magma satisfying this law is a quasigroup ... and the squaring map S: x ↦ x◇x cubes to the identity
  (S(S(S(x)))=x) and satisfies S(y)◇(x◇y)=S(S(x)) ... The operation x◆y=S(x)◇y satisfies the semi-symmetric
  quasigroup law 14".
- Nothing newer. Among 8-12 only 11 is open; 14, 17, 20, ... are open too.

---------------------------------------------------------------------------------------------------------------

## 6. Structural facts stated in the sources (for the lab's use)

- **Quasigroup forcing for finite models.** These are stated by C:
  - 1076 (finite models are idempotent quasigroups), 1110 (quasigroup, S bijective), 1719 (quasigroup, S³ = id).
  - 467 and 670: left quasigroups. 501: left multiplications bijective. 677: left multiplications bijective.
  - 704 and 1279: S injective (bijective in a quasigroup). 1516: S bijective in quasigroups.
  - Finite 1516 models have surjective squaring (Z1516).
  - Note the general principle in P §7.3.8: "any law of the form x = f(y) ⋄ g(x, y) for some maps f, g has left
    multiplication map L_f(y) surjective, hence bijective".
- **Reductions:**
  - Idempotent models of 467 and 1516 are those of 63; of 704 those of 73; of 883 and 1279 those of 118; of 1110
    those of 125 (GM).
  - 883 ≡ 1323 ≡ 1526 ≡ dual of 2744 for finite magmas (C).
  - 501, 1083 and 1719 map to law 14 (N, C), hence have no idempotent models of order ≡ 2 mod 3 (GM).
- **Infinite families:**
  - 467: odd k²+l², k and l of different parity (N).
  - 883: n ≡ 1, 2 mod 3 (N). 1719: n ≡ 0, 1 mod 3 (N).
  - 677: prime powers ≡ 0, 1 mod 5 and S(2,5,n)-gluings at n ≡ 1, 5 mod 20 (GM, Z677).
  - All large n for 467, 670, 704, 883, 1076, 1110, 1279, 1313, 1516 (GM).
  - The gluing construction (any law x = p(x, y) with idempotent models of sizes S gives every n admitting an
    edge-decomposition of K_n into K_s, s ∈ S) is a standard ETP tool (GM; Le Floch, Z677).
- **Linear-model families:**
  - 677: Type 1 and Type 2 (Z677, Dec 5, 2024).
  - 1110: x + a(y−x) with a(1−a)² = 1, and ϕx − y with ϕ² = ϕ + 1 (C).
  - 1286: the variety {1 = ba³+bab, 0 = a+ba²b+b²} (P); "a root of a⁵+2a⁴+3a³+3a²+a+1" (C).
- **Known non-existence techniques for 677:** only exhaustive search (Z677, Jan 8, 2026). No congruence obstruction
  is stated in any source. My own observation from the Jan 2026 list, not a source claim: the known even orders ≤ 100
  (16, 76, 80, 96) are all ≡ 0 mod 4.

---------------------------------------------------------------------------------------------------------------

## 7. Checks run

`python3 -I reviews/historian_checks/spectra/check_sources.py <dir with eq677 db files>` (run with `nice -n 19`,
under 1 s). Every check of a source claim passed except one: the commentary's first linear family for 1110, as
literally written.

- Linear models stated in sources:
  - 677 over ℤ/11, (a,b) = (10,2), (6,6), (5,7), (4,8); over ℤ/13, (9,11); over ℤ/5, (2,4).
  - 1286 over ℤ/11, (1,7), and over ℤ/7, (6,2).
  - 1516 over ℤ/11, (7,5), and over ℤ/7, (4,1), (4,5), (6,2).
- GM idempotent linear models: 670 (p = 11, b = 6; p = 29, b = 3), 1076 (47, 3), 1313 (5, 4; 19, 4), 467 and 1516
  (11, 5).
- Law 1110, the commentary's families for primes p ≤ 47:
  - ϕx − y with ϕ² = ϕ + 1 holds at p = 5, 11, 19, 29, 31, 41.
  - "x + a(y−x), a(1−a)² = 1" holds at p = 5, 7, 11, 17, 19, 23, 37, 43 only in the form ax + (1−a)y. As written it
    fails except at p = 7.
- Scan of all primes p ≤ 50:
  - The p with an idempotent linear model include 11 for 467, 704, 883, 1110, 1279 and 1516. This supports
    footnote 1 of section 3.
  - 677's idempotent primes are exactly 5, 11, 31 and 41, as GM's q ≡ 0, 1 mod 5 predicts.
- Tables transcribed from Zulip (row = left operand): Brox's order-9 model of 677 and Livne Bar-on's order-9 and
  order-8 models of 1516 satisfy their laws (Latin squares). So does Jiang's 𝔽₂³ formula (order 8).
- eq677 DB: db/5/0, 7/0-1, 9/0, 11/0-3, 13/0, 16/0-1, 19/0-1, 21/0 and 83/0 all satisfy 677. All are Latin squares,
  and all satisfy 255.

---------------------------------------------------------------------------------------------------------------

## 8. Sources read

| # | Source | URL | Extent |
|---|---|---|---|
| 1 | B. Le Floch, *Spectra of equational laws*, notes, July 14, 2025 (37 pp.) | https://leanprover.zulipchat.com/user_uploads/3121/jrBQt8qmSzvI3w359L3p-LVR/spectrum.pdf | §1.1, §2 in full; §4 searched |
| 2 | same, July 10, 2025 (20 pp.) | https://leanprover.zulipchat.com/user_uploads/3121/apvdoKH3jwd1mrnPxZcvlXL_/spectrum.pdf | per-law paragraphs compared with item 1 |
| 3 | same, July 1, 2025 (6 pp., §"Spectrum of laws of order up to 4" only) | https://leanprover.zulipchat.com/user_uploads/3121/2kbrfArXGBOH-Ko9D13RqRkq/spectrum.pdf | per-law paragraphs |
| 4 | B. Le Floch, `spectrum.json` (Jul 1, 2025; 741 entries) | https://leanprover.zulipchat.com/user_uploads/3121/rhtlgrHH1Qio18T61MZeJE-T/spectrum.json | entries of the 15 laws (empty) |
| 5 | B. Gunby-Mann, *Spectra from clique decompositions of K_n* (Jul 14, 2025, 3 pp.) | https://leanprover.zulipchat.com/user_uploads/3121/Ln5Nhztwtnfftwo3eIviWsJV/Two-variable-Clique-Decompositions.pdf | full (text ends mid-sentence) |
| 6 | Zulip archive, topic "Order 3 Spectra" (31 msgs, Jun 29 - Jul 14, 2025) | https://leanprover-community.github.io/archive/stream/458659-Equational/topic/Order.203.20Spectra.html | full |
| 7 | Zulip archive, "FINITE: 677 -> 255" (631 msgs, Dec 5, 2024 - Feb 10, 2026) | https://leanprover-community.github.io/archive/stream/458659-Equational/topic/FINITE.3A.20677.20-.3E.20255.html | searched for sizes; quoted messages read in full, plus Oct 2025 - Feb 2026 in full |
| 8 | Zulip archive, "1516 -> 255" (230 msgs, Oct-Nov 2024) | https://leanprover-community.github.io/archive/stream/458659-Equational/topic/1516.20-.3E.20255.html | searched; quoted messages in full |
| 9 | Zulip archive, "Implication Statistics" (23 msgs, Nov 2024) | https://leanprover-community.github.io/archive/stream/458659-Equational/topic/Implication.20Statistics.html | full |
| 10 | Zulip archive, "Austin pairs" (441 msgs, to Dec 2024) | https://leanprover-community.github.io/archive/stream/458659-Equational/topic/Austin.20pairs.html | searched for the 15 laws |
| 11 | Zulip archive, 21 further topics: Equations with full spectrum; Cheap variations/alternatives to linear models?; Questions for equation commentaries; Some results from order 5; Future directions; Citations to the ETP; Writing the paper; Writing the paper, outstanding tasks 2.0; ATPs; Submitting the paper; Paper sign off; Employing the newest AI tools; Equational classes generated by 3-element magmas; Thoughts and impressions thread; 1076 !=> 3; 1323; An old new idea; Minimal countermodel to order 4 equations; GREEDY-GREEDY HYBRID: Refute 1516->255; Simple and (sub)directly irreducible spectrum; Constructing a database of finite counterexamples | https://leanprover-community.github.io/archive/stream/458659-Equational/ (topic pages) | searched for the 15 numbers and "spectr"; relevant messages read |
| 12 | Zulip archive index of stream Equational (334 topics; "Last updated: Feb 28 2026") | https://leanprover-community.github.io/archive/stream/458659-Equational/index.html | full |
| 13 | ETP contributors (Bolan et al.), *The Equational Theories Project ...*, arXiv:2512.07087v2 (Dec 16, 2025; 74 pp.) | https://arxiv.org/pdf/2512.07087v2 ; https://arxiv.org/abs/2512.07087 | §5.1 + Table 1, Ex. 5.2, §7.3.1, §7.3.6 + Tables 3-4, §8, §9, §14 list, appendices; all "spectr" hits |
| 14 | same, project-site build (PDF of Sep 12, 2026, 76 pp., "Date: December 2025") | https://teorth.github.io/equational_theories/paper.pdf | same sections; sentence diff against item 13 (no substantive change) |
| 15 | Zulip upload `Paper.pdf` (Dec 5, 2025 draft of item 13) | https://leanprover.zulipchat.com/user_uploads/3121/IhxAJmqwYU58D8DBNq598DAz/Paper.pdf | "spectr" hits |
| 16 | ETP repository: `paper/spectrum.tex`, `paper/automated.tex` (Table 4 source), `paper/referee reports/response.tex` | https://raw.githubusercontent.com/teorth/equational_theories/main/paper/spectrum.tex (and siblings) | full / searched |
| 17 | ETP commentary `commentary/Equation{467,501,670,677,704,883,907,1076,1083,1110,1279,1286,1313,1516,1719}.md` (+ 63, 73, 118, 125, 1323, 1526); history of Equation1076.md; PRs #1310, #1390 | https://raw.githubusercontent.com/teorth/equational_theories/main/commentary/ ; https://github.com/teorth/equational_theories/commits/main/commentary/Equation1076.md | full |
| 18 | ETP Lean `equational_theories/FullSpectrum.lean`, `Generated/FullSpectrum.lean` | https://raw.githubusercontent.com/teorth/equational_theories/main/equational_theories/FullSpectrum.lean | theorem statements |
| 19 | ETP repository listings (root, data/, commentary/, paper/, blueprint/src/chapter/, equational_theories/, scripts/) via Software Heritage (visit 2026-09-16, revision 1aec8a7 of 2026-09-12); `data/README.md`, `data/smallest_magma.txt`, `blueprint/src/content.tex`, `chapter/{677,1516,1323,equations,cohomology}.tex` | https://archive.softwareheritage.org/api/1/origin/https://github.com/teorth/equational_theories/visit/latest/ ; raw files as above | listings full; chapters searched |
| 20 | ETP GitHub issues #1029 and #1052, issue search "spectrum" | https://github.com/teorth/equational_theories/issues/1052 ; .../issues/1029 ; .../issues?q=spectrum | full (WebFetch) |
| 21 | eq677 model database (R. Schneider): README, `db/<n>/<k>` (n ≤ 30 probed; 15 files read), visualization by D. Renshaw | https://raw.githubusercontent.com/memoryleak47/eq677/main/README.md ; https://dwrensha.github.io/eq677/index.html | sizes/counts; models re-checked |
| 22 | *EQ677 Model Searcher - User Manual* (J. Brox/Claude, Feb 9, 2026) | https://leanprover.zulipchat.com/user_uploads/3121/mQyEZUe9yk7L6gE2B6EPXs2S/SCHNEIDER_User_Manual_CLAUDE.pdf | searched (no size results) |
| 23 | Zulip uploads: Kisielewicz model for 1516 (infinite model), Not-/Inconclusive-full-spectrum lists | https://leanprover.zulipchat.com/user_uploads/3121/umiLtw_6bEG4SaqiqJ2gB7gf/Kisielewicz-model-for-equation-1516.pdf ; .../YweIiLKR0qUQPnujwVTykHtE/Not-full-spectrum-up-to-4694.txt ; .../nmccj3gcnmTjChImODxTaDfx/Inconclusive-spectrum-up-to-4694.txt | skimmed; not relevant |
| 24 | arXiv API searches (abs:"equational theories project", spectrum+magma, finite models+magma, "equational law", "finite magmas", Dupont/quasigroup spectrum, au:Gunby) and the author feed of B. Le Floch | https://export.arxiv.org/api/query?search_query=... ; https://arxiv.org/a/lefloch_b_1.atom2 | titles/abstracts 2025-2026 |
| 25 | arXiv 2601.20759 (Berlioz-Melliès; "Stone spectrum", a different notion), 2603.29909 and 2609.39872 (Le Floch; 0 hits for "spectr") | https://arxiv.org/pdf/2601.20759v1 ; https://arxiv.org/pdf/2603.29909v1 ; https://arxiv.org/pdf/2609.39872v1 | full-text searched |
| 26 | arXiv abstracts 2602.16324, 2605.21200, 2609.05690, 2604.08446, 2608.15979, 2609.00706, 2603.19487 | https://arxiv.org/abs/<id> | abstracts (none about these spectra) |
| 27 | T. Tao, *Mathematics Distillation Challenge - Equational Theories* (blog, Mar 13, 2026); ETP wiki "Tour of selected equations"; ETP home page; OEIS searches | https://terrytao.wordpress.com/2026/03/13/mathematics-distillation-challenge-equational-theories/ ; https://github.com/teorth/equational_theories/wiki/Tour-of-selected-equations ; https://teorth.github.io/equational_theories/ ; https://oeis.org/search?q=... | WebFetch summary / searched (nothing relevant) |

---------------------------------------------------------------------------------------------------------------

## 9. Failed retrievals and limits

| Target | Result |
|---|---|
| Lean Zulip API, unauthenticated (`https://leanprover.zulipchat.com/api/v1/messages?...narrow=channel Equational`) | `{"result":"error","msg":"Not logged in: API authentication or user session required","code":"UNAUTHORIZED"}`. **Messages after 2026-02-28** (the archive's last update) **were not accessible**. Anything posted on Zulip since March 2026 is unknown to this report. |
| GitHub REST API for teorth/equational_theories (`api.github.com/.../git/trees/main?recursive=1`; `gh api`; GitHub MCP `get_file_contents`) | HTTP 403 from the session proxy ("GitHub access to this repository is not enabled for this session"); MCP: "Access denied: repository ... is not configured for this session". I did not request push access and did not clone (no git). Listings came from Software Heritage instead. |
| `https://github.com/teorth/equational_theories/tree/main/data` with curl | HTTP 403 (proxy). WebFetch to github.com worked and was used for issues, PRs and history. |
| jsDelivr listing `data.jsdelivr.com/v1/package/gh/teorth/equational_theories@main?structure=flat` | 403 "Package size exceeded the configured limit of 50 MB." |
| Software Heritage origin for `https://github.com/memoryleak47/eq677` | 404 "Origin ... not found". The database was probed file by file through raw.githubusercontent.com, so files with k > 5 at sizes ≤ 19 and sizes 31-100 were not all read (counts come from the visualization page). |
| OEIS search for 1,5,7,9,11,13,16,19,21,25 | no match (`null`) |
| arXiv API, first request for 2608.15979 etc. | empty response (0 bytes); the retry succeeded |
| Lean Zulip topics not mirrored or not opened | Only the topics listed in section 8 were read. Messages in other channels and private messages were not searched. |
| Undefined term | ETP paper Table 4, "certain special E677 models": the class is not defined in the paper or its LaTeX source |

---------------------------------------------------------------------------------------------------------------

## 10. Short summary per law: does a source newer than the July 2025 notes say anything about orders 8-12?

- **467**: No. Newer sources (commentary, last edited 2025) say only "unknown". The same-day GM note (Jul 14, 2025)
  implies 11 IN; 10 and 12 are unaddressed.
- **501**: No. Nothing beyond the notes (8, 9 IN). 10, 11 and 12 are unaddressed.
- **670**: No. GM (Jul 14, 2025, not newer) gives 11 IN; 8, 9, 10 and 12 are unaddressed.
- **677** (and 11-14): **Yes.**
  - Zulip "FINITE: 677 -> 255", Sep 2025 - Feb 2026: complete search to 11; Le Floch's "known spectrum ≤100"
    list of Jan 8, 2026.
  - ETP paper v2 (Dec 2025) and its Sep 2026 build: 8 OUT, 9 IN, Table 4.
  - eq677 database (2025-26).
  - Together: 8 OUT, 9 IN, 10 OUT (Mace4, Jan 2025), 11 IN, 13 IN. **12 and 14 are open in every source.**
- **704**: No. Notes: 8 IN, 9 OUT. GM: 11 IN. 10 and 12 are unaddressed.
- **883**: No. Notes: 8, 10, 11 IN. 9 and 12 are unaddressed.
- **907**: No. Notes: 9 IN. 8, 10, 11 and 12 are unaddressed.
- **1076**: No. The commentary (Oct-Dec 2025) adds only structure: finite models are idempotent quasigroups. 8-12
  are unaddressed everywhere.
- **1083**: No. Notes: 8, 9 IN; 12 IN by product. 10 and 11 are unaddressed.
- **1110**: No. Notes: 8, 9 IN. GM and the commentary's ϕ-model: 11 IN. 10 and 12 are unaddressed.
- **1279**: No. Notes: 8 IN, 9 OUT. GM: 11 IN. 10 and 12 are unaddressed.
- **1286**: Only the ETP paper v2 (Dec 2025; facts from 2024) and the commentary: 11 IN. 8, 9, 10 and 12 are
  unaddressed.
- **1313** (and 11-14): No. Nothing about 8-14 in any source. GM (Jul 14, 2025) gives 16 and 19.
- **1516**: No newer source. The older Zulip thread "1516 -> 255" (Nov 2024) gives 8, 9, 11 IN and 10 OUT, the
  last with the author's caveat. 12 is unaddressed.
- **1719** (not asked): No. Notes: 8, 9, 10, 12 IN. 11 is unaddressed.
