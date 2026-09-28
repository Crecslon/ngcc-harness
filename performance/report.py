#!/usr/bin/env python3
"""Render a campaign run directory into Markdown reports.

    python3 performance/report.py RUN_DIR [--system ID] [--out DIR]

The system ID (performance/systems.csv, e.g. x86_1) comes from the run's
campaign.json or its hostname; it keeps reports from different architectures
and machines apart. Writes, next to the other per-candidate reports:
  <id>/perf_<ID>.md      one report per candidate, following the guide's report
                         items (1)-(7), plus the share of each operation spent in
                         the ICCS placeholder hash functions and DRNG
and, in --out (default performance/):
  summary_<ID>.md        cycles per operation and ICCS hash share, all candidates
  method_<ID>.md         method, host settings and limitations
  symmetric-survey.md    which candidates use the ICCS helpers (source analysis,
                         shared by all systems), with this system's measured share

Numbers are taken only from records in RUN_DIR. No estimate of performance
with any particular hash candidate is published: several hash submissions are
not yet constant-time (e.g. table-based S-boxes), so their timings are not
production figures. The hash-cost data stays in RUN_DIR/hashcost/.
"""

from __future__ import annotations

import argparse
import csv
import sys
import json
import os
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATS = [("kem", "Key encapsulation"), ("sign", "Digital signatures"), ("kex", "Key exchange"),
        ("hash", "Hash functions")]
ORDER = ["keygen", "enc", "dec", "sign", "verify", "exchange", "init_a", "init_b"] + \
    [f"pass{k}" for k in range(1, 17)] + ["derive_a", "derive_b"]


def op_order(key: str):
    base, _, size = key.partition("_") if key.startswith("hash") else (key, "", "")
    return (ORDER.index(base) if base in ORDER else len(ORDER), int(size or 0), key)


OPS = {"kem": ["keygen", "enc", "dec"], "sign": ["keygen", "sign", "verify"], "kex": ["exchange"],
       "hash": ["hash_32", "hash_65536"]}


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def fmt_int(x):
    if x is None:
        return "–"
    if x >= 1e9:
        return f"{x / 1e9:.2f} G"
    if x >= 1e6:
        return f"{x / 1e6:.2f} M"
    if x >= 1e4:
        return f"{x / 1e3:.1f} k"
    return f"{x:.0f}"


def fmt_time(s):
    if s is None:
        return "–"
    for unit, f in (("s", 1), ("ms", 1e3), ("µs", 1e6), ("ns", 1e9)):
        if s * f >= 1:
            return f"{s * f:.3g} {unit}"
    return f"{s * 1e9:.3g} ns"


def pct(x):
    return "–" if x is None else f"{100 * x:.0f}%" if x >= 0.095 else f"{100 * x:.1f}%"


class Run:
    def __init__(self, run: Path):
        self.dir = run
        self.campaign = load(run / "campaign.json") or {}
        self.build = (load(run / "build.json") or {}).get("instances", {})
        self.records = defaultdict(dict)   # (cand, label) -> op_key -> record
        for f in sorted((run / "records").rglob("*.json")):
            r = load(f)
            key = r["operation"] + (f"_{r['input_bytes']}" if r.get("input_bytes") else "")
            r["_path"] = f.relative_to(run).as_posix()
            self.records[(r["candidate"], r["label"])][key] = r
        # the measuring host as recorded in the timing records (campaign.json's
        # start environment may predate the fixed host settings, e.g. the build phase)
        envs = [r["environment"] for recs in self.records.values() for r in recs.values()
                if r.get("status") == "complete" and r.get("environment")]
        main = [e for e in envs if str(e.get("cpu_number")) == "2"] or envs
        self.env = main[0] if main else self.campaign.get("environment_at_start", {})
        self.cpus = sorted({e.get("cpu_number") for e in envs})
        self.profiles = defaultdict(dict)
        for f in sorted((run / "profile").rglob("*__*.json")):
            r = load(f)
            if "operation" not in r:
                continue
            key = r["operation"] + (f"_{r['input_bytes']}" if r.get("input_bytes") else "")
            r["_path"] = f.relative_to(run).as_posix()
            self.profiles[(r["candidate"], r["label"])][key] = r
        self.names, self.pages = {}, {}
        with (ROOT / "downloads.csv").open(encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter=";"):
                self.names[row["ID"]] = row["Algorithm"]
                self.pages[row["ID"]] = row.get("PageURL", "")
        self.survey = {}
        with (ROOT / "performance/symmetric_survey.csv").open(encoding="utf-8") as f:
            for row in csv.DictReader((l for l in f if not l.startswith("#")), delimiter=";"):
                self.survey[row["ID"]] = row
        self.kat_issues = []
        with (ROOT / "performance/kat_issues.csv").open(encoding="utf-8") as f:
            self.kat_issues = list(csv.DictReader((l for l in f if not l.startswith("#")), delimiter=";"))
        self.params = defaultdict(list)
        with (ROOT / "data/parameters.csv").open(encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter=";"):
                self.params[row["ID"]].append(row)


OUT = ROOT / "performance"
SYSTEM = "x86_1"          # set in main() from --system / the run
SYSTEM_DESC = ""


def load_systems() -> dict:
    with (ROOT / "performance/systems.csv").open(encoding="utf-8") as f:
        return {r["ID"]: r for r in csv.DictReader((l for l in f if not l.startswith("#")), delimiter=";")}


CHECK = False            # --check: compare with the files on disk instead of writing
DIFFERENT: list[str] = []


def emit(path: Path, text: str) -> None:
    if CHECK:
        if not path.is_file() or path.read_text(encoding="utf-8") != text:
            DIFFERENT.append(path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path))
        return
    path.write_text(text, encoding="utf-8")


def evidence_dir(run) -> str:
    return run.dir.relative_to(ROOT).as_posix() if run.dir.is_relative_to(ROOT) else str(run.dir)


def record_host_state(run) -> tuple[int, dict]:
    """(complete timing records, {deviation: count}) from each record's stored environment."""
    import collections
    n, issues = 0, collections.Counter()
    for recs in run.records.values():
        for r in recs.values():
            if r.get("status") != "complete":
                continue
            n += 1
            e = r.get("environment") or {}
            if e.get("intel_pstate_no_turbo") == "0" or e.get("cpufreq_boost") == "1":
                issues["turbo enabled"] += 1
            if e.get("cpufreq_governor") not in (None, "performance"):
                issues[f"governor {e.get('cpufreq_governor')}"] += 1
            if e.get("smt_control") not in (None, "off", "forceoff", "notsupported", "notimplemented"):
                issues[f"SMT {e.get('smt_control')}"] += 1
            if not r.get("mean_cycles"):
                issues["no hardware cycle count"] += 1
    return n, dict(issues)


def cand_page(cand: str) -> Path:
    return ROOT / cand / f"perf_{SYSTEM}.md"


def summary_page(out: Path) -> Path:
    return out / f"summary_{SYSTEM}.md"


def method_page_path(out: Path) -> Path:
    return out / f"method_{SYSTEM}.md"


def link(frm: Path, to: Path) -> str:
    """Relative Markdown link target from the page at frm to the page at to."""
    return os.path.relpath(to, frm.parent).replace(os.sep, "/")


def value(rec, unit="cycles"):
    if not rec or rec.get("status") != "complete":
        return None
    return rec.get("mean_cycles") if unit == "cycles" else rec.get("mean_seconds")


def clock_text(env: dict) -> str:
    turbo = {"1": "off", "0": "on"}.get(env.get("intel_pstate_no_turbo") or "",
                                         {"0": "off", "1": "on"}.get(env.get("cpufreq_boost") or "", "unknown"))
    mhz = int(env.get("cpufreq_max_khz") or 0) / 1e6
    return f"max {mhz:.2f} GHz, governor {env.get('cpufreq_governor')}, turbo {turbo}, SMT {env.get('smt_control')}"


def cell(rec):
    if not rec:
        return "–"
    if rec.get("status") != "complete":
        return "failed"
    c = rec.get("mean_cycles")
    s = fmt_int(c) if c else fmt_time(rec.get("mean_seconds"))
    return s + ("" if rec.get("guide_100_measurements_met") else f" (n={rec.get('measurements')})")


def instances_of(run: Run, cand: str):
    labels = sorted({l for (c, l) in run.records if c == cand} |
                    {e["label"] for e in run.build.values() if e["candidate"] == cand})
    def natural(label):
        return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", label)]
    return sorted(labels, key=natural)


def summary(run: Run, out: Path, arch: str):
    env = run.env
    lines = [f"# Performance — {arch}, system {SYSTEM}", "",
             "Independent measurements of the NGCC Round 1 implementations on one "
             f"{env.get('cpu_model', 'x86-64')} core ({clock_text(env)}). "
             "Cycles are the mean of all timed calls in five trials, normally each in a "
             "fresh process. **Symmetric %** is the share of each operation spent in the ICCS "
             "placeholder hash functions (`pseudohash`, `pseudoXOF`, `sm3hash`); the ICCS DRNG is "
             "counted separately on the candidate pages. Candidates that implement their own "
             "hashing show a low share here — see the [symmetric cryptography survey](symmetric-survey.md). "
             "These are not submitter self-assessments and not NICCS results.", "",
             f"See [method and limitations]({method_page_path(out).name}). `–` = not measured (no harness build or "
             "timeout); `n=` marks operations with fewer than 100 timed calls; ⚠ marks instances whose "
             "submitted KAT vectors are not reproduced by the submitted code (timed, but output not "
             "validated — see the candidate page).", ""]
    for cat, title in CATS:
        rows = []
        for cand in sorted({c for (c, l) in run.records if c.startswith(cat)} |
                           {e["candidate"] for e in run.build.values() if e["candidate"].startswith(cat)}):
            for label in instances_of(run, cand):
                recs = run.records.get((cand, label), {})
                entry = run.build.get(f"{cand}/{label}", {})
                if entry.get("variant", "reference") != "reference" and not recs:
                    continue
                cells = []
                for op in OPS[cat]:
                    cells.append(cell(recs.get(op)))
                    if cat in ("kem", "sign", "kex"):
                        p = run.profiles.get((cand, label), {}).get(op)
                        cells.append(pct(p.get("hash_share")) if p and "hash_share" in p else "–")
                variant = " (AVX2)" if label.endswith("-avx2") else ""
                status = entry.get("kat")
                if status and status != "PASS":
                    variant += f" ⚠ KAT {status}"
                rows.append(f"| [{cand}]({link(summary_page(out), cand_page(cand))}) | {run.names.get(cand, '')} | "
                            f"`{label}`{variant} | " + " | ".join(cells) + " |")
        if not rows:
            continue
        lines += [f"## {title}", ""]
        if cat == "hash":
            lines += ["| id | algorithm | instance | 32 B (cycles) | 64 KiB (cycles) |", "|---|---|---|---|---|"]
        else:
            hdr = " | ".join(f"{op} | sym %" for op in OPS[cat])
            lines += [f"| id | algorithm | instance | {hdr} |", "|---|---|---|" + "---|" * (2 * len(OPS[cat]))]
        lines += rows + [""]
    emit(summary_page(out), "\n".join(lines) + "\n")


def candidate_page(run: Run, cand: str, out: Path, arch: str):
    cat = cand.split("-")[0]
    name = run.names.get(cand, "")
    env = run.env
    labels = instances_of(run, cand)
    L = [f"# {cand} {name} — performance on {arch} (system {SYSTEM})", "",
         f"[Performance {SYSTEM}]({link(cand_page(cand), summary_page(out))}) › `{cand}` · "
         f"[method]({link(cand_page(cand), method_page_path(out))}) · [NICCS page]({run.pages.get(cand, '')})", "",
         "Independent measurement following the structure of the NICCS x86 self-assessment "
         "guide, §3.5 (1)–(7). Not a submitter self-assessment.", ""]
    # (1)
    fn = {"kem": "key encapsulation", "sign": "digital signature", "kex": "key exchange", "hash": "hash"}[cat]
    L += ["## 1. Basic information", "",
          f"- Category: {'public-key' if cat != 'hash' else 'cryptographic hash'} algorithm; function: {fn}",
          f"- Algorithm: {name}",
          "- Implementation versions measured: " + ", ".join(sorted({
              "optimized (AVX2)" if l.endswith("-avx2") else "reference" for l in labels})),
          "- Parameter sets: " + ", ".join(f"`{l}`" for l in labels), ""]
    # (2)
    L += ["## 2. Assessment environment", "",
          "| item | value |", "|---|---|",
          f"| processor | {env.get('cpu_model')} (CPU {env.get('cpu_number')}, one core) |",
          f"| clock | {clock_text(env)} |",
          f"| memory | {int(env.get('memory_total_kib') or 0) // 1024} MiB |",
          f"| OS / kernel | {env.get('os')} / {env.get('kernel')} |",
          f"| compiler / build tool | {env.get('compiler')} / {env.get('cmake')} |",
          f"| campaign start / end (UTC) | {run.campaign.get('started_utc', '')[:19]} / {run.campaign.get('ended_utc', '')[:19]} |", ""]
    # (3)
    L += ["## 3. Functional testing (KAT)", "",
          "Each library was checked against the submitted KAT vectors (SHA-256 manifest "
          f"`{cand}/kat.sha256` in the harness) before timing.", "",
          "| instance | build flags | KAT |", "|---|---|---|"]
    notes = []
    for l in labels:
        e = run.build.get(f"{cand}/{l}", {})
        issue = next((i for i in run.kat_issues if i["ID"] == cand and re.search(i["Label"], l)), None)
        mark = ""
        if issue:
            if issue not in notes:
                notes.append(issue)
            mark = f" [{notes.index(issue) + 1}]"
            if issue["Action"] == "exclude":
                mark += " (not timed)"
        L.append(f"| `{l}` | {e.get('flags', '–')} | {e.get('kat', '–')}{mark} |")
    L.append("")
    for n, issue in enumerate(notes, 1):
        L.append(f"[{n}] {issue['Cause']}" + (" These instances are timed anyway; their output is not validated."
                                              if issue["Action"] == "measure" else ""))
        L.append("")
    # (4)
    L += ["## 4. Performance", ""]
    if cat == "hash":
        L += ["| instance | message | mean cycles | cycles/byte | mean time | MB/s | n |", "|---|---|---|---|---|---|---|"]
    else:
        L += ["| instance | operation | mean cycles | mean time | ops/s | median trial | n (trials × iters) |",
              "|---|---|---|---|---|---|---|"]
    for l in labels:
        for key, r in sorted(run.records.get((cand, l), {}).items(), key=lambda kv: op_order(kv[0])):
            if r.get("status") != "complete":
                L.append(f"| `{l}` | {key} | failed | | | | |")
                continue
            n = f"{r['measurements']} ({r['plan']['trials']} × {r['plan']['iterations_per_trial']})"
            if cat == "hash":
                c = r.get("mean_cycles")
                L.append(f"| `{l}` | {r['input_bytes']} B | {fmt_int(c)} | {c / r['input_bytes']:.1f} | "
                         f"{fmt_time(r['mean_seconds'])} | {r.get('throughput_MB_per_second') or 0:.1f} | {n} |"
                         if c else f"| `{l}` | {r['input_bytes']} B | – | – | {fmt_time(r['mean_seconds'])} | "
                         f"{r.get('throughput_MB_per_second') or 0:.1f} | {n} |")
            else:
                retries = sum(int(pr.get("meta", {}).get("sign_failures_retried", 0) or 0)
                              for pr in r.get("processes", []))
                if retries:
                    n += f"; {retries} failed signing attempts retried"
                L.append(f"| `{l}` | {key} | {fmt_int(r.get('mean_cycles'))} | {fmt_time(r['mean_seconds'])} | "
                         f"{r['operations_per_second']:.3g} | {fmt_time(r['median_trial_seconds'])} | {n} |")
    L.append("")
    # (5)
    L += ["## 5. Resource consumption", "",
          "Static memory is approximated by the library's loadable ELF segments; peak memory is "
          "the process high-water mark (VmHWM) including the benchmark driver and libc, so both are "
          "upper-bound proxies rather than isolated algorithm memory.", "",
          "| instance | operation | static: ELF image (bytes) | baseline RSS | peak RSS |", "|---|---|---|---|---|"]
    for l in labels:
        elf = run.build.get(f"{cand}/{l}", {}).get("elf_load_bytes")
        for key, r in sorted(run.records.get((cand, l), {}).items(), key=lambda kv: op_order(kv[0])):
            if r.get("peak_rss_bytes"):
                L.append(f"| `{l}` | {key} | {elf if elf is not None else '–'} | "
                         f"{r['baseline_rss_bytes'] // 1024} KiB | {r['peak_rss_bytes'] // 1024} KiB |")
    L.append("")
    # (6)
    if cat != "hash":
        L += ["## 6. Transmission and storage overhead", ""]
        if cat == "kex":
            L += ["| instance | passes | messages (bytes) | total | long-term pk / sk | shared secret |",
                  "|---|---|---|---|---|---|"]
        else:
            L += ["| instance | public key | secret key | " + ("ciphertext | shared secret |" if cat == "kem" else "signature |"),
                  "|---|---|---|---|" + ("---|" if cat == "kem" else "")]
        for l in labels:
            recs = run.records.get((cand, l), {})
            r = next((x for x in recs.values() if x.get("sizes")), None)
            if not r:
                continue
            s = r["sizes"]
            if cat == "kem":
                L.append(f"| `{l}` | {s.get('pk_bytes')} | {s.get('sk_bytes')} | {s.get('ct_bytes')} | {s.get('ss_bytes')} |")
            elif cat == "sign":
                L.append(f"| `{l}` | {s.get('pk_bytes')} | {s.get('sk_bytes')} | {s.get('signature_bytes')} |")
            else:
                msgs = [s[k] for k in sorted((k for k in s if re.match(r"msg\d+_bytes", k)), key=lambda k: int(k[3:-6]))]
                L.append(f"| `{l}` | {r.get('kex', {}).get('kex_passes')} | {' / '.join(map(str, msgs))} | "
                         f"{s.get('total_msg_bytes')} | {s.get('pk_bytes')} / {s.get('sk_bytes')} | {s.get('ss_actual_bytes', s.get('ss_bytes'))} |")
        L.append("")
    # share of the ICCS placeholder functions
    if cat != "hash":
        sv = run.survey.get(cand, {})
        L += ["## Symmetric primitives", "",
              f"[Survey]({link(cand_page(cand), out / 'symmetric-survey.md')}) verdict: "
              f"**{sv.get('Verdict', 'not surveyed')}**" + (f" — {sv['Notes']}" if sv.get("Notes") else ""), "",
              "Share of each operation spent in the ICCS placeholder hash functions and in the ICCS DRNG "
              "(reference build, measured in the same run with link-time wrappers):", "",
              "| instance | operation | pseudohash/XOF/sm3 | DRNG | calls per operation |", "|---|---|---|---|---|"]
        for l in labels:
            for key, p in sorted(run.profiles.get((cand, l), {}).items(), key=lambda kv: op_order(kv[0])):
                if p.get("status") != "complete":
                    continue
                ops = p["total"]["operations"]
                calls = defaultdict(float)
                for c in p["calls"]:
                    calls[c["fn"]] += c["calls"] / ops
                cstr = ", ".join(f"{fn} {v:.3g}" for fn, v in sorted(calls.items()))
                L.append(f"| `{l}` | {key} | {pct(p.get('hash_share'))} | {pct(p.get('share', {}).get('drng', 0))} | {cstr or '–'} |")
        L.append("")
    # (7)
    L += ["## 7. Raw evidence index", "",
          f"Paths are relative to `{evidence_dir(run)}/` in the "
          "[harness](https://github.com/ngcc-dev/ngcc-harness); each JSON file records its commands, "
          "environment and trials.", "",
          "| instance | item | file |", "|---|---|---|"]
    for l in labels:
        e = run.build.get(f"{cand}/{l}", {})
        if e.get("kat_log"):
            L.append(f"| `{l}` | KAT log (sha256 `{e['kat_log_sha256'][:16]}…`) | `{e['kat_log']}` |")
        for key, r in sorted(run.records.get((cand, l), {}).items()):
            L.append(f"| `{l}` | timing {key} | `{r['_path']}` |")
        for key, p in sorted(run.profiles.get((cand, l), {}).items()):
            L.append(f"| `{l}` | hash profile {key} | `{p['_path']}` |")
    L += ["", "Scripts: `performance/campaign.py`, `performance/ngcc_perf.c`, `performance/hashprof/` "
          "in the [harness](https://github.com/ngcc-dev/ngcc-harness).", ""]
    emit(cand_page(cand), "\n".join(L) + "\n")


def survey_page(run: Run, out: Path):
    counts = defaultdict(int)
    for r in run.survey.values():
        counts[r["Verdict"]] += 1
    L = ["# Symmetric cryptography survey", "",
         "The NGCC public-key submissions were asked to use the ICCS placeholder functions "
         "`pseudohash` (SM3/HMAC-SM3), `pseudoXOF` (KDF-SM3) and `sm3hash` for hashing, and the "
         "ICCS SM3 DRNG for randomness, so that the selected NGCC hash can later be substituted. "
         "This survey records which reference implementations do so, which bypass the helpers with "
         "their own primitives, and how much of each operation the helpers take.", "",
         "Totals: " + ", ".join(f"{v} {k}" for k, v in sorted(counts.items(), key=lambda kv: -kv[1])) + ".", "",
         "Evidence: call-graph reachability from the exported API in the harness-built libraries, "
         "object-level constant scans (Keccak, SHA-2, SM3, AES, SM4, ChaCha), and source reading for "
         "candidates without a harness build. A primitive that is compiled but unreachable is not "
         "counted.", "",
         f"The last column is measured on system {SYSTEM} ({SYSTEM_DESC}); see its "
         f"[summary]({summary_page(out).name}).", "",
         f"| id | algorithm | verdict | notes | largest hash share on {SYSTEM} (op) |", "|---|---|---|---|---|"]
    for cand in sorted(run.survey, key=lambda c: (c.split("-")[0], c)):
        best = None
        for (c, l), profs in run.profiles.items():
            if c != cand:
                continue
            for key, p in profs.items():
                if "hash_share" in p and (best is None or p["hash_share"] > best[0]):
                    best = (p["hash_share"], f"{l} {key}")
        r = run.survey[cand]
        ref = f"[{cand}]({link(out / 'symmetric-survey.md', cand_page(cand))})" if cand_page(cand).is_file() else cand
        L.append(f"| {ref} | {run.names.get(cand, '')} | {r['Verdict']} | {r['Notes']} | "
                 f"{pct(best[0]) + ' (' + best[1] + ')' if best else '–'} |")
    emit(out / "symmetric-survey.md", "\n".join(L) + "\n")


def host_state_text(run) -> str:
    n, issues = record_host_state(run)
    if not issues:
        return (f"All {n} timing records were taken in this state (turbo off, `performance` governor, "
                "SMT off, hardware cycle counter available), as stored in each record.")
    return (f"Of {n} timing records, some deviate from the fixed host state: "
            + "; ".join(f"{k} ({v})" for k, v in sorted(issues.items())) + ".")


def secondary_core_text(run) -> str:
    main = run.env.get("cpu_number")
    other = sorted({(c, l) for (c, l), recs in run.records.items() for r in recs.values()
                    if r.get("status") == "complete" and (r.get("environment") or {}).get("cpu_number") != main})
    cores = ", ".join(str(c) for c in run.cpus)
    if not other:
        return f"- All timing ran on CPU {main}."
    names = ", ".join(f"{c} {l}" for c, l in other)
    return (f"- Timing ran on performance core(s) {cores}. The slowest instances ({names}) were timed on a "
            f"second performance core in parallel with the main run on CPU {main}, as was the hash "
            "profiling; each record states its CPU. Cycle counts are comparable across these identical cores.")


def method_page(run: Run, out: Path, arch: str):
    c = run.campaign
    pl = c.get("planning", {})
    cfg = c.get("arch_config") or {}
    env = run.env
    L = [f"# Performance method and limitations — system {SYSTEM}", "",
         f"System {SYSTEM}: {SYSTEM_DESC}. [Summary]({summary_page(out).name}).", "",
         "## Measurement", "",
         f"- One {env.get('cpu_model')} core (CPU {env.get('cpu_number')}; {clock_text(env)}). "
         "Cycles come from the hardware counter (`perf_event_open`, user mode); time from "
         "`CLOCK_MONOTONIC_RAW`. " + host_state_text(run),
         f"- Reference builds use the guide's flags `{cfg.get('reference')}` plus "
         f"`{c.get('harness_additions')}` for shared libraries and pre-C99 declarations; an instance "
         "that fails to build or to pass its KATs that way is rebuilt with the harness defaults, and "
         "its page says so. Optimized builds use the guide's performance flags.",
         "- Every library is checked against the submitted KAT vectors before timing. Instances "
         "whose vectors are not reproduced by the submitted code are still timed and are marked ⚠, "
         "with the identified cause on their candidate page (`performance/kat_issues.csv`); an "
         "instance without a reference source of its own is not timed. The DRNG is seeded with "
         "bytes 00..2f; signatures use a 64-byte message; hash inputs are the guide's S1–S8 lengths.",
         f"- Each operation is calibrated with one call, then measured in {pl.get('trials', 5)} trials. "
         f"Trials normally run in separate processes (fresh address-space layout); if setup takes "
         f"more than {pl.get('separate_process_setup_s', 60):.0f} s, the trials share one process. "
         f"Each trial runs a fixed number of calls, targeting {pl.get('trial_target_s', 1)} s and "
         f"at least {pl.get('min_total', 100)} calls in total; if that would exceed "
         f"{pl.get('op_budget_s', 1800) / 60:.0f} minutes, fewer calls are used, but never fewer than "
         "one per trial. No operation is cut short by a time limit.",
         "- Reported cycles are the arithmetic mean over all timed calls (the guide's metric); the "
         "median of the trial means is also recorded as a robustness check.",
         "- Key exchange: `exchange` covers both initialisations, every pass and both key "
         "derivations of one protocol run (no network time); single steps are timed call by call.", "",
         "## Share of the ICCS placeholder functions", "",
         "Each reference library is relinked with link-time wrappers (`-Wl,--wrap`) around "
         "`pseudohash`, `pseudoXOF`, `sm3hash` and the DRNG's `get_random_number`. Every call that "
         "crosses an object-file boundary is timed with the CPU tick counter and recorded with its "
         "input and output length; nested calls are not counted twice. The reported share is the "
         "time inside these functions divided by the time of the whole operation, measured in the "
         "same process on the same inputs as the benchmark. The wrappers cost a few tens of cycles "
         "per call.", "",
         "No performance figure with any particular hash candidate is given here: several hash "
         "submissions are not yet constant-time (e.g. table-based S-boxes), so their current timings "
         "are not production figures. The recorded call shapes are kept with the campaign data for "
         "a later comparison.", "",
         "## Limitations", "",
         "- Static and peak memory are process-level proxies (ELF image, VmHWM), not isolated "
         "algorithm memory.",
         "- The ICCS share covers only the three helper functions; candidates that implement their "
         "own SHAKE/AES/SM3 show that time as non-symmetric (see the survey).",
         "- Link-time wrapping is not reliable with LTO, so shares are measured on reference builds.",
         "- The complete functional test vectors are referenced by digest, not embedded.",
         "- Very slow operations have fewer than 100 timed calls; their pages say how many. "
         "Operations too slow for more than one call use their calibration call as the measurement.",
         secondary_core_text(run),
         "- A single key-exchange step is timed around each call, so its wall time includes the "
         "counter start/stop system calls (a floor of roughly a microsecond); its user-mode cycle "
         "count does not. The `exchange` figure has no such overhead.", ""]
    emit(method_page_path(out), "\n".join(L) + "\n")


def main():
    global SYSTEM, SYSTEM_DESC, CHECK
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("--system", help="system ID from performance/systems.csv (default: from the run)")
    ap.add_argument("--out", type=Path, default=OUT, help="directory for the shared pages")
    ap.add_argument("--check", action="store_true",
                    help="regenerate in memory and compare with the committed pages; exit 1 on any difference")
    a = ap.parse_args()
    run = Run(a.run_dir.resolve())
    systems = load_systems()
    host = (run.env or {}).get("hostname") or run.campaign.get("environment_at_start", {}).get("hostname")
    system = a.system or run.campaign.get("system_id") or next(
        (sid for sid, r in systems.items() if r["Hostname"] == host), None)
    if system not in systems:
        ap.error(f"unknown system {system!r} (host {host!r}); add it to performance/systems.csv or pass --system")
    SYSTEM, SYSTEM_DESC = system, systems[system]["Description"]
    CHECK = a.check
    arch = {"x86_64": "x86-64", "aarch64": "AArch64"}.get(systems[system]["Arch"], systems[system]["Arch"])
    out = a.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    cands = sorted({c for (c, l) in run.records} | {e["candidate"] for e in run.build.values()})
    for cand in cands:
        candidate_page(run, cand, out, arch)
    summary(run, out, arch)
    survey_page(run, out)
    method_page(run, out, arch)
    if CHECK:
        for path in DIFFERENT:
            print(f"differs from regenerated output: {path}")
        print(f"report check: system {SYSTEM}: {len(cands) + 3} pages, {len(DIFFERENT)} differ")
        return 1 if DIFFERENT else 0
    print(f"report: system {SYSTEM}: {len(cands)} candidate reports (<id>/perf_{SYSTEM}.md), "
          f"{summary_page(out).name}, {method_page_path(out).name}, symmetric-survey.md in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
