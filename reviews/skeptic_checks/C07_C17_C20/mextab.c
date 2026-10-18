/* Skeptic check (C07): mex operations computed directly from the definition.
 *
 * Spec encoding (my own): idx in [0, 512): L = (idx >> 8) & 1, R = (idx >> 7) & 1,
 * D = idx & 127, where bit (m-1) of D set means mask m in {1..7} is an option:
 *   mask bit 1 -> x = f(a', b), bit 2 -> y = f(a, b'), bit 4 -> z = f(a', b'),
 *   option value = XOR of the selected values, for every a' < a, b' < b.
 * L adds f(a', b) for all a' < a; R adds f(a, b') for all b' < b.
 * f(a, b) = mex of the option values.
 *
 * Modes:
 *   mextab rect NR NC OUTFILE [idx...]   tables NR x NC (int32, row-major) for the listed specs
 *                                        (all 512 if none listed), concatenated in the listed order
 *   mextab jac NB OUTFILE                rows 0..2 of D[x^y] (mask 3 only) for b < NB, computed
 *                                        from the definition (rows 0 and 1 are not assumed); writes row 2
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define VMAX (1 << 20)
static uint32_t stamp[VMAX];
static uint32_t cur = 0;

static void mark(int32_t v) {
    if (v < 0 || v >= VMAX) { fprintf(stderr, "value out of range %d\n", v); exit(2); }
    stamp[v] = cur;
}

static int32_t mex_now(void) {
    int32_t v = 0;
    while (stamp[v] == cur) v++;
    return v;
}

static void table(int idx, int NR, int NC, int32_t *f) {
    int L = (idx >> 8) & 1, R = (idx >> 7) & 1, D = idx & 127;
    int masks[7], nm = 0;
    for (int m = 1; m <= 7; m++) if (D & (1 << (m - 1))) masks[nm++] = m;
    for (int a = 0; a < NR; a++) {
        for (int b = 0; b < NC; b++) {
            cur++;
            if (cur == 0) { memset(stamp, 0, sizeof stamp); cur = 1; }
            if (L) for (int ap = 0; ap < a; ap++) mark(f[ap * NC + b]);
            if (R) for (int bp = 0; bp < b; bp++) mark(f[a * NC + bp]);
            if (nm) {
                for (int ap = 0; ap < a; ap++) {
                    int32_t x = f[ap * NC + b];
                    for (int bp = 0; bp < b; bp++) {
                        int32_t y = f[a * NC + bp], z = f[ap * NC + bp];
                        for (int t = 0; t < nm; t++) {
                            int m = masks[t];
                            int32_t v = 0;
                            if (m & 1) v ^= x;
                            if (m & 2) v ^= y;
                            if (m & 4) v ^= z;
                            mark(v);
                        }
                    }
                }
            }
            f[a * NC + b] = mex_now();
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage\n"); return 1; }
    if (!strcmp(argv[1], "rect")) {
        int NR = atoi(argv[2]), NC = atoi(argv[3]);
        FILE *out = fopen(argv[4], "wb");
        int32_t *f = malloc(sizeof(int32_t) * NR * NC);
        int nidx = argc - 5;
        for (int k = 0; k < (nidx ? nidx : 512); k++) {
            int idx = nidx ? atoi(argv[5 + k]) : k;
            table(idx, NR, NC, f);
            fwrite(f, sizeof(int32_t), (size_t)NR * NC, out);
        }
        fclose(out);
        free(f);
        return 0;
    }
    if (!strcmp(argv[1], "jac")) {
        int NB = atoi(argv[2]);
        FILE *out = fopen(argv[3], "wb");
        int32_t *r0 = malloc(sizeof(int32_t) * NB), *r1 = malloc(sizeof(int32_t) * NB),
                *r2 = malloc(sizeof(int32_t) * NB);
        /* f(a,b) = mex{ f(a',b) XOR f(a,b') : a' < a, b' < b } */
        for (int b = 0; b < NB; b++) {
            /* row 0: no a' < 0 */
            cur++; r0[b] = mex_now();
            /* row 1: a' = 0 */
            cur++;
            for (int bp = 0; bp < b; bp++) mark(r0[b] ^ r1[bp]);
            r1[b] = mex_now();
            /* row 2: a' in {0, 1} */
            cur++;
            for (int bp = 0; bp < b; bp++) { mark(r0[b] ^ r2[bp]); mark(r1[b] ^ r2[bp]); }
            r2[b] = mex_now();
        }
        int bad0 = 0, bad1 = 0;
        for (int b = 0; b < NB; b++) { if (r0[b] != 0) bad0++; if (r1[b] != b) bad1++; }
        fprintf(stderr, "row0 != 0 at %d places; row1 != b at %d places\n", bad0, bad1);
        fwrite(r2, sizeof(int32_t), NB, out);
        fclose(out);
        return 0;
    }
    return 1;
}
