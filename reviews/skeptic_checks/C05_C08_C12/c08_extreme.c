/* Skeptic check for C08, third method: targeted counterexample search.
 *
 * Associativity of o_s fails when x^s nu(a) nu(b) leaves the image of nu, i.e. (Messaoudi 2000,
 * Arnoux) when the conjugate coordinates rho^s z(a) z(b) leave the window of greedy expansions.
 * So the most dangerous pairs are those whose conjugates z(n) = sum d_i(n) rho^i are extreme.
 * For every n <= N we compute z(n) for one non-dominant root rho (given on the command line),
 * keep the M most extreme n in each of ND directions, and test the embedding identity
 * nu(a o b) = x^s nu(a) nu(b) on all candidate pairs (exact, __int128); a failing pair is
 * certified by an explicit triple (c searched in [1, C] and among the candidates).
 *
 * Usage: ./c08_extreme d c_1..c_d G_0..G_{d-1} re im smin smax N M ND C
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <complex.h>
typedef __int128 i128;
#define LIM (((i128)1) << 120)
static i128 G[600]; static int K, D; static long long cf[16];
static i128 XP[600][16]; static int XPK;
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
static int nu_of(const Exp *e, i128 *v) {
    for (int t = 0; t < D; t++) v[t] = 0;
    for (int i = 0; i < e->n; i++) { int k = e->idx[i]; if (k > XPK) return 0;
        for (int t = 0; t < D; t++) { v[t] += e->dig[i] * XP[k][t]; if (ab128(v[t]) > LIM) return 0; } }
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
static int pair_ok(i128 a, i128 b, int s) {
    Exp ea, eb, ep; i128 P, v1[16], v2[16];
    if (!greedy(a, &ea) || !greedy(b, &eb)) return -1;
    if (!circle(&ea, &eb, s, &P) || !greedy(P, &ep)) return -1;
    if (!nu_of(&ep, v1) || !conv_nu(&ea, &eb, s, v2)) return -1;
    for (int t = 0; t < D; t++) if (v1[t] != v2[t]) return 0;
    return 1;
}
static int triple_assoc(i128 a, i128 b, i128 c, int s) {
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
    double re = atof(argv[q++]), im = atof(argv[q++]);
    int smin = atoi(argv[q++]), smax = atoi(argv[q++]);
    long N = atol(argv[q++]); int M = atoi(argv[q++]); int ND = atoi(argv[q++]); long C = atol(argv[q++]);
    for (int i = 0; i < D; i++) G[i] = init[i];
    K = D - 1;
    while (K < 590) { i128 nx = 0; for (int i = 0; i < D; i++) nx += (i128)cf[i] * G[K - i]; if (nx <= G[K]) { printf("ERROR\n"); return 1; } if (nx >= LIM) break; G[++K] = nx; }
    for (int k = 0; k < 600; k++) for (int t = 0; t < 16; t++) XP[k][t] = 0;
    for (int k = 0; k < D; k++) XP[k][k] = 1;
    XPK = D - 1;
    for (int k = D; k < 590; k++) {
        i128 top = XP[k - 1][D - 1]; int ok = 1;
        for (int t = D - 1; t >= 1; t--) XP[k][t] = XP[k - 1][t - 1];
        XP[k][0] = 0;
        for (int t = 0; t < D; t++) { XP[k][t] += top * (i128)cf[D - 1 - t]; if (ab128(XP[k][t]) > LIM / 64) ok = 0; }
        if (!ok) break;
        XPK = k;
    }
    double complex rho = re + im * I, pw[200];
    pw[0] = 1; for (int i = 1; i < 200; i++) pw[i] = pw[i - 1] * rho;
    /* candidate selection: per direction keep top M scores (simple insertion into sorted arrays) */
    long *cand = calloc((size_t)M * ND, sizeof(long)); double *score = malloc(sizeof(double) * M * ND);
    for (int j = 0; j < M * ND; j++) { cand[j] = 0; score[j] = -1e300; }
    Exp e;
    for (long n = 1; n <= N; n++) {
        greedy(n, &e);
        double complex z = 0; for (int i = 0; i < e.n; i++) z += (double)e.dig[i] * pw[e.idx[i]];
        for (int dir = 0; dir < ND; dir++) {
            double th = 2 * M_PI * dir / ND;
            double sc = creal(z * cexp(-I * th));
            double *S = score + (size_t)dir * M; long *Cn = cand + (size_t)dir * M;
            if (sc <= S[M - 1]) continue;
            int pos = M - 1; while (pos > 0 && S[pos - 1] < sc) { S[pos] = S[pos - 1]; Cn[pos] = Cn[pos - 1]; pos--; }
            S[pos] = sc; Cn[pos] = n;
        }
    }
    /* unique candidate list */
    long *U = malloc(sizeof(long) * M * ND); int nu_ = 0;
    for (int j = 0; j < M * ND; j++) { if (!cand[j]) continue; int dup = 0; for (int t = 0; t < nu_; t++) if (U[t] == cand[j]) { dup = 1; break; } if (!dup) U[nu_++] = cand[j]; }
    for (int s = smin; s <= smax; s++) {
        long np = 0, sk = 0; int done = 0;
        for (int i = 0; i < nu_ && !done; i++) for (int j = i; j < nu_ && !done; j++) {
            int r = pair_ok(U[i], U[j], s);
            if (r < 0) { sk++; continue; }
            np++;
            if (r == 0) {
                long c, cc = -1;
                for (c = 1; c <= C && cc < 0; c++) if (triple_assoc(U[i], U[j], c, s) == 0) cc = c;
                for (int t = 0; t < nu_ && cc < 0; t++) if (triple_assoc(U[i], U[j], U[t], s) == 0) cc = U[t];
                if (cc > 0) printf("%d CERT %ld %ld %ld\n", s, U[i], U[j], cc); else printf("%d CAND %ld %ld\n", s, U[i], U[j]);
                done = 1;
            }
        }
        if (!done) printf("%d NOFAIL %ld %ld candidates=%d\n", s, np, sk, nu_);
        fflush(stdout);
    }
    return 0;
}
