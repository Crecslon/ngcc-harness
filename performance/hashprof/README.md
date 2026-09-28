# ICCS hash/XOF instrumentation

Measures how much of each public-key operation is spent in the ICCS placeholder
helpers — `pseudohash` (SM3/HMAC-SM3), `pseudoXOF` (KDF-SM3), `sm3hash` — and in
the ICCS DRNG (`get_random_number`), and records the input and output length of
every call. `performance/campaign.py profile` drives it; the shares appear on
each `<id>/perf_<ID>.md` page and in `performance/symmetric-survey.md`.

| file | purpose |
|---|---|
| `wrap.c` | link-time wrappers (`-Wl,--wrap=...`): each call is timed with a tick counter (`rdtsc` on x86, `cntvct_el0` on AArch64) and accumulated per (function, input bits, output bits); nested calls are counted once; accounting is on only around the measured operation |
| `relink.sh` | relinks one built instance from its existing objects with the wrappers into `performance/hashprof/lib/<candidate>/lib<label>.so`, reusing the harness's own link command; only the helpers the objects define are wrapped; the candidate's own library is untouched |
| `hashprof.c` | driver: the same deterministic setup as `../ngcc_perf.c`, then N operations with accounting on; prints the total ticks and one `CALL` line per call shape |
| `hashcost.c` | prices call shapes in a hot loop with the official helpers (`iccs`) or with a hash candidate's `CryptHash` (`lib`); its output is kept in the campaign run directory and not published |

```sh
make -C performance                                   # builds ngcc_perf, hashprof and hashcost
L=$(performance/hashprof/relink.sh kem-22 Mithril-128)
performance/hashprof/hashprof $L keygen 0 100 1       # LIB OP BYTES ITERS WARMUPS
```

The reported share is the time inside the wrapped functions divided by the time
of the whole operation, both in ticks, measured in the same process with the same
deterministic inputs as the benchmark. The wrappers' bookkeeping falls outside
the timed call but inside the operation total, so shares of operations with very
many short calls are slightly understated.

Limitations: only calls that cross an object-file boundary are wrapped, which
covers every call from scheme code into the ICCS helpers; hash code that a
candidate implements itself (its own SHAKE, AES or SM3) is not counted — the
survey lists those candidates. Profiles are taken on the reference builds of
the public-key candidates only. Built libraries and binaries are Git-ignored
(`lib/`, `build/`, `hashprof`, `hashcost`).
