# NGCC uniform build: sign-21 ReSolveD-alpha (reference implementation)
NGCC_ID   := sign-21
NGCC_TYPE := sig
NGCC_ALG  := ReSolveD-alpha
include ../api/link_rules.mk

REF := Implementations/Reference_Implementation
NGCC_KAT_DIR := Test_Vectors/Test_Vectors

# Source list and flags from each instance Makefile (default XOF=PSEUDO build of
# its KAT_SIG target, minus the KAT_SIG.c driver). -DXOF_PSEUDO selects the NGCC
# SM3 pseudoXOF (auxfunc.c) as the hash/XOF, which is what the submitted
# Makefile builds by default; without it xof.h falls back to the XKCP Keccak
# tree under sha3/ (XOF=SHAKE, not built here). The block cipher (AES /
# Rijndael-256 in enc.c) is the portable C code in both cases (HAVE_OPENSSL is
# not defined). The submitted flags are -std=c99 (plus -O3 -march=native, not
# copied). drng.c/auxfunc.c are the ICCS files (identical to api/ modulo the
# final newline); SIG_AlgorithmInstance.c draws all randomness from
# drng_algorithm.
RSD_SRCS := bavc.c drng.c enc.c prg.c fields.c instances.c quicksilver.c rsd.c \
            random_oracle.c tccr.c universal_hashing.c utils.c voleith_impl.c vole.c \
            auxfunc.c SIG_AlgorithmInstance.c

define RSD
SRCS_ReSolveD-alpha-$(1) := $(RSD_SRCS)
DEFS_ReSolveD-alpha-$(1) := -DXOF_PSEUDO
CFLAGS_ReSolveD-alpha-$(1) := -std=c99
$$(eval $$(call ngcc_instance,ReSolveD-alpha-$(1),$(REF)/ReSolveD-alpha-$(1)))
endef

$(foreach l,160f 160s 256f 256s 384f 384s 512f 512s,$(eval $(call RSD,$(l))))

include ../api/link_finish.mk
