#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "QSH/Implementations/03_Implementations/1_Reference_Implementation/QSH-512/CryptHash_AlgorithmInstance.c"

static uint64_t rotr(uint64_t x, int r, const qsh_params *p)
{
    r %= p->w;
    x &= p->mask;
    if (r == 0)
        return x;
    return ((x >> r) | (x << (p->w - r))) & p->mask;
}

static void Ginv(uint64_t q[4], const qsh_params *p)
{
    uint64_t a = q[0], b = q[1], c = q[2], d = q[3];

    b = rotr(b, p->w / 4 - 1, p) ^ c;
    c = (c - rotl(d, p->w / 4, p->w, p->mask)) & p->mask;
    d = rotr(d, p->w / 4, p) ^ a;
    a = (a - b) & p->mask;
    b = rotr(b, p->w / 2 - 4, p) ^ c;
    c = (c - rotl(d, p->w / 2 - 1, p->w, p->mask)) & p->mask;
    d = rotr(d, p->w / 2, p) ^ a;
    a = (a - rotl(b, 1, p->w, p->mask)) & p->mask;

    q[0] = a;
    q[1] = b;
    q[2] = c;
    q[3] = d;
}

static void G_along_inv(uint64_t *s, int axis, const qsh_params *p)
{
    uint64_t q[4];
    unsigned a, b, k;

    if (axis == 0) {
        for (a = 0; a < 4; a++)
            for (b = 0; b < 4; b++) {
                for (k = 0; k < 4; k++)
                    q[k] = s[idx(k, a, b)];
                Ginv(q, p);
                for (k = 0; k < 4; k++)
                    s[idx(k, a, b)] = q[k];
            }
    } else {
        for (a = 0; a < 4; a++)
            for (b = 0; b < 4; b++) {
                for (k = 0; k < 4; k++)
                    q[k] = s[idx(a, k, b)];
                Ginv(q, p);
                for (k = 0; k < 4; k++)
                    s[idx(a, k, b)] = q[k];
            }
    }
}

static void R3inv(uint64_t *s, const qsh_params *p)
{
    apply_plane(s, +1, 1);
    G_along_inv(s, 1, p);
    apply_plane(s, -1, 1);
    apply_plane(s, +1, 0);
    G_along_inv(s, 0, p);
    apply_plane(s, -1, 0);
    G_along_inv(s, 0, p);
}

static void E3inv(uint64_t *s, const qsh_params *p)
{
    int r;
    G_along_inv(s, 0, p);
    for (r = 0; r < p->rounds; r++)
        R3inv(s, p);
}

static void F3inv(const uint64_t *z, const uint64_t *m, uint64_t flag,
                  uint64_t *h, const qsh_params *p)
{
    uint64_t s[U];
    unsigned j;

    for (j = 0; j < V; j++) {
        s[j] = (z[j] - m[j]) & p->mask;
        s[V + j] = z[V + j];
    }
    E3inv(s, p);
    for (j = 0; j < V; j++) {
        h[j] = s[j];
        h[V + j] = (s[V + j] - m[j]) & p->mask;
    }
    h[0] ^= flag;
}

static int one_message(const unsigned char *msg, size_t len,
                       const qsh_params *p, uint64_t reset[U])
{
    uint64_t block0[V], block1[V], zero[U] = {0}, state[U], check[U];
    unsigned long long bits = 8ull * len;
    unsigned long long total_bytes = (bits + 2ull * p->m - bits % p->m) / 8;

    build_block(msg, bits, total_bytes, 0, block0, p);
    build_block(msg, bits, total_bytes, 1, block1, p);
    F3inv(zero, block1, FLAG_CHUNK_END | FLAG_ROOT, state, p);
    F3inv(state, block0, FLAG_CHUNK_START, reset, p);

    F3(reset, block0, FLAG_CHUNK_START, state, p);
    F3(state, block1, FLAG_CHUNK_END | FLAG_ROOT, check, p);
    return memcmp(check, zero, sizeof(zero)) == 0;
}

int main(void)
{
    static const unsigned char m0[] = "QSH review A";
    static const unsigned char m1[] = "QSH review message B";
    static const struct {
        int bits;
        uint64_t r0;
        uint64_t r1;
    } expected[] = {
        {512, 0xfb0f95a4, 0xb8b609bf},
        {768, 0xd863fe5d1b1d6233, 0xf70cb15272fe6154},
        {1024, 0xd863fe5d1b1d6233, 0xf70cb15272fe6154},
    };
    size_t i;

    for (i = 0; i < sizeof(expected) / sizeof(expected[0]); i++) {
        qsh_params p;
        uint64_t reset0[U], reset1[U];

        if (select_params(expected[i].bits, &p) != 0 ||
            !one_message(m0, sizeof(m0) - 1, &p, reset0) ||
            !one_message(m1, sizeof(m1) - 1, &p, reset1) ||
            reset0[0] != expected[i].r0 || reset1[0] != expected[i].r1 ||
            memcmp(reset0, reset1, sizeof(reset0)) == 0) {
            printf("NOT CONFIRMED: QSH-%d\n", expected[i].bits);
            return 1;
        }
        printf("QSH-%d: distinct resets %016llx and %016llx give the same zero digest\n",
               expected[i].bits,
               (unsigned long long)reset0[0],
               (unsigned long long)reset1[0]);
    }
    puts("CONFIRMED: explicit full-mode free-start collisions for all QSH variants");
    return 0;
}
