# NGCC uniform build: hash-29 XRH-2 (reference implementation)
NGCC_ID   := hash-29
NGCC_TYPE := hash
NGCC_ALG  := XRH-2
include ../api/link_rules.mk

REF := XRH-2/Implementations/Reference_Implementation
NGCC_KAT_DIR := XRH-2/Test_Vectors

# Each instance dir holds CryptHash_AlgorithmInstance.c, drng.c
# (byte-identical to api/drng.c) and the KAT driver (dropped by the default
# glob).
$(eval $(call ngcc_instance,XRH-2-512,$(REF)/XRH-2-512))
$(eval $(call ngcc_instance,XRH-2-768,$(REF)/XRH-2-768))
$(eval $(call ngcc_instance,XRH-2-1024,$(REF)/XRH-2-1024))

include ../api/link_finish.mk
