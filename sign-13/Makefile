# NGCC uniform build: sign-13 GreatWall (reference implementation)
NGCC_ID   := sign-13
NGCC_TYPE := sig
NGCC_ALG  := GreatWall
include ../api/link_rules.mk

REF := Implementations/Reference_Implementation
NGCC_KAT_DIR := Test_Vectors

# FAEST-derived VOLE-in-the-head scheme, 8 parameter sets, one directory each
# (config.h fixes the level and f/s variant). Source list from each instance
# Makefile (SRCS of the KAT_SIG target) minus KAT_SIG.c; only the
# greatwall-<N>-matrix.c of the instance's security level is linked.
#
# Randomness: the tree ships two implementations of rand_bytes().
# randomness_os.c reads getrandom()/dev/urandom; randomness_randombytes.c
# wraps get_random_number(&drng_algorithm, ...). The submission's KAT build
# links the latter and so does this one. rng.c/PQCgenKAT_sign.c (NIST
# AES-CTR DRBG via OpenSSL) are not linked, so the submission's -lcrypto is
# not needed. The shipped drng.c equals api/drng.c apart from its licence
# header; there is no auxfunc.c, so api/auxfunc.c is added (unused).
#
# Compiler notes: KeccakHash.h declares no prototypes for Keccak_Hash*
# (KeccakHash.c defines them), so hash.h calls them implicitly; the uniform
# flags downgrade that to a warning (int return/args are ABI-compatible on
# x86-64 and the KATs pass). The code needs C11 (one-argument static_assert
# in vector_com.c), so it does not build with -std=c99.
GW_SRCS := SIG_AlgorithmInstance.c drng.c api.c aes.c aes_impl.c block.c block_impl.c \
           faest.c greatwall.c greatwall_impl.c hash.c KeccakHash.c KeccakP-1600-reference.c \
           KeccakSponge.c owf_proof.c polynomials.c polynomials_impl.c prgs.c quicksilver.c \
           randomness_randombytes.c small_vole.c transpose.c universal_hash.c util.c \
           vector_com.c vole_check.c vole_commit.c

# label, security level (matrix file)
define GW
SRCS_$(1) := $(GW_SRCS) greatwall-$(2)-matrix.c
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(1)))
endef

$(eval $(call GW,GreatWall128f,128))
$(eval $(call GW,GreatWall128s,128))
$(eval $(call GW,GreatWall192f,192))
$(eval $(call GW,GreatWall192s,192))
$(eval $(call GW,GreatWall256f,256))
$(eval $(call GW,GreatWall256s,256))
$(eval $(call GW,GreatWall512f,512))
$(eval $(call GW,GreatWall512s,512))

include ../api/link_finish.mk
