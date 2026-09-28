# NGCC uniform build: kem-41 ZEN (reference implementation)
NGCC_ID   := kem-41
NGCC_TYPE := kem
NGCC_ALG  := ZEN
include ../api/link_rules.mk

REF := Implementations/Reference_Implementation
NGCC_KAT_DIR := Test_Vectors

# Per each instance's Makefile (SOURCES): auxfunc.c drng.c sample.c ntt.c
# poly.c symmetric.c pke.c KEM_AlgorithmInstance.c, no defines (params.h is
# per directory). Listed explicitly because the default glob would also pick
# up SPEED_KEM.c (upper case, not matched by the exclusion pattern).
# All randomness comes from drng_algorithm (pke.c, KEM_AlgorithmInstance.c).
ZEN_SRCS := auxfunc.c drng.c sample.c ntt.c poly.c symmetric.c pke.c KEM_AlgorithmInstance.c

define ZEN
SRCS_$(1) := $(ZEN_SRCS)
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(1)))
endef

$(eval $(call ZEN,ZEN_128))
$(eval $(call ZEN,ZEN_256))
$(eval $(call ZEN,ZEN_512))

include ../api/link_finish.mk
