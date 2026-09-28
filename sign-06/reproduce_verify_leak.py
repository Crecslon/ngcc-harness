#!/usr/bin/env python3
"""Measure COMPASS-SIG heap growth on rejected, fully parsed signatures."""

import argparse
import ctypes
import hashlib
import os
from pathlib import Path
import subprocess
import sys


U8 = ctypes.c_ubyte
ULL = ctypes.c_ulonglong
PAGE_SIZE = os.sysconf("SC_PAGE_SIZE")


def array(data):
    return (U8 * len(data)).from_buffer_copy(data)


def rss_bytes():
    with open("/proc/self/statm", encoding="ascii") as stream:
        return int(stream.read().split()[1]) * PAGE_SIZE


def worker(path, calls):
    lib = ctypes.CDLL(path)
    lib.ngcc_seed.argtypes = [ctypes.POINTER(U8), ULL]
    lib.ngcc_seed.restype = ctypes.c_int
    for field in ("pk", "sk", "sn"):
        getattr(lib, f"sig_get_{field}_len_bytes").restype = ULL
    lib.sig_keygen.argtypes = [
        ctypes.POINTER(U8), ctypes.POINTER(ULL),
        ctypes.POINTER(U8), ctypes.POINTER(ULL),
    ]
    lib.sig_keygen.restype = ctypes.c_int
    lib.sig_sign.argtypes = [
        ctypes.POINTER(U8), ULL, ctypes.POINTER(U8), ULL,
        ctypes.POINTER(U8), ctypes.POINTER(ULL),
    ]
    lib.sig_sign.restype = ctypes.c_int
    lib.sig_verify.argtypes = [
        ctypes.POINTER(U8), ULL, ctypes.POINTER(U8), ULL,
        ctypes.POINTER(U8), ULL,
    ]
    lib.sig_verify.restype = ctypes.c_int

    sizes = {
        field: int(getattr(lib, f"sig_get_{field}_len_bytes")())
        for field in ("pk", "sk", "sn")
    }
    seed = array(hashlib.sha512(b"COMPASS-SIG verifier leak witness").digest())
    assert lib.ngcc_seed(seed, len(seed)) == 0
    pk, sk = (U8 * sizes["pk"])(), (U8 * sizes["sk"])()
    pk_len, sk_len = ULL(sizes["pk"]), ULL(sizes["sk"])
    assert lib.sig_keygen(pk, ctypes.byref(pk_len), sk, ctypes.byref(sk_len)) == 0

    message = array(b"public message")
    signature = (U8 * sizes["sn"])()
    signature_len = ULL(sizes["sn"])
    assert lib.sig_sign(
        sk, sk_len.value, message, len(message), signature,
        ctypes.byref(signature_len),
    ) == 0
    assert lib.sig_verify(
        pk, pk_len.value, signature, signature_len.value, message, len(message)
    ) == 0

    # Control: an all-zero encoding is rejected before reaching the allocating
    # verification path and should not grow resident memory with each call.
    early = (U8 * sizes["sn"])()
    assert lib.sig_verify(
        pk, pk_len.value, early, sizes["sn"], message, len(message)
    ) == -1
    before = rss_bytes()
    for _ in range(calls):
        assert lib.sig_verify(
            pk, pk_len.value, early, sizes["sn"], message, len(message)
        ) == -1
    control_growth = rss_bytes() - before

    # Flipping the public challenge keeps the signature structurally valid,
    # drives verification through its matrix/XOF work, and fails only at the
    # final challenge comparison.
    signature[0] ^= 1
    assert lib.sig_verify(
        pk, pk_len.value, signature, signature_len.value, message, len(message)
    ) == -1
    before = rss_bytes()
    for _ in range(calls):
        assert lib.sig_verify(
            pk, pk_len.value, signature, signature_len.value, message, len(message)
        ) == -1
    attack_growth = rss_bytes() - before

    # Allow a small allocator/runtime startup allowance in the control.  The
    # affected path leaks tens of KiB per call in every submitted parameter set.
    assert control_growth <= 2 * 1024 * 1024
    assert attack_growth >= calls * 8 * 1024
    name = Path(path).stem.removeprefix("lib")
    print(
        f"{name}: CONTROL early rejects grew {control_growth // 1024} KiB; "
        f"CONFIRMED {calls} deep rejects grew {attack_growth // 1024} KiB "
        f"({attack_growth / calls / 1024:.1f} KiB/call)"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("libraries", nargs="+")
    parser.add_argument("--calls", type=int, default=500)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.worker:
        assert len(args.libraries) == 1
        worker(args.libraries[0], args.calls)
        return

    for path in args.libraries:
        subprocess.run(
            [sys.executable, __file__, "--worker", "--calls", str(args.calls), path],
            check=True,
        )


if __name__ == "__main__":
    main()
