# NGCC uniform build: kem-20 MAMBA-Frost (reference implementation)
NGCC_ID   := kem-20
NGCC_TYPE := kem
NGCC_ALG  := MAMBA-Frost
include ../api/link_rules.mk

REF := Implementations/Reference_Implementation
NGCC_KAT_DIR := Test_Vectors

# Per each instance's Makefile (KAT_KEM target): Frost[-CC]/src/frost[cc]<n>.c
# (which #includes kem.c, noise.c and frost_macrify_reference.c) + util.c +
# common/sha3/fips202.c + common/aes/aes_c.c + KEM_AlgorithmInstance.c
# randombytes_adapter.c drng.c auxfunc.c, with -DNIX -D_AMD64_ -D_REFERENCE_
# -D_AES128_FOR_A_ -DFROST_USE_E8_CODE (the submitted KATs use the AES128
# expansion of A; without -D_AES128_FOR_A_ the SHAKE backend is selected and
# the KATs do not match). The 512 sets add -DFROST_U16_STREAMING_MATMUL.
# randombytes_adapter.c routes randombytes() to drng_algorithm.
# The CC-128/192/256 directories are the same code as 128/192/256 under other
# symbol names and ship identical KATs; they are still built as separate
# instances because they are separate submitted parameter-set directories.
FROST_DEFS := -DNIX -D_AMD64_ -D_REFERENCE_ -D_AES128_FOR_A_ -DFROST_USE_E8_CODE

# label (= ALGORITHM_INSTANCE = dir), core dir, core file, extra defines
define FROST
SRCS_$(1) := $(2)/src/$(3).c $(2)/src/util.c common/sha3/fips202.c common/aes/aes_c.c \
             KEM_AlgorithmInstance.c randombytes_adapter.c drng.c auxfunc.c
INC_$(1)  := -Isrc/$(1)/$(2)/src -Isrc/$(1)/common/sha3 -Isrc/$(1)/common/aes -Isrc/$(1)/common/random
DEFS_$(1) := $(FROST_DEFS) $(4)
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(1)))
endef

$(eval $(call FROST,MAMBA-Frost-128,Frost,frost128,))
$(eval $(call FROST,MAMBA-Frost-192,Frost,frost192,))
$(eval $(call FROST,MAMBA-Frost-256,Frost,frost256,))
$(eval $(call FROST,MAMBA-Frost-384,Frost,frost384,))
$(eval $(call FROST,MAMBA-Frost-512,Frost,frost512,-DFROST_U16_STREAMING_MATMUL))
$(eval $(call FROST,MAMBA-Frost-CC-128,Frost-CC,frostcc128,))
$(eval $(call FROST,MAMBA-Frost-CC-192,Frost-CC,frostcc192,))
$(eval $(call FROST,MAMBA-Frost-CC-256,Frost-CC,frostcc256,))
$(eval $(call FROST,MAMBA-Frost-CC-384,Frost-CC,frostcc384,))
$(eval $(call FROST,MAMBA-Frost-CC-512,Frost-CC,frostcc512,-DFROST_U16_STREAMING_MATMUL))

include ../api/link_finish.mk
