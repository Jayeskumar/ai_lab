/*
 * Skeptic check for C19 (independent code): play the Cusenza strategy from n*e0 for every n in [0, NMAX)
 * (split-type move whenever possible -- here always the LOWEST level with >= 2 chips; otherwise the combine
 * with the smallest index) and print, for each n:  n  length  W  B  splitphase_len  lazy_ok
 * where W = sum over combines C_i (i >= 2) of (i - 1), B = Cusenza's bound sum a_i delta_i, and the split
 * phase is the initial run of split-type moves (its end point is checked to be a 0/1 string without two
 * adjacent zeros below the top, i.e. lazy).
 * A second strategy variant (HIGHEST level with >= 2 chips first) is played for every `every`-th n and its
 * length and split-phase length compared (Lemma 2.2 of Cusenza et al.; Theorem 2 of the lab).
 * usage: c19_greedy NMAX [every]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LV 64
static long FIB[LV + 4];

static long play(long n, int highest_first, long *Wout, long *splitlen, int *lazy_ok) {
    long c[LV + 4];
    memset(c, 0, sizeof c);
    c[0] = n;
    long len = 0, W = 0;
    int in_split_phase = 1;
    int lo = 0;          /* every level below lo holds <= 1 chip (lowest-first variant) */
    int top = 0;         /* highest level that may be occupied */
    *splitlen = 0;
    *lazy_ok = -1;
    for (;;) {
        int k = -1;
        if (!highest_first) {
            for (int j = lo; j <= top; j++) if (c[j] >= 2) { k = j; break; }
        } else {
            for (int j = top; j >= 0; j--) if (c[j] >= 2) { k = j; break; }
        }
        if (k >= 0) {
            c[k] -= 2;
            if (k == 0) c[1] += 1;
            else if (k == 1) { c[0] += 1; c[2] += 1; }
            else { c[k - 2] += 1; c[k + 1] += 1; }
            if (k + 1 > top) top = k + 1;
            if (k == 1 && top < 2) top = 2;
            len++;
            if (in_split_phase) (*splitlen)++;
            lo = k >= 2 ? k - 2 : 0;
            continue;
        }
        if (in_split_phase) {
            in_split_phase = 0;
            int t = -1;
            for (int j = 0; j <= top; j++) if (c[j]) t = j;
            *lazy_ok = 1;
            for (int j = 0; j < t; j++) if (c[j] == 0 && c[j + 1] == 0) *lazy_ok = 0;
            for (int j = 0; j <= t; j++) if (c[j] > 1) *lazy_ok = 0;
        }
        int m = -1;
        for (int j = 0; j + 1 <= top; j++) if (c[j] && c[j + 1]) { m = j; break; }
        if (m < 0) break;
        c[m] -= 1; c[m + 1] -= 1; c[m + 2] += 1;
        if (m + 2 > top) top = m + 2;
        len++;
        W += m + 1;
        lo = m;
    }
    *Wout = W;
    return len;
}

static long bound(long n) {
    long B = 0;
    int k = 0;
    while (FIB[k + 1] <= n) k++;
    for (; k >= 0 && n > 0; k--) {
        if (FIB[k] <= n) { n -= FIB[k]; B += FIB[k + 2] - (k + 1) - 2; }
    }
    return B;
}

int main(int argc, char **argv) {
    long N0 = atol(argv[1]), N1 = atol(argv[2]);
    int every = argc > 3 ? atoi(argv[3]) : 1;
    FIB[0] = 1; FIB[1] = 2;
    for (int i = 2; i < LV + 4; i++) FIB[i] = FIB[i - 1] + FIB[i - 2];
    long bad_identity = 0, bad_variant = 0, bad_lazy = 0, nvar = 0;
    for (long n = N0; n < N1; n++) {
        long W, sl, W2, sl2; int lz, lz2;
        long L = play(n, 0, &W, &sl, &lz);
        long B = bound(n);
        if (L != B - W) bad_identity++;
        if (n > 0 && lz != 1) bad_lazy++;
        if (every && n % every == 0) {
            long L2 = play(n, 1, &W2, &sl2, &lz2);
            nvar++;
            if (L2 != L || sl2 != sl || W2 != W) bad_variant++;
        }
        printf("%ld %ld %ld %ld %ld %d\n", n, L, W, B, sl, lz);
    }
    fprintf(stderr, "range=[%ld,%ld) bad_identity=%ld variants_checked=%ld bad_variant=%ld bad_lazy=%ld\n",
            N0, N1, bad_identity, nvar, bad_variant, bad_lazy);
    return 0;
}
