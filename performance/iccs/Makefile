# ICCS placeholder helpers as hash "instances", timed by performance/campaign.py
# (phase baseline) exactly like a hash candidate: the same driver, flags, message
# lengths and planning. Each library exposes CryptHash() over one helper with a
# fixed output width; api/auxfunc.c is compiled unchanged.
#
#   sm3hash-256                    sm3hash (SM3)
#   pseudohash-{512,768,1024}      pseudohash (HMAC-SM3 cascade); only these widths exist
#   pseudoXOF-N                    pseudoXOF (KDF-SM3), N = every digest width of a hash candidate
NGCC_ROOT := ../..
NGCC_ID   := iccs
NGCC_TYPE := hash
NGCC_ALG  := ICCS placeholder helpers
include ../../api/link_rules.mk

# $(1)=label $(2)=ICCS_SM3HASH|ICCS_PSEUDOHASH|ICCS_PSEUDOXOF $(3)=output bits
define ICCS
SRCS_$(1) := iccs_hash.c iccs_auxfunc.c
DEFS_$(1) := -D$(2) -DICCS_OUTPUT_BITS=$(3)
SHIMDEFS_$(1) := -DNGCC_INSTANCE_HEADER_NONE -DNGCC_INSTANCE='"$(1)"' -DNGCC_DIGEST_BITS=$(3)
$$(eval $$(call ngcc_instance,$(1),ref))
endef

$(eval $(call ICCS,sm3hash-256,ICCS_SM3HASH,256))
$(foreach n,512 768 1024,$(eval $(call ICCS,pseudohash-$(n),ICCS_PSEUDOHASH,$(n))))
$(foreach n,256 384 512 768 1024 1152 1280 2048,$(eval $(call ICCS,pseudoXOF-$(n),ICCS_PSEUDOXOF,$(n))))

include ../../api/link_finish.mk
