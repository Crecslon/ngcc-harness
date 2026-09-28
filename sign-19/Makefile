# NGCC uniform build: sign-19 Phoenix (reference implementation)
NGCC_ID   := sign-19
NGCC_TYPE := sig
NGCC_ALG  := Phoenix
include ../api/link_rules.mk

REF := Implementations and Test_Vectors/Implementations/Reference_Implementation
NGCC_KAT_DIR := Implementations and Test_Vectors/Test_Vectors

# Source lists and defines from each instance Makefile (CORE_SOURCES +
# SUBMISSION_SOURCES of its KAT_SIG target, minus the KAT_SIG.c driver).
# -DPARAMS selects params/params-<params>.h, -DPARAMNAME sets
# ALGORITHM_INSTANCE (otherwise hard-wired to "Phoenix-SHAKE-128s").
# -DSUBMISSION_DRNG is required: without it randombytes() (used for the hedged
# opt_rand in sign.c) reads /dev/urandom instead of drng_algorithm.
#
# The SM3 directories ship the official ICCS drng.c/auxfunc.c (identical to
# api/), which are linked. The SHAKE directories ship a drng.c that is NOT the
# ICCS DRNG (SHAKE256_df/SHAKE256_DRNG_* over shake256() instead of SM3). The
# submitted SHAKE KATs reproduce only with the official DRNG, so the shipped
# drng.c is dropped for SHAKE and api/drng.c is linked instead (the shipped
# drng.h is API-identical). The SHAKE dirs have no auxfunc.c, so api/auxfunc.c
# is added by the generic rules.
#
# Known result: the ten Phoenix-SM3-* instances MISMATCH their submitted KATs
# (with any -O level). PK usually matches, and R matches, but the TFORS
# grinding counter and the rest of the signature differ (192s/256s: the PK root
# differs too). The submitted KAT signatures do not even verify under the
# submitted SM3 reference code (sig_verify rejects them), so the SM3 vectors
# were produced by different code; the Optimized avx2 SM3 tree does not
# reproduce them either (its prf_addr/H_msg use sm3_xof). The instances are
# kept for benchmarking. Compiler warnings in the SM3 code (memcpy of SPX_N >
# 32 bytes from a 32-byte SM3 output in prf_addr/thash for 384/512) are
# genuine out-of-bounds reads in the submission.
PHX_COMMON := address.c counter.c merkle.c octopus.c randombytes.c sign.c tfors.c \
              utils.c utilsx1.c gwots.c gwotsx1.c SIG_AlgorithmInstance.c drng.c
PHX_SRCS_SHAKE := $(filter-out drng.c,$(PHX_COMMON)) hash_shake.c fips202.c thash_shake_simple.c
PHX_SRCS_SM3   := $(PHX_COMMON) auxfunc.c hash_sm3.c sm3_drng.c thash_sm3_simple.c

# hash (SHAKE|SM3), params name (lower case), level
define PHX
SRCS_Phoenix-$(1)-$(3) := $(PHX_SRCS_$(1))
DEFS_Phoenix-$(1)-$(3) := -DPARAMS=phoenix-$(2)-$(3) -DALLOW_DEEP_TREES -DSUBMISSION_DRNG \
                          -DPARAMNAME='"Phoenix-$(1)-$(3)"'
CFLAGS_Phoenix-$(1)-$(3) := -std=c99
$$(eval $$(call ngcc_instance,Phoenix-$(1)-$(3),$(REF)/Phoenix-$(1)-$(3)))
endef

PHX_LEVELS := 128f 128s 192f 192s 256f 256s 384f 384s 512f 512s
$(foreach l,$(PHX_LEVELS),$(eval $(call PHX,SHAKE,shake,$(l))))
$(foreach l,$(PHX_LEVELS),$(eval $(call PHX,SM3,sm3,$(l))))

include ../api/link_finish.mk
