#!/usr/bin/env python3
"""Check the Aigis-Sig+ sign-bit collapse and challenge probabilities."""

from math import comb, log2
from pathlib import Path


ROOT = Path(__file__).resolve().parent / "Implementations" / "Implementations"
for level, tau in (("I", 24), ("II", 44)):
    copies = [
        ROOT / "Reference_Implementation" / f"Aigis-Sig+-{level}" / "polyvec.c",
        ROOT / "Optimized_Implementation" / "avx2" / f"Aigis-Sig+-{level}" / "sample.c",
        ROOT / "Additional_Implementation" / "neon" / f"Aigis-Sig+-{level}" / "sample.c",
        ROOT / "Additional_Implementation" / "aarch64" / f"Aigis-Sig+-{level}" / "polyvec.c",
    ]
    for path in copies:
        source = path.read_text(errors="replace")
        assignment = "c->coeffs[b] = 1 - 2 * (signs & 1);"
        assert assignment in source, path
        assert "signs = 0;" in source[source.index(assignment) :], path

    support_bits = log2(comb(512, tau) * (tau + 1))
    most_likely_work = log2(comb(512, tau)) + 1
    specified_bits = log2(comb(512, tau)) + tau
    print(f"Aigis-Sig+-{level}: {specified_bits:.6f} specified bits; "
          f"{support_bits:.6f} bits of output support; "
          f"most-likely challenge work 2^{most_likely_work:.6f}; "
          f"Grover cost 2^{most_likely_work / 2:.6f}")
    if level == "I":
        assert 137.16 < most_likely_work < 137.18
        assert 68.58 < most_likely_work / 2 < 68.60
    else:
        assert 213.45 < most_likely_work < 213.47
        assert 217.94 < support_bits < 217.97

print("CONFIRMED sign-01-5: sets I and II collapse their challenge signs")
