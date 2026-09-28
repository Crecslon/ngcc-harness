/* Link-time wrappers (-Wl,--wrap=...) around the ICCS symmetric helpers.
 *
 * Every call to pseudohash, pseudoXOF, sm3hash or get_random_number that
 * crosses an object-file boundary is timed with a cheap tick counter and
 * accumulated per (function, input bits, output bits). Nested calls are not
 * double counted. Accounting is on only while the driver enables it, so setup
 * work and untimed KEX steps are excluded. See performance/hashprof/README.md.
 */
#include <stdint.h>
#include <string.h>
#include <time.h>
#if defined(__x86_64__) || defined(__i386__)
#include <x86intrin.h>
static inline uint64_t ticks(void) { return __rdtsc(); }
#define NGCC_TICK_SOURCE "rdtsc"
#elif defined(__aarch64__)
static inline uint64_t ticks(void)
{
    uint64_t v;
    __asm__ __volatile__("isb; mrs %0, cntvct_el0" : "=r"(v) :: "memory");
    return v;
}
#define NGCC_TICK_SOURCE "cntvct_el0"
#else
static inline uint64_t ticks(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC_RAW, &t);
    return (uint64_t)t.tv_sec * 1000000000u + (uint64_t)t.tv_nsec;
}
#define NGCC_TICK_SOURCE "clock_gettime_ns"
#endif

enum { F_PSEUDOHASH, F_PSEUDOXOF, F_SM3HASH, F_DRNG, F_N };
typedef struct { uint32_t fn; uint64_t in_bits, out_bits, calls, ticks; } entry_t;
#define SLOTS 8192
static entry_t table[SLOTS];
static uint64_t overflow_calls;
static int depth, enabled;

static void account(uint32_t fn, uint64_t in_bits, uint64_t out_bits, uint64_t dt)
{
    uint64_t h = (fn * 0x9e3779b97f4a7c15ULL) ^ (in_bits * 0xbf58476d1ce4e5b9ULL) ^ (out_bits * 0x94d049bb133111ebULL);
    for (uint32_t probe = 0; probe < SLOTS; probe++) {
        entry_t *e = &table[(h + probe) & (SLOTS - 1)];
        if (!e->calls) { e->fn = fn; e->in_bits = in_bits; e->out_bits = out_bits; }
        if (e->fn == fn && e->in_bits == in_bits && e->out_bits == out_bits) {
            e->calls++; e->ticks += dt; return;
        }
    }
    overflow_calls++;
}

#define TIMED(fn, in_bits, out_bits, call) do { \
    if (!enabled || depth) { depth++; int r_ = (call); depth--; return r_; } \
    depth++; uint64_t t0_ = ticks(); int r_ = (call); uint64_t t1_ = ticks(); depth--; \
    account((fn), (in_bits), (out_bits), t1_ - t0_); return r_; } while (0)

__attribute__((weak)) int __real_pseudohash(int, const unsigned char *, unsigned long long, unsigned char *);
int __wrap_pseudohash(int d, const unsigned char *m, unsigned long long l, unsigned char *o)
{ TIMED(F_PSEUDOHASH, l, (uint64_t)d, __real_pseudohash(d, m, l, o)); }

__attribute__((weak)) int __real_pseudoXOF(unsigned long long, const unsigned char *, unsigned long long, unsigned char *);
int __wrap_pseudoXOF(unsigned long long d, const unsigned char *m, unsigned long long l, unsigned char *o)
{ TIMED(F_PSEUDOXOF, l, d, __real_pseudoXOF(d, m, l, o)); }

__attribute__((weak)) int __real_sm3hash(int, const unsigned char *, unsigned long long, unsigned char *);
int __wrap_sm3hash(int d, const unsigned char *m, unsigned long long l, unsigned char *o)
{ TIMED(F_SM3HASH, l, (uint64_t)d, __real_sm3hash(d, m, l, o)); }

__attribute__((weak)) int __real_get_random_number(void *, unsigned char *, unsigned long long);
int __wrap_get_random_number(void *c, unsigned char *o, unsigned long long bits)
{ TIMED(F_DRNG, 0, bits, __real_get_random_number(c, o, bits)); }

/* Exported driver interface (listed in hashprof.map). */
const char *ngcc_hashprof_tick_source(void) { return NGCC_TICK_SOURCE; }
uint64_t ngcc_hashprof_ticks(void) { return ticks(); }
void ngcc_hashprof_enable(int on) { enabled = on; }
void ngcc_hashprof_reset(void) { memset(table, 0, sizeof table); overflow_calls = 0; }
/* Copies up to max used entries; returns the number of used entries. */
size_t ngcc_hashprof_entries(entry_t *out, size_t max, uint64_t *overflow)
{
    size_t n = 0;
    for (size_t i = 0; i < SLOTS; i++)
        if (table[i].calls) { if (n < max) out[n] = table[i]; n++; }
    if (overflow) *overflow = overflow_calls;
    return n;
}
