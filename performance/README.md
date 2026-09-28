# Performance study (in progress)

This is a separate listing from the security reports. The initial x86 method is
based on the [NICCS self-assessment announcement](https://www.niccs.org.cn/niccs/Notice/pc/content/content_2066798866453762048.html)
and its locally preserved [x86 guide](../doc/perf-x86.pdf), especially §§3.3–3.5.
The current [raw data](data/) are **preliminary VM measurements**, not complete
guide-conformant self-assessments or official submitter results.

The guide calls for KAT correctness, all instances and interfaces, average
execution time and CPU cycles, throughput, static and peak memory, data sizes,
environment and build records, raw evidence, a 64-byte signing message, and
hash messages of 32, 128, 512, 1024, 4096, 8192, 16384 and 65536 bytes. It
recommends at least 100 measurements when repeated testing is needed.

Our runner pins one CPU, seeds the candidate's ICCS DRNG with bytes `00..2f`,
does three untimed warm-ups, then takes five separate timed trials of each API
operation. The arithmetic mean over all successful operations is primary; the
middle of the five trial means is supplementary for a contended VM. A process
targets at least one second and 100 calls per trial, subject to a 20,000-call
trial cap. It measures one operation with a 60-second internal budget and a 65-second
external hard timeout including setup. Fewer than 100 measurements or a failed
KAT is never silently presented as a complete result. Each operation's actual
input rule, sample counts, trial times, command, library and archive digests,
compiler flags, environment and limitations are in its JSON record.
For KEM decapsulation, the honest shared-secret comparison is done before
timing; the timed loop calls the submitted decapsulation API and checks its
return code and output length, without including the byte comparison.

The VM currently denies hardware CPU-cycle counters (`perf_event_paranoid=4`).
We report **no CPU-cycle number** rather than mislabeling virtual TSC ticks.
The ELF `PT_LOAD` image size and process baseline/peak RSS are resource proxies,
not isolated static/peak algorithm memory. Shared-library builds require
`-fPIC` beyond the guide's listed flags. These gaps, plus the absence of full
functional vectors inside each JSON report, are stated in every record. No
reference or optimized result is called fully guide-conformant yet. KAT PASS
only verifies the submitted vectors; it does not rule out rare honest failures.

## Source provenance and builds

All 119 submission packages are represented by their software source/include
files. Local ZIP copies are optional and Git-ignored. The [source catalog](source_catalog.csv)
records per-package counts and archive hashes; path-name counts there are not
claims that a variant builds. `IDS=<id> ./download.sh` can fetch an official ZIP
into ignored `orig/` for re-auditing. `performance/import_sources.py` checks
its SHA-256 against `SOURCE_ARCHIVES.md`, then imports source files or package
license notices without overwriting any differing file. `performance/import_dove.py` handles DOVE's
nested RARs using `bsdtar`. Submitted build scripts and binaries are not
executed. The staged variants use the same uniform API as the reference
harness. At present, four submissions have explicit performance build rules;
the other imported source trees are **source-only**, not benchmark-ready yet.

Current pilot:

```sh
make -C performance build-mithril-ref
make -C performance build-mithril-avx2
make -C performance build-scloud-ref
make -C performance build-scloud-avx2
make -C performance build-zcdmc-ref
make -C performance build-zcdmc-avx2
make -C performance build-bit-ref
make -C performance build-bit-avx2
make -C performance
make -C performance smoke-x86
python3 performance/smoke.py \
  --library sign-02/lib/libBiT-256-avx2.so \
  --kat-log sign-02/results/BiT-256-avx2.log
python3 performance/run.py \
  --library kem-22/lib/libMithril-256-avx2.so \
  --kat-log kem-22/results/Mithril-256-avx2.log \
  --output performance/data/my-new-run.json
```

## Full campaign (all harness-built candidates)

`performance/campaign.py` extends the pilot to every candidate with a harness
Makefile — KEMs, signatures, key exchange and hash functions — and adds the
share of each operation spent in the ICCS placeholder hash functions. Fix the host first (one
performance core, turbo off, `performance` governor, SMT off,
`kernel.perf_event_paranoid=2`); `campaign.py check` lists what is still
wrong, and the measuring phases refuse to run on an unfixed host.

```sh
python3 performance/campaign.py check --cpu 2
python3 performance/campaign.py all --cpu 2          # resumable; see --run-dir
python3 performance/report.py performance/runs/<host>-campaign-<UTC>
```

Phases: `build` (guide reference flags, falling back per instance to the
harness defaults when a submission does not build or pass its KATs that way),
`calibrate` (one call per operation), `measure`, `profile` and `hashcost`.
Work is bounded by iteration counts, not wall time: each operation gets five
trials, normally each in a fresh process so memory-layout effects are sampled
rather than fixed per operation; fast operations get at least 100 timed calls,
slow ones fewer (at least one per trial), and the cheapest run first. Records
include the plan, all trials, sizes, memory proxies and evidence digests.

`performance/hashprof/` relinks reference libraries so that each call of the
ICCS helpers (`pseudohash`, `pseudoXOF`, `sm3hash`, DRNG) is timed and its
input/output length recorded. `hashcost` prices those call shapes with the
official helpers and with every hash candidate; that data stays in the run
directory and is not published, because several hash submissions are not yet
constant-time (e.g. table-based S-boxes), so their timings are not production
figures.

Reports are named by test system so that architectures and machines never
overwrite each other. `performance/systems.csv` registers each system with an
ID of the form `<arch>_<n>` (e.g. `x86_1` = host `blk`); `campaign.py` records
the ID in the run's `campaign.json` and refuses to mix systems in one run
directory. `report.py` then writes one report per candidate as
`<id>/perf_<ID>.md`, next to the other per-candidate reports (guide §3.5 items
1–7, KAT issues from `kat_issues.csv`, and the ICCS hash/DRNG share), plus
`performance/summary_<ID>.md` and `performance/method_<ID>.md`; the source-based
`performance/symmetric-survey.md` (from `symmetric_survey.csv`) is shared by all
systems. Run directories stay per host and time
(`performance/runs/<hostname>-campaign-<UTC>/`). The same scripts run on
AArch64: `campaign.py` selects the ARM guide flags and the wrapper uses
`cntvct_el0` instead of `rdtsc`; register the ARM machine (e.g. `arm_1`) first.

## Run on a new x86-64 host

After these changes have been committed and published, an ordinary clone
contains everything needed for the four integrated families; ZIPs and full
test-vector text are not required. On a Linux host with GCC, GNU make, Python
3, `taskset` (util-linux), `readelf` (binutils), and an AVX2-capable CPU:

```sh
git clone https://github.com/ngcc-dev/ngcc-harness.git
cd ngcc-harness
make -C performance smoke-x86
python3 performance/run_x86.py --dry-run
python3 performance/run_x86.py
```

The last command rebuilds and KAT-checks all 26 reference/AVX2 instances,
then runs five timed trials per API operation with a 60-second operation
budget. On a fixed-clock 2.1 GHz Alder Lake P-core it takes about ten
minutes; the smoke command above writes no measurement records. To use an
available CPU explicitly, pass `--cpu N`; on a hybrid CPU choose a
performance core, since the generic cycle counter may not count on the other
core type (such rows are then recorded without cycles). Use
`--family mithril` (or `scloud`, `zcdmc`, `bit`) to partition the run. On a
machine without AVX2, use `--variant ref` and build/check those reference
variants separately. ARM optimized benchmarking is not wired up yet.

New records go under ignored `performance/runs/<host>-<UTC>/`; they are not
silently added to the public dataset. Review them before moving selected
records into `performance/data/`. Every record includes KAT provenance,
build flags, host information, five raw trials, and explicit guide gaps.
`run_x86.py` checks each completed record and reports partial/failed runs.

The Mithril AVX2 integration covers all three levels. Scloud+ SHAKE-128 is a
staged example with reference and AVX2 builds. ZC-DMC now has reference and
AVX2 builds for all six levels. BiT has reference and AVX2 builds for all
three levels; its 128/256 assembly requires only linker symbol aliases, while
all submitted source files remain unchanged. `performance/smoke.py` checks
KAT evidence and
runs short functional timings **without writing or publishing numbers**; pass
`--library` and `--kat-log` to test an individual build. Scloud+'s `neon`
backend source is also retained, and
`make -C kem-35 -f ../performance/kem-35.mk PERF_NEON=1 list` shows the ARM
target; it cannot be compiled or KAT-tested on this x86 VM.
`make -C performance smoke-x86` rebuilds and KAT-checks all four staged x86
optimized families before their short operation checks. It writes no new
performance JSON; full measurement runs are deliberately deferred.
Scloud+'s KAT manifest is derived from the official archived SHAKE-128 vector,
so a clean checkout does not need the full vector text to check this pilot.
Future physical x86 and ARM measurements will be stored separately, never
pooled with these VM records.
