#!/usr/bin/env python3
"""Certify the public-support precondition and reduced-system dimensions."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent / "Implementations" / "Reference_Implementation"


def value(text: str, name: str) -> int:
    match = re.search(rf"^#define {name} (\d+)$", text, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name}")
    return int(match.group(1))


expected = {
    "128": (1764, 210, 10),
    "256": (3965, 325, 12),
    "384": (6391, 498, 14),
    "512": (9360, 728, 15),
}

for level, want in expected.items():
    directory = ROOT / f"Loong-Block-ms-{level}"
    source = (directory / "src" / "loong_pke.c").read_text()
    params = (directory / "src" / "loong_parameters.h").read_text()
    assert "(void)reader;" in source
    assert "rbc_elt_set_coefficient(&candidate, pool_size, 1U)" in source
    assert "matrix_mul(s, h, LOONG_N, LOONG_N, x, LOONG_N1);" in source
    assert "vec_add_inplace(s, y, LOONG_PKE_XS_SIZE);" in source

    n = value(params, "LOONG_N")
    m = value(params, "LOONG_M")
    columns = value(params, "LOONG_N1")
    dx = value(params, "LOONG_AXY_00")
    dy = value(params, "LOONG_AXY_11")
    got = (n * (m - dy), n * dx, columns)
    assert got == want
    print(f"BAG-Loong-{level}: {got[0]} equations, {got[1]} unknowns, {got[2]} columns")

print("CONFIRMED kem-03-3 precondition: X and Y supports are fixed public monomial spans")
