# Performance method and limitations — system x86_1

System x86_1: Intel Core i7-12700 (Alder Lake), one performance core, turbo off, fixed 2.1 GHz, SMT off. [Summary](summary_x86_1.md).

## Measurement

- One 12th Gen Intel(R) Core(TM) i7-12700 core (CPU 2), SMT off, turbo off, governor `performance`. Cycles come from the hardware counter (`perf_event_open`, user mode); time from `CLOCK_MONOTONIC_RAW`.
- Reference builds use the guide's flags `-std=c99 -Wpedantic -Wall -Wextra -O2` plus `-fPIC -D_GNU_SOURCE -Wno-error=implicit-function-declaration -Wno-error=incompatible-pointer-types -Wno-error=int-conversion -Wno-error=implicit-int` for shared libraries and pre-C99 declarations; an instance that fails to build or to pass its KATs that way is rebuilt with the harness defaults, and its page says so. Optimized builds use the guide's performance flags.
- Only libraries that pass the submitted KATs are timed. The DRNG is seeded with bytes 00..2f; signatures use a 64-byte message; hash inputs are the guide's S1–S8 lengths.
- Each operation is calibrated with one call, then measured in 5 trials. Trials normally run in separate processes (fresh address-space layout); if setup takes more than 60 s, the trials share one process. Each trial runs a fixed number of calls, targeting 1.0 s and at least 100 calls in total; if that would exceed 15 minutes, fewer calls are used, but never fewer than one per trial. No operation is cut short by a time limit.
- Reported cycles are the arithmetic mean over all timed calls (the guide's metric); the median of the trial means is also recorded as a robustness check.
- Key exchange: `exchange` covers both initialisations, every pass and both key derivations of one protocol run (no network time); single steps are timed call by call.

## Share of the ICCS placeholder functions

Each reference library is relinked with link-time wrappers (`-Wl,--wrap`) around `pseudohash`, `pseudoXOF`, `sm3hash` and the DRNG's `get_random_number`. Every call that crosses an object-file boundary is timed with the CPU tick counter and recorded with its input and output length; nested calls are not counted twice. The reported share is the time inside these functions divided by the time of the whole operation, measured in the same process on the same inputs as the benchmark. The wrappers cost a few tens of cycles per call.

No performance figure with any particular hash candidate is given here: several hash submissions are not yet constant-time (e.g. table-based S-boxes), so their current timings are not production figures. The recorded call shapes are kept with the campaign data for a later comparison.

## Limitations

- Static and peak memory are process-level proxies (ELF image, VmHWM), not isolated algorithm memory.
- The ICCS share covers only the three helper functions; candidates that implement their own SHAKE/AES/SM3 show that time as non-symmetric (see the survey).
- Link-time wrapping is not reliable with LTO, so shares are measured on reference builds.
- The complete functional test vectors are referenced by digest, not embedded.
- Very slow operations have fewer than 100 timed calls; their pages say how many. Operations too slow for more than one call use their calibration call as the measurement.
- Timing ran on performance core(s) 2, 4: the three slowest instances (TRINE-512-Balanced, TRINE-512-ShortSig, UVW-512) and the hash profiling ran on a second performance core in parallel with the main run; each record states its CPU. Cycle counts are comparable across these identical cores.
- A single key-exchange step is timed around each call, so its wall time includes the counter start/stop system calls (a floor of roughly a microsecond); its user-mode cycle count does not. The `exchange` figure has no such overhead.

**Host warnings during this campaign:** CPU 2 governor is powersave, not performance; CPU 2 shares its core with CPUs 2-3 (SMT on); hardware cycle counter unavailable: set kernel.perf_event_paranoid=2; turbo/boost is enabled

