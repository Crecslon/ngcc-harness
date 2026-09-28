# NGCC uniform build: hash-28 XRH-1 (reference implementation)
NGCC_ID   := hash-28
NGCC_TYPE := hash
NGCC_ALG  := XRH-1
include ../api/link_rules.mk

REF := XRH-1/Implementations/Reference_Implementation
NGCC_KAT_DIR := XRH-1/Test_Vectors

# Each instance dir holds CryptHash_AlgorithmInstance.c, drng.c
# (byte-identical to api/drng.c) and the KAT driver (dropped by the default
# glob).
$(eval $(call ngcc_instance,XRH-1-512,$(REF)/XRH-1-512))
$(eval $(call ngcc_instance,XRH-1-768,$(REF)/XRH-1-768))
$(eval $(call ngcc_instance,XRH-1-1024,$(REF)/XRH-1-1024))

include ../api/link_finish.mk
