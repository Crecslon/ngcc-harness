# Symmetric cryptography survey

The NGCC public-key submissions were asked to use the ICCS placeholder functions `pseudohash` (SM3/HMAC-SM3), `pseudoXOF` (KDF-SM3) and `sm3hash` for hashing, and the ICCS SM3 DRNG for randomness, so that the selected NGCC hash can later be substituted. This survey records which reference implementations do so, which bypass the helpers with their own primitives, and how much of each operation the helpers take.

Totals: 67 ICCS-only, 7 bypass, 6 mixed, 4 instance-dependent.

Evidence: call-graph reachability from the exported API in the harness-built libraries, object-level constant scans (Keccak, SHA-2, SM3, AES, SM4, ChaCha), and source reading for candidates without a harness build. A primitive that is compiled but unreachable is not counted.

The last column is measured on system x86_1 (Intel Core i7-12700 (Alder Lake), one performance core, turbo off, fixed 2.1 GHz, SMT off); see its [summary](summary_x86_1.md).

| id | algorithm | verdict | notes | largest hash share on x86_1 (op) |
|---|---|---|---|---|
| [kem-01](../kem-01/perf_x86_1.md) | Aigis-Enc+ | ICCS-only | own fips202.c compiled but unreachable from the API | 39% (Aigis-enc3 enc) |
| [kem-02](../kem-02/perf_x86_1.md) | Amoeba | ICCS-only |  | 74% (Amoeba128 keygen) |
| [kem-03](../kem-03/perf_x86_1.md) | BAG-Loong | ICCS-only | `loong_hash_tagged_sm3_256` wraps sm3hash | 79% (BAG-Loong-128 enc) |
| [kem-04](../kem-04/perf_x86_1.md) | BAG-Piglet | ICCS-only | `*_using_shake` names parse pseudoXOF output; AES-256-CTR dead; DRNG only with -DBAG_PIGLET_KAT | 56% (bag_piglet_512 keygen) |
| [kem-05](../kem-05/perf_x86_1.md) | BIKE-MLThre | mixed | hash/XOF via ICCS; seeds from NIST AES-256-CTR-DRBG (OpenSSL) only with -DNIST_RAND, otherwise libc rand() | 1.2% (BIKE_v2_128 enc) |
| [kem-06](../kem-06/perf_x86_1.md) | BRA | ICCS-only | pseudohash for G/H; seed expansion via per-seed ICCS DRNG instances; XKCP Keccak dead | 4.5% (BRA-128 enc) |
| [kem-07](../kem-07/perf_x86_1.md) | BRQC | ICCS-only | pseudohash for G/H; seed expansion via per-seed ICCS DRNG instances; XKCP Keccak dead | 5.3% (BRQC-128 enc) |
| [kem-08](../kem-08/perf_x86_1.md) | BW-KEM | ICCS-only | optimized AVX2 auxfunc.c adds an SM3 counter-block fast path | 78% (BW_KEM_C512 enc) |
| [kem-09](../kem-09/perf_x86_1.md) | CheetahKEM | ICCS-only |  | 83% (Cheetah512 keygen) |
| [kem-10](../kem-10/perf_x86_1.md) | C-Multi-UR-AG | ICCS-only | own fips202.c compiled but unreachable from the API | 2.9% (CMultiURAG-256 enc) |
| [kem-11](../kem-11/perf_x86_1.md) | COMPASS-KEM | ICCS-only | `shake*` names are shims over pseudoXOF | 97% (COMPASS-KEM-256 keygen) |
| [kem-12](../kem-12/perf_x86_1.md) | CTL Algorithm | ICCS-only | sha3.c shim has no permutation and is unused | 12% (CTL-257-512 enc) |
| [kem-13](../kem-13/perf_x86_1.md) | DKEM (Ding Key Encapsulation) | ICCS-only | default DKE_HASH=0; own SM3/HMAC compiled but unreachable; DKE_HASH=2 would switch to SHAKE | 82% (DKEM-512 keygen) |
| [kem-14](../kem-14/perf_x86_1.md) | DTRU | ICCS-only |  | 33% (DTRU-768 enc) |
| [kem-15](../kem-15/perf_x86_1.md) | FLIT | ICCS-only |  | 52% (FLIT128_REF enc) |
| [kem-16](../kem-16/perf_x86_1.md) | HARE | ICCS-only | pseudoXOF only (recomputes prefix per call); lives under _shared/ | 3.0% (HARE-128-kr keygen) |
| [kem-17](../kem-17/perf_x86_1.md) | Hybrid Equivalent Punctured and Quasi-Cyclic | ICCS-only | never calls the DRNG: zero-initialised PRNG (known kem-17-1/-3) | 89% (hep-qc-1 dec) |
| [kem-18](../kem-18/perf_x86_1.md) | LoongKEM | ICCS-only |  | 87% (Loong512 keygen) |
| [kem-19](../kem-19/perf_x86_1.md) | Lore | instance-dependent | Lore-SM3: ICCS-only; Lore-SHAKE: own FIPS 202 (bypass); AVX2/NEON SIMD SM3 in auxfunc | 73% (Lore-SM3-L1 keygen) |
| [kem-20](../kem-20/perf_x86_1.md) | MAMBA-Frost | mixed | all SHAKE calls are pseudoXOF shims; matrix A via own AES-128 with -D_AES128_FOR_A_ | 3.8% (MAMBA-Frost-128 dec) |
| [kem-21](../kem-21/perf_x86_1.md) | MAMBA-Viper | ICCS-only | `shake*` names are shims over pseudoXOF | 48% (MAMBA-Viper-128 enc) |
| [kem-22](../kem-22/perf_x86_1.md) | Mithril | ICCS-only |  | 40% (Mithril-128 keygen) |
| [kem-23](../kem-23/perf_x86_1.md) | Mito | ICCS-only |  | 1.7% (Mito-2-E-128 dec) |
| [kem-24](../kem-24/perf_x86_1.md) | MORNING-Scabbard | ICCS-only |  | 70% (scabbard128 keygen) |
| [kem-25](../kem-25/perf_x86_1.md) | NEV | ICCS-only | with -DUSE_ICCS (SHA3 build selectable) | 69% (NEV_2048_3329_ICCS enc) |
| [kem-26](../kem-26/perf_x86_1.md) | NSS-HQC | bypass | own inline Keccak (SHA3-512, SHAKE256) for everything; DRNG for randomness | 0.0% (HQC-128 dec) |
| [kem-27](../kem-27/perf_x86_1.md) | NTRE Key Encapsulation Mechanism | ICCS-only |  | 49% (NTRE-128 enc) |
| [kem-28](../kem-28/perf_x86_1.md) | OAEP-NTRU | ICCS-only |  | 66% (OAEP-NTRU-2592 enc) |
| [kem-29](../kem-29/perf_x86_1.md) | Polar-KEM | ICCS-only |  | 98% (PolarKEM-512 keygen) |
| [kem-30](../kem-30/perf_x86_1.md) | PolarLAC | ICCS-only | default BIT_USE_SHAKE=0 | 73% (POLARLAC-512 enc) |
| [kem-31](../kem-31/perf_x86_1.md) | QIMEN-PIKE | bypass | own SM3 + counter XOF (pike_hash.c) for G, KDF and streams; DRNG only | 0.0% (NGCC-1 dec) |
| [kem-32](../kem-32/perf_x86_1.md) | Quasi-Cyclic Twisted McEliece Key Encapsulation Mechanism | bypass | own SHAKE256 for session key/keygen expansion; OpenSSL AES-256-CTR-DRBG seeded by the ICCS DRNG; auxfunc not linked | 0.0% (QCTM128 dec) |
| [kem-33](../kem-33/perf_x86_1.md) | QUBE | ICCS-only |  | 62% (qube-128 enc) |
| [kem-34](../kem-34/perf_x86_1.md) | Rudraksh2 | ICCS-only |  | 96% (lwekem512 enc) |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | instance-dependent | SM3 sets: private modified copy of auxfunc (official not linked); AES/SHAKE sets: own AES/Keccak (bypass); benchmark pilot uses SHAKE | 93% (Scloudplus-192-SM3-packed10 keygen) |
| [kem-36](../kem-36/perf_x86_1.md) | TRIKE | ICCS-only |  | 4.7% (TRIKE-2 enc) |
| [kem-37](../kem-37/perf_x86_1.md) | TriQ-KEM | ICCS-only |  | 12% (TriQ-KEM-128 keygen) |
| [kem-38](../kem-38/perf_x86_1.md) | UVW Key Encapsulation Mechanism | ICCS-only |  | 14% (UVW-KEM-128 enc) |
| [kem-39](../kem-39/perf_x86_1.md) | Weaver | ICCS-only | grep hits for AES/Keccak/OpenSSL are not reachable in the built library | 82% (WeaverKEM-128 keygen) |
| [kem-40](../kem-40/perf_x86_1.md) | YuanYang.KEM | ICCS-only |  | 42% (yuanyang-512 enc) |
| [kem-41](../kem-41/perf_x86_1.md) | ZEN | ICCS-only |  | 67% (ZEN_128 enc) |
| [kex-01](../kex-01/perf_x86_1.md) | ADKEX (Authenticated Ding Key Exchange) | ICCS-only | default DKE_HASH=0; own SM3/HMAC compiled but unreachable; DKE_HASH=2 would switch to SHAKE | 81% (ADKEX-512 exchange) |
| [kex-02](../kex-02/perf_x86_1.md) | AFS-KEX | ICCS-only | optimized AVX2 auxfunc.c adds an SM3 counter-block fast path | 76% (AFS_KEX_C512 exchange) |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | ICCS-only | PolarLAC/ZEN/BiT components; Keccak only if BIT_USE_SHAKE=1 | 78% (CreTAKE-S2S-BiT512-ePLAC512 exchange) |
| [kex-04](../kex-04/perf_x86_1.md) | DKEX (Ding Key Exchange) | mixed | KEX core via ICCS; embedded ML-DSA uses its own SHAKE | 36% (DKEX-512 exchange) |
| [kex-05](../kex-05/perf_x86_1.md) | Loom | ICCS-only | grep hits for AES/Keccak/OpenSSL are not reachable in the built library | 6.2% (LoomKEX-512 exchange) |
| [kex-06](../kex-06/perf_x86_1.md) | MAMBA-NIKE | bypass | SHAKE128/256 + ChaCha20; DRNG only with -DKAT_BUILD, otherwise /dev/urandom | 0.0% (MAMBA-NIKE-128 exchange) |
| [kex-07](../kex-07/perf_x86_1.md) | NEV-AKE | ICCS-only | own fips202.c compiled but unreachable | 55% (NEV_AKE_2048_769 exchange) |
| [kex-08](../kex-08/perf_x86_1.md) | NIIKE | bypass | no hash or KDF at all: raw j-invariant (known kex-08-1) | 0.0% (NIIKE-lv128 exchange) |
| [kex-09](../kex-09/perf_x86_1.md) | TriQ-KEX | ICCS-only |  | 7.0% (TriQ-KEX-128 exchange) |
| [sign-01](../sign-01/perf_x86_1.md) | Aigis-Sig+ | ICCS-only | own fips202.c compiled but unreachable from the API | 64% (Aigis-sig1 sign) |
| [sign-02](../sign-02/perf_x86_1.md) | BIT: Bimodal Triangular distribution based lattice signatures | ICCS-only | own fips202.c compiled but unreachable (BIT_USE_SHAKE=0) | 88% (BiT-512 keygen) |
| [sign-03](../sign-03/perf_x86_1.md) | CEDRUS+C | ICCS-only |  | 99% (CEDRUSC-384s keygen) |
| [sign-04](../sign-04/perf_x86_1.md) | CEDRUSɑ | ICCS-only |  | 99% (CEDRUSALPHA-384f keygen) |
| [sign-05](../sign-05/perf_x86_1.md) | Chinith | mixed | random oracles via ICCS; seed-tree/VOLE PRG via SM4 / Ballet / Vistrutah | 36% (sm4th_em_d2_128s_tight sign) |
| [sign-06](../sign-06/perf_x86_1.md) | COMPASS-SIG | ICCS-only | `shake*` names are shims over pseudoXOF | 95% (COMPASS-SIG-256 keygen) |
| [sign-07](../sign-07/perf_x86_1.md) | CS | ICCS-only |  | 62% (CS-512 sign) |
| [sign-08](../sign-08/perf_x86_1.md) | DARTS | ICCS-only | x4 shake names loop over the ICCS XOF | 88% (DARTS128 sign) |
| [sign-09](../sign-09/perf_x86_1.md) | DOVE | ICCS-only |  | 63% (dove_pkc_skc_512 verify) |
| [sign-10](../sign-10/perf_x86_1.md) | Facto-DSA | ICCS-only |  | 88% (Facto-DSA-512 verify) |
| [sign-11](../sign-11/perf_x86_1.md) | FlexTree | ICCS-only |  | 99% (Flextree-384f keygen) |
| [sign-12](../sign-12/perf_x86_1.md) | Galas Signature Scheme | ICCS-only |  | 46% (Galas-256S verify) |
| [sign-13](../sign-13/perf_x86_1.md) | GreatWall Signature Algorithm | bypass | own XKCP Keccak + AES-CTR PRGs; no auxfunc.c shipped | 0.0% (GreatWall128f keygen) |
| [sign-14](../sign-14/perf_x86_1.md) | Lynxer | mixed | with -DXOF_PSEUDO (as the KATs need): oracles via pseudoXOF, PRG via AES/Rijndael/SHACAL-2; source default is own Keccak (bypass) | 99% (Lynxer-512f keygen) |
| [sign-15](../sign-15/perf_x86_1.md) | MORNING-ATLAS | ICCS-only |  | 83% (lwrdsa192 keygen) |
| [sign-16](../sign-16/perf_x86_1.md) | Octarine | ICCS-only |  | 60% (Octarine-128 keygen) |
| [sign-17](../sign-17/perf_x86_1.md) | OPS Digital Signature Algorithm | ICCS-only | optimized AVX2 auxfunc.c adds sm3x4 / pseudoXOF_4x | 92% (OPSsig-512 keygen) |
| [sign-18](../sign-18/perf_x86_1.md) | Origami | ICCS-only | `shake*` names are shims over pseudoXOF | 100% (Origami-512 keygen) |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | instance-dependent | SM3 sets mixed (own SM3 for all tree hashing/PRF, pseudoXOF for digest/indices); SHAKE sets bypass with a SHAKE-based drng.c | 12% (Phoenix-SM3-256s sign) |
| [sign-20](../sign-20/perf_x86_1.md) | Qing Luan | ICCS-only | builds wide hash and counter XOF on sm3hash, not pseudohash/pseudoXOF | 88% (QingLuan-512 keygen) |
| [sign-21](../sign-21/perf_x86_1.md) | ReSolveD-ɑ | bypass | Keccak oracles + AES/Rijndael/SHACAL-2 PRGs; pseudoXOF only with -DXOF_PSEUDO (undefined) | 72% (ReSolveD-alpha-512f keygen) |
| [sign-22](../sign-22/perf_x86_1.md) | Rhyme | instance-dependent | SM3 sets: counter XOF on sm3hash; SHAKE sets: own FIPS 202 (bypass) | 77% (Rhyme-SM3-256 sign) |
| [sign-23](../sign-23/perf_x86_1.md) | Shuttle | ICCS-only | uses the ICCS SM3 DRBG (init/get_random_number) as its XOF; AVX2/AVX-512 SM3 DRBG in optimized | 0.0% (SHUTTLE-128 keygen) |
| [sign-24](../sign-24/perf_x86_1.md) | Sigurd | ICCS-only |  | 62% (Sigurd-512 sign) |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | ICCS-only |  | 17% (SQISign2Dsquare-Level2-eff_uncompressed verify) |
| [sign-26](../sign-26/perf_x86_1.md) | SQIsign2D-push1/2 | ICCS-only | iccs/xof_iccs.c glue; NIST SHAKE/AES leftovers unused | 0.0% (SQIsign2D-lvl1 verify) |
| [sign-27](../sign-27/perf_x86_1.md) | SQIsignTriangle | ICCS-only | `shake*` names are shims over pseudoXOF | 83% (SQIsignTriangle_lvl6 verify) |
| [sign-28](../sign-28/perf_x86_1.md) | SYDO | mixed | hashing via pseudoXOF; PRGs via own AES/Rijndael and a BLAKE2s-round cipher | 26% (sydo_512s sign) |
| [sign-29](../sign-29/perf_x86_1.md) | Tins | ICCS-only |  | 55% (Tins512 verify) |
| [sign-30](../sign-30/perf_x86_1.md) | TRINE | ICCS-only | with -DUSE_ICCS (SHA3 build selectable) | 64% (TRINE-128-Balanced keygen) |
| [sign-31](../sign-31/perf_x86_1.md) | TSUOV | ICCS-only |  | 79% (TSUOV_512 sign) |
| [sign-32](../sign-32/perf_x86_1.md) | UVW signature | ICCS-only | grep hits for AES/Keccak/OpenSSL are not reachable in the built library | 1.0% (UVW-128 verify) |
| [sign-33](../sign-33/perf_x86_1.md) | VDOO: Vinegar-Diagonal-Oil-Oil | ICCS-only |  | 0.3% (vdoo_128 verify) |
| [sign-34](../sign-34/perf_x86_1.md) | YuanYang.DSA | ICCS-only |  | 59% (yuanyang-512 verify) |
