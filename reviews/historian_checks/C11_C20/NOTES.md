# Historian checks for reviews/historian_C11_C20.md (2026-10-19)

All scripts are light (seconds); run from this directory with `python3 -I <script>`
(`laver_first_failing_row.py` imports `laver_wraparound.py`, so run it without `-I`).

| script | purpose | result (2026-10-19) |
|---|---|---|
| `g03_grundy.py` | first Grundy values / P-positions of the deleting-divisors game G03, for the OEIS lookup | 0,0,0,1,0,2,0,0,0,1,0,3,0,1,0,2,0,1,0,3,0,1,0,4,... |
| `laver_wraparound.py` | CLM-C17-05: brute force at N = 3; equivalence "wrap-around at p ⇔ p*N = N ⇔ period(p) divides N"; N ≤ 128 with the full instance | 0 tables at N = 3; 0 violations; full instance exactly at 1, 2, 4, ..., 128 |
| `laver_first_failing_row.py` | topmost row of the recursion table A_N whose period does not divide N (N ≤ 300, N not a power of 2) | always row N − 2^(v2(N)+1), with period 2^(v2(N)+1) |
| `laver_top_block.py` | the [DERIVED] corner-block argument: rows N−2^(k+1)+1..N−1 of A_N are shifted rows of A_(k+1) and row N−2^(k+1) is s+1, ..., N | 0 failures for all 1,013 non-powers of 2 with N ≤ 1024 and 15 further N up to 4095 (1280, 1536, 2304, 2560, 3072, 3584, 3840, 3968, 4032, 4064, 4080, 4088, 4092, 4094, 4095) |
| `klimov_problem75_check.py` | the lab's order-5 full-period cycle (C16 README) read in Klimov's convention u_(k+2) = u_k * u_(k+1) | de Bruijn B(5,2), Latin square, pair map one 25-cycle: a UFS-groupoid that is a quasigroup |

## OEIS queries (https://oeis.org/search?q=...&fmt=json, 2026-10-19; "null" = no match)

| query | claim | result |
|---|---|---|
| 0,0,0,1,0,2,0,0,0,1,0,3,0,1,0,2,0,1,0,3,0,1,0,4 | CLM-C12-04 (G03 Grundy, n ≥ 1) | no match |
| 0,1,0,2,0,0,0,1,0,3,0,1,0,2,0,1,0,3,0,1,0,4,0,1,0,2 | same, shifted window | no match |
| 1,2,3,5,7,8,9,11,13,15,17,19,21,23,25,27,29,31,32,33,35 | G03 P-positions | no match |
| 2,4,8,34,148,1044,12326 | CLM-C14-10 Cartesian/strong primes | no match |
| 8,34,148,1044,12326,274658 | same, window | no match |
| 2,4,9,34,150,1044,12333 | CLM-C14-10 symmetric difference primes | no match |
| 2,4,7,34,142,1044,12310 | CLM-C14-10 lexicographic primes | no match |
| 1,2,2,7,14,54,240,2035,33113 | CLM-C14-13 prime two-graphs | no match |
| 0,1,2,5,10,20,37,67,117,201 | CLM-C19-03 L(F_k) | no match |
| 1,1,2,3,5,8,13,21,34,55 | control | A000045 etc. (endpoint works) |

## Downloads

Each in its own directory under the session scratchpad
(`.../scratchpad/historian2/<name>/`); text extracted with pdftotext. Short sha256 of the
decisive ones: JCIS 2013 `abe56bc385906f90`; Fraenkel–Klein preprint `a39fdbd0e76c4c5f`;
Oh–Yoo–Yun `6dda5406a164393f`; Dürr–Rapaport–Theyssier `8d1d7f1b6ec14799`;
Klimov 2604.05754v2 `35e965a34726c503`; Aguilera–Iannella 2610.06106v1 `fd87dbeb5094a842`;
Biane SLC B80c `ca2563560d477cb0`; Abiad–Butler–Haemers `87779d25a6e90bbb`.
