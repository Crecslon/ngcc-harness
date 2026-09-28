#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "api.h"
#include "drng.h"
#include "packing.h"
#include "params.h"
#include "sampler.h"
#include "sign.h"

DRNG_ctx drng_algorithm;

static unsigned parity_product_coefficient(const poly *secret, const poly *challenge,
                                           int coefficient) {
    unsigned value = 0;
    for (int i = 0; i < N; i++) {
        int k = coefficient - i;
        if (k < 0)
            k += N;
        value ^= ((unsigned)secret->coeffs[i] & 1u) &
                 ((unsigned)challenge->coeffs[k] & 1u);
    }
    return value;
}

int main(int argc, char **argv) {
    unsigned signature_count = argc > 1 ? (unsigned)strtoul(argv[1], NULL, 0) : 25000;
    uint8_t seed[48] = {0};
    for (unsigned i = 0; i < sizeof(seed); i++)
        seed[i] = (uint8_t)i;
    if (init_random_number(&drng_algorithm, seed, sizeof(seed)) != 0)
        return 2;

    uint8_t *public_key = malloc(CRYPTO_PUBLICKEYBYTES);
    uint8_t *secret_key = malloc(CRYPTO_SECRETKEYBYTES);
    uint8_t *signature = malloc(CRYPTO_BYTES);
    uint8_t message[32] = {0};
    if (public_key == NULL || secret_key == NULL || signature == NULL ||
        crypto_sign_keypair(public_key, secret_key) != 0)
        return 3;

    secret_basis basis;
    uint8_t unpacked_public_key[CRYPTO_PUBLICKEYBYTES], key[SEEDBYTES];
    unpack_sk(unpacked_public_key, &basis, key, secret_key);

    int64_t score = 0, zero_predictor_score = 0;
    uint64_t bits = 0;
    for (unsigned trial = 0; trial < signature_count; trial++) {
        memcpy(message, &trial, sizeof(trial));
        size_t signature_length = 0;
        if (crypto_sign_signature(signature, &signature_length, message,
                                  sizeof(message), secret_key) != 0)
            return 4;
        if (crypto_sign_verify(signature, signature_length, message,
                               sizeof(message), public_key) != 0)
            return 5;

        uint8_t challenge_bytes[CTILDEBYTES];
        poly z1, z_bottom[D_REST], challenge;
        if (unpack_sig(challenge_bytes, &z1, z_bottom,
                       signature, signature_length) != 0)
            return 6;
        SampleChallenge(&challenge, challenge_bytes);

        for (int row = 0; row < D_REST; row++) {
            for (int j = 0; j < N; j++) {
                unsigned response_parity = (unsigned)z_bottom[row].coeffs[j] & 1u;
                unsigned secret_product = parity_product_coefficient(
                    &basis.row_small[row][0], &challenge, j);
                score += (response_parity ^ secret_product) ? -1 : 1;
                zero_predictor_score += response_parity ? -1 : 1;
                bits++;
            }
        }
    }

    double bias = (double)score / bits;
    double zero_predictor_bias = (double)zero_predictor_score / bits;
    printf("signatures=%u bits=%llu bias=%.9g zero_predictor_bias=%.9g\n",
           signature_count, (unsigned long long)bits, bias, zero_predictor_bias);

    /* The fixed 25,000-signature transcript is deterministic.  These loose
     * bounds still distinguish its secret-aware score from the wrong predictor. */
    if (signature_count >= 25000 &&
        (!(bias > 0.0003 && bias < 0.0011) || fabs(zero_predictor_bias) > 0.0005))
        return 7;

    free(signature);
    free(secret_key);
    free(public_key);
    puts("RHYME_SM3_ACCEPTED_SIGNATURE_PARITY_CONFIRMED");
    return 0;
}
