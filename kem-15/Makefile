# NGCC uniform build: kem-15 FLIT (reference implementation)
NGCC_ID   := kem-15
NGCC_TYPE := kem
NGCC_ALG  := FLIT
include ../api/link_rules.mk

REF := Implementations/Reference_Implementation
NGCC_KAT_DIR := Test_Vectors

# Per each directory's Makefile (KAT_KEM target): kem.c ntt.c poly.c decode.c
# packing.c reduce.c verify.c auxfunc.c drng.c indcpa.c KEM_AlgorithmInstance.c
# (KAT_KEM.c is the driver). No defines; the candidate's -O3 -march=native is
# dropped. kem.c/indcpa.c draw from drng_algorithm directly. ALGORITHM_INSTANCE
# is FLIT<n>_REF, matching Test_Vectors/KAT_KEM_FLIT<n>_REF.txt (the *_OPT
# files there belong to the Optimized_Implementation).
FLIT_SRCS := kem.c ntt.c poly.c decode.c packing.c reduce.c verify.c indcpa.c \
             auxfunc.c drng.c KEM_AlgorithmInstance.c

# label (= ALGORITHM_INSTANCE), dir
define FLIT
SRCS_$(1) := $(FLIT_SRCS)
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(2)))
endef

$(eval $(call FLIT,FLIT128_REF,FLIT128))
$(eval $(call FLIT,FLIT256_REF,FLIT256))
$(eval $(call FLIT,FLIT512_REF,FLIT512))

include ../api/link_finish.mk
