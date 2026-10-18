/* Skeptic check for CLM-C12-08/11/12/13: subtraction games with sparse move sets, own code.
 * Usage: ./c12_sub kind N      kind in {squares, triangular, fibonacci, primes}
 * Prints P-density and max Grundy value at N/16, N/8, N/4, N/2, N (and powers of 10 up to N).
 * Grundy values are stored as uint8 (abort if a value >= 255 appears).
 * squares/triangular/fibonacci: direct mex over all moves; primes: bitset method
 * (C[v] = set of positions having an option of value v), O(N^2/64).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int main(int argc, char **argv) {
    const char *kind = argv[1];
    long N = atol(argv[2]);
    uint8_t *g = calloc(N + 1, 1);
    long *mv = malloc(sizeof(long) * 200000); long nm = 0;
    if (!strcmp(kind, "squares")) for (long k = 1; k * k <= N; k++) mv[nm++] = k * k;
    else if (!strcmp(kind, "triangular")) for (long k = 1; k * (k + 1) / 2 <= N; k++) mv[nm++] = k * (k + 1) / 2;
    else if (!strcmp(kind, "fibonacci")) { long a = 1, b = 2; mv[nm++] = 1; while (b <= N) { mv[nm++] = b; long c = a + b; a = b; b = c; } }
    long checkpoints[64]; int nc = 0;
    for (long c = 10; c <= N; c *= 10) checkpoints[nc++] = c;
    checkpoints[nc++] = N / 16; checkpoints[nc++] = N / 8; checkpoints[nc++] = N / 4; checkpoints[nc++] = N / 2; checkpoints[nc++] = N;
    long P = 0; int maxg = 0;
    if (strcmp(kind, "primes")) {
        for (long n = 0; n <= N; n++) {
            uint64_t seen[4] = {0, 0, 0, 0};
            for (long i = 0; i < nm && mv[i] <= n; i++) { int v = g[n - mv[i]]; seen[v >> 6] |= 1ULL << (v & 63); }
            int v = 0; while (seen[v >> 6] >> (v & 63) & 1) v++;
            if (v >= 255) { fprintf(stderr, "value too large\n"); return 1; }
            g[n] = (uint8_t)v;
            if (v == 0) P++;
            if (v > maxg) { maxg = v; printf("%s record n=%ld g=%d\n", kind, n, v); }
            for (int c = 0; c < nc; c++) if (checkpoints[c] == n) printf("%s n=%ld P_density=%.6f max_g=%d\n", kind, n, (double)P / (n + 1), maxg);
        }
    } else {
        /* primes: sieve, bitset of primes, C[v] bitsets */
        long W = (N >> 6) + 2;
        uint8_t *comp = calloc(N + 1, 1);
        uint64_t *PB = calloc(W, 8);
        for (long i = 2; i <= N; i++) if (!comp[i]) { PB[i >> 6] |= 1ULL << (i & 63); for (long j = i * i; j <= N && i <= 100000; j += i) comp[j] = 1; }
        int maxv = 40;
        uint64_t **C = malloc(sizeof(uint64_t *) * maxv);
        for (int v = 0; v < maxv; v++) C[v] = calloc(W, 8);
        for (long n = 0; n <= N; n++) {
            int v = 0; while (v < maxv && (C[v][n >> 6] >> (n & 63) & 1)) v++;
            if (v >= maxv - 1) { fprintf(stderr, "value too large\n"); return 1; }
            g[n] = (uint8_t)v;
            if (v == 0) P++;
            if (v > maxg) maxg = v;
            /* every m = n + p (p prime) gets an option of value v: C[v] |= PB << n */
            long ws = n >> 6; int bs = n & 63;
            uint64_t *Cv = C[v];
            for (long i = 0; i + ws < W; i++) {
                uint64_t w = PB[i] << bs;
                if (bs && i > 0) w |= PB[i - 1] >> (64 - bs);
                Cv[i + ws] |= w;
            }
            if (bs) { /* carry of the last word */ }
            for (int c = 0; c < nc; c++) if (checkpoints[c] == n) printf("%s n=%ld P_density=%.6f max_g=%d\n", kind, n, (double)P / (n + 1), maxg);
        }
    }
    return 0;
}
