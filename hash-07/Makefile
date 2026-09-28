# NGCC uniform build: hash-07 Dragon (reference implementation)
NGCC_ID   := hash-07
NGCC_TYPE := hash
NGCC_ALG  := Dragon
include ../api/link_rules.mk

REF := Dragon/Implementations and Test_vector/Dragon-x86/Implementations/Reference_Implementation
NGCC_KAT_DIR := Dragon/Implementations and Test_vector/Dragon-x86/Test_Vector

# Per each instance's run_kat.sh: CryptHash_AlgorithmInstance.c, drng.c
# (byte-identical to api/drng.c) and the KAT driver (dropped by the default
# glob). The x86 package is the one listed as reference; the Dragon-ARM tree
# and the Others/ self-assessment variants are not used. The XOF instances
# are fixed-length builds (DIGEST_BIT_LENGTH 1280/1152/1024).
$(eval $(call ngcc_instance,Dragon-512,$(REF)/Dragon-512))
$(eval $(call ngcc_instance,Dragon-768,$(REF)/Dragon-768))
$(eval $(call ngcc_instance,Dragon-1024,$(REF)/Dragon-1024))
$(eval $(call ngcc_instance,Dragon-XOF-256,$(REF)/Dragon-XOF-256))
$(eval $(call ngcc_instance,Dragon-XOF-384,$(REF)/Dragon-XOF-384))
$(eval $(call ngcc_instance,Dragon-XOF-512,$(REF)/Dragon-XOF-512))

include ../api/link_finish.mk
