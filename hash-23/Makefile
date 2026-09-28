# NGCC uniform build: hash-23 QILIN (reference implementation)
NGCC_ID   := hash-23
NGCC_TYPE := hash
NGCC_ALG  := QILIN
include ../api/link_rules.mk

REF := QILIN/Implementations/Reference_Implementation
NGCC_KAT_DIR := QILIN/Test_Vectors

# Per the candidate Makefile: CryptHash_AlgorithmInstance.c drng.c
# KAT_CryptHash.c (default glob minus the KAT driver). drng.c is
# byte-identical to api/drng.c.
# CryptHash_AlgorithmInstance.h does `typedef unsigned long long uint64_t;`,
# which conflicts with <stdint.h> (already included by the shim through
# link_common.h). The candidate sources compile because they include that
# header first; the shim therefore skips it (NGCC_INSTANCE_HEADER_NONE) and
# gets ALGORITHM_INSTANCE / DIGEST_BIT_LENGTH copied from the header.
# label, digest bits
define QILIN
SHIMDEFS_$(1) := -DNGCC_INSTANCE_HEADER_NONE -DNGCC_INSTANCE='"$(1)"' -DNGCC_DIGEST_BITS=$(2)
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(1)))
endef

$(eval $(call QILIN,QILIN-512,512))
$(eval $(call QILIN,QILIN-768,768))
$(eval $(call QILIN,QILIN-1024,1024))

include ../api/link_finish.mk
