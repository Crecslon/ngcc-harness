# NGCC uniform build: sign-30 TRINE (reference implementation)
NGCC_ID   := sign-30
NGCC_TYPE := sig
NGCC_ALG  := TRINE
include ../api/link_rules.mk

REF := Implementations/Reference_Implementation
NGCC_KAT_DIR := Test_Vectors

# Source list and defines from each directory's CMakeLists.txt (kat_* target;
# the shipped Makefile is a stale MEDS template naming meds.c): TRINE_CORE_SOURCES
# minus osfreq.c (a benchmark CPU-frequency helper referenced by nothing) +
# randombytes_iccs.c (randombytes() -> get_random_number(&drng_algorithm, ...))
# + iccs/{SIG_AlgorithmInstance,drng,auxfunc}.c, with -DPARAMS=<n> -DUSE_ICCS
# (hashkdf.c then hashes with the ICCS auxfunc.c instead of fips202.c; the
# SHA3 build does not reproduce the KATs). The six directories differ only in
# the default PARAMS in params.h. ALGORITHM_INSTANCE is TRINE_ALGORITHM_INSTANCE,
# which CMake sets to "TRINE-Balanced-I" etc.; the submitted KAT files are
# named KAT_SIG_TRINE-<L>-{Balanced,ShortSig}.txt, so it is set to the label.
TRINE_SRCS := trine.c util.c field.c matrixmod.c matrixelim.c triform.c canonical.c \
              corank1.c trine_expand.c trine_codec.c bitstream.c hashkdf.c \
              randombytes_iccs.c iccs/SIG_AlgorithmInstance.c iccs/drng.c iccs/auxfunc.c

# $(1)=label (KAT name) $(2)=directory $(3)=PARAMS
define TRINE
SRCS_$(1) := $(TRINE_SRCS)
INC_$(1)  := -Isrc/$(1)/iccs
DEFS_$(1) := -DPARAMS=$(3) -DUSE_ICCS -DTRINE_ALGORITHM_INSTANCE='"$(1)"'
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(2)))
endef

# Slow reference code: the ICCS build buffers the whole transcript and hashes
# it at the end (~425 MB / ~185 MB per sign and per verify at level 512, see
# pseudocode.md). The 10-record run of the 256 instances exceeds the harness's
# 900 s timeout, so they are verified on the first 3 records (strict:3).
# KAT_SIG_TRINE-512-Balanced.txt holds only the first 2 records and
# KAT_SIG_TRINE-512-ShortSig.txt only the first record (the submitters also
# shipped 10-record copies named KAT_SIG_TRINE-512-*.txt.txt, of which these are
# prefixes). TRINE-512-ShortSig is verified on that one record;
# TRINE-512-Balanced does not finish 2 records within 900 s, so it is verified on
# its first record with a 30-minute timeout.
TESTFLAGS_TRINE-256-Balanced := --count 3
TESTFLAGS_TRINE-256-ShortSig := --count 3
TESTFLAGS_TRINE-512-Balanced := --count 1 --timeout 1800
TESTFLAGS_TRINE-512-ShortSig := --count 1 --timeout 1800

$(eval $(call TRINE,TRINE-128-Balanced,TRINE-128-balanced,1))
$(eval $(call TRINE,TRINE-256-Balanced,TRINE-256-balanced,2))
$(eval $(call TRINE,TRINE-512-Balanced,TRINE-512-balanced,3))
$(eval $(call TRINE,TRINE-128-ShortSig,TRINE-128-ShortSig,4))
$(eval $(call TRINE,TRINE-256-ShortSig,TRINE-256-ShortSig,5))
$(eval $(call TRINE,TRINE-512-ShortSig,TRINE-512-ShortSig,6))

include ../api/link_finish.mk
