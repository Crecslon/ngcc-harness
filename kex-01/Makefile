# NGCC uniform build: kex-01 ADKEX (reference implementation)
NGCC_ID   := kex-01
NGCC_TYPE := kex
NGCC_ALG  := ADKEX
include ../api/link_rules.mk

REF := Implementations/Reference_Implementation
NGCC_KAT_DIR := Test_Vectors

# Source list and defines from each instance's build.sh (minus KAT_KEX.c):
# the three directories are identical apart from build.sh; the parameter set
# is chosen by -DADKEX_MODE=N -DDKE_MODE=N. -DDKE_HASH=0 -DDKE_RANDOM=0
# -DDKE_FORCE_SCALAR select the SM3 hash, the DRNG (all randomness from
# drng_algorithm; randombytes.c then compiles to nothing) and the scalar
# reference paths (no AVX2/NEON). Two-pass protocol. build.sh also passes
# -fcommon, which is not needed here (links without it). The "ALGORITHM_INSTANCE
# redefined" warning is benign: parameters.h defines "DKE-<n>" first and
# KEX_AlgorithmInstance.h then sets the final "ADKEX-<n>".
ADKEX_SRCS := sm3.c dke_sm3.c dke_hash.c reduce.c ntt.c poly.c polyvec.c random_sampling.c \
              dke_utils.c packing.c verify.c dkecpa.c dkecca.c randombytes.c drng.c auxfunc.c \
              adkex_derand.c KEX_AlgorithmInstance.c

# label, mode
define ADKEX
SRCS_$(1) := $(ADKEX_SRCS)
DEFS_$(1) := -DADKEX_MODE=$(2) -DDKE_MODE=$(2) -DDKE_HASH=0 -DDKE_RANDOM=0 -DDKE_FORCE_SCALAR
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(1)))
endef

$(eval $(call ADKEX,ADKEX-128,128))
$(eval $(call ADKEX,ADKEX-256,256))
$(eval $(call ADKEX,ADKEX-512,512))

include ../api/link_finish.mk
