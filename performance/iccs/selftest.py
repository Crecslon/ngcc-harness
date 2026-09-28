#!/usr/bin/env python3
"""Check one ICCS baseline library (performance/iccs/Makefile) against an
independent implementation built on the SM3 of Python's hashlib (OpenSSL).

    python3 performance/iccs/selftest.py LIB LABEL

sm3hash-256 is also checked against the two GB/T 32905-2016 examples. The
pseudohash and pseudoXOF models follow api/auxfunc.c for byte-aligned inputs:
pseudoXOF is the counter-mode KDF SM3(m || ct) with a 32-bit big-endian counter
from 1; pseudohash is the HMAC-SM3 cascade with the fixed ICCS key. Prints a log
ending in "RESULT iccs LABEL PASS" (or FAIL); exit status 0 only on PASS.
"""

from __future__ import annotations

import ctypes
import hashlib
import hmac
import sys

KEY = bytes.fromhex("5307f6d5eb6a3ced3d24c53cc9c82cce2f8936397023f0695c26c80c1ab182a7"
                    "1db02ba92f544018115a96e719662ca32b7c7efc0a6d2482150766ba6f655b8e")
GBT = [(b"abc", "66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0"),
       (b"abcd" * 16, "debe9ff92275b8a138604889c18e5a4d6fdb70e5387e5765293dcba39c0c5732")]
LENGTHS = (0, 1, 3, 31, 32, 55, 56, 63, 64, 65, 119, 128, 512, 1024, 4096, 8192, 16384, 65536)


def sm3(data: bytes) -> bytes:
    return hashlib.new("sm3", data).digest()


def mac(data: bytes) -> bytes:
    return hmac.new(KEY, data, "sm3").digest()


def pseudoxof(bits: int, m: bytes) -> bytes:
    out = b"".join(sm3(m + ct.to_bytes(4, "big")) for ct in range(1, (bits + 255) // 256 + 1))
    return out[:bits // 8]


def pseudohash(bits: int, m: bytes) -> bytes:
    dom = bytes([bits // 256, 0])
    k1, h1 = mac(dom + m), sm3(m + dom)
    h2 = sm3(k1 + h1)
    if bits == 512:
        return h1 + h2
    k2 = mac(h1)
    h3 = sm3(h2 + k2)
    if bits == 768:
        return h1 + h2 + h3
    k3, k4 = mac(h2), mac(h3)
    return h1 + h2 + h3 + sm3(k3 + h3 + k4)


def expected(label: str, m: bytes) -> bytes:
    fn, bits = label.rsplit("-", 1)
    bits = int(bits)
    if fn == "sm3hash":
        return sm3(m)
    if fn == "pseudohash":
        return pseudohash(bits, m)
    if fn == "pseudoXOF":
        return pseudoxof(bits, m)
    raise ValueError(f"unknown ICCS helper {fn!r}")


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    lib_path, label = sys.argv[1:]
    bits = int(label.rsplit("-", 1)[1])
    crypt_hash = ctypes.CDLL(lib_path).CryptHash
    crypt_hash.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_ulonglong, ctypes.c_char_p]
    crypt_hash.restype = ctypes.c_int
    cases = [(f"len={n}", bytes((7 * i + 1) & 0xFF for i in range(n))) for n in LENGTHS]
    if label.startswith("sm3hash"):
        cases += [(f"GB/T 32905 {m[:8].decode()}{'...' if len(m) > 8 else ''}", m) for m, _ in GBT]
    print(f"instance = {label}\nlibrary = {lib_path}\nmodel = api/auxfunc.c semantics on hashlib SM3 "
          f"({hashlib.new('sm3').name})")
    failures = 0
    for name, m in cases:
        out = ctypes.create_string_buffer(bits // 8)
        rc = crypt_hash(bits, m, 8 * len(m), out)
        want = expected(label, m)
        gbt = next((bytes.fromhex(d) for g, d in GBT if g == m), None) if label.startswith("sm3hash") else None
        ok = rc == 0 and out.raw == want and (gbt is None or want == gbt)
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {name} rc={rc} {out.raw[:16].hex()}...")
    print(f"RESULT iccs {label} {'PASS' if not failures else 'FAIL'} ({len(cases) - failures}/{len(cases)})")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
