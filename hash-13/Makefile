# NGCC uniform build: hash-13 JuziHash (reference implementation)
NGCC_ID   := hash-13
NGCC_TYPE := hash
NGCC_ALG  := JuziHash
include ../api/link_rules.mk

REF := Juzi/Implementations/Implementation/Reference_Implementation
NGCC_KAT_DIR := Juzi/Test_Vectors

# Per the candidate Makefile: KAT_CryptHash.c drng.c CryptHash_AlgorithmInstance.c
# (default glob minus the KAT driver). drng.c is byte-identical to api/drng.c.
$(eval $(call ngcc_instance,JuziHash-512,$(REF)/JuziHash-512))
$(eval $(call ngcc_instance,JuziHash-1024,$(REF)/JuziHash-1024))

include ../api/link_finish.mk
