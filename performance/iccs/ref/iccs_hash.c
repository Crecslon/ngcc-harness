/* CryptHash() over one ICCS helper with a fixed output width (see ../Makefile). */
#include "auxfunc.h"

int CryptHash(int digest_len_bits, const unsigned char *msg, unsigned long long msg_len_bits,
              unsigned char *digest)
{
    if (digest_len_bits != ICCS_OUTPUT_BITS)
        return -1;
#if defined(ICCS_SM3HASH)
    return sm3hash(digest_len_bits, msg, msg_len_bits, digest);
#elif defined(ICCS_PSEUDOHASH)
    return pseudohash(digest_len_bits, msg, msg_len_bits, digest);
#elif defined(ICCS_PSEUDOXOF)
    return pseudoXOF((unsigned long long)digest_len_bits, msg, msg_len_bits, digest);
#else
#error "define ICCS_SM3HASH, ICCS_PSEUDOHASH or ICCS_PSEUDOXOF"
#endif
}
