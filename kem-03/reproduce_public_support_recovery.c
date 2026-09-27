/* Public-key-only recovery of X for five fresh BAG-Loong-128 reference keys.
 * The candidate's PKE source is included to call its otherwise static public
 * matrix generator and serializer without changing the submitted code. */
#include "loong_pke.c"
#include "drng.h"
#include <stdio.h>
#include <stdint.h>
#include <time.h>

DRNG_ctx drng_algorithm; /* required by the submission's random API wrapper */

#define N LOONG_N
#define N1 LOONG_N1
#define M LOONG_M
#define DX LOONG_AXY_00
#define NU (N*DX)            /* unknowns per column */
#define NE (N*(M-5))         /* equations per column after projection */
#define W ((NU+1+63)/64)

static int ybits[M]; /* public Y support: a^0..a^3 and a^5 */

static uint64_t rows[NE][W];

int main(int argc, char **argv) {
	unsigned char pk[LOONG_PK_BYTES], skp[LOONG_SK_PRIME_BYTES];
	unsigned char ps[LOONG_PK_SEED_BYTES], ks[LOONG_PK_SEED_BYTES];
	int trials = argc > 1 ? atoi(argv[1]) : 5;
	FILE *f = fopen("/dev/urandom", "rb");
	int t, all_ok = 1;
	if (f == NULL || trials < 1 || trials > 100) { fputs("invalid trial count or missing randomness\n", stderr); return 2; }
	/* Public, fixed supports from the reference sampler: pool = 1,a,...,a^5;
	   X: a^0..a^4, Y: a^0..a^3, a^5 (AXY_01 = 4 intersection). */
	ybits[0]=ybits[1]=ybits[2]=ybits[3]=ybits[5]=1;
	for (t = 0; t < trials; t++) {
		rbc_elt *g = calloc(LOONG_PKE_L, sizeof(rbc_elt));
		rbc_elt *h = calloc(N*N, sizeof(rbc_elt));
		rbc_elt *s = calloc(N*N1, sizeof(rbc_elt));
		rbc_elt *x = calloc(N*N1, sizeof(rbc_elt));
		rbc_elt *xr = calloc(N*N1, sizeof(rbc_elt));
		int j, k, b, i, ok = 1, minrank = NU;
		clock_t c0;
		if (g == NULL || h == NULL || s == NULL || x == NULL || xr == NULL) {
			fputs("allocation failed\n", stderr);
			return 2;
		}
		if (fread(ps, 1, sizeof ps, f) != sizeof ps ||
		    fread(ks, 1, sizeof ks, f) != sizeof ks) { fputs("random read failed\n", stderr); return 2; }
		if (loong_pke_keygen_derandomized(pk, sizeof pk, skp, sizeof skp, ps, sizeof ps, ks, sizeof ks)) { puts("keygen fail"); return 1; }
		c0 = clock();
		/* attacker: public data only */
		generate_public_objects(g, h, pk + LOONG_PK_SEED_OFFSET, LOONG_PK_SEED_BYTES);
		logical_vec_decode(s, N*N1, pk + LOONG_PK_S_OFFSET, LOONG_X_OR_S_BYTES);
		for (j = 0; j < N1; j++) {
			int r = 0, col, piv[NU];
			memset(rows, 0, sizeof rows);
			/* equation (i, bit b not in Ysupp): sum_k,d c_{k,d} [H_ik a^d]_b = [S_ij]_b */
			for (i = 0; i < N; i++) {
				int e = 0;
				for (b = 0; b < M; b++) {
					if (ybits[b]) continue;
					int row = i*(M-5) + e++;
					for (k = 0; k < N; k++) for (int d = 0; d < DX; d++) {
						rbc_elt mono, prod; rbc_elt_set_zero(&mono);
						rbc_elt_set_coefficient(&mono, d, 1);
						rbc_elt_mul(&prod, &h[i*N+k], &mono);
						if (rbc_elt_get_coefficient(&prod, b)) { int u = k*DX+d; rows[row][u/64] |= 1ULL << (u%64); }
					}
					if (rbc_elt_get_coefficient(&s[i*N1+j], b)) rows[row][NU/64] |= 1ULL << (NU%64);
				}
			}
			/* Gaussian elimination */
			for (col = 0; col < NU; col++) {
				int p = -1;
				for (i = r; i < NE; i++) if ((rows[i][col/64] >> (col%64)) & 1) { p = i; break; }
				if (p < 0) { piv[col] = -1; continue; }
				if (p != r) for (int w = 0; w < W; w++) { uint64_t tmp = rows[p][w]; rows[p][w] = rows[r][w]; rows[r][w] = tmp; }
				for (i = 0; i < NE; i++) if (i != r && ((rows[i][col/64] >> (col%64)) & 1))
					for (int w = 0; w < W; w++) rows[i][w] ^= rows[r][w];
				piv[col] = r++;
			}
			if (r < minrank) minrank = r;
			/* consistency: no row 0 = 1 */
			for (i = r; i < NE; i++) if ((rows[i][NU/64] >> (NU%64)) & 1) ok = 0;
			for (k = 0; k < N; k++) {
				rbc_elt_set_zero(&xr[k*N1+j]);
				for (int d = 0; d < DX; d++) {
					int u = k*DX+d; int bit = piv[u] >= 0 ? (rows[piv[u]][NU/64] >> (NU%64)) & 1 : 0;
					if (bit) rbc_elt_set_coefficient(&xr[k*N1+j], d, 1);
				}
			}
		}
		double sec = (double)(clock() - c0) / CLOCKS_PER_SEC;
		/* compare with the real secret */
		logical_vec_decode(x, N*N1, skp + LOONG_SK_X_OFFSET, LOONG_X_OR_S_BYTES);
		int eq = 1;
		for (i = 0; i < N*N1; i++) if (x[i].v[0] != xr[i].v[0]) eq = 0;
		/* also check the recovered key's serialization matches sk' byte-for-byte */
		unsigned char xb[LOONG_X_OR_S_BYTES];
		logical_vec_encode(xb, sizeof xb, xr, N*N1);
		int bytes_match = memcmp(xb, skp + LOONG_SK_X_OFFSET, sizeof xb) == 0;
		printf("trial %d: min rank %d/%d, consistent=%d, X recovered exactly=%d, bytes match=%d, %.3fs\n",
		       t + 1, minrank, NU, ok, eq, bytes_match, sec);
		if (minrank != NU || !ok || !eq || !bytes_match) all_ok = 0;
		free(g); free(h); free(s); free(x); free(xr);
	}
	fclose(f);
	if (!all_ok) return 1;
	puts("CONFIRMED kem-03-3: public-key-only recovery of X on all fresh keys");
	return 0;
}
