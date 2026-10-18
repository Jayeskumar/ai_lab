/* Nim-multiplication on [0, 256) from Conway's definition (own code, independent of the lab):
 *   a (x) b = mex { (a' (x) b) ^ (a (x) b') ^ (a' (x) b') : a' < a, b' < b }.
 * Writes the 256x256 table as raw bytes to the file given as argv[1]. */
#include <stdio.h>
#include <string.h>
int main(int argc, char **argv) {
    static unsigned char T[256][256];
    static int mark[512];
    int stamp = 0;
    memset(mark, 0, sizeof mark);
    for (int a = 0; a < 256; a++)
        for (int b = 0; b < 256; b++) {
            stamp++;
            for (int a2 = 0; a2 < a; a2++)
                for (int b2 = 0; b2 < b; b2++) {
                    int v = T[a2][b] ^ T[a][b2] ^ T[a2][b2];
                    mark[v] = stamp;
                }
            int m = 0;
            while (mark[m] == stamp) m++;
            T[a][b] = (unsigned char)m;
        }
    FILE *f = fopen(argv[1], "wb");
    fwrite(T, 1, sizeof T, f);
    fclose(f);
    printf("2x2=%d 4x4=%d 16x16=%d 3x3=%d\n", T[2][2], T[4][4], T[16][16], T[3][3]);
    return 0;
}
