/* Skeptic check for C08, second method (own implementation of the embedding criterion).
 *
 * For G_k = c_1 G_{k-1} + ... + c_d G_{k-d}, let nu(n) = sum_i d_i(n) x^i reduced modulo
 * chi(x) = x^d - c_1 x^{d-1} - ... - c_d (d_i = greedy digits).  If nu(a o_s b) = x^s nu(a) nu(b)
 * for all a, b then o_s is associative.  A pair violating the identity is a candidate; an explicit
 * triple with (a o b) o c != a o (b o c) (c searched in [1, C]) certifies non-associativity.
 *
 * Usage: ./c08_pairs d c_1..c_d G_0..G_{d-1} smin smax A T R C seed
 *   pairs: all 1 <= a <= b <= A, then T random pairs in [1,R]^2
 * Output per shift: "s CERT a b c" | "s CAND a b (no c <= C)" | "s NOFAIL pairs skipped"
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef __int128 i128;
#define LIM (((i128)1) << 120)
static i128 G[600]; static int K, D; static long long cf[16];
static i128 XP[600][16];   /* x^k mod chi, coefficient vectors (basis 1, x, ..., x^{D-1}) */
static int XPK;            /* valid up to XPK (all |coef| < LIM) */

typedef struct { int n; short idx[200]; i128 dig[200]; } Exp;
static int greedy(i128 n, Exp *e) {
    e->n = 0; if (n < 0 || n > LIM) return 0;
    int k = K; while (k >= 0 && G[k] > n) k--;
    for (; k >= 0 && n; k--) if (G[k] <= n) { i128 q = n / G[k]; n -= q * G[k]; e->idx[e->n] = (short)k; e->dig[e->n++] = q; if (e->n >= 200) return 0; }
    return n == 0;
}
static int circle(const Exp *a, const Exp *b, int s, i128 *out) {
    i128 sum = 0;
    for (int i = 0; i < a->n; i++) for (int j = 0; j < b->n; j++) {
        int idx = a->idx[i] + b->idx[j] + s; if (idx > K) return 0;
        i128 dd = a->dig[i] * b->dig[j]; if (dd > LIM || (dd > 1 && G[idx] > LIM / dd)) return 0;
        sum += dd * G[idx]; if (sum > LIM) return 0;
    }
    *out = sum; return 1;
}
static i128 ab128(i128 x) { return x < 0 ? -x : x; }
/* nu(P) and x^s nu(a) nu(b) as coefficient vectors; returns 0 on overflow */
static int nu_of(const Exp *e, i128 *v) {
    for (int t = 0; t < D; t++) v[t] = 0;
    for (int i = 0; i < e->n; i++) { int k = e->idx[i]; if (k > XPK) return 0;
        for (int t = 0; t < D; t++) { i128 add = e->dig[i] * XP[k][t]; v[t] += add; if (ab128(v[t]) > LIM) return 0; } }
    return 1;
}
static int conv_nu(const Exp *a, const Exp *b, int s, i128 *v) {
    for (int t = 0; t < D; t++) v[t] = 0;
    for (int i = 0; i < a->n; i++) for (int j = 0; j < b->n; j++) {
        int k = a->idx[i] + b->idx[j] + s; if (k > XPK) return 0;
        i128 dd = a->dig[i] * b->dig[j];
        for (int t = 0; t < D; t++) { if (XP[k][t] != 0 && ab128(dd) > LIM / ab128(XP[k][t])) return 0; v[t] += dd * XP[k][t]; if (ab128(v[t]) > LIM) return 0; }
    }
    return 1;
}
static uint64_t rs; static uint64_t rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static void p128(i128 x) { char b[64]; int n = 0; if (!x) { printf("0"); return; } while (x) { b[n++] = '0' + (int)(x % 10); x /= 10; } while (n) putchar(b[--n]); }

/* 1 = identity holds, 0 = fails, -1 = overflow */
static int pair_ok(i128 a, i128 b, int s, Exp *ea, Exp *eb) {
    i128 P; Exp ep; i128 v1[16], v2[16];
    if (!greedy(a, ea) || !greedy(b, eb)) return -1;
    if (!circle(ea, eb, s, &P) || !greedy(P, &ep)) return -1;
    if (!nu_of(&ep, v1) || !conv_nu(ea, eb, s, v2)) return -1;
    for (int t = 0; t < D; t++) if (v1[t] != v2[t]) return 0;
    return 1;
}
static int triple_assoc(i128 a, i128 b, i128 c, int s) {  /* 1 assoc, 0 not, -1 overflow */
    Exp ea, eb, ec, eab, ebc; i128 ab, bc, l, r;
    if (!greedy(a, &ea) || !greedy(b, &eb) || !greedy(c, &ec)) return -1;
    if (!circle(&ea, &eb, s, &ab) || !circle(&eb, &ec, s, &bc)) return -1;
    if (!greedy(ab, &eab) || !greedy(bc, &ebc)) return -1;
    if (!circle(&eab, &ec, s, &l) || !circle(&ea, &ebc, s, &r)) return -1;
    return l == r;
}
int main(int argc, char **argv) {
    int q = 1; D = atoi(argv[q++]); long long init[16];
    for (int i = 0; i < D; i++) cf[i] = atoll(argv[q++]);
    for (int i = 0; i < D; i++) init[i] = atoll(argv[q++]);
    int smin = atoi(argv[q++]), smax = atoi(argv[q++]); long A = atol(argv[q++]); long T = atol(argv[q++]);
    long long R = atoll(argv[q++]); long C = atol(argv[q++]); rs = strtoull(argv[q++], 0, 10) | 1;
    for (int i = 0; i < D; i++) G[i] = init[i];
    K = D - 1;
    while (K < 590) { i128 nx = 0; for (int i = 0; i < D; i++) nx += (i128)cf[i] * G[K - i]; if (nx <= G[K]) { printf("ERROR not increasing\n"); return 1; } if (nx >= LIM) break; G[++K] = nx; }
    /* x^k mod chi: x^D = c_1 x^{D-1} + ... + c_D */
    for (int k = 0; k < 600; k++) for (int t = 0; t < 16; t++) XP[k][t] = 0;
    for (int k = 0; k < D; k++) XP[k][k] = 1;
    XPK = D - 1;
    for (int k = D; k < 590; k++) {
        /* x^k = x * x^{k-1}: shift, reduce top coefficient */
        i128 top = XP[k - 1][D - 1]; int ok = 1;
        for (int t = D - 1; t >= 1; t--) XP[k][t] = XP[k - 1][t - 1];
        XP[k][0] = 0;
        for (int t = 0; t < D; t++) { i128 add = top * (i128)cf[D - 1 - t]; XP[k][t] += add; if (ab128(XP[k][t]) > LIM / 64) ok = 0; }
        if (!ok) break;
        XPK = k;
    }
    for (int s = smin; s <= smax; s++) {
        long npairs = 0, skipped = 0; int done = 0;
        Exp ea, eb;
        for (long a = 1; a <= A && !done; a++) for (long b = a; b <= A && !done; b++) {
            int r = pair_ok(a, b, s, &ea, &eb);
            if (r < 0) { skipped++; continue; }
            npairs++;
            if (r == 0) {
                long c; int found = 0;
                for (c = 1; c <= C; c++) { int t = triple_assoc(a, b, c, s); if (t == 0) { found = 1; break; } }
                if (found) printf("%d CERT %ld %ld %ld\n", s, a, b, c); else printf("%d CAND %ld %ld\n", s, a, b);
                done = 1;
            }
        }
        for (long t = 0; t < T && !done; t++) {
            i128 a = 1 + (i128)(rnd() % (uint64_t)R), b = 1 + (i128)(rnd() % (uint64_t)R);
            int r = pair_ok(a, b, s, &ea, &eb);
            if (r < 0) { skipped++; continue; }
            npairs++;
            if (r == 0) {
                long c; int found = 0;
                for (c = 1; c <= C; c++) { int tt = triple_assoc(a, b, c, s); if (tt == 0) { found = 1; break; } }
                printf("%d %s ", s, found ? "CERT" : "CAND"); p128(a); printf(" "); p128(b);
                if (found) printf(" %ld", c);
                printf("\n"); done = 1;
            }
        }
        if (!done) printf("%d NOFAIL %ld %ld\n", s, npairs, skipped);
        fflush(stdout);
    }
    return 0;
}
