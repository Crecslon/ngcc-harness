# NGCC uniform build: kem-30 PolarLAC (reference implementation)
NGCC_ID   := kem-30
NGCC_TYPE := kem
NGCC_ALG  := PolarLAC
include ../api/link_rules.mk

REF := Implementations/Reference_Implementation/x86
NGCC_KAT_DIR := Test_Vectors/Reference_Implementation/x86

# Per each instance's Makefile (COMMON_SOURCES): auxfunc.c drng.c fips202.c
# symmetric.c sample.c poly.c pke.c polar.c ntt.c fft.c KEM_AlgorithmInstance.c
# (the default glob; test.c, cycles_test.c and KAT_KEM.c are excluded), with
# the candidate's default backend switches -DBIT_USE_SHAKE=0
# -DRL_KEM_USE_CONJ_NTT_REJECTION=0. BIT_USE_SHAKE=0 selects SM3 (auxfunc.c)
# and drng_algorithm as randomness source, which is what the submitted KATs
# were generated with; BIT_USE_SHAKE=1 would draw from the OS instead.
define POLARLAC
DEFS_$(1) := -DBIT_USE_SHAKE=0 -DRL_KEM_USE_CONJ_NTT_REJECTION=0
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(1)))
endef

$(eval $(call POLARLAC,POLARLAC-128))
$(eval $(call POLARLAC,POLARLAC-256))
$(eval $(call POLARLAC,POLARLAC-512))
$(eval $(call POLARLAC,POLARLAC-512-Star))
$(eval $(call POLARLAC,POLARLAC-Light))

include ../api/link_finish.mk
