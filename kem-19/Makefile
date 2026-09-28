# NGCC uniform build: kem-19 Lore (reference implementation)
NGCC_ID   := kem-19
NGCC_TYPE := kem
NGCC_ALG  := Lore
include ../api/link_rules.mk

REF := Implementations and Test_Vectors/Implementations/Reference_Implementation
TV  := Implementations and Test_Vectors/Test_Vectors

# Per each directory's Makefile (kat_api target: SOURCES_BASE + KEM_AlgorithmInstance.c
# drng.c, KAT_KEM.c being the driver) with -DLORE_LEVEL=<n>
# -DLORE_USE_API_PKC_DRNG; the latter makes randombytes.c call
# get_random_number(&drng_algorithm, ...) instead of getrandom(). The candidate's
# -O3 -fomit-frame-pointer is dropped. The level directories are not identical
# copies (poly.c, kem.c, ... differ), so each is built from its own directory
# with the LORE_LEVEL matching its name.
# Two hash backends ship separate reference trees and separate KAT sets
# (Test_Vectors/Lore-SHAKE, Test_Vectors/Lore-SM3) under the same instance
# name Lore-L<n> (ALGORITHM_INSTANCE = LORE_INSTANCE_NAME from params.h); the
# labels and the metadata instance name (-DNGCC_INSTANCE) carry the backend so
# RESULT lines are unambiguous, and KATNAME_/KATDIR_ map back to the submitted
# file (the regenerated kat/KAT_KEM_Lore-L<n>.txt is shared by both backends
# and holds whichever ran last). The SM3 tree ships drng.c + auxfunc.c; the SHAKE tree ships only
# drng.c, so the harness adds api/auxfunc.c there (as the candidate's SHAKE
# Makefile links no auxfunc.c, drng.c's SM3 comes from the official copy).
LORE_COMMON := kem.c pke.c indcpa.c polyvec.c poly.c ntt.c sampler.c reduce.c \
               toomcook.c verify.c bch_codec.c randombytes.c KEM_AlgorithmInstance.c drng.c
LORE_SHAKE_SRCS := $(LORE_COMMON) symmetric-shake.c fips202.c
LORE_SM3_SRCS   := $(LORE_COMMON) symmetric-sm3.c sm3_xof.c sm3.c auxfunc.c

# backend (SHAKE|SM3), level
define LORE
SRCS_Lore-$(1)-L$(2)    := $$(LORE_$(1)_SRCS)
DEFS_Lore-$(1)-L$(2)    := -DLORE_LEVEL=$(2) -DLORE_USE_API_PKC_DRNG
KATDIR_Lore-$(1)-L$(2)  := $(TV)/Lore-$(1)
KATNAME_Lore-$(1)-L$(2) := Lore-L$(2)
SHIMDEFS_Lore-$(1)-L$(2) := -DNGCC_INSTANCE='"Lore-$(1)-L$(2)"'
$$(eval $$(call ngcc_instance,Lore-$(1)-L$(2),$(REF)/Lore-$(1)/Lore-L$(2)))
endef

$(foreach b,SHAKE SM3,$(foreach l,1 2 3 4,$(eval $(call LORE,$(b),$(l)))))

include ../api/link_finish.mk
