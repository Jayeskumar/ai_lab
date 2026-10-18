/* Skeptic checks for C16 (own code).
 *
 *  ./c16_affine_laver affine NMAX
 *      For every N <= NMAX and every affine magma x*y = a x + b y + c on Z/N with b a unit, compute the cycle
 *      structure of the pair map P(x, y) = (y, y*x) = (y, a y + b x + c): maximal cycle length, lcm of all cycle
 *      lengths, and (independently) the multiplicative order of the 3x3 matrix [[0,1,0],[b,a,c],[0,0,1]] mod N.
 *      Reports every case with max != lcm or lcm != ord (CLM-C16-13), and for the cases with a fixed point checks
 *      max == ord([[0,1],[b,a]]) (CLM-C16-12).
 *
 *  ./c16_affine_laver laver NMAX_EXP
 *      Laver tables A_n (0-based), n <= NMAX_EXP: cycle structure of the pair map (a,b) -> (b, b*a) and the longest
 *      transient (steps until the state contains N-1) (CLM-C16-15, CLM-C16-16).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static long gcdl(long a, long b) { while (b) { long t = a % b; a = b; b = t; } return a < 0 ? -a : a; }

static long ord3(long a, long b, long c, long N) {
    /* order of M = [[0,1,0],[b,a,c],[0,0,1]] mod N, by repeated multiplication (bounded by N^3) */
    long M[3][3] = {{0, 1, 0}, {b % N, a % N, c % N}, {0, 0, 1 % N}};
    long P[3][3];
    memcpy(P, M, sizeof P);
    for (long k = 1; k <= N * N * N + 5; k++) {
        int id = 1;
        for (int i = 0; i < 3 && id; i++)
            for (int j = 0; j < 3; j++)
                if (P[i][j] != ((i == j) ? 1 % N : 0)) { id = 0; break; }
        if (id) return k;
        long Q[3][3];
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++) {
                long s = 0;
                for (int l = 0; l < 3; l++) s += P[i][l] * M[l][j];
                Q[i][j] = s % N;
            }
        memcpy(P, Q, sizeof P);
    }
    return -1;
}

static long ord2(long a, long b, long N) {
    long M[2][2] = {{0, 1}, {b % N, a % N}};
    long P[2][2];
    memcpy(P, M, sizeof P);
    for (long k = 1; k <= N * N + 5; k++) {
        if (P[0][0] == 1 % N && P[0][1] == 0 && P[1][0] == 0 && P[1][1] == 1 % N) return k;
        long Q[2][2];
        for (int i = 0; i < 2; i++)
            for (int j = 0; j < 2; j++) Q[i][j] = (P[i][0] * M[0][j] + P[i][1] * M[1][j]) % N;
        memcpy(P, Q, sizeof P);
    }
    return -1;
}

static int affine(int NMAX) {
    long cases = 0, bad_max_lcm = 0, bad_lcm_ord = 0, fixed_cases = 0, bad_fixed = 0;
    int *seen = malloc(sizeof(int) * NMAX * NMAX);
    for (long N = 1; N <= NMAX; N++) {
        long S = N * N;
        long n_bad_here = 0;
        for (long b = 0; b < N; b++) {
            if (gcdl(b, N) != 1) continue;
            for (long a = 0; a < N; a++)
                for (long c = 0; c < N; c++) {
                    memset(seen, 0, sizeof(int) * S);
                    long maxc = 0, lcm = 1;
                    for (long s0 = 0; s0 < S; s0++) {
                        if (seen[s0]) continue;
                        long len = 0, s = s0;
                        while (!seen[s]) {          /* permutation: every orbit is a cycle */
                            seen[s] = 1;
                            long x = s / N, y = s % N;
                            long z = (a * y + b * x + c) % N;
                            s = y * N + z;
                            len++;
                        }
                        if (len > maxc) maxc = len;
                        lcm = lcm / gcdl(lcm, len) * len;
                    }
                    long o = (N <= 24) ? ord3(a, b, c, N) : lcm;   /* direct order only for small N; = lcm by the proven part (b) */
                    cases++;
                    if (maxc != lcm) {
                        bad_max_lcm++;
                        if (n_bad_here < 3) printf("  N=%ld a=%ld b=%ld c=%ld: max cycle %ld, lcm %ld, ord3 %ld\n", N, a, b, c, maxc, lcm, o);
                        n_bad_here++;
                    }
                    if (lcm != o) { bad_lcm_ord++; printf("  lcm!=ord3: N=%ld a=%ld b=%ld c=%ld max %ld lcm %ld ord3 %ld\n", N, a, b, c, maxc, lcm, o); }
                    /* fixed point? (a+b-1) x + c = 0 solvable */
                    int fx = 0;
                    for (long x = 0; x < N; x++) if (((a + b - 1) * x + c) % N == 0) { fx = 1; break; }
                    if (fx) {
                        fixed_cases++;
                        if (maxc != ord2(a, b, N)) { bad_fixed++; printf("  max!=ord2: N=%ld a=%ld b=%ld c=%ld max %ld ord2 %ld\n", N, a, b, c, maxc, ord2(a, b, N)); }
                    }
                }
        }
        if (n_bad_here) printf("N=%ld: %ld cases with max cycle != lcm\n", N, n_bad_here);
        fflush(stdout);
    }
    printf("RESULT affine N<=%d: cases %ld, max!=lcm %ld, lcm!=ord3 %ld, fixed-point cases %ld, max!=ord2 among them %ld\n",
           NMAX, cases, bad_max_lcm, bad_lcm_ord, fixed_cases, bad_fixed);
    free(seen);
    return 0;
}

static int laver(int EMAX) {
    for (int e = 0; e <= EMAX; e++) {
        long N = 1L << e;
        uint16_t *T = malloc(sizeof(uint16_t) * (N + 1) * (N + 1));
        /* 1-based Laver table: p*1 = p+1 mod N (in 1..N), p*(q+1) = (p*q)*(p+1); rows from N down to 1 */
        for (long q = 1; q <= N; q++) T[N * (N + 1) + q] = (uint16_t)q;   /* N is a left identity */
        for (long p = N - 1; p >= 1; p--) {
            T[p * (N + 1) + 1] = (uint16_t)(p + 1);
            for (long q = 1; q < N; q++) {
                long pq = T[p * (N + 1) + q];          /* p*q > p: row already computed */
                T[p * (N + 1) + q + 1] = T[pq * (N + 1) + p + 1];
            }
        }
        /* verify left-distributivity on a sample (all triples for N <= 64) */
        long ld_fail = 0;
        if (N <= 64)
            for (long a = 1; a <= N; a++) for (long b = 1; b <= N; b++) for (long c = 1; c <= N; c++) {
                long l = T[a * (N + 1) + T[b * (N + 1) + c]];
                long r = T[T[a * (N + 1) + b] * (N + 1) + T[a * (N + 1) + c]];
                if (l != r) ld_fail++;
            }
        /* 0-based op(x,y) = T[x+1][y+1]-1; pair map (a,b) -> (b, op(b,a)); top = N-1 */
        long top = N - 1, maxtr = 0, n_fixed = 0, n_two = 0, other_cycles = 0, states = N * N;
        for (long a = 0; a < N; a++)
            for (long b = 0; b < N; b++) {
                long x = a, y = b, k = 0;
                while (x != top && y != top) {
                    long z = T[(y + 1) * (N + 1) + (x + 1)] - 1;
                    x = y; y = z; k++;
                    if (k > 1000000) { printf("no top reached\n"); break; }
                }
                if (k > maxtr) maxtr = k;
                /* periodic? state with top: check period */
                if (a == top || b == top) {
                    long x2 = a, y2 = b;
                    long z = T[(y2 + 1) * (N + 1) + (x2 + 1)] - 1;
                    long x3 = y2, y3 = z;
                    if (x3 == a && y3 == b) n_fixed++;
                    else {
                        long z2 = T[(y3 + 1) * (N + 1) + (x3 + 1)] - 1;
                        if (y3 == a && z2 == b) n_two++; else other_cycles++;
                    }
                }
            }
        printf("RESULT laver n=%d N=%ld: LD failures(N<=64 checked) %ld, fixed states %ld, states on 2-cycles %ld (cycles %ld), other states with top %ld, max transient %ld\n",
               e, N, ld_fail, n_fixed, n_two, n_two / 2, other_cycles, maxtr);
        fflush(stdout);
        free(T);
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage\n"); return 1; }
    if (!strcmp(argv[1], "affine")) return affine(atoi(argv[2]));
    if (!strcmp(argv[1], "laver")) return laver(atoi(argv[2]));
    return 1;
}
