#!/usr/bin/env python3
"""Certify the sampler mismatch and parity biases in sign-22-3."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent / "Implementations and Test_Vectors" / "Implementations"
DEN = 1 << 63


def cdt_bias(header: str, mode: int, name: str) -> float:
    start = re.search(rf"#(?:if|elif) RHYME_MODE == {mode}\b", header)
    assert start, f"missing RHYME_MODE {mode}"
    tail = header[start.end() :]
    end = re.search(r"\n#(?:elif RHYME_MODE|else|endif)\b", tail)
    block = tail[: end.start()] if end else tail
    match = re.search(
        rf"static const uint64_t {name}\[\d+\] = \{{(.*?)\}};", block, re.S
    )
    assert match, f"missing {name} for mode {mode}"
    cdf = [int(x) for x in re.findall(r"(\d+)ULL", match.group(1))]
    counts = []
    previous = 0
    for value in cdf:
        counts.append(value - previous)
        previous = value
    counts.append(DEN - previous)  # the sampler's one-in-2^63 terminal value
    return sum((1 if magnitude % 2 == 0 else -1) * count
               for magnitude, count in enumerate(counts)) / DEN


def main() -> None:
    representative = ROOT / "Reference_Implementation" / "Rhyme-SM3" / "Rhyme-SM3-128"
    sm3_header = (representative / "include" / "params_tables.h").read_text()
    shake_header = (
        ROOT / "Reference_Implementation" / "Rhyme-SHAKE" / "Rhyme-SHAKE-128"
        / "include" / "params_tables.h"
    ).read_text()

    for tree in ("Reference_Implementation", "Optimized_Implementation"):
        for level in (128, 256, 384, 512):
            sm3 = (ROOT / tree / "Rhyme-SM3" / f"Rhyme-SM3-{level}" / "src" / "sign.c").read_text()
            shake = (ROOT / tree / "Rhyme-SHAKE" / f"Rhyme-SHAKE-{level}" / "src" / "sign.c").read_text()
            assert "SampleGauss(&e[i]" in sm3 and "SampleGaussE(&e[i]" not in sm3
            assert "SampleGaussE(&e[i]" in shake

    expected = {
        128: 0.0006332200183354205,
        256: 0.0004882833418597476,
        384: 0.0004194067553786733,
        512: 0.0003765158837782945,
    }
    for level, want in expected.items():
        bias = cdt_bias(sm3_header, level, "rhyme_cdt_g")
        assert abs(bias - want) < 1e-15
        control = cdt_bias(shake_header, level, "rhyme_cdt_e")
        print(f"Rhyme-SM3-{level}: E[(-1)^e]={bias:.12g}; "
              f"SHAKE doubled-width control={control:.3g}")

    print("RHYME_SM3_PARITY_BIAS_CONFIRMED")


if __name__ == "__main__":
    main()
