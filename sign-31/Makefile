# NGCC uniform build: sign-31 TSUOV (reference implementation)
NGCC_ID   := sign-31
NGCC_TYPE := sig
NGCC_ALG  := TSUOV
include ../api/link_rules.mk

PKC := Implementations/Digital_Signature-TSUOV-x86-Reference_Implementation/API_PKC
REF := $(PKC)/Implementations/Reference_Implementation

# Source list from TSUOV_<n>/Makefile (KAT_SIG target, minus the KAT_SIG.c
# driver) and API_PKC/Implementations/Reference_Implementation/CMakeLists.txt:
# tsuov_core.c mgf.c Fql.c SIG_AlgorithmInstance.c auxfunc.c drng.c, i.e. the
# default glob, with -DTSUOV_VARIANT=<n> (tsuov_params.h then also sets
# ALGORITHM_INSTANCE "TSUOV_<n>"). sig_random_seed() in SIG_AlgorithmInstance.c
# draws every seed from drng_algorithm.
# KATs: the top-level Test_Vectors/KAT_SIG_TSUOV-<n>.txt files are in a private
# format (lower-case keys, hex lengths) that the ICCS KAT_SIG.c driver does not
# produce; the ICCS-format vectors of this tree are
# API_PKC/Test_Vector/KAT_SIG_TSUOV_<n>.txt, which are used here.
define TSUOV
DEFS_TSUOV_$(1)   := -DTSUOV_VARIANT=$(1)
KATDIR_TSUOV_$(1) := $(PKC)/Test_Vector
$$(eval $$(call ngcc_instance,TSUOV_$(1),$(REF)/TSUOV_$(1)))
endef

$(eval $(call TSUOV,128))
$(eval $(call TSUOV,256))
$(eval $(call TSUOV,512))

include ../api/link_finish.mk
