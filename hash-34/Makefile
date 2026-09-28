# NGCC uniform build: hash-34 WChain (reference implementation)
NGCC_ID   := hash-34
NGCC_TYPE := hash
NGCC_ALG  := WChain
include ../api/link_rules.mk

REF := WChain/Implementations and Test_Vectors/Implementations/Reference_Implementation
NGCC_KAT_DIR := WChain/Implementations and Test_Vectors/Test_Vectors

# Per each instance's build_kat.sh: CryptHash_AlgorithmInstance.c drng.c
# wchain_c.c (+ the KAT driver, dropped by the default glob) with
# -DWCHAIN_NO_MAIN (drops the stand-alone main() in wchain_c.c) and
# -DWCHAIN_DISABLE_SIMD (portable code path, no <immintrin.h>). drng.c is
# byte-identical to api/drng.c.
define WCHAIN
DEFS_$(1) := -DWCHAIN_NO_MAIN -DWCHAIN_DISABLE_SIMD
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(1)))
endef

$(eval $(call WCHAIN,WChain-V1-512))
$(eval $(call WCHAIN,WChain-V2-1024))

include ../api/link_finish.mk
