# NGCC uniform build: hash-33 Thunder (reference implementation)
NGCC_ID   := hash-33
NGCC_TYPE := hash
NGCC_ALG  := Thunder
include ../api/link_rules.mk

REF := Thunder/Implementations and Test_vector/Thunder-X86/Implementations/Reference_Implementation
NGCC_KAT_DIR := Thunder/Implementations and Test_vector/Thunder-X86/Test_Vector

# Per each instance's run_kat.sh: CryptHash_AlgorithmInstance.c, drng.c
# (byte-identical to api/drng.c) and the KAT driver (dropped by the default
# glob). The x86 package is the one listed as reference; the Thunder-ARM tree
# and the Others/ self-assessment variants are not used. The XOF instances
# are fixed-length builds (DIGEST_BIT_LENGTH 1280/1152/1024).
$(eval $(call ngcc_instance,Thunder-512,$(REF)/Thunder-512))
$(eval $(call ngcc_instance,Thunder-768,$(REF)/Thunder-768))
$(eval $(call ngcc_instance,Thunder-1024,$(REF)/Thunder-1024))
$(eval $(call ngcc_instance,Thunder-XOF-256,$(REF)/Thunder-XOF-256))
$(eval $(call ngcc_instance,Thunder-XOF-384,$(REF)/Thunder-XOF-384))
$(eval $(call ngcc_instance,Thunder-XOF-512,$(REF)/Thunder-XOF-512))

include ../api/link_finish.mk
