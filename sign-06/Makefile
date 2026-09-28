# NGCC uniform build: sign-06 COMPASS-SIG (reference implementation)
NGCC_ID   := sign-06
NGCC_TYPE := sig
NGCC_ALG  := COMPASS-SIG
include ../api/link_rules.mk

REF := Implementations/Reference_Implementation
NGCC_KAT_DIR := Test_Vectors

# Source list from each instance Makefile (SOURCES, the "test/test_kat<N>"
# target) plus SIG_AlgorithmInstance.c. The four COMPASS-SIG-<N> directories
# are byte-identical apart from their Makefile; the level is selected with
# -DCOMPASS_SIG_MODE=<N> (config.h defaults to 256), which the shim also sees so
# ALGORITHM_INSTANCE resolves to "COMPASS-SIG-<N>". randombytes.c (/dev/urandom,
# test programs only) is not linked: keygen draws its seed from drng_algorithm
# (sign.c) and signing is deterministic unless COMPASS_SIG_RANDOMIZED_SIGNING,
# which the KAT build does not set. SHAKE is replaced by the ICCS pseudoXOF in
# symmetric-shake.c (no fips202.c). The shipped drng.c/auxfunc.c are used.
CMP_SRCS := sign.c packing.c polyvec.c poly.c ntt.c reduce.c rounding.c \
            symmetric-shake.c drng.c auxfunc.c SIG_AlgorithmInstance.c

define CMP
SRCS_COMPASS-SIG-$(1) := $(CMP_SRCS)
DEFS_COMPASS-SIG-$(1) := -DCOMPASS_SIG_MODE=$(1)
$$(eval $$(call ngcc_instance,COMPASS-SIG-$(1),$(REF)/COMPASS-SIG-$(1)))
endef

$(eval $(call CMP,128))
$(eval $(call CMP,256))
$(eval $(call CMP,384))
$(eval $(call CMP,512))

include ../api/link_finish.mk

.PHONY: reproduce reproduce-verify-leak
reproduce: reproduce-verify-leak

reproduce-verify-leak: libs
	python3 reproduce_verify_leak.py $(LIBS)
