/* Cost of individual hash calls, for the hash-substitution estimate.
 *
 *   hashcost iccs      < shapes    lines: FN IN_BITS OUT_BITS  (FN = pseudohash |
 *                                  pseudoXOF | sm3hash | drng), using the official
 *                                  api/auxfunc.c and api/drng.c linked into this tool
 *   hashcost lib LIB   < shapes    lines: DIGEST_BITS IN_BITS  (CryptHash of a
 *                                  hash-candidate library built by the harness)
 *
 * For every shape, prints the input fields followed by the median cost per call
 * over five batches, in CPU cycles when the hardware counter is readable
 * (perf_event_paranoid <= 2), otherwise in nanoseconds (the header says which).
 */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <inttypes.h>
#include <linux/perf_event.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <time.h>
#include <unistd.h>
#include "../../api/auxfunc.h"
#include "../../api/drng.h"

static int perf_fd = -1;

static uint64_t now_ns(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC_RAW, &t);
    return (uint64_t)t.tv_sec * 1000000000u + (uint64_t)t.tv_nsec;
}

static void counter_start(void)
{
    if (perf_fd >= 0) { ioctl(perf_fd, PERF_EVENT_IOC_RESET, 0); ioctl(perf_fd, PERF_EVENT_IOC_ENABLE, 0); }
}

static uint64_t counter_stop(uint64_t t0)
{
    uint64_t v = 0;
    if (perf_fd < 0) return now_ns() - t0;
    ioctl(perf_fd, PERF_EVENT_IOC_DISABLE, 0);
    if (read(perf_fd, &v, sizeof v) != sizeof v) v = 0;
    return v;
}

typedef int (*hash_fn)(int, const unsigned char *, unsigned long long, unsigned char *);
static unsigned char *msg, *out;
static DRNG_ctx drng;

static int call(int mode, const char *fn, hash_fn h, uint64_t a, uint64_t in_bits)
{
    if (mode) return h((int)a, msg, in_bits, out);
    if (!strcmp(fn, "pseudohash")) return pseudohash((int)a, msg, in_bits, out);
    if (!strcmp(fn, "pseudoXOF")) return pseudoXOF(a, msg, in_bits, out);
    if (!strcmp(fn, "sm3hash")) return sm3hash((int)a, msg, in_bits, out);
    if (!strcmp(fn, "drng")) return get_random_number(&drng, out, a);
    return -1;
}

static int cmp(const void *x, const void *y)
{
    double a = *(const double *)x, b = *(const double *)y;
    return (a > b) - (a < b);
}

int main(int argc, char **argv)
{
    int mode = argc == 3 && !strcmp(argv[1], "lib");
    if (!(argc == 2 && !strcmp(argv[1], "iccs")) && !mode) {
        fprintf(stderr, "usage: %s iccs | lib LIB  (shapes on stdin)\n", argv[0]); return 2;
    }
    hash_fn h = NULL;
    if (mode) {
        void *lib = dlopen(argv[2], RTLD_NOW | RTLD_LOCAL);
        if (!lib) { fprintf(stderr, "dlopen: %s\n", dlerror()); return 2; }
        void *f = dlsym(lib, "CryptHash");
        if (!f) { fprintf(stderr, "no CryptHash in %s\n", argv[2]); return 2; }
        memcpy(&h, &f, sizeof h);
    }
    struct perf_event_attr attr;
    memset(&attr, 0, sizeof attr);
    attr.type = PERF_TYPE_HARDWARE; attr.size = sizeof attr; attr.config = PERF_COUNT_HW_CPU_CYCLES;
    attr.disabled = 1; attr.exclude_kernel = 1; attr.exclude_hv = 1;
    perf_fd = (int)syscall(__NR_perf_event_open, &attr, 0, -1, -1, 0);
    unsigned char seed[48];
    for (int i = 0; i < 48; i++) seed[i] = (unsigned char)i;
    init_random_number(&drng, seed, sizeof seed);
    printf("#unit\t%s\n", perf_fd >= 0 ? "cycles" : "ns");
    char fn[32];
    uint64_t a, in_bits;
    size_t cap = 0;
    for (;;) {
        int got = mode ? scanf("%" SCNu64 " %" SCNu64, &a, &in_bits)
                       : scanf("%31s %" SCNu64 " %" SCNu64, fn, &in_bits, &a);
        if (got != (mode ? 2 : 3)) break;
        size_t need = (size_t)((in_bits + 7) / 8 + (a + 7) / 8 + 256);
        if (need > cap) {
            free(msg); free(out); cap = need;
            msg = calloc(cap, 1); out = calloc(cap, 1);
            if (!msg || !out) { perror("calloc"); return 2; }
            for (size_t i = 0; i < cap; i++) msg[i] = (unsigned char)(i * 131u + 7u);
        }
        /* warm up, then size batches to about 2 ms each */
        uint64_t t0 = now_ns();
        long k = 0;
        do { if (call(mode, fn, h, a, in_bits)) { fprintf(stderr, "call failed\n"); return 3; } k++; }
        while (now_ns() - t0 < 2000000u && k < 1000000);
        double per[5];
        for (int b = 0; b < 5; b++) {
            uint64_t s = now_ns();
            counter_start();
            for (long i = 0; i < k; i++) call(mode, fn, h, a, in_bits);
            per[b] = (double)counter_stop(s) / (double)k;
        }
        qsort(per, 5, sizeof per[0], cmp);
        if (mode) printf("%" PRIu64 "\t%" PRIu64 "\t%.1f\n", a, in_bits, per[2]);
        else printf("%s\t%" PRIu64 "\t%" PRIu64 "\t%.1f\n", fn, in_bits, a, per[2]);
        fflush(stdout);
    }
    return 0;
}
