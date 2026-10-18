/* Skeptic check (C17, CLM-C17-05): anchored solutions of x*(y+1) = (x*y)*(x+1) (all x, y mod N).
 * With the anchor x*0 = x+1 the instances y = 0..N-2 force the table row by row from x = N-1 down
 * (every entry of row x < N-1 is > x, so only rows already computed are needed; "stuck" is reported
 * otherwise).  The wrap-around instance y = N-1 then reads x+1 = (x*(N-1))*(x+1).
 * usage: ldforce NMAX   -> prints the N <= NMAX for which the forced table satisfies the wrap-around,
 *                          and any N where the forcing got stuck. */
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    int NMAX = atoi(argv[1]);
    int *T = malloc(sizeof(int) * (size_t)NMAX * NMAX);
    int nsol = 0, nstuck = 0;
    for (int N = 1; N <= NMAX; N++) {
        for (long i = 0; i < (long)N * N; i++) T[i] = -1;
        for (int x = 0; x < N; x++) T[(long)x * N + 0] = (x + 1) % N;   /* anchor column, every row */
        int stuck = 0;
        for (int x = N - 1; x >= 0 && !stuck; x--) {
            for (int y = 0; y < N - 1; y++) {
                int v = T[(long)x * N + y];
                int w = T[(long)v * N + (x + 1) % N];
                if (w < 0) { stuck = 1; break; }
                T[(long)x * N + y + 1] = w;
            }
        }
        if (stuck) { printf("stuck %d\n", N); nstuck++; continue; }
        int wrap = 1;
        for (int x = 0; x < N; x++) {
            int v = T[(long)x * N + N - 1];
            if (T[(long)v * N + (x + 1) % N] != (x + 1) % N) { wrap = 0; break; }
        }
        if (wrap) { printf("solution %d\n", N); nsol++; }
    }
    printf("done NMAX=%d solutions=%d stuck=%d\n", NMAX, nsol, nstuck);
    return 0;
}
