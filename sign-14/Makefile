# NGCC uniform build: sign-14 Lynxer (reference implementation)
NGCC_ID   := sign-14
NGCC_TYPE := sig
NGCC_ALG  := Lynxer
include ../api/link_rules.mk

REF := Implementations/Reference_Implementation
NGCC_KAT_DIR := Test_Vectors

# VOLE-in-the-head scheme, 8 parameter sets, one directory each (the
# directories differ only in SIG_AlgorithmInstance.[ch], which select the
# parameter set). Source list from each instance Makefile (SRCS of the KAT_SIG
# target, default XOF=PSEUDO) minus KAT_SIG.c.
#
# -DXOF_PSEUDO is the submission's default and is what the submitted KATs were
# generated with: xof.h then uses the NGCC SM3-based pseudoXOF from auxfunc.c.
# The alternative Keccak backend (make XOF=SHAKE: -DWITH_KECCAK_X4 plus the
# sha3/ sources) is not built. Randomness is drawn from drng_algorithm
# (SIG_AlgorithmInstance.c); no OS entropy source exists in the tree. The
# shipped drng.c/auxfunc.c are used. -O3 -march=native from the submission are
# replaced by the uniform flags.
LYNX_SRCS := bavc.c drng.c enc.c prg.c fields.c instances.c lynx_matrices.c quicksilver.c \
             owf.c random_oracle.c tccr.c universal_hashing.c utils.c voleith_impl.c vole.c \
             auxfunc.c SIG_AlgorithmInstance.c

define LYNX
SRCS_$(1) := $(LYNX_SRCS)
DEFS_$(1) := -DXOF_PSEUDO
$$(eval $$(call ngcc_instance,$(1),$(REF)/$(1)))
endef

$(eval $(call LYNX,Lynxer-160f))
$(eval $(call LYNX,Lynxer-160s))
$(eval $(call LYNX,Lynxer-256f))
$(eval $(call LYNX,Lynxer-256s))
$(eval $(call LYNX,Lynxer-384f))
$(eval $(call LYNX,Lynxer-384s))
$(eval $(call LYNX,Lynxer-512f))
$(eval $(call LYNX,Lynxer-512s))

include ../api/link_finish.mk

# The pinned public reproducer downloads and verifies the official source archive.
.PHONY: exploit-public-forgery
exploit-public-forgery:
	./reproduce_public_forgery.sh
