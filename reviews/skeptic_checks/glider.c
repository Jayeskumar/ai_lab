/* Skeptic check for CLM-C02-04 (carry rules with sum b = m never terminate from all unary starts).
 *
 * Reduction used (proved in the review): from a unary start n, after level 0 fires t = floor(n/m)
 * times the window is t*b, and the upward sweep evolves the window by the monotone map
 *   F(x_1..x_J) = (x_2 + s b_1, ..., x_J + s b_{J-1}, s b_J),  s = floor(x_1/m).
 * If the window ever dominates T (T_i = sum_{j>=i} b_j) the derivation is infinite (Lemma 4).
 * If all entries are < m the sweep (hence every derivation, abelian property) terminates.
 * For an aperiodic rule (gcd of the support of b = 1) one of the two always happens
 * (window mass is non-increasing; once constant, firing counts satisfy m t_l = sum b_j t_{l-j}
 * and the only periodic solutions are constant, giving window = t'*T).  Rules with gcd g > 1
 * reduce to the aperiodic rule b'_i = b_{gi} on levels gN, so only aperiodic rules are enumerated.
 *
 * usage: glider m_min m_max Jmax Tmax
 * prints one summary line per m plus every rule with no locking t <= Tmax.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

static int m, J, Tmax;
static long long b[32], T[32];
static long long rules_tested, worst_t, nolock;
static long long worst_b[32]; static int worst_J;
static long long steps_total;

/* returns first t in 1..Tmax whose orbit locks (window >= T), or 0 if none */
static int first_lock(void) {
    long long W[32], N[32];
    for (int t = 1; t <= Tmax; t++) {
        for (int i = 0; i < J; i++) W[i] = (long long)t * b[i];
        for (long long step = 0; ; step++) {
            int dom = 1, dead = 1;
            for (int i = 0; i < J; i++) {
                if (W[i] < T[i]) dom = 0;
                if (W[i] >= m) dead = 0;
            }
            if (dom) { steps_total += step; return t; }
            if (dead) { steps_total += step; break; }
            if (step > 100000000LL) { fprintf(stderr, "step cap hit\n"); exit(2); }
            long long s = W[0] / m;
            for (int i = 0; i + 1 < J; i++) N[i] = W[i + 1] + s * b[i];
            N[J - 1] = s * b[J - 1];
            memcpy(W, N, sizeof(long long) * J);
        }
    }
    return 0;
}

static void rec(int pos, int rem) {
    if (pos == J - 1) {
        if (rem < 1) return;               /* b_J >= 1 */
        b[pos] = rem;
        int g = 0;
        for (int i = 0; i < J; i++) if (b[i]) g = gcd(g, i + 1);
        if (g != 1) return;                /* periodic rules reduce to aperiodic ones */
        long long acc = 0;
        for (int i = J - 1; i >= 0; i--) { acc += b[i]; T[i] = acc; }
        rules_tested++;
        int t = first_lock();
        if (t == 0) {
            nolock++;
            printf("NO LOCK up to t=%d: m=%d b=(", Tmax, m);
            for (int i = 0; i < J; i++) printf("%lld%s", b[i], i + 1 < J ? "," : ")\n");
        } else if (t > worst_t) {
            worst_t = t; worst_J = J;
            memcpy(worst_b, b, sizeof(b));
        }
        return;
    }
    for (int x = 0; x <= rem; x++) { b[pos] = x; rec(pos + 1, rem - x); }
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: glider m_min m_max Jmax Tmax\n"); return 1; }
    int mmin = atoi(argv[1]), mmax = atoi(argv[2]), Jmax = atoi(argv[3]);
    Tmax = atoi(argv[4]);
    for (m = mmin; m <= mmax; m++) {
        rules_tested = 0; worst_t = 0; nolock = 0; steps_total = 0;
        for (J = 1; J <= Jmax; J++) rec(0, m);
        printf("m=%d J<=%d: aperiodic rules with sum b = m: %lld; without lock (t<=%d): %lld; "
               "largest first-locking t = %lld at b=(", m, Jmax, rules_tested, Tmax, nolock, worst_t);
        for (int i = 0; i < worst_J; i++) printf("%lld%s", worst_b[i], i + 1 < worst_J ? "," : "");
        printf(")  [window steps simulated: %lld]\n", steps_total);
        fflush(stdout);
    }
    return 0;
}
