/*
 * Skeptic check for cycle C19 (independent of systems/ and lab/).
 *
 * Exhaustive analysis of the Zeckendorf game for every n in [N0, N1].
 * Levels k = 0, 1, 2, ... carry FIB[k] = F_{k+1} = 1, 2, 3, 5, 8, ... (paper index i = k + 1).
 * Moves (from Cusenza et al. 2022, Def. 1.1):
 *   C1 : 2[0] -> [1]                      (split-type: "combine 1s")
 *   S2 : 2[1] -> [0] + [2]                (split-type)
 *   S_{k+1}, k >= 2 : 2[k] -> [k-2] + [k+1] (split-type)
 *   C_{k+2}, k >= 0 : [k] + [k+1] -> [k+2]  (combine; weight/excess k + 1 = i - 1)
 *
 * For each n all positions of value n (= all partitions of n into Fibonacci parts) are enumerated,
 * and over this DAG we compute
 *   f(P)      : longest number of moves from P to the end (no strategy assumed)
 *   smin/smax : min/max length over paths that follow the Cusenza strategy (split-type move whenever
 *               possible, any of them; otherwise the combine with the smallest index)
 *   wmin(P)   : min total excess sum (i-1) over the combines C_i (i >= 2) of any path to the end
 *   split stabilisation: end point of maximal split-type sequences (uniqueness checked), min/max length
 * and check:
 *   (a) every position is reachable from n*e0                                  (Prop. 6, CLM-C19-08)
 *   (b) potential Psi = sum c_k w_k, w_k = FIB[k+2] - k - 3, changes by 1 + excess on every move
 *       (Thm 1, CLM-C19-01), and f(P) = B(n) - Psi(P) - wmin(P) for every P
 *   (c) smin(P) = smax(P) = f(P) for every P  (strategy optimal from ANY position, Cusenza Thm 1.2/L2.3)
 *   (d) split-type moves from every P have a unique end point and a unique length  (Thm 2 (a))
 *   (e) the end point from n*e0 is a 0/1 string without two adjacent zeros below the top (Thm 2)
 * Output: one line per n:  n states L B D splitlen lazydigits flags
 *
 * usage: c19_exact N0 N1 [mode]   mode 0 = all checks (default), 1 = only f and strategy (less memory)
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXK 20
static long FIB[64];
static int K;               /* number of levels with FIB[k] <= n */
static uint64_t RAD[MAXK + 1]; /* mixed radix multipliers */
static long NN;

static uint64_t *keys;
static long npos, cap;

static void gen(int k, long rem, uint64_t key) {
    if (k == 0) {
        key += (uint64_t)rem * RAD[0];
        if (npos == cap) {
            cap = cap ? 2 * cap : 1024;
            keys = realloc(keys, cap * sizeof(uint64_t));
            if (!keys) { fprintf(stderr, "oom\n"); exit(1); }
        }
        keys[npos++] = key;
        return;
    }
    for (long c = 0; c * FIB[k] <= rem; c++) gen(k - 1, rem - c * FIB[k], key + (uint64_t)c * RAD[k]);
}

static int cmpu64(const void *a, const void *b) {
    uint64_t x = *(const uint64_t *)a, y = *(const uint64_t *)b;
    return x < y ? -1 : x > y;
}

static void decode(uint64_t key, int *c) {
    for (int k = 0; k < K; k++) {
        uint64_t m = RAD[k + 1] / RAD[k];
        c[k] = (int)(key % m);
        key /= m;
    }
}

static uint64_t encode(const int *c) {
    uint64_t key = 0;
    for (int k = 0; k < K; k++) key += (uint64_t)c[k] * RAD[k];
    return key;
}

static long find(uint64_t key) {
    long lo = 0, hi = npos - 1;
    while (lo <= hi) {
        long mid = (lo + hi) / 2;
        if (keys[mid] == key) return mid;
        if (keys[mid] < key) lo = mid + 1; else hi = mid - 1;
    }
    return -1;
}

static long w(int k) { return FIB[k + 2] - k - 3; } /* a_{k+1} = F_{k+3} - (k+1) - 2 */

typedef struct { int type; int k; } Move;   /* type 0 = split-type (C1/S2/S), 1 = combine C_{k+2} */

static int moves_of(const int *c, Move *mv) {
    int m = 0;
    for (int k = 0; k < K; k++) {
        if (c[k] >= 2) { mv[m].type = 0; mv[m].k = k; m++; }
    }
    for (int k = 0; k + 1 < K; k++) {
        if (c[k] >= 1 && c[k + 1] >= 1) { mv[m].type = 1; mv[m].k = k; m++; }
    }
    return m;
}

static int apply(const int *c, Move mv, int *d) {
    memcpy(d, c, sizeof(int) * K);
    int k = mv.k;
    if (mv.type == 0) {
        d[k] -= 2;
        if (k == 0) d[1] += 1;
        else if (k == 1) { d[0] += 1; d[2] += 1; }
        else { d[k - 2] += 1; d[k + 1] += 1; }
        return 0;          /* excess 0 */
    } else {
        d[k] -= 1; d[k + 1] -= 1; d[k + 2] += 1;
        return k + 1;      /* excess i - 1 with i = k + 2 */
    }
}

static long *psi;
static int cmp_by_psi_desc(const void *a, const void *b) {
    long x = psi[*(const long *)a], y = psi[*(const long *)b];
    return x > y ? -1 : x < y;
}

int main(int argc, char **argv) {
    long N0 = atol(argv[1]), N1 = atol(argv[2]);
    int mode = argc > 3 ? atoi(argv[3]) : 0;
    FIB[0] = 1; FIB[1] = 2;
    for (int i = 2; i < 64; i++) FIB[i] = FIB[i - 1] + FIB[i - 2];
    for (long n = N0; n <= N1; n++) {
        NN = n;
        K = 0;
        while (FIB[K] <= n) K++;
        if (n == 0) K = 1;
        if (K + 2 > MAXK) { fprintf(stderr, "too many levels\n"); return 1; }
        /* levels K, K+1 are never occupied (value would exceed n); give them radix 1 slots anyway */
        RAD[0] = 1;
        for (int k = 0; k < K; k++) RAD[k + 1] = RAD[k] * (uint64_t)(n / FIB[k] + 1);
        npos = 0;
        gen(K - 1, n, 0);
        qsort(keys, npos, sizeof(uint64_t), cmpu64);
        int c[MAXK + 2], d[MAXK + 2];
        Move mv[2 * MAXK + 4];
        memset(c, 0, sizeof c); memset(d, 0, sizeof d);
        psi = malloc(npos * sizeof(long));
        long *order = malloc(npos * sizeof(long));
        int *f = malloc(npos * sizeof(int));
        int *smin = malloc(npos * sizeof(int)), *smax = malloc(npos * sizeof(int));
        int *wmin = NULL, *lmin = NULL, *lmax = NULL;
        long *send = NULL;
        unsigned char *reach = NULL;
        if (mode == 0) {
            wmin = malloc(npos * sizeof(int));
            lmin = malloc(npos * sizeof(int)); lmax = malloc(npos * sizeof(int));
            send = malloc(npos * sizeof(long));
            reach = calloc(npos, 1);
        }
        for (long p = 0; p < npos; p++) {
            decode(keys[p], c);
            long s = 0;
            for (int k = 0; k < K; k++) s += c[k] * w(k);
            psi[p] = s;
            order[p] = p;
        }
        qsort(order, npos, sizeof(long), cmp_by_psi_desc);
        long bad_dpsi = 0, bad_identity = 0, bad_strategy = 0, bad_split_unique = 0, bad_split_len = 0;
        long terminal = -1, nterminal = 0;
        for (long t = 0; t < npos; t++) {
            long p = order[t];
            decode(keys[p], c);
            int m = moves_of(c, mv);
            if (m == 0) {
                f[p] = 0; smin[p] = 0; smax[p] = 0;
                if (mode == 0) { wmin[p] = 0; lmin[p] = 0; lmax[p] = 0; send[p] = p; }
                terminal = p; nterminal++;
                continue;
            }
            int best = -1, bw = 1 << 30;
            int hasSplit = 0;
            for (int j = 0; j < m; j++) if (mv[j].type == 0) hasSplit = 1;
            int sm = 1 << 30, sM = -1;
            int lm = 1 << 30, lM = -1;
            long se = -2;
            int smallest_combine = -1;
            for (int j = 0; j < m; j++) if (mv[j].type == 1) { smallest_combine = j; break; }
            for (int j = 0; j < m; j++) {
                int ex = apply(c, mv[j], d);
                uint64_t key = encode(d);
                long q = find(key);
                if (q < 0) { fprintf(stderr, "successor not found n=%ld\n", n); return 1; }
                if (psi[q] - psi[p] != 1 + ex) bad_dpsi++;
                if (f[q] + 1 > best) best = f[q] + 1;
                if (mode == 0 && wmin[q] + ex < bw) bw = wmin[q] + ex;
                int compliant = hasSplit ? (mv[j].type == 0) : (j == smallest_combine);
                if (compliant) {
                    if (smin[q] + 1 < sm) sm = smin[q] + 1;
                    if (smax[q] + 1 > sM) sM = smax[q] + 1;
                }
                if (mode == 0 && mv[j].type == 0) {
                    if (lmin[q] + 1 < lm) lm = lmin[q] + 1;
                    if (lmax[q] + 1 > lM) lM = lmax[q] + 1;
                    if (se == -2) se = send[q];
                    else if (se != send[q]) bad_split_unique++;
                }
            }
            f[p] = best; smin[p] = sm; smax[p] = sM;
            if (sm != best || sM != best) bad_strategy++;
            if (mode == 0) {
                wmin[p] = bw;
                if (hasSplit) { lmin[p] = lm; lmax[p] = lM; send[p] = se; if (lm != lM) bad_split_len++; }
                else { lmin[p] = 0; lmax[p] = 0; send[p] = p; }
            }
        }
        /* start position n*e0 */
        memset(c, 0, sizeof c);
        c[0] = (int)n;
        long start = find(encode(c));
        long B = psi[terminal];
        if (mode == 0) {
            for (long p = 0; p < npos; p++) if (f[p] != B - psi[p] - wmin[p]) bad_identity++;
            /* reachability from start: positions in increasing psi order are processed after predecessors */
            reach[start] = 1;
            for (long t = npos - 1; t >= 0; t--) {   /* increasing psi */
                long p = order[t];
                if (!reach[p]) continue;
                decode(keys[p], c);
                int m = moves_of(c, mv);
                for (int j = 0; j < m; j++) {
                    apply(c, mv[j], d);
                    reach[find(encode(d))] = 1;
                }
            }
        }
        long nreach = 0;
        if (mode == 0) for (long p = 0; p < npos; p++) nreach += reach[p];
        /* split end point from start */
        char lazy[64] = "";
        int lazy_ok = -1, splitlen = -1;
        if (mode == 0) {
            decode(keys[send[start]], c);
            int top = -1;
            for (int k = 0; k < K; k++) if (c[k]) top = k;
            lazy_ok = 1;
            for (int k = 0; k <= top; k++) {
                if (c[k] > 1) lazy_ok = 0;
                if (k + 1 <= top && c[k] == 0 && c[k + 1] == 0) lazy_ok = 0;
                lazy[k] = (char)('0' + c[k]);
            }
            lazy[top + 1] = 0;
            splitlen = lmin[start];
        }
        /* terminal digits must be Zeckendorf: 0/1, no two adjacent ones */
        decode(keys[terminal], c);
        int zeck_ok = 1;
        for (int k = 0; k < K; k++) {
            if (c[k] > 1) zeck_ok = 0;
            if (k + 1 < K && c[k] && c[k + 1]) zeck_ok = 0;
        }
        printf("%ld %ld %d %ld %ld %d %s reach=%ld nterm=%ld zeck=%d lazy=%d bad_dpsi=%ld bad_identity=%ld "
               "bad_strategy=%ld bad_split_unique=%ld bad_split_len=%ld\n",
               n, npos, f[start], B, B - f[start], splitlen, lazy, nreach, nterminal, zeck_ok, lazy_ok,
               bad_dpsi, bad_identity, bad_strategy, bad_split_unique, bad_split_len);
        fflush(stdout);
        free(psi); free(order); free(f); free(smin); free(smax);
        if (mode == 0) { free(wmin); free(lmin); free(lmax); free(send); free(reach); }
    }
    return 0;
}
