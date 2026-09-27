/* AddressSanitizer probe for all four ATLAS hint decoders. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "api.h"
#include "drng.h"
#include "packing.h"
#include "params.h"
#include "poly.h"
#include "polyvec.h"

DRNG_ctx drng_algorithm;

int main(void)
{
    unsigned char *sig = calloc(SIG_SIZE_PACKED, 1);
    polyvecl *z = malloc(sizeof(*z));
    polyveck *h = malloc(sizeof(*h));
    poly *c = malloc(sizeof(*c));
    unsigned char *hint;

    if (sig == NULL || z == NULL || h == NULL || c == NULL) {
        return 2;
    }
    hint = sig + (size_t)L * POLZ_SIZE_PACKED;
#if N == 128
    hint[0] = 200;
    hint[OMEGA + K - 1] = 1;
    printf("calling unpack_sig with position 200 and N=%u\n", (unsigned)N);
#elif N == 256
    hint[OMEGA + K - 1] = 255;
    printf("calling unpack_sig with unchecked hint count 255 and N=%u\n", (unsigned)N);
#elif N == 512
    hint[9 * (OMEGA >> 3) + K - 1] = 255;
    printf("calling unpack_sig with unchecked hint count 255 and N=%u\n", (unsigned)N);
#else
#error Unsupported ATLAS N
#endif
    fflush(stdout);
    unpack_sig(z, h, c, sig);
    puts("unpack_sig returned without a sanitizer diagnostic");
    free(c);
    free(h);
    free(z);
    free(sig);
    return 0;
}
