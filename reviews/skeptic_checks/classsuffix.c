/* Skeptic check of the Historian's growth identities (P), (E).
 * For one length-preserving relation u = v over q letters, for n = 0..nmax print
 *   n  h_n  s_1(n) ... s_r(n)
 * where h_n = number of classes of Sigma^n and s_i(n) = number of classes of Sigma^n that contain a
 * word ending with w_i (i.e. the elements of length n of the left ideal M[w_i]).
 * Input line:  q nmax u v r w_1 ... w_r     (words as digit strings; "-" = empty word)
 * Encoding: letter at position i (0 = first letter) is base-q digit i.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int32_t *par, *stamp;

static int64_t find(int64_t x) {
    while (par[x] >= 0) {
        int64_t p = par[x];
        if (par[p] >= 0) par[x] = par[p];
        x = p;
    }
    return x;
}
static int unite(int64_t a, int64_t b) {
    a = find(a); b = find(b);
    if (a == b) return 0;
    if (par[a] > par[b]) { int64_t t = a; a = b; b = t; }
    par[a] += par[b]; par[b] = (int32_t)a;
    return 1;
}

int main(void) {
    char line[8192];
    while (fgets(line, sizeof line, stdin)) {
        int q, nmax, r;
        char us[64], vs[64];
        int off = 0, used;
        if (sscanf(line, "%d %d %63s %63s %d%n", &q, &nmax, us, vs, &r, &used) != 5) continue;
        off = used;
        char ws[16][64];
        for (int i = 0; i < r; i++) {
            if (sscanf(line + off, "%63s%n", ws[i], &used) != 1) return 1;
            off += used;
            if (strcmp(ws[i], "-") == 0) ws[i][0] = 0;
        }
        int k = (int)strlen(us);
        int64_t qp[64]; qp[0] = 1;
        for (int i = 1; i < 64; i++) qp[i] = qp[i - 1] * q;
        par = (int32_t *)malloc(sizeof(int32_t) * qp[nmax]);
        stamp = (int32_t *)malloc(sizeof(int32_t) * qp[nmax]);
        int64_t U = 0, V = 0;
        for (int t = 0; t < k; t++) { U += (int64_t)(us[t] - '0') * qp[t]; V += (int64_t)(vs[t] - '0') * qp[t]; }
        printf("REL %s %s\n", us, vs);
        int32_t sid = 0;
        for (int n = 0; n <= nmax; n++) {
            int64_t N = qp[n];
            memset(par, 0xff, sizeof(int32_t) * N);
            memset(stamp, 0, sizeof(int32_t) * N);
            int64_t unions = 0;
            if (n >= k)
                for (int i = 0; i + k <= n; i++)
                    for (int64_t right = 0; right < qp[n - k - i]; right++)
                        for (int64_t left = 0; left < qp[i]; left++) {
                            int64_t base = right * qp[i + k] + left;
                            unions += unite(base + U * qp[i], base + V * qp[i]);
                        }
            printf("%d %lld", n, (long long)(N - unions));
            for (int i = 0; i < r; i++) {
                int lw = (int)strlen(ws[i]);
                sid++;
                if (lw > n) { printf(" 0"); continue; }
                int64_t W = 0;
                for (int t = 0; t < lw; t++) W += (int64_t)(ws[i][t] - '0') * qp[t];
                int64_t cnt = 0, P = qp[n - lw];
                for (int64_t pre = 0; pre < P; pre++) {       /* word = pre (first n-lw letters) + w */
                    int64_t root = find(pre + W * P);
                    if (stamp[root] != sid) { stamp[root] = sid; cnt++; }
                }
                printf(" %lld", (long long)cnt);
            }
            printf("\n");
        }
        free(par); free(stamp);
        fflush(stdout);
    }
    return 0;
}
