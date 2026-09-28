# NGCC uniform build: kem-35 Scloud+ (reference implementation)
NGCC_ID   := kem-35
NGCC_TYPE := kem
NGCC_ALG  := Scloud+
include ../api/link_rules.mk

BASE := Implementations and Test_Vectors/Implementations
REF  := $(BASE)/Reference_Implementation
NGCC_KAT_DIR := Implementations and Test_Vectors/Test_Vectors

# Each leaf Scloudplus-<L>/kem/ holds only parameters.h and a forwarding
# KEM_AlgorithmInstance.c; the code lives in _shared/. Source list and defines
# from the leaf CMakeLists.txt (kat_kem_scloudplus target, BACKEND=REF):
#   common/{encode,kem,pke,sample,util}.c ref/{matrix,pack}_reference.c
#   + AES:   common/hash_aes_shake.c ref/aes_reference.c
#   + SHAKE: common/hash_aes_shake.c
#   + SM3:   common/hash_sm3_portable.c ref/sm3_reference.c
# with -DSCLOUDPLUS_FAMILY_<F> -DSCLOUDPLUS_TIER_REFERENCE
# -DSCLOUDPLUS_REF_FAMILY_<F>. The KAT target drops common/random.c
# (getrandom/urandom) and links api_pkc/kat_random.c, whose randombytes() calls
# get_random_number(&drng_algorithm, ...), plus the shipped api_pkc/drng.c.
# No family uses the ICCS auxfunc.c: AES/SHAKE carry their own Keccak/AES, and
# the SM3 family links a vendored copy of the ICCS SM3 helper
# (ref/sm3_reference.c), so api/auxfunc.c is not added (NOAUX).
# ALGORITHM_INSTANCE is SYSTEM_NAME = Scloudplus-<L>-<F>-packed10, which is the
# label and the KAT file name part.
SHARED_REL := ../../../_shared
SC_COMMON := $(addprefix $(SHARED_REL)/scloudplus_core/,common/encode.c common/kem.c \
             common/pke.c common/sample.c common/util.c \
             ref/matrix_reference.c ref/pack_reference.c)
SC_API := $(SHARED_REL)/api_pkc/kat_random.c $(SHARED_REL)/api_pkc/drng.c
SC_HASH_AES   := $(addprefix $(SHARED_REL)/scloudplus_core/,common/hash_aes_shake.c ref/aes_reference.c)
SC_HASH_SHAKE := $(addprefix $(SHARED_REL)/scloudplus_core/,common/hash_aes_shake.c)
SC_HASH_SM3   := $(addprefix $(SHARED_REL)/scloudplus_core/,common/hash_sm3_portable.c ref/sm3_reference.c)

# $(1)=level $(2)=family (AES|SHAKE|SM3)
define SCLOUD
SRCS_Scloudplus-$(1)-$(2)-packed10 := KEM_AlgorithmInstance.c $(SC_COMMON) $(SC_HASH_$(2)) $(SC_API)
INC_Scloudplus-$(1)-$(2)-packed10  := -Isrc/Scloudplus-$(1)-$(2)-packed10/$(SHARED_REL)/api_pkc \
    -Isrc/Scloudplus-$(1)-$(2)-packed10/$(SHARED_REL)/scloudplus_core/include \
    -Isrc/Scloudplus-$(1)-$(2)-packed10/$(SHARED_REL)/scloudplus_core/common
DEFS_Scloudplus-$(1)-$(2)-packed10 := -DSCLOUDPLUS_FAMILY_$(2) -DSCLOUDPLUS_TIER_REFERENCE -DSCLOUDPLUS_REF_FAMILY_$(2)
NOAUX_Scloudplus-$(1)-$(2)-packed10 := 1
$$(eval $$(call ngcc_instance,Scloudplus-$(1)-$(2)-packed10,$(REF)/Scloudplus-$(1)/kem))
endef

$(foreach l,128 192 256 384 512,$(foreach f,AES SHAKE SM3,$(eval $(call SCLOUD,$(l),$(f)))))

include ../api/link_finish.mk
