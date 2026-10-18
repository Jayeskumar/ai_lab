/* Skeptic check for CLM-C12-03 / CLM-C12-04 (independent of the lab's code).
 *
 * Game G03: from n move to n - d where d | n and 1 < d < n.
 * Computes the exact Grundy values g(0..N) by the mex recursion (divisors from a
 * smallest-prime-factor sieve), then compares with the closed form F written from the
 * English statement of CLM-C12-04, and with the P-set of CLM-C12-03.
 *
 * Build: gcc -O2 -o c12_g03 c12_g03.c
 * Run:   ./c12_g03 N          (prints a JSON-ish report to stdout)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static int v2(uint64_t n) { int a = 0; while (n && !(n & 1)) { n >>= 1; a++; } return a; }

/* closed form of CLM-C12-04, transcribed from the claim statement */
static int F(uint64_t n) {
    if (n == 0 || (n & 1)) return 0;
    int a = v2(n);
    uint64_t m = n >> a;
    if (m >= 17) return a;
    if (m == 1) { if (a == 4) return 2; return (a & 1) ? 0 : a - 1; }
    if (m == 3) { static const int t[6] = {0, 2, 3, 4, 3, 6}; return a <= 5 ? t[a] : a - 2; }
    if (m == 5) { static const int t[6] = {0, 1, 3, 4, 3, 6}; return a <= 5 ? t[a] : a + 2; }
    if (m == 7 || m == 9 || m == 11 || m == 15) return a <= 2 ? a : a + 1;
    if (m == 13) return a <= 3 ? a : a + 1;
    return -1; /* unreachable */
}

static int isP(uint64_t n) { /* CLM-C12-03: 0, odd numbers, 2^(2j+1) */
    if (n == 0 || (n & 1)) return 1;
    if ((n & (n - 1)) == 0 && (v2(n) & 1)) return 1;
    return 0;
}

int main(int argc, char **argv) {
    uint64_t N = argc > 1 ? strtoull(argv[1], 0, 10) : 10000000ULL;
    uint32_t *spf = calloc(N + 1, sizeof(uint32_t));
    uint8_t *g = calloc(N + 1, 1);
    if (!spf || !g) { fprintf(stderr, "alloc failed\n"); return 1; }
    for (uint64_t i = 2; i <= N; i++) if (!spf[i]) for (uint64_t j = i; j <= N; j += i) if (!spf[j]) spf[j] = (uint32_t)i;
    static uint64_t divs[20000];
    uint64_t mism_F = 0, mism_P = 0, first_mism[20]; int nf = 0;
    uint64_t exc_by_m[16] = {0}; uint64_t exc_other = 0; int maxdev = 0; uint64_t maxdev_n = 0;
    int maxg = 0; uint64_t records[200][2]; int nrec = 0; int best = -1;
    uint64_t total_divs = 0;
    for (uint64_t n = 0; n <= N; n++) {
        int val = 0;
        if (n >= 4) {
            /* factorise n, enumerate divisors */
            int nd = 1; divs[0] = 1;
            uint64_t x = n;
            while (x > 1) {
                uint64_t p = spf[x]; int e = 0;
                while (x % p == 0) { x /= p; e++; }
                int cur = nd; uint64_t pk = 1;
                for (int k = 1; k <= e; k++) { pk *= p; for (int i = 0; i < cur; i++) divs[nd++] = divs[i] * pk; }
            }
            uint64_t seen = 0; /* values < 64 */
            for (int i = 0; i < nd; i++) {
                uint64_t d = divs[i];
                if (d > 1 && d < n) { int gv = g[n - d]; if (gv < 64) seen |= (1ULL << gv); else { fprintf(stderr, "value >= 64\n"); return 2; } }
            }
            total_divs += nd;
            while (seen & (1ULL << val)) val++;
        }
        g[n] = (uint8_t)val;
        if (val > maxg) maxg = val;
        if (val > best) { best = val; if (nrec < 200) { records[nrec][0] = n; records[nrec][1] = val; nrec++; } }
        int f = F(n);
        if (f != val) { mism_F++; if (nf < 20) first_mism[nf++] = n; }
        if (isP(n) != (val == 0)) mism_P++;
        if (n >= 1 && !(n & 1)) {
            int a = v2(n); uint64_t m = n >> a;
            if (val != a) { if (m <= 15) exc_by_m[m]++; else exc_other++; }
            int oddpow2 = (m == 1) && (a & 1);
            if (!oddpow2) { int dv = val - a; if (dv < 0) dv = -dv; if (dv > maxdev) { maxdev = dv; maxdev_n = n; } }
        }
    }
    printf("{\"N\": %llu, \"sum_num_divisors\": %llu, \"max_g\": %d,\n", (unsigned long long)N, (unsigned long long)total_divs, maxg);
    printf(" \"mismatches_g_vs_F\": %llu, \"first_mismatches\": [", (unsigned long long)mism_F);
    for (int i = 0; i < nf; i++) printf("%s%llu", i ? ", " : "", (unsigned long long)first_mism[i]);
    printf("],\n \"mismatches_Pset_vs_CLM_C12_03\": %llu,\n", (unsigned long long)mism_P);
    printf(" \"positions_g_ne_v2_by_odd_part\": {");
    int fst = 1;
    for (int m = 1; m <= 15; m += 2) { printf("%s\"%d\": %llu", fst ? "" : ", ", m, (unsigned long long)exc_by_m[m]); fst = 0; }
    printf("}, \"positions_g_ne_v2_odd_part_ge_17\": %llu,\n", (unsigned long long)exc_other);
    printf(" \"max_abs_g_minus_v2_off_odd_powers_of_2\": %d, \"attained_first_at\": %llu,\n", maxdev, (unsigned long long)maxdev_n);
    printf(" \"records\": [");
    for (int i = 0; i < nrec; i++) printf("%s[%llu, %llu]", i ? ", " : "", (unsigned long long)records[i][0], (unsigned long long)records[i][1]);
    printf("]}\n");
    return 0;
}
