# NGCC uniform build: sign-20 Qing Luan (reference implementation)
NGCC_ID   := sign-20
NGCC_TYPE := sig
NGCC_ALG  := Qing Luan
include ../api/link_rules.mk

REF := Implementations and Test_Vectors/Implementations/Reference_Implementation
NGCC_KAT_DIR := Implementations and Test_Vectors/Test_Vectors

# The ICCS API build of each level is the api_pkc/ adapter (source list from
# api_pkc/Makefile, target qingluan_kat_api, minus the KAT_SIG.c driver): the
# QingLuan core from ../src (fq_arith rsdp restr mpc keygen sign verify) plus
# api_pkc/{drng,auxfunc,SIG_AlgorithmInstance,utils_adapter,hash_adapter}.c.
# src/hash.c and src/utils.c are replaced by the adapters, so randombytes()
# draws from drng_algorithm (the reference utils.c has its own DRBG/OS entropy).
# -Iapi_pkc must precede -Iinclude so the adapter hash.h shadows include/hash.h.
# api_pkc/drng.c is identical to api/drng.c; api_pkc/auxfunc.c is the ICCS file
# plus an HMAC key-length check, and is linked as shipped.
# -DQINGLUAN_<level> selects ALGORITHM_INSTANCE (params.h also self-defines it).
QL_SRCS := src/fq_arith.c src/rsdp.c src/restr.c src/mpc.c src/keygen.c src/sign.c src/verify.c \
           api_pkc/drng.c api_pkc/auxfunc.c api_pkc/SIG_AlgorithmInstance.c \
           api_pkc/utils_adapter.c api_pkc/hash_adapter.c

define QL
SRCS_QingLuan-$(1) := $(QL_SRCS)
INC_QingLuan-$(1)  := -Isrc/QingLuan-$(1)/api_pkc -Isrc/QingLuan-$(1)/include
DEFS_QingLuan-$(1) := -DQINGLUAN_$(1)
CFLAGS_QingLuan-$(1) := -std=c11
$$(eval $$(call ngcc_instance,QingLuan-$(1),$(REF)/QingLuan-$(1)))
endef

$(eval $(call QL,128))
$(eval $(call QL,256))
$(eval $(call QL,384))
$(eval $(call QL,512))

include ../api/link_finish.mk
