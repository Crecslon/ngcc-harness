# NGCC uniform build: kex-06 MAMBA-NIKE (reference implementation)
NGCC_ID   := kex-06
NGCC_TYPE := kex
NGCC_ALG  := MAMBA-NIKE
include ../api/link_rules.mk

REF := Implementations/Reference_Implementation
NGCC_KAT_DIR := Test_Vectors

# Per each instance's Makefile: KEX_AlgorithmInstance.c crypto_stream_chacha20.c
# poly.c toom.c error_correction.c nike.c reduce.c fips202.c auxfunc.c drng.c
# (= the default glob minus KAT_KEX.c; the shipped *.o files and KAT_KEX binary
# are ignored), with -DKAT_BUILD. KAT_BUILD is required: it makes
# nike_randombytes() in KEX_AlgorithmInstance.c draw from drng_algorithm;
# without it randomness comes from /dev/urandom and every KAT mismatches.
# params.h is per directory. Reference_Implementation/AlgorithmInstance is the
# blank ICCS API template, not a parameter set. API_PKC/API_PKC/ holds a second
# copy of the submission tree; its Test_Vectors are identical to Test_Vectors/.
# One-pass protocol.
define MAMBA
DEFS_$(1) := -DKAT_BUILD
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(1)))
endef

$(eval $(call MAMBA,MAMBA-NIKE-128))
$(eval $(call MAMBA,MAMBA-NIKE-192))
$(eval $(call MAMBA,MAMBA-NIKE-256))
$(eval $(call MAMBA,MAMBA-NIKE-384))
$(eval $(call MAMBA,MAMBA-NIKE-512))

include ../api/link_finish.mk
