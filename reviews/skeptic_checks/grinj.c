/* Skeptic check of the injectivity premise in the Historian's derivation of identity (E):
 * for M = <A | u = v> (|u| = |v| = k) with longest common border z, u = z u', v = z v',
 * the map  ZM[z] -> ZM,  b |-> b([u'_-] - [v'_-])   (w_- = w without its last letter)
 * must be injective in every degree.  Over a field this map, in degree l, has one column per
 * class b in M[z] of length l with entries +1 at [b u'_-] and -1 at [b v'_-]: it is the
 * (signed) incidence matrix of a multigraph, so it is injective iff that graph is a forest
 * (no loop [b u'_-] = [b v'_-], no cycle).  Injectivity over Q <=> injectivity over Z here.
 * Input line: q Lmax u v z      Output: per degree l: l  #columns  forest(1/0)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int64_t qp[40];

typedef struct { int32_t *par; } UF;

static int64_t uf_find(int32_t *par, int64_t x) {
    while (par[x] >= 0) { int64_t p = par[x]; if (par[p] >= 0) par[x] = par[p]; x = p; }
    return x;
}
static int uf_unite(int32_t *par, int64_t a, int64_t b) {
    a = uf_find(par, a); b = uf_find(par, b);
    if (a == b) return 0;
    if (par[a] > par[b]) { int64_t t = a; a = b; b = t; }
    par[a] += par[b]; par[b] = (int32_t)a; return 1;
}

int main(void) {
    char line[1024];
    while (fgets(line, sizeof line, stdin)) {
        int q, Lmax; char us[64], vs[64], zs[64];
        if (sscanf(line, "%d %d %63s %63s %63s", &q, &Lmax, us, vs, zs) != 5) continue;
        int k = (int)strlen(us), lz = (int)strlen(zs);
        qp[0] = 1; for (int i = 1; i < 40; i++) qp[i] = qp[i - 1] * q;
        int32_t **cls = (int32_t **)calloc(Lmax + 1, sizeof(int32_t *));
        int64_t U = 0, V = 0;
        for (int t = 0; t < k; t++) { U += (int64_t)(us[t] - '0') * qp[t]; V += (int64_t)(vs[t] - '0') * qp[t]; }
        for (int n = 0; n <= Lmax; n++) {
            cls[n] = (int32_t *)malloc(sizeof(int32_t) * qp[n]);
            memset(cls[n], 0xff, sizeof(int32_t) * qp[n]);
            if (n >= k)
                for (int i = 0; i + k <= n; i++)
                    for (int64_t right = 0; right < qp[n - k - i]; right++)
                        for (int64_t left = 0; left < qp[i]; left++) {
                            int64_t base = right * qp[i + k] + left;
                            uf_unite(cls[n], base + U * qp[i], base + V * qp[i]);
                        }
        }
        /* u' = u[lz..k-1], v' = v[lz..k-1]; u'_- and v'_- drop the last letter */
        int lp = k - lz - 1;                       /* |u'_-| */
        int64_t Up = 0, Vp = 0, Z = 0;
        for (int t = 0; t < lp; t++) { Up += (int64_t)(us[lz + t] - '0') * qp[t]; Vp += (int64_t)(vs[lz + t] - '0') * qp[t]; }
        for (int t = 0; t < lz; t++) Z += (int64_t)(zs[t] - '0') * qp[t];
        printf("REL %s %s z=%s\n", us, vs, zs);
        for (int l = lz; l + lp <= Lmax; l++) {
            int L2 = l + lp;
            int32_t *seen = (int32_t *)malloc(sizeof(int32_t) * qp[l]);
            memset(seen, 0, sizeof(int32_t) * qp[l]);
            int32_t *g = (int32_t *)malloc(sizeof(int32_t) * qp[L2]);   /* graph union-find on classes */
            memset(g, 0xff, sizeof(int32_t) * qp[L2]);
            int64_t cols = 0; int forest = 1;
            int64_t P = qp[l - lz];
            for (int64_t pre = 0; pre < P; pre++) {
                int64_t w = pre + Z * P;                  /* word of length l ending with z */
                int64_t rb = uf_find(cls[l], w);
                if (seen[rb]) continue;
                seen[rb] = 1; cols++;
                int64_t x = uf_find(cls[L2], w + Up * qp[l]);   /* w . u'_- */
                int64_t y = uf_find(cls[L2], w + Vp * qp[l]);   /* w . v'_- */
                if (!uf_unite(g, x, y)) forest = 0;             /* loop or cycle */
            }
            printf("%d %lld %d\n", l, (long long)cols, forest);
            free(seen); free(g);
        }
        for (int n = 0; n <= Lmax; n++) free(cls[n]);
        free(cls);
        fflush(stdout);
    }
    return 0;
}
