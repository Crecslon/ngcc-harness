#!/usr/bin/env python3
"""Reproduce DKEM-512's silent honest-session mismatch."""

import argparse
import ctypes
import hashlib
from pathlib import Path


U8 = ctypes.c_ubyte
ULL = ctypes.c_ulonglong


def array(data):
    return (U8 * len(data)).from_buffer_copy(data)


def level_from_path(path):
    for level in (128, 256, 512):
        if f"DKEM-{level}" in Path(path).name:
            return level
    raise ValueError(f"cannot identify DKEM parameter set from {path}")


def check(path, trials):
    level = level_from_path(path)
    lib = ctypes.CDLL(path)
    lib.ngcc_seed.argtypes = [ctypes.POINTER(U8), ULL]
    lib.ngcc_seed.restype = ctypes.c_int
    for field in ("pk", "sk", "ct", "ss"):
        getattr(lib, f"kem_get_{field}_len_bytes").restype = ULL
    lib.kem_keygen.argtypes = [
        ctypes.POINTER(U8), ctypes.POINTER(ULL),
        ctypes.POINTER(U8), ctypes.POINTER(ULL),
    ]
    lib.kem_keygen.restype = ctypes.c_int
    lib.kem_enc.argtypes = [
        ctypes.POINTER(U8), ULL, ctypes.POINTER(U8), ctypes.POINTER(ULL),
        ctypes.POINTER(U8), ctypes.POINTER(ULL),
    ]
    lib.kem_enc.restype = ctypes.c_int
    lib.kem_dec.argtypes = [
        ctypes.POINTER(U8), ULL, ctypes.POINTER(U8), ULL,
        ctypes.POINTER(U8), ctypes.POINTER(ULL),
    ]
    lib.kem_dec.restype = ctypes.c_int

    sizes = {
        field: int(getattr(lib, f"kem_get_{field}_len_bytes")())
        for field in ("pk", "sk", "ct", "ss")
    }
    seed = array(hashlib.sha384(b"DKEM int16 NTT overflow witness").digest())
    assert lib.ngcc_seed(seed, len(seed)) == 0
    pk, sk = (U8 * sizes["pk"])(), (U8 * sizes["sk"])()
    pk_len, sk_len = ULL(sizes["pk"]), ULL(sizes["sk"])
    assert lib.kem_keygen(pk, ctypes.byref(pk_len), sk, ctypes.byref(sk_len)) == 0

    mismatches = []
    for trial in range(1, trials + 1):
        ct = (U8 * sizes["ct"])()
        sent, received = (U8 * sizes["ss"])(), (U8 * sizes["ss"])()
        ct_len, sent_len, received_len = (
            ULL(sizes["ct"]), ULL(sizes["ss"]), ULL(sizes["ss"])
        )
        assert lib.kem_enc(
            pk, pk_len.value, sent, ctypes.byref(sent_len),
            ct, ctypes.byref(ct_len),
        ) == 0
        rc = lib.kem_dec(
            sk, sk_len.value, ct, ct_len.value,
            received, ctypes.byref(received_len),
        )
        if bytes(sent) != bytes(received):
            mismatches.append((trial, rc))

    if level == 512:
        assert mismatches
        assert all(rc == 0 for _, rc in mismatches)
        print(
            f"DKEM-512: CONFIRMED {len(mismatches)}/{trials} honest session(s) "
            f"mismatched; first at trial {mismatches[0][0]}, kem_dec returned 0"
        )
    else:
        assert not mismatches
        print(f"DKEM-{level}: CONTROL 0/{trials} honest sessions mismatched")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("libraries", nargs="+")
    parser.add_argument("--control-trials", type=int, default=3000)
    parser.add_argument("--affected-trials", type=int, default=2000)
    args = parser.parse_args()
    for path in args.libraries:
        level = level_from_path(path)
        trials = args.affected_trials if level == 512 else args.control_trials
        check(path, trials)


if __name__ == "__main__":
    main()
