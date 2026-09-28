# NGCC uniform build: sign-22 Rhyme (reference implementation)
NGCC_ID   := sign-22
NGCC_TYPE := sig
NGCC_ALG  := Rhyme
include ../api/link_rules.mk

REF := Implementations and Test_Vectors/Implementations/Reference_Implementation
TV  := Implementations and Test_Vectors/Test_Vectors

# Source list and defines from each instance Makefile (CORE + KAT_DEPS of its
# KAT_SIG target, minus the KAT_SIG.c driver); the two families differ only in
# the SM3 XOF files (sm3.c sm3_xof.c). -DRHYME_NO_AES excludes the AES-NI
# src/aes256ctr.c, as in the submitted build.
# Randomness: each instance has two randombytes.c. The top-level randombytes.c
# draws from drng_algorithm and is the one linked; src/randombytes.c reads
# /dev/urandom and is NOT linked. drng.c/auxfunc.c are identical to api/.
# ALGORITHM_INSTANCE defaults to "Rhyme" unless set with -D, as the submitted
# Makefile does. KAT files live in per-family subdirectories of Test_Vectors.
RHY_CORE := src/poly.c src/ntt.c src/ntt_tables.c src/sampler.c src/encoding.c \
            src/packing.c src/sign.c src/zpntt.c src/symmetric-shake.c src/fips202.c \
            rhyme_xof.c src/keygen/kg_main.c src/keygen/kg_solver.c src/keygen/kg_zint.c \
            src/keygen/kg_ntt.c src/keygen/kg_primes.c \
            randombytes.c auxfunc.c drng.c SIG_AlgorithmInstance.c
RHY_SRCS_SHAKE := $(RHY_CORE)
# the SM3 tree has no src/fips202.c (its symmetric-shake.c uses rhyme_xof/SM3)
RHY_SRCS_SM3   := $(filter-out src/fips202.c,$(RHY_CORE)) sm3.c sm3_xof.c

# family (SHAKE|SM3), level
define RHY
SRCS_Rhyme-$(1)-$(2) := $(RHY_SRCS_$(1))
INC_Rhyme-$(1)-$(2)  := -Isrc/Rhyme-$(1)-$(2)/include -Isrc/Rhyme-$(1)-$(2)/src/keygen
DEFS_Rhyme-$(1)-$(2) := -DRHYME_NO_AES -DRHYME_MODE=$(2) -DOUTPUT_BLANK_TEST_VECTORS=0 \
                        -DALGORITHM_INSTANCE='"Rhyme-$(1)-$(2)"'
CFLAGS_Rhyme-$(1)-$(2) := -std=c99
KATDIR_Rhyme-$(1)-$(2) := $(TV)/Rhyme-$(1)
$$(eval $$(call ngcc_instance,Rhyme-$(1)-$(2),$(REF)/Rhyme-$(1)/Rhyme-$(1)-$(2)))
endef

$(foreach f,SHAKE SM3,$(foreach l,128 256 384 512,$(eval $(call RHY,$(f),$(l)))))

include ../api/link_finish.mk

.PHONY: audit-parity audit-parity-runtime
audit-parity:
	python3 reproduce_sm3_parity_bias.py

audit-parity-runtime:
	sh reproduce_sm3_parity_runtime.sh
