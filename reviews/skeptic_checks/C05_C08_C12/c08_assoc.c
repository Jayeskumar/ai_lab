/* Skeptic check for C08: associativity of circle products a o_s b = sum d_i(a) d_j(b) G_{i+j+s}
 * on a greedy numeration system G (G_0 = 1), written independently of systems/circle.py.
 *
 * Usage: ./c08_assoc d c_1..c_d G_0..G_{d-1} smin smax N T R seed
 *   recurrence G_k = c_1 G_{k-1} + ... + c_d G_{k-d} for k >= d (coefficients may be negative)
 *   tests per shift: exhaustive cube [1,N]^3, then T random triples in [1,R]^3
 * Output: one line per shift: "s PASS tested skipped" or "s FAIL a b c".
 * All arithmetic in __int128 with explicit overflow detection (overflowing triples are skipped
 * and counted).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef __int128 i128;
#define LIM (((i128)1) << 122)
static i128 G[512];
static int K;   /* G[0..K] valid, all < LIM */

typedef struct { int n; short idx[160]; i128 dig[160]; } Exp;

static int greedy(i128 n, Exp *e) {   /* returns 0 on failure */
    e->n = 0;
    if (n < 0 || n > LIM) return 0;   /* G[K+1] >= LIM by construction, so the table suffices */
    int k = K;
    while (k >= 0 && G[k] > n) k--;
    for (; k >= 0 && n; k--) {
        if (G[k] <= n) { i128 d = n / G[k]; n -= d * G[k]; e->idx[e->n] = (short)k; e->dig[e->n] = d; e->n++; if (e->n >= 160) return 0; }
    }
    return n == 0;
}

static int circle(const Exp *a, const Exp *b, int s, i128 *out) {
    i128 sum = 0;
    for (int i = 0; i < a->n; i++) for (int j = 0; j < b->n; j++) {
        int idx = a->idx[i] + b->idx[j] + s;
        if (idx > K) return 0;
        i128 dd = a->dig[i] * b->dig[j];
        if (dd > LIM) return 0;
        if (dd > 1 && G[idx] > LIM / dd) return 0;
        sum += dd * G[idx];
        if (sum > LIM) return 0;
    }
    *out = sum;
    return 1;
}

static uint64_t rs;
static uint64_t rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }

static void p128(i128 x) { char buf[64]; int n = 0; if (x == 0) { printf("0"); return; } while (x) { buf[n++] = '0' + (int)(x % 10); x /= 10; } while (n) putchar(buf[--n]); }

/* returns 1 = associative on this triple, 0 = failure, -1 = skipped (overflow) */
static int test(const Exp *ea, const Exp *eb, const Exp *ec, int s) {
    i128 ab, bc, l, r; Exp eab, ebc;
    if (!circle(ea, eb, s, &ab) || !circle(eb, ec, s, &bc)) return -1;
    if (!greedy(ab, &eab) || !greedy(bc, &ebc)) return -1;
    if (!circle(&eab, ec, s, &l) || !circle(ea, &ebc, s, &r)) return -1;
    return l == r;
}

int main(int argc, char **argv) {
    int a_ = 1;
    int d = atoi(argv[a_++]);
    long long c[16], init[16];
    for (int i = 0; i < d; i++) c[i] = atoll(argv[a_++]);
    for (int i = 0; i < d; i++) init[i] = atoll(argv[a_++]);
    int smin = atoi(argv[a_++]), smax = atoi(argv[a_++]);
    int N = atoi(argv[a_++]); long T = atol(argv[a_++]); long long R = atoll(argv[a_++]);
    rs = strtoull(argv[a_++], 0, 10) | 1;
    for (int i = 0; i < d; i++) G[i] = init[i];
    K = d - 1;
    while (K < 500) {
        i128 nx = 0;
        for (int i = 0; i < d; i++) nx += (i128)c[i] * G[K - i];
        if (nx <= G[K]) { printf("ERROR not increasing at %d\n", K + 1); return 1; }
        if (nx >= LIM) break;
        G[++K] = nx;
    }
    for (int i = 1; i <= K; i++) if (G[i] <= G[i - 1]) { printf("ERROR not increasing\n"); return 1; }
    if (G[0] != 1) { printf("ERROR G0 != 1\n"); return 1; }
    Exp *small = malloc(sizeof(Exp) * (N + 1));
    for (int n = 1; n <= N; n++) greedy(n, &small[n]);
    for (int s = smin; s <= smax; s++) {
        long tested = 0, skipped = 0; int failed = 0;
        for (int a = 1; a <= N && !failed; a++) for (int b = 1; b <= N && !failed; b++) for (int cc = 1; cc <= N && !failed; cc++) {
            int r = test(&small[a], &small[b], &small[cc], s);
            if (r < 0) { skipped++; continue; }
            tested++;
            if (r == 0) { printf("%d FAIL %d %d %d\n", s, a, b, cc); failed = 1; }
        }
        for (long t = 0; t < T && !failed; t++) {
            i128 x = 1 + (i128)(rnd() % (uint64_t)R), y = 1 + (i128)(rnd() % (uint64_t)R), z = 1 + (i128)(rnd() % (uint64_t)R);
            Exp ex, ey, ez;
            if (!greedy(x, &ex) || !greedy(y, &ey) || !greedy(z, &ez)) { skipped++; continue; }
            int r = test(&ex, &ey, &ez, s);
            if (r < 0) { skipped++; continue; }
            tested++;
            if (r == 0) { printf("%d FAIL ", s); p128(x); printf(" "); p128(y); printf(" "); p128(z); printf("\n"); failed = 1; }
        }
        if (!failed) printf("%d PASS %ld %ld\n", s, tested, skipped);
        fflush(stdout);
    }
    return 0;
}
