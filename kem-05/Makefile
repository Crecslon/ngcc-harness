# NGCC uniform build: kem-05 BIKE-MLThre (reference implementation)
NGCC_ID   := kem-05
NGCC_TYPE := kem
NGCC_ALG  := BIKE-MLThre
include ../api/link_rules.mk

REF := Implementations/reference

# Per Implementations/reference/Makefile (SRC + KAT_SRC minus the kat/KAT_KEM.c
# driver) with -DNIST_RAND=1 -DBIKE_SECURITY_<n> -DBIKE_MLTHRE_ENABLED=1; one
# source tree, the level is selected by the define (SECURITY=192 is a legacy set
# without a submitted KAT and is not built). The candidate's -m64 -O3 -std=c99
# is dropped. The shipped libbike_v2.a and kat_bike_kem_128 are ignored.
# Randomness: kem.c draws its seeds from the NIST AES-256-CTR DRBG in
# FromNIST/rng.c (OpenSSL EVP, hence -lcrypto); kat/KEM_AlgorithmInstance.c
# reseeds that DRBG with 64 bytes from drng_algorithm at every kem_keygen and
# kem_enc, so all randomness derives from the official DRNG.
# ALGORITHM_INSTANCE is BIKE_v2_<n>, while the submitted reference KATs are
# Test_Vectors/TEST_VECTORS/reference/KAT_KEM_BIKE_MLThre_<n>.txt (identical to
# Implementations/TEST_VECTORS/reference/) -> KATNAME_/KATDIR_.
BIKE_SRCS := auxfunc.c conversions.c decode_ml.c hash_wrapper.c kem.c mlthre_model.c \
             mlthre_policy.c mlthre_runtime_sampling.c ntl.c ring_buffer.c sampling.c \
             threshold.c utilities.c xof_prng.c FromNIST/rng.c \
             kat/KEM_AlgorithmInstance.c kat/drng.c

# level
define BIKE
SRCS_BIKE_v2_$(1)    := $(BIKE_SRCS)
INC_BIKE_v2_$(1)     := -Isrc/BIKE_v2_$(1)/kat
DEFS_BIKE_v2_$(1)    := -DNIST_RAND=1 -DBIKE_SECURITY_$(1) -DBIKE_MLTHRE_ENABLED=1
LDLIBS_BIKE_v2_$(1)  := -lcrypto
KATDIR_BIKE_v2_$(1)  := Test_Vectors/TEST_VECTORS/reference
KATNAME_BIKE_v2_$(1) := BIKE_MLThre_$(1)
$$(eval $$(call ngcc_instance,BIKE_v2_$(1),$(REF)))
endef

$(eval $(call BIKE,128))
$(eval $(call BIKE,256))
$(eval $(call BIKE,512))

include ../api/link_finish.mk
