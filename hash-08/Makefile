# NGCC uniform build: hash-08 Duet (reference implementation)
NGCC_ID   := hash-08
NGCC_TYPE := hash
NGCC_ALG  := Duet
include ../api/link_rules.mk

REF := Duet/Implementations/Reference_Implementation
NGCC_KAT_DIR := Duet/Test_Vectors

# Per Reference_Implementation/generate_kat.sh: CryptHash_Duet-<bits>.c,
# drng.c (byte-identical to api/drng.c) and the KAT driver (dropped by the
# default glob). The instance header is CryptHash_Duet-<bits>.h rather than
# CryptHash_AlgorithmInstance.h, so the shim is pointed at it.
define DUET
SHIMDEFS_$(1) := -DNGCC_INSTANCE_HEADER='"CryptHash_$(1).h"'
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(1)))
endef

$(eval $(call DUET,Duet-512))
$(eval $(call DUET,Duet-768))
$(eval $(call DUET,Duet-1024))

include ../api/link_finish.mk
