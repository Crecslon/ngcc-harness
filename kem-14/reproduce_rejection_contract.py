#!/usr/bin/env python3
"""Reproduce DTRU's explicit rejection and missing public-key binding."""

import ctypes as C
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PK_LEN = 640
SK_LEN = 864
CT_LEN = 512
SS_LEN = 32
Z_LEN = 32


def load_library():
    lib = C.CDLL(str(ROOT / "lib" / "libDTRU-Light.so"))
    lib.ngcc_seed.argtypes = [C.c_void_p, C.c_ulonglong]
    lib.kem_keygen.argtypes = [C.c_void_p, C.c_void_p,
                               C.c_void_p, C.c_void_p]
    lib.kem_enc.argtypes = [C.c_void_p, C.c_ulonglong, C.c_void_p,
                            C.c_void_p, C.c_void_p, C.c_void_p]
    lib.kem_dec.argtypes = [C.c_void_p, C.c_ulonglong, C.c_void_p,
                            C.c_ulonglong, C.c_void_p, C.c_void_p]
    return lib


def keygen(lib):
    pk = (C.c_ubyte * PK_LEN)()
    sk = (C.c_ubyte * SK_LEN)()
    pk_len = C.c_ulonglong()
    sk_len = C.c_ulonglong()
    assert lib.kem_keygen(pk, C.byref(pk_len), sk, C.byref(sk_len)) == 0
    assert (pk_len.value, sk_len.value) == (PK_LEN, SK_LEN)
    return pk, sk


def decapsulate(lib, sk, ct):
    ss = (C.c_ubyte * SS_LEN)()
    ss_len = C.c_ulonglong()
    rc = lib.kem_dec(sk, SK_LEN, ct, CT_LEN, ss, C.byref(ss_len))
    assert ss_len.value == SS_LEN
    return rc, bytes(ss)


def check_all_reference_sources():
    ref = (ROOT / "Implementations and Test_Vectors" / "Implementations" /
           "Reference_Implementation")
    sources = sorted(ref.glob("DTRU-*/KEM_AlgorithmInstance.c"))
    assert len(sources) == 7
    for source in sources:
        text = source.read_text(encoding="utf-8-sig")
        dec = text.split("int kem_dec(", 1)[1]
        compact = "".join(dec.split())
        assert "returnfail;" in compact
        assert "pseudohash(512,ct2," in compact
    return len(sources)


def main():
    source_count = check_all_reference_sources()
    lib = load_library()
    seed = (C.c_ubyte * 48)(*range(48))
    assert lib.ngcc_seed(seed, 48) == 0

    pk1, sk1 = keygen(lib)
    pk2, sk2 = keygen(lib)
    assert bytes(pk1) != bytes(pk2)

    ct = (C.c_ubyte * CT_LEN)()
    sent = (C.c_ubyte * SS_LEN)()
    ct_len = C.c_ulonglong()
    ss_len = C.c_ulonglong()
    assert lib.kem_enc(pk1, PK_LEN, sent, C.byref(ss_len), ct,
                       C.byref(ct_len)) == 0
    assert (ct_len.value, ss_len.value) == (CT_LEN, SS_LEN)
    honest_rc, honest_ss = decapsulate(lib, sk1, ct)
    assert honest_rc == 0 and honest_ss == bytes(sent)

    invalid = (C.c_ubyte * CT_LEN).from_buffer_copy(bytes(ct))
    invalid[0] ^= 1
    reject_rc, reject1 = decapsulate(lib, sk1, invalid)
    reject_rc_again, reject1_again = decapsulate(lib, sk1, invalid)
    assert reject_rc == reject_rc_again == 1
    assert reject1 == reject1_again and reject1 != honest_ss
    print("ATTACK kem-14-2 DTRU-Light CONFIRMED "
          f"invalid_return={reject_rc} honest_return={honest_rc} "
          f"reference_trees={source_count}")

    # The implementation hashes only c || z on rejection. Give a second,
    # distinct key the same z to isolate the omitted ID(pk) input. This is a
    # correlated-key binding witness, not an honest-key IND-CCA attack.
    correlated = (C.c_ubyte * SK_LEN).from_buffer_copy(bytes(sk2))
    correlated[SK_LEN - Z_LEN:SK_LEN] = sk1[SK_LEN - Z_LEN:SK_LEN]
    correlated_rc, reject2 = decapsulate(lib, correlated, invalid)
    control_rc, reject_control = decapsulate(lib, sk2, invalid)
    assert correlated_rc == control_rc == 1
    assert reject2 == reject1
    assert reject_control != reject1
    print("ATTACK kem-14-3 DTRU-Light CONFIRMED distinct_pk=yes "
          "same_z_rejection_key_alias=yes different_z_control=distinct")


if __name__ == "__main__":
    main()
