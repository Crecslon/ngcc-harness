# NGCC uniform build: sign-26 SQIsign2D-push1/2 (reference implementation)
NGCC_ID   := sign-26
NGCC_TYPE := sig
NGCC_ALG  := SQIsign2D-push1/2
include ../api/link_rules.mk

NGCC_KAT_DIR := Test_Vectors

# Implementations/sqisign2d_lvlN are four identical copies of one CMake project
# (SQISIGN_BUILD_TYPE=ref, GMP_LIBRARY=SYSTEM => -lgmp). Source list from
# src/**/CMakeLists.txt and .cmake/*.cmake for the ICCS KAT target
# kat_sig_sqisign2d_lvlN = sqisign_lvlN_iccs + sqisign_common_iccs +
# src/iccs/{SIG_AlgorithmInstance,drng}.c. The ICCS common library replaces
# the generic randombytes_system.c/randombytes_ctrdrbg.c, aes_c.c, fips202.c
# and xof_shake.c with src/iccs/randombytes_iccs.c (randombytes() ->
# get_random_number(&drng_algorithm, ...)) and src/iccs/xof_iccs.c (the
# hash/XOF over the ICCS auxfunc.c); both are required to reproduce the KATs.
# Defines from .cmake/target.cmake on x86_64 Linux (TARGET_AMD64 RADIX_64
# TARGET_OS_UNIX), SQISIGN_VARIANT=lvlN from src/CMakeLists.txt, and the KAT
# target's ALGORITHM_INSTANCE="SQIsign2D-lvlN" (the header's #ifndef default
# is only "SQIsign2D"). flags.cmake adds -O3 -funroll-loops; the harness keeps
# its uniform -O2 and adds -funroll-loops. The documented build is
# CMAKE_BUILD_TYPE=Release, i.e. -DNDEBUG: without it a debug-only assertion in
# secret_key_encode() (sqisign.c:439, denominator coprime to the ideal norm)
# aborts key generation at the first KAT record.
# Known defect: Test_Vectors/KAT_SIG_SQIsign2D-lvl3.txt is a splice of level-2
# and level-3 records (10 of 12 have SK_Len = 676, the level-2 size), so the
# level-3 instance cannot reproduce it (see pseudocode.md, "Discrepancy 2").
SQI_SRCS := src/sqisign.c \
    src/iccs/SIG_AlgorithmInstance.c src/iccs/drng.c src/iccs/auxfunc.c \
    src/iccs/randombytes_iccs.c src/iccs/xof_iccs.c \
    src/common/generic/mem.c src/common/generic/tools.c \
    src/intbig/ref/generic/intbig.c \
    $(addprefix src/quaternion/ref/generic/,algebra.c ideal.c dim4.c dim2.c integers.c \
        lattice.c finit.c printer.c lll.c matkermod.c) \
    src/klpt/ref/klptx/tools.c \
    src/gf/ref/gfx/fp2.c src/gf/ref/gfx/fp.c src/gf/ref/gfx/mp.c \
    $(addprefix src/ec/ref/ecx/,ec.c kps.c xisog.c xeval.c isog_chains.c basis.c biextension.c) \
    src/id2iso/ref/id2isox/id2iso.c \
    src/hd/ref/hdx/hd.c src/hd/ref/hdx/theta_structure.c src/hd/ref/hdx/theta_isogenies.c \
    src/dim2id2iso/ref/dim2id2isox/dim2id2iso.c \
    src/sqisigndim2/ref/sqisigndim2x/sign.c src/sqisigndim2/ref/sqisigndim2x/keygen.c \
    src/sqisigndim2/ref/sqisigndim2x/doublepath.c

# $(1)=level (lvl1..lvl4) $(2)=prime-field file in src/gf/ref/<level>/
define SQI2D
SRCS_SQIsign2D-$(1) := $(SQI_SRCS) src/gf/ref/$(1)/$(2) \
    $(addprefix src/precomp/ref/$(1)/,gf_constants.c torsion_constants.c quaternion_data.c \
        endomorphism_action.c klpt_constants.c)
INC_SQIsign2D-$(1) := $(addprefix -Isrc/SQIsign2D-$(1)/,src/iccs include \
    src/common/generic/include src/intbig/ref/generic/include \
    src/quaternion/ref/generic/include src/precomp/ref/$(1)/include \
    src/klpt/ref/include src/gf/ref/include src/ec/ref/include src/hd/ref/include \
    src/id2iso/ref/include src/dim2id2iso/ref/include src/sqisigndim2/ref/include)
DEFS_SQIsign2D-$(1) := -DNDEBUG -DTARGET_AMD64 -DRADIX_64 -DTARGET_OS_UNIX -DSQISIGN_VARIANT=$(1) \
    -DOUTPUT_BLANK_TEST_VECTORS=0 -DALGORITHM_INSTANCE='"SQIsign2D-$(1)"'
CFLAGS_SQIsign2D-$(1) := -funroll-loops
LDLIBS_SQIsign2D-$(1) := -lgmp
$$(eval $$(call ngcc_instance,SQIsign2D-$(1),Implementations/sqisign2d_$(1)))
endef

$(eval $(call SQI2D,lvl1,fp_13178.c))
$(eval $(call SQI2D,lvl2,fp_191118.c))
$(eval $(call SQI2D,lvl3,fp_263156.c))
$(eval $(call SQI2D,lvl4,fp_527324.c))

include ../api/link_finish.mk
