# NGCC uniform build: kem-26 NSS-HQC (reference implementation)
NGCC_ID   := kem-26
NGCC_TYPE := kem
NGCC_ALG  := NSS-HQC
include ../api/link_rules.mk

REF := Implementations and Test_Vectors/Implementations/Reference_Implementation
NGCC_KAT_DIR := Implementations and Test_Vectors/Test_Vectors

# Per each instance's Makefile (CORE_OBJS): KEM_AlgorithmInstance.c
# nss_hqc_core.c code_layer.c auxfunc.c drng.c, no extra defines (the
# parameter set is fixed by the per-directory params.h). The default source
# glob picks exactly these (KAT_KEM.c, selftest.c and hardening_test.c are
# excluded). nss_hqc_core.c draws all randomness from drng_algorithm.
# Optimized_Implementation/HQC-* is byte-identical to the reference.
$(eval $(call ngcc_instance,HQC-128,$(REF)/HQC-128))
$(eval $(call ngcc_instance,HQC-256,$(REF)/HQC-256))
$(eval $(call ngcc_instance,HQC-384,$(REF)/HQC-384))
$(eval $(call ngcc_instance,HQC-512,$(REF)/HQC-512))

include ../api/link_finish.mk
