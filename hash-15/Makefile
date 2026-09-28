# NGCC uniform build: hash-15 Litchi (reference implementation)
NGCC_ID   := hash-15
NGCC_TYPE := hash
NGCC_ALG  := Litchi
include ../api/link_rules.mk

REF := Litchi/Implementations/Reference_Implementation
NGCC_KAT_DIR := Litchi/Test_Vectors

# Per each README.txt: CryptHash_AlgorithmInstance.c drng.c litchi_<n>.c plus
# the KAT driver (dropped by the default glob). drng.c is byte-identical to
# api/drng.c. Labels follow ALGORITHM_INSTANCE (litchi_512 ...), which also
# names the KAT files; litchi_xof is a fixed 1024-bit build of the XOF.
$(eval $(call ngcc_instance,litchi_512,$(REF)/Litchi-512))
$(eval $(call ngcc_instance,litchi_768,$(REF)/Litchi-768))
$(eval $(call ngcc_instance,litchi_1024,$(REF)/Litchi-1024))
$(eval $(call ngcc_instance,litchi_xof,$(REF)/Litchi-XOF))

include ../api/link_finish.mk
