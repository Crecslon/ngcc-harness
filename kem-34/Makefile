# NGCC uniform build: kem-34 Rudraksh2 (reference implementation)
NGCC_ID   := kem-34
NGCC_TYPE := kem
NGCC_ALG  := Rudraksh2
include ../api/link_rules.mk

REF := Implementations/Reference_Implementation
NGCC_KAT_DIR := Test_Vectors

# The reference directories ship no Makefile. The NGCC API is implemented in
# KEM_lwekem<N>.c / KEM_lwekem<N>.h (header named differently from
# KEM_AlgorithmInstance.h); it uses indcpa.c poly.c polyvec.c cbd.c minal.c
# reduce.c ntt.c verify.c plus the official auxfunc.c/drng.c. api.c is an
# alternative, namespaced (kem_light_ref_*) copy of the same API that would
# clash with KEM_lwekem<N>.c, and kex.c includes a kem.h that is not shipped,
# so neither is compiled. No defines: params.h in each directory fixes the
# parameter set. Randomness comes from drng_algorithm (KEM_lwekem<N>.c,
# indcpa.c). Test_Vectors/ and Implementations/Test_Vectors/ are identical.
define RUDRAKSH
SRCS_$(1) := KEM_$(1).c indcpa.c poly.c polyvec.c cbd.c minal.c reduce.c ntt.c verify.c \
             auxfunc.c drng.c
SHIMDEFS_$(1) := -DNGCC_INSTANCE_HEADER='"KEM_$(1).h"'
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(1)))
endef

$(eval $(call RUDRAKSH,lwekem128))
$(eval $(call RUDRAKSH,lwekem256))
$(eval $(call RUDRAKSH,lwekem512))

include ../api/link_finish.mk
