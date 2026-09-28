# NGCC uniform build: hash-16 LLH (reference implementation)
NGCC_ID   := hash-16
NGCC_TYPE := hash
NGCC_ALG  := LLH
include ../api/link_rules.mk

REF := LLH/Implementations and Test_Vectors/LLH_C/API_CryptHash/Implementations/Reference_Implementation
NGCC_KAT_DIR := LLH/Implementations and Test_Vectors/LLH_C/API_CryptHash/Test_Vectors

# Per the candidate Makefile: KAT_SRCS = CryptHash_AlgorithmInstance.c
# KAT_CryptHash.c drng.c. llh_core.c is #included by
# CryptHash_AlgorithmInstance.c and must not be compiled on its own, hence the
# explicit list. drng.c is byte-identical to api/drng.c.
define LLH
SRCS_$(1) := CryptHash_AlgorithmInstance.c drng.c
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(1)))
endef

$(eval $(call LLH,LLH-256))
$(eval $(call LLH,LLH-512))
$(eval $(call LLH,LLH-768))
$(eval $(call LLH,LLH-1024))

include ../api/link_finish.mk
