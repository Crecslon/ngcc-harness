# NGCC uniform build: hash-03 C Hash (reference implementation)
NGCC_ID   := hash-03
NGCC_TYPE := hash
NGCC_ALG  := C Hash
include ../api/link_rules.mk

REF := C Hash/Implementations/Reference_Implementation
NGCC_KAT_DIR := C Hash/Test_Vectors

# Each instance dir holds CryptHash_AlgorithmInstance.c, the unmodified
# official drng.c (byte-identical to api/drng.c) and the KAT driver (dropped by
# the default glob). The "Others/" tree (an independent AI-assisted C-HASH
# implementation with its own KATs) is not used.
$(eval $(call ngcc_instance,CHash_512,$(REF)/CHash_512))
$(eval $(call ngcc_instance,CHash_1024,$(REF)/CHash_1024))

include ../api/link_finish.mk
