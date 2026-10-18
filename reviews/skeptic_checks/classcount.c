/* Skeptic check (independent of systems/rewriting.py):
 * exact number of congruence classes of length-n words modulo ONE length-preserving
 * relation u = v, by union-find over all q^n words.
 *
 * Input lines:  q nmax u v      (u, v = strings of digits 0..q-1, |u| = |v| = k)
 * Output lines: u v c_1 c_2 ... c_nmax
 *
 * Word encoding: letter at position i (0 = first letter) is digit i of the base-q code.
 * An occurrence of u at position i in a word w is rewritten to v; every such edge
 * {x u y, x v y} is produced exactly once from the word x u y, so the union-find
 * computes the equivalence closure of one-step rewriting = the congruence on Sigma^n.
 * classes = q^n - (number of successful unions).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int32_t *par;

static int64_t find(int64_t x) {
    while (par[x] >= 0) {
        int64_t p = par[x];
        if (par[p] >= 0) par[x] = par[p];   /* path halving */
        x = p;
    }
    return x;
}

static int unite(int64_t a, int64_t b) {
    a = find(a); b = find(b);
    if (a == b) return 0;
    if (par[a] > par[b]) { int64_t t = a; a = b; b = t; }   /* a has larger size (more negative) */
    par[a] += par[b];
    par[b] = (int32_t)a;
    return 1;
}

int main(void) {
    char line[4096];
    int64_t cap = 0;
    while (fgets(line, sizeof line, stdin)) {
        int q, nmax;
        char us[256], vs[256];
        if (sscanf(line, "%d %d %255s %255s", &q, &nmax, us, vs) != 4) continue;
        int k = (int)strlen(us);
        if ((int)strlen(vs) != k) { fprintf(stderr, "length mismatch\n"); return 1; }
        int64_t qp[64]; qp[0] = 1;
        for (int i = 1; i < 64; i++) qp[i] = qp[i - 1] * q;
        if (qp[nmax] > cap) {
            free(par);
            cap = qp[nmax];
            par = (int32_t *)malloc(sizeof(int32_t) * cap);
            if (!par) { fprintf(stderr, "oom\n"); return 1; }
        }
        int64_t U = 0, V = 0;
        for (int t = 0; t < k; t++) { U += (int64_t)(us[t] - '0') * qp[t]; V += (int64_t)(vs[t] - '0') * qp[t]; }
        printf("%s %s", us, vs);
        for (int n = 1; n <= nmax; n++) {
            int64_t N = qp[n];
            memset(par, 0xff, sizeof(int32_t) * N);   /* all roots of size 1 (-1) */
            int64_t unions = 0;
            if (n >= k) {
                for (int i = 0; i + k <= n; i++) {
                    int64_t L = qp[i], R = qp[n - k - i];
                    for (int64_t right = 0; right < R; right++) {
                        int64_t base = right * qp[i + k];
                        for (int64_t left = 0; left < L; left++) {
                            int64_t w1 = base + U * qp[i] + left;
                            int64_t w2 = base + V * qp[i] + left;
                            unions += unite(w1, w2);
                        }
                    }
                }
            }
            printf(" %lld", (long long)(N - unions));
        }
        printf("\n");
        fflush(stdout);
    }
    return 0;
}
