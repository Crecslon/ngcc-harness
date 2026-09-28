# NGCC uniform build: kem-25 NEV (reference implementation)
NGCC_ID   := kem-25
NGCC_TYPE := kem
NGCC_ALG  := NEV
include ../api/link_rules.mk

REF := Implementations/Reference_Implementation
NGCC_KAT_DIR := Test_Vectors

# Per each directory's Makefile (PQCgenKAT_*-iccs targets): poly.c ntt.c
# owpke.c verify.c sample.c pack.c cca.c cpa.c + symmetrics/{hashkdf,fips202,
# auxfunc}.c + kat_test/{rng,drng,KEM_AlgorithmInstance}.c with -DPARAMS=<N>
# -DUSE_ICCS (the ICCS SM3/pseudoXOF hash backend the submitted KATs use;
# -DUSE_SHA3 is the candidate's speed build). The twelve directories are
# identical apart from their Makefile; PARAMS alone selects the set and
# KEM_AlgorithmInstance.h derives ALGORITHM_INSTANCE (NEV_<n>_<q>[_C]_ICCS)
# from it. randombytes.c (/dev/urandom) is replaced by kat_test/rng.c, which
# draws from drng_algorithm. -march=native/-O3 of the candidate build dropped.
NEV_SRCS := poly.c ntt.c owpke.c verify.c sample.c pack.c cca.c cpa.c \
            symmetrics/hashkdf.c symmetrics/fips202.c symmetrics/auxfunc.c \
            kat_test/rng.c kat_test/drng.c kat_test/KEM_AlgorithmInstance.c

# label (= ALGORITHM_INSTANCE), dir, PARAMS
define NEV
SRCS_$(1) := $(NEV_SRCS)
INC_$(1)  := -Isrc/$(1)/symmetrics -Isrc/$(1)/kat_test
DEFS_$(1) := -DPARAMS=$(3) -DUSE_ICCS
SHIMDEFS_$(1) := -DNGCC_INSTANCE_HEADER='"kat_test/KEM_AlgorithmInstance.h"'
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(2)))
endef

$(eval $(call NEV,NEV_512_769_C_ICCS,NEV-C1-c,1))
$(eval $(call NEV,NEV_1024_769_C_ICCS,NEV-C2-c,2))
$(eval $(call NEV,NEV_2048_769_C_ICCS,NEV-C3-c,3))
$(eval $(call NEV,NEV_512_1409_ICCS,NEV-R1,4))
$(eval $(call NEV,NEV_1024_1409_ICCS,NEV-R2,5))
$(eval $(call NEV,NEV_2048_1409_ICCS,NEV-R3,6))
$(eval $(call NEV,NEV_512_3329_ICCS,NEV-D1,7))
$(eval $(call NEV,NEV_1024_3329_ICCS,NEV-D2,8))
$(eval $(call NEV,NEV_2048_3329_ICCS,NEV-D3,9))
$(eval $(call NEV,NEV_512_769_ICCS,NEV-C1,10))
$(eval $(call NEV,NEV_1024_769_ICCS,NEV-C2,11))
$(eval $(call NEV,NEV_2048_769_ICCS,NEV-C3,12))

include ../api/link_finish.mk
