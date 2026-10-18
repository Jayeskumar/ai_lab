/* Skeptic check for C09 (arithmetic of Knuth's circle semigroup), independent of systems/.
 *
 * Products are computed from the DEFINITION a o b = sum_{k in Z(a)} sum_{l in Z(b)} F_{k+l}
 * (Zeckendorf index sets, Mathlib indexing F_1 = F_2 = 1, indices >= 2), never from the
 * shadow formula.  Enumeration bound: F_{k+l} >= F_k F_l gives a o b >= a b, so all products
 * <= X come from pairs a <= b with a b <= X; every such pair is evaluated (no monotonicity
 * assumption).  The conjugate nu'(n) = sum_{k in Z(n)} psi^k = n psi + n* (n* = sum F_{k-1})
 * is compared with psi^3, psi^2, -psi^2, -psi EXACTLY via signs of X - Y sqrt5.
 *
 * Build: gcc -O2 -o c09_circle c09_circle.c     Run: ./c09_circle X
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static uint64_t F[100];

/* sign of X - Y*sqrt(5) for 64-bit integers with |X|,|Y| < 2^31 */
static int cmp_s5(int64_t X, int64_t Y) {
    if (Y == 0) return (X > 0) - (X < 0);
    if (X >= 0 && Y < 0) return 1;
    if (X <= 0 && Y > 0) return -1;
    __int128 d = (__int128)X * X - (__int128)5 * Y * Y;   /* never 0 unless X = Y = 0 */
    int s = (d > 0) - (d < 0);
    return (X > 0) ? s : -s;
}

/* Zeckendorf mask (bit k = index k) and shadow */
static uint64_t zmask(uint64_t n) {
    uint64_t m = 0; int k = 90;
    while (n) { while (F[k] > n) k--; m |= 1ULL << k; n -= F[k]; k -= 2; }
    return m;
}

int main(int argc, char **argv) {
    uint64_t X = argc > 1 ? strtoull(argv[1], 0, 10) : 1000000ULL;
    F[0] = 0; F[1] = 1; for (int i = 2; i < 93; i++) F[i] = F[i - 1] + F[i - 2];
    uint8_t *red = calloc(X + 1, 1);
    uint64_t pairs = 0;
    /* enumerate pairs a <= b, a*b <= X */
    for (uint64_t a = 1; a * a <= X; a++) {
        uint64_t za = zmask(a);
        uint64_t c[64] = {0};             /* c[l] = sum_{k in Z(a)} F_{k+l} */
        for (int l = 2; l < 50; l++) { uint64_t s = 0; for (int k = 2; k < 50; k++) if (za >> k & 1) { if (k + l >= 93) { s = UINT64_MAX; break; } s += F[k + l]; } c[l] = s; }
        uint64_t bmax = X / a;
        uint64_t zb = zmask(a);           /* incremental Zeckendorf counter for b */
        for (uint64_t b = a; b <= bmax; b++) {
            if (b > a) { /* zb := zmask(b) from zmask(b-1): add F_2 then normalise */
                zb = zmask(b);
            }
            uint64_t p = 0; int over = 0;
            uint64_t t = zb;
            while (t) { int l = __builtin_ctzll(t); t &= t - 1; if (c[l] == UINT64_MAX || p + c[l] > X) { over = 1; break; } p += c[l]; }
            pairs++;
            if (!over && p <= X) red[p] = 1;
        }
    }
    /* scan */
    uint64_t irr = 0, zone = 0, zone_irr = 0, forced = 0, viol_window = 0, viol_shadow = 0, viol_obstruction = 0;
    uint64_t next_cp = 1000;
    printf("{\"X\": %llu, \"pairs_evaluated\": %llu, \"by_scale\": [", (unsigned long long)X, (unsigned long long)pairs);
    int first = 1;
    for (uint64_t n = 1; n <= X; n++) {
        uint64_t z = zmask(n);
        int64_t ns = 0; uint64_t t = z;
        while (t) { int k = __builtin_ctzll(t); t &= t - 1; ns += (int64_t)F[k - 1]; }
        int64_t A = 2 * ns + (int64_t)n;   /* nu'(n) = (A - n sqrt5)/2 */
        /* window of C08: -psi^2 < nu' < -psi  <=>  A+3 > (n+1)sqrt5  and  A+1 < (n+1)sqrt5 */
        if (!(cmp_s5(A + 3, (int64_t)n + 1) > 0 && cmp_s5(A + 1, (int64_t)n + 1) < 0)) viol_window++;
        /* shadow formula n* = floor((n+1)/phi): 2n* + n + 1 <= (n+1)sqrt5 < 2n* + n + 3 */
        if (!(cmp_s5(2 * ns + (int64_t)n + 1, (int64_t)n + 1) < 0 && cmp_s5(2 * ns + (int64_t)n + 3, (int64_t)n + 1) > 0)) viol_shadow++;
        /* product zone psi^3 < nu' < psi^2  <=>  A-4 > (n-2) sqrt5  and  A-3 < (n-1) sqrt5 */
        int in_zone = cmp_s5(A - 4, (int64_t)n - 2) > 0 && cmp_s5(A - 3, (int64_t)n - 1) < 0;
        if (!red[n]) irr++;
        if (in_zone) { zone++; if (!red[n]) zone_irr++; }
        else { forced++; if (red[n]) viol_obstruction++; }
        if (n == next_cp || n == X) {
            printf("%s{\"n\": %llu, \"irreducible\": %llu, \"irr_density\": %.6f, \"forced_density\": %.6f, \"irr_fraction_in_zone\": %.6f}",
                   first ? "" : ", ", (unsigned long long)n, (unsigned long long)irr, (double)irr / n, (double)forced / n, zone ? (double)zone_irr / zone : 0.0);
            first = 0;
            if (n == next_cp) next_cp *= 10;
        }
    }
    printf("],\n \"window_violations\": %llu, \"shadow_formula_violations\": %llu, \"reducible_outside_zone\": %llu,\n",
           (unsigned long long)viol_window, (unsigned long long)viol_shadow, (unsigned long long)viol_obstruction);
    printf(" \"first_irreducibles\": [");
    int c = 0; for (uint64_t n = 1; n <= X && c < 40; n++) if (!red[n]) { printf("%s%llu", c ? ", " : "", (unsigned long long)n); c++; }
    printf("]}\n");
    return 0;
}
