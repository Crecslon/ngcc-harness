# NGCC uniform build: kem-11 COMPASS-KEM (reference implementation)
NGCC_ID   := kem-11
NGCC_TYPE := kem
NGCC_ALG  := COMPASS-KEM
include ../api/link_rules.mk

REF := Implementations and Test_Vectors/Implementations/Reference_Implementation
NGCC_KAT_DIR := Implementations and Test_Vectors/Test_Vector

# Per each directory's Makefile (kat target): kem.c indcpa.c polyvec.c poly.c
# ntt.c cbd.c reduce.c verify.c drng.c auxfunc.c symmetric-shake.c
# KEM_AlgorithmInstance.c with -DSECURITY_LEVEL=<n> (KAT_KEM.c is the driver;
# -O3 -fomit-frame-pointer dropped). kem.c draws its coins from drng_algorithm;
# the shipped randombytes.c (/dev/urandom) is not linked, as in the candidate
# build. Shipped kem_kat binaries are ignored.
COMPASS_SRCS := kem.c indcpa.c polyvec.c poly.c ntt.c cbd.c reduce.c verify.c \
                drng.c auxfunc.c symmetric-shake.c KEM_AlgorithmInstance.c

# label (= ALGORITHM_INSTANCE = dir), SECURITY_LEVEL
define COMPASS
SRCS_$(1) := $(COMPASS_SRCS)
DEFS_$(1) := -DSECURITY_LEVEL=$(2)
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(1)))
endef

$(eval $(call COMPASS,COMPASS-KEM-128,128))
$(eval $(call COMPASS,COMPASS-KEM-256,256))
$(eval $(call COMPASS,COMPASS-KEM-384,384))
$(eval $(call COMPASS,COMPASS-KEM-512,512))

include ../api/link_finish.mk
