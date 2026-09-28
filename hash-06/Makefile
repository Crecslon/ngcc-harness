# NGCC uniform build: hash-06 Cuishen (reference implementation)
NGCC_ID   := hash-06
NGCC_TYPE := hash
NGCC_ALG  := Cuishen
include ../api/link_rules.mk

REF := Cuishen/Implementations/Reference_Implementation
NGCC_KAT_DIR := Cuishen/Test_Vectors

# Per Reference_Implementation/generate_kat.sh: CryptHash_Cuishen-<bits>.c,
# drng.c (byte-identical to api/drng.c) and the KAT driver (dropped by the
# default glob). The instance header is CryptHash_Cuishen-<bits>.h rather than
# CryptHash_AlgorithmInstance.h, so the shim is pointed at it.
define CUISHEN
SHIMDEFS_$(1) := -DNGCC_INSTANCE_HEADER='"CryptHash_$(1).h"'
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(1)))
endef

$(eval $(call CUISHEN,Cuishen-512))
$(eval $(call CUISHEN,Cuishen-768))
$(eval $(call CUISHEN,Cuishen-1024))

include ../api/link_finish.mk
