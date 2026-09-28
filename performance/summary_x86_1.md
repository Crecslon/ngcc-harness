# Performance — x86-64, system x86_1

Independent measurements of the NGCC Round 1 implementations on one 12th Gen Intel(R) Core(TM) i7-12700 core (max 2.10 GHz, governor performance, turbo off, SMT off). Cycles are the mean of all timed calls in five trials, normally each in a fresh process. **Symmetric %** is the share of each operation spent in the ICCS placeholder hash functions (`pseudohash`, `pseudoXOF`, `sm3hash`); the ICCS DRNG is counted separately on the candidate pages. Candidates that implement their own hashing show a low share here — see the [symmetric cryptography survey](symmetric-survey.md). These are not submitter self-assessments and not NICCS results.

See [method and limitations](method_x86_1.md). `–` = not measured (no harness build or timeout); `n=` marks operations with fewer than 100 timed calls; ⚠ marks instances whose submitted KAT vectors are not reproduced by the submitted code (timed, but output not validated — see the candidate page).

## Key encapsulation

| id | algorithm | instance | keygen | sym % | enc | sym % | dec | sym % |
|---|---|---|---|---|---|---|---|---|
| [kem-01](../kem-01/perf_x86_1.md) | Aigis-Enc+ | `Aigis-enc1` | 269.2 k | 30% | 331.4 k | 35% | 373.2 k | 33% |
| [kem-01](../kem-01/perf_x86_1.md) | Aigis-Enc+ | `Aigis-enc2` | 448.1 k | 30% | 602.4 k | 35% | 705.1 k | 31% |
| [kem-01](../kem-01/perf_x86_1.md) | Aigis-Enc+ | `Aigis-enc3` | 1.01 M | 38% | 1.35 M | 39% | 1.61 M | 35% |
| [kem-02](../kem-02/perf_x86_1.md) | Amoeba | `Amoeba128` | 379.2 k | 74% | 525.7 k | 71% | 590.4 k | 63% |
| [kem-02](../kem-02/perf_x86_1.md) | Amoeba | `Amoeba192` | 516.8 k | 73% | 732.8 k | 70% | 832.4 k | 61% |
| [kem-02](../kem-02/perf_x86_1.md) | Amoeba | `Amoeba256` | 622.2 k | 71% | 858.4 k | 67% | 993.2 k | 58% |
| [kem-02](../kem-02/perf_x86_1.md) | Amoeba | `Amoeba384` | 923.9 k | 71% | 1.28 M | 67% | 1.49 M | 57% |
| [kem-02](../kem-02/perf_x86_1.md) | Amoeba | `Amoeba512` | 1.21 M | 71% | 1.66 M | 67% | 1.94 M | 57% |
| [kem-03](../kem-03/perf_x86_1.md) | BAG-Loong | `BAG-Loong-128` | 57.12 M | 69% | 54.70 M | 79% | 99.48 M | 69% |
| [kem-03](../kem-03/perf_x86_1.md) | BAG-Loong | `BAG-Loong-256` | 149.90 M | 49% | 128.42 M | 61% | 251.28 M | 54% |
| [kem-03](../kem-03/perf_x86_1.md) | BAG-Loong | `BAG-Loong-384` | 347.64 M | 45% | 264.60 M | 59% | 514.28 M | 56% |
| [kem-03](../kem-03/perf_x86_1.md) | BAG-Loong | `BAG-Loong-512` | 589.88 M | 36% | 391.51 M | 54% | 749.64 M | 53% |
| [kem-04](../kem-04/perf_x86_1.md) | BAG-Piglet | `bag_piglet_128` | 1.61 M | 53% | 3.45 M | 17% | 12.12 M | 14% |
| [kem-04](../kem-04/perf_x86_1.md) | BAG-Piglet | `bag_piglet_256` | 7.19 M | 24% | 22.75 M | 5.6% | 81.52 M | 4.4% |
| [kem-04](../kem-04/perf_x86_1.md) | BAG-Piglet | `bag_piglet_384` | 20.60 M | 33% | 55.27 M | 8.9% | 221.57 M | 6.3% |
| [kem-04](../kem-04/perf_x86_1.md) | BAG-Piglet | `bag_piglet_512` | 92.32 M | 56% | 193.81 M | 18% | 725.11 M | 14% |
| [kem-05](../kem-05/perf_x86_1.md) | BIKE-MLThre | `BIKE_v2_128` | 1.45 G | 0.0% | 13.48 M | 1.2% | 88.85 M | 0.2% |
| [kem-05](../kem-05/perf_x86_1.md) | BIKE-MLThre | `BIKE_v2_256` | 15.62 G | 0.0% | 88.31 M | 0.5% | 454.96 M | 0.1% |
| [kem-05](../kem-05/perf_x86_1.md) | BIKE-MLThre | `BIKE_v2_512` | 211.25 G (n=5) | 0.0% | 660.20 M | 0.4% | 3.27 G | 0.1% |
| [kem-06](../kem-06/perf_x86_1.md) | BRA | `BRA-128` | 2.04 M | 0.0% | 4.52 M | 4.5% | 50.59 M | 0.4% |
| [kem-06](../kem-06/perf_x86_1.md) | BRA | `BRA-256` | 4.37 M | 0.0% | 9.38 M | 3.4% | 102.18 M | 0.3% |
| [kem-06](../kem-06/perf_x86_1.md) | BRA | `BRA-512` | 8.37 M | 0.0% | 18.55 M | 3.4% | 262.02 M | 0.2% |
| [kem-07](../kem-07/perf_x86_1.md) | BRQC | `BRQC-128` | 3.03 M | 0.0% | 6.65 M | 5.3% | 94.14 M | 0.4% |
| [kem-07](../kem-07/perf_x86_1.md) | BRQC | `BRQC-256` | 9.07 M | 0.0% | 18.72 M | 3.1% | 256.46 M | 0.2% |
| [kem-07](../kem-07/perf_x86_1.md) | BRQC | `BRQC-512` | 26.53 M | 0.0% | 55.45 M | 2.1% | 1.07 G | 0.1% |
| [kem-08](../kem-08/perf_x86_1.md) | BW-KEM | `BW_KEM_C128` | 256.8 k | 65% | 288.5 k | 63% | 338.7 k | 59% |
| [kem-08](../kem-08/perf_x86_1.md) | BW-KEM | `BW_KEM_C256` | 645.6 k | 72% | 664.0 k | 71% | 793.0 k | 64% |
| [kem-08](../kem-08/perf_x86_1.md) | BW-KEM | `BW_KEM_C512` | 2.14 M | 77% | 2.16 M | 78% | 2.51 M | 72% |
| [kem-09](../kem-09/perf_x86_1.md) | CheetahKEM | `Cheetah128` | 283.6 k | 64% | 367.7 k | 61% | 425.3 k | 54% |
| [kem-09](../kem-09/perf_x86_1.md) | CheetahKEM | `Cheetah256` | 748.1 k | 68% | 859.1 k | 65% | 973.5 k | 57% |
| [kem-09](../kem-09/perf_x86_1.md) | CheetahKEM | `Cheetah384` | 2.25 M | 82% | 2.39 M | 79% | 2.63 M | 74% |
| [kem-09](../kem-09/perf_x86_1.md) | CheetahKEM | `Cheetah512` | 3.60 M | 83% | 3.77 M | 81% | 4.09 M | 76% |
| [kem-10](../kem-10/perf_x86_1.md) | C-Multi-UR-AG | `CMultiURAG-128` | 12.19 M | 0.0% | 23.60 M | 2.8% | 128.36 M | 0.5% |
| [kem-10](../kem-10/perf_x86_1.md) | C-Multi-UR-AG | `CMultiURAG-256` | 37.54 M | 0.0% | 55.27 M | 2.9% | 339.59 M | 0.5% |
| [kem-10](../kem-10/perf_x86_1.md) | C-Multi-UR-AG | `CMultiURAG-512` | 165.29 M | 0.0% | 240.27 M | 1.8% | 1.45 G | 0.3% |
| [kem-11](../kem-11/perf_x86_1.md) | COMPASS-KEM | `COMPASS-KEM-128` | 1.61 M | 96% | 1.64 M | 95% | 1.66 M | 93% |
| [kem-11](../kem-11/perf_x86_1.md) | COMPASS-KEM | `COMPASS-KEM-256` | 6.24 M | 97% | 6.25 M | 97% | 6.30 M | 96% |
| [kem-11](../kem-11/perf_x86_1.md) | COMPASS-KEM | `COMPASS-KEM-384` | 3.81 M | 91% | 3.97 M | 88% | 4.15 M | 84% |
| [kem-11](../kem-11/perf_x86_1.md) | COMPASS-KEM | `COMPASS-KEM-512` | 6.63 M | 93% | 6.83 M | 90% | 7.07 M | 87% |
| [kem-12](../kem-12/perf_x86_1.md) | CTL Algorithm | `CTL-257-512` | 17.76 M | 8.4% | 61.0 k | 12% | 349.0 k | 6.2% |
| [kem-12](../kem-12/perf_x86_1.md) | CTL Algorithm | `CTL-769-1024` | 79.80 M | 2.5% | 113.7 k | 10% | 711.3 k | 5.1% |
| [kem-12](../kem-12/perf_x86_1.md) | CTL Algorithm | `CTL-3329-2048` | 2.15 G | 0.1% | 11.91 M | 0.4% | 79.73 M | 0.3% |
| [kem-13](../kem-13/perf_x86_1.md) | DKEM (Ding Key Encapsulation) | `DKEM-128` | 199.1 k | 65% | 226.9 k | 62% | 254.3 k | 56% |
| [kem-13](../kem-13/perf_x86_1.md) | DKEM (Ding Key Encapsulation) | `DKEM-256` | 594.4 k | 70% | 606.5 k | 69% | 653.3 k | 64% |
| [kem-13](../kem-13/perf_x86_1.md) | DKEM (Ding Key Encapsulation) | `DKEM-512` | 2.04 M | 82% | 2.12 M | 82% | 2.23 M | 77% |
| [kem-14](../kem-14/perf_x86_1.md) | DTRU | `DTRU-648` | 334.5 k | 0.0% | 164.8 k | 25% | 323.2 k | 26% |
| [kem-14](../kem-14/perf_x86_1.md) | DTRU | `DTRU-648-PACK_PK` | 336.0 k | 0.0% | 179.1 k | 23% | 337.5 k | 25% |
| [kem-14](../kem-14/perf_x86_1.md) | DTRU | `DTRU-768` | 293.7 k | 0.0% | 196.9 k | 33% | 367.9 k | 32% |
| [kem-14](../kem-14/perf_x86_1.md) | DTRU | `DTRU-768-PACK_PK` | 298.4 k | 0.0% | 213.9 k | 31% | 385.9 k | 30% |
| [kem-14](../kem-14/perf_x86_1.md) | DTRU | `DTRU-1024` | 346.4 k | 0.0% | 233.8 k | 31% | 451.0 k | 31% |
| [kem-14](../kem-14/perf_x86_1.md) | DTRU | `DTRU-1024-PACK_PK` | 351.1 k | 0.0% | 254.5 k | 28% | 473.5 k | 29% |
| [kem-14](../kem-14/perf_x86_1.md) | DTRU | `DTRU-1536` | 460.0 k | 0.0% | 385.8 k | 33% | 731.8 k | 30% |
| [kem-14](../kem-14/perf_x86_1.md) | DTRU | `DTRU-1536-PACK_PK` | 479.3 k | 0.0% | 424.7 k | 30% | 776.0 k | 29% |
| [kem-14](../kem-14/perf_x86_1.md) | DTRU | `DTRU-2048` | 804.6 k | 0.0% | 533.0 k | 31% | 1.02 M | 28% |
| [kem-14](../kem-14/perf_x86_1.md) | DTRU | `DTRU-2048-PACK_PK` | 813.9 k | 0.0% | 579.0 k | 28% | 1.07 M | 27% |
| [kem-14](../kem-14/perf_x86_1.md) | DTRU | `DTRU-Light` | 119.3 k | 0.0% | 97.8 k | 28% | 192.0 k | 31% |
| [kem-14](../kem-14/perf_x86_1.md) | DTRU | `DTRU-Prime` | 113.74 M | 0.0% | 335.8 k | 15% | 679.9 k | 18% |
| [kem-15](../kem-15/perf_x86_1.md) | FLIT | `FLIT128_REF` | 140.0 k | 31% | 121.3 k | 52% | 156.9 k | 31% |
| [kem-15](../kem-15/perf_x86_1.md) | FLIT | `FLIT256_REF` | 348.2 k | 28% | 255.5 k | 42% | 362.5 k | 22% |
| [kem-15](../kem-15/perf_x86_1.md) | FLIT | `FLIT512_REF` | 1.41 M | 29% | 943.2 k | 52% | 1.26 M | 27% |
| [kem-16](../kem-16/perf_x86_1.md) | HARE | `HARE-128-kr` | 5.89 M | 3.0% | 12.93 M | 2.3% | 19.48 M | 2.1% |
| [kem-16](../kem-16/perf_x86_1.md) | HARE | `HARE-256-kr` | 26.13 M | 1.5% | 55.20 M | 1.1% | 84.79 M | 1.1% |
| [kem-16](../kem-16/perf_x86_1.md) | HARE | `HARE-384-kr` | 78.03 M | 1.1% | 161.95 M | 0.9% | 244.38 M | 1.0% |
| [kem-16](../kem-16/perf_x86_1.md) | HARE | `HARE-512-kr` | 166.96 M | 1.5% | 342.73 M | 1.0% | 519.62 M | 1.0% |
| [kem-17](../kem-17/perf_x86_1.md) | Hybrid Equivalent Punctured and Quasi-Cyclic | `hep-qc-1` | 232.07 M | 87% | 15.14 M | 43% | 246.18 M | 89% |
| [kem-17](../kem-17/perf_x86_1.md) | Hybrid Equivalent Punctured and Quasi-Cyclic | `hep-qc-3` | 504.91 M | 81% | 45.13 M | 42% | 482.18 M | 88% |
| [kem-17](../kem-17/perf_x86_1.md) | Hybrid Equivalent Punctured and Quasi-Cyclic | `hep-qc-5` | 883.58 M | 74% | 103.32 M | 39% | 814.49 M | 84% |
| [kem-17](../kem-17/perf_x86_1.md) | Hybrid Equivalent Punctured and Quasi-Cyclic | `hep-qc-7` | 4.22 G | 55% | 684.81 M | 39% | 3.39 G | 73% |
| [kem-18](../kem-18/perf_x86_1.md) | LoongKEM | `Loong128` | 6.26 M | 79% | 6.34 M | 78% | 6.42 M | 77% |
| [kem-18](../kem-18/perf_x86_1.md) | LoongKEM | `Loong256` | 15.94 M | 79% | 15.84 M | 78% | 16.15 M | 77% |
| [kem-18](../kem-18/perf_x86_1.md) | LoongKEM | `Loong384` | 46.99 M | 86% | 47.40 M | 85% | 47.89 M | 85% |
| [kem-18](../kem-18/perf_x86_1.md) | LoongKEM | `Loong512` | 75.46 M | 87% | 75.94 M | 87% | 77.37 M | 86% |
| [kem-19](../kem-19/perf_x86_1.md) | Lore | `Lore-SHAKE-L1` | 173.0 k | 0.0% | 333.7 k | 0.0% | 392.1 k | 0.0% |
| [kem-19](../kem-19/perf_x86_1.md) | Lore | `Lore-SHAKE-L2` | 717.4 k | 0.0% | 1.07 M | 0.0% | 1.35 M | 0.0% |
| [kem-19](../kem-19/perf_x86_1.md) | Lore | `Lore-SHAKE-L3` | 1.58 M | 0.0% | 2.06 M | 0.0% | 2.35 M | 0.0% |
| [kem-19](../kem-19/perf_x86_1.md) | Lore | `Lore-SHAKE-L4` | 2.71 M | 0.0% | 3.58 M | 0.0% | 4.28 M | 0.0% |
| [kem-19](../kem-19/perf_x86_1.md) | Lore | `Lore-SM3-L1` | 240.3 k | 73% | 363.5 k | 68% | 416.7 k | 60% |
| [kem-19](../kem-19/perf_x86_1.md) | Lore | `Lore-SM3-L2` | 1.06 M | 60% | 1.35 M | 53% | 1.62 M | 44% |
| [kem-19](../kem-19/perf_x86_1.md) | Lore | `Lore-SM3-L3` | 2.38 M | 58% | 2.78 M | 53% | 3.05 M | 48% |
| [kem-19](../kem-19/perf_x86_1.md) | Lore | `Lore-SM3-L4` | 5.19 M | 64% | 5.95 M | 59% | 6.65 M | 52% |
| [kem-20](../kem-20/perf_x86_1.md) | MAMBA-Frost | `MAMBA-Frost-128` | 38.49 M | 2.2% | 43.04 M | 3.2% | 43.47 M | 3.8% |
| [kem-20](../kem-20/perf_x86_1.md) | MAMBA-Frost | `MAMBA-Frost-192` | 112.69 M | 1.3% | 119.72 M | 2.0% | 120.24 M | 2.4% |
| [kem-20](../kem-20/perf_x86_1.md) | MAMBA-Frost | `MAMBA-Frost-256` | 241.73 M | 1.3% | 257.78 M | 1.7% | 258.75 M | 2.0% |
| [kem-20](../kem-20/perf_x86_1.md) | MAMBA-Frost | `MAMBA-Frost-384` | 538.40 M | 0.9% | 593.01 M | 1.6% | 595.55 M | 1.9% |
| [kem-20](../kem-20/perf_x86_1.md) | MAMBA-Frost | `MAMBA-Frost-512` | 972.04 M | 0.9% | 990.48 M | 2.1% | 992.50 M | 2.4% |
| [kem-20](../kem-20/perf_x86_1.md) | MAMBA-Frost | `MAMBA-Frost-CC-128` | 38.45 M | 2.2% | 43.00 M | 3.2% | 43.36 M | 3.8% |
| [kem-20](../kem-20/perf_x86_1.md) | MAMBA-Frost | `MAMBA-Frost-CC-192` | 111.68 M | 1.3% | 118.93 M | 2.0% | 120.02 M | 2.4% |
| [kem-20](../kem-20/perf_x86_1.md) | MAMBA-Frost | `MAMBA-Frost-CC-256` | 241.47 M | 1.3% | 255.32 M | 1.7% | 258.07 M | 2.0% |
| [kem-20](../kem-20/perf_x86_1.md) | MAMBA-Frost | `MAMBA-Frost-CC-384` | 541.61 M | 1.3% | 571.29 M | 1.4% | 572.50 M | 1.5% |
| [kem-20](../kem-20/perf_x86_1.md) | MAMBA-Frost | `MAMBA-Frost-CC-512` | 998.62 M | 1.6% | 972.28 M | 1.5% | 973.29 M | 1.5% |
| [kem-21](../kem-21/perf_x86_1.md) | MAMBA-Viper | `MAMBA-Viper-128` | 225.5 k | 46% | 349.4 k | 48% | 422.5 k | 46% |
| [kem-21](../kem-21/perf_x86_1.md) | MAMBA-Viper | `MAMBA-Viper-192` | 479.3 k | 48% | 654.3 k | 47% | 747.5 k | 43% |
| [kem-21](../kem-21/perf_x86_1.md) | MAMBA-Viper | `MAMBA-Viper-256` | 798.2 k | 47% | 1.01 M | 45% | 1.12 M | 42% |
| [kem-21](../kem-21/perf_x86_1.md) | MAMBA-Viper | `MAMBA-Viper-384` | 2.35 M | 47% | 2.70 M | 46% | 2.88 M | 43% |
| [kem-21](../kem-21/perf_x86_1.md) | MAMBA-Viper | `MAMBA-Viper-512` | 3.79 M | 46% | 4.24 M | 45% | 4.45 M | 43% |
| [kem-22](../kem-22/perf_x86_1.md) | Mithril | `Mithril-128` | 340.6 k | 40% | 376.6 k | 38% | 408.2 k | 35% |
| [kem-22](../kem-22/perf_x86_1.md) | Mithril | `Mithril-128-avx2` (AVX2) | 160.4 k | – | 160.5 k | – | 160.3 k | – |
| [kem-22](../kem-22/perf_x86_1.md) | Mithril | `Mithril-256` | 865.5 k | 28% | 994.3 k | 25% | 1.12 M | 23% |
| [kem-22](../kem-22/perf_x86_1.md) | Mithril | `Mithril-256-avx2` (AVX2) | 272.4 k | – | 269.0 k | – | 275.3 k | – |
| [kem-22](../kem-22/perf_x86_1.md) | Mithril | `Mithril-512` | 2.66 M | 20% | 3.16 M | 17% | 3.66 M | 15% |
| [kem-22](../kem-22/perf_x86_1.md) | Mithril | `Mithril-512-avx2` (AVX2) | 560.5 k | – | 576.9 k | – | 610.7 k | – |
| [kem-23](../kem-23/perf_x86_1.md) | Mito | `Mito-1-128` | 12.63 M | 0.3% | 20.92 M | 1.0% | 29.58 M | 1.6% |
| [kem-23](../kem-23/perf_x86_1.md) | Mito | `Mito-1-256` | 38.14 M | 0.1% | 63.41 M | 0.6% | 89.90 M | 1.1% |
| [kem-23](../kem-23/perf_x86_1.md) | Mito | `Mito-1-512` | 234.79 M | 0.0% | 391.13 M | 0.3% | 550.81 M | 0.5% |
| [kem-23](../kem-23/perf_x86_1.md) | Mito | `Mito-1-E-128` | 11.69 M | 0.3% | 19.36 M | 1.0% | 27.35 M | 1.6% |
| [kem-23](../kem-23/perf_x86_1.md) | Mito | `Mito-1-E-256` | 39.69 M | 0.1% | 65.98 M | 0.6% | 93.36 M | 1.0% |
| [kem-23](../kem-23/perf_x86_1.md) | Mito | `Mito-1-E-512` | 224.83 M | 0.0% | 374.52 M | 0.3% | 527.42 M | 0.5% |
| [kem-23](../kem-23/perf_x86_1.md) | Mito | `Mito-2-E-128` | 17.27 M | 0.2% | 24.84 M | 1.1% | 32.99 M | 1.7% |
| [kem-23](../kem-23/perf_x86_1.md) | Mito | `Mito-2-E-256` | 55.07 M | 0.1% | 79.54 M | 0.6% | 105.35 M | 1.0% |
| [kem-23](../kem-23/perf_x86_1.md) | Mito | `Mito-2-E-512` | 346.96 M | 0.0% | 501.43 M | 0.3% | 660.21 M | 0.5% |
| [kem-24](../kem-24/perf_x86_1.md) | MORNING-Scabbard | `scabbard128` | 741.6 k | 70% | 775.8 k | 69% | 779.7 k | 67% |
| [kem-24](../kem-24/perf_x86_1.md) | MORNING-Scabbard | `scabbard256` | 1.72 M | 53% | 1.84 M | 52% | 1.89 M | 49% |
| [kem-24](../kem-24/perf_x86_1.md) | MORNING-Scabbard | `scabbard512` | 5.12 M | 51% | 5.57 M | 49% | 5.77 M | 45% |
| [kem-25](../kem-25/perf_x86_1.md) | NEV | `NEV_512_769_C_ICCS` | 95.3 k | 35% | 70.2 k | 39% | 85.0 k | 16% |
| [kem-25](../kem-25/perf_x86_1.md) | NEV | `NEV_512_769_ICCS` | 94.8 k | 34% | 80.0 k | 43% | 85.9 k | 24% |
| [kem-25](../kem-25/perf_x86_1.md) | NEV | `NEV_512_1409_ICCS` | 126.8 k | 42% | 95.2 k | 54% | 95.1 k | 39% |
| [kem-25](../kem-25/perf_x86_1.md) | NEV | `NEV_512_3329_ICCS` | 166.9 k | 61% | 152.8 k | 67% | 149.8 k | 56% |
| [kem-25](../kem-25/perf_x86_1.md) | NEV | `NEV_1024_769_C_ICCS` | 205.1 k | 29% | 149.2 k | 41% | 188.8 k | 18% |
| [kem-25](../kem-25/perf_x86_1.md) | NEV | `NEV_1024_769_ICCS` | 206.1 k | 28% | 165.7 k | 44% | 186.6 k | 25% |
| [kem-25](../kem-25/perf_x86_1.md) | NEV | `NEV_1024_1409_ICCS` | 253.5 k | 32% | 173.8 k | 51% | 188.2 k | 31% |
| [kem-25](../kem-25/perf_x86_1.md) | NEV | `NEV_1024_3329_ICCS` | 263.4 k | 49% | 227.5 k | 61% | 229.3 k | 46% |
| [kem-25](../kem-25/perf_x86_1.md) | NEV | `NEV_2048_769_C_ICCS` | 620.7 k | 43% | 364.5 k | 52% | 401.2 k | 19% |
| [kem-25](../kem-25/perf_x86_1.md) | NEV | `NEV_2048_769_ICCS` | 622.6 k | 43% | 409.9 k | 56% | 413.3 k | 28% |
| [kem-25](../kem-25/perf_x86_1.md) | NEV | `NEV_2048_1409_ICCS` | 672.5 k | 32% | 481.8 k | 59% | 466.8 k | 34% |
| [kem-25](../kem-25/perf_x86_1.md) | NEV | `NEV_2048_3329_ICCS` | 720.2 k | 53% | 575.6 k | 69% | 525.9 k | 49% |
| [kem-26](../kem-26/perf_x86_1.md) | NSS-HQC | `HQC-128` | 36.60 M | 0.0% | 64.37 M | 0.0% | 128.53 M | 0.0% |
| [kem-26](../kem-26/perf_x86_1.md) | NSS-HQC | `HQC-256` | 108.08 M | 0.0% | 194.06 M | 0.0% | 343.84 M | 0.0% |
| [kem-26](../kem-26/perf_x86_1.md) | NSS-HQC | `HQC-384` | 366.16 M | 0.0% | 661.21 M | 0.0% | 1.09 G | 0.0% |
| [kem-26](../kem-26/perf_x86_1.md) | NSS-HQC | `HQC-512` | 868.07 M | 0.0% | 1.58 G | 0.0% | 2.53 G | 0.0% |
| [kem-27](../kem-27/perf_x86_1.md) | NTRE Key Encapsulation Mechanism | `NTRE-128` | 142.3 k | 28% | 113.7 k | 49% | 113.2 k | 30% |
| [kem-27](../kem-27/perf_x86_1.md) | NTRE Key Encapsulation Mechanism | `NTRE-256` | 261.1 k | 29% | 220.1 k | 49% | 230.7 k | 28% |
| [kem-27](../kem-27/perf_x86_1.md) | NTRE Key Encapsulation Mechanism | `NTRE-512` | 574.5 k | 22% | 535.8 k | 44% | 541.9 k | 30% |
| [kem-28](../kem-28/perf_x86_1.md) | OAEP-NTRU | `OAEP-NTRU-648` | 179.1 k | 13% | 124.8 k | 52% | 127.9 k | 33% |
| [kem-28](../kem-28/perf_x86_1.md) | OAEP-NTRU | `OAEP-NTRU-1296` | 493.8 k | 23% | 431.5 k | 59% | 339.0 k | 42% |
| [kem-28](../kem-28/perf_x86_1.md) | OAEP-NTRU | `OAEP-NTRU-2592` | 1.19 M | 20% | 1.12 M | 66% | 955.5 k | 53% |
| [kem-29](../kem-29/perf_x86_1.md) | Polar-KEM | `PolarKEM-128` | 166.5 k | 94% | 532.3 k | 91% | 1.04 M | 95% |
| [kem-29](../kem-29/perf_x86_1.md) | Polar-KEM | `PolarKEM-256` | 325.7 k | 97% | 678.8 k | 88% | 1.32 M | 92% |
| [kem-29](../kem-29/perf_x86_1.md) | Polar-KEM | `PolarKEM-512` | 644.7 k | 98% | 1.33 M | 88% | 2.61 M | 93% |
| [kem-30](../kem-30/perf_x86_1.md) | PolarLAC | `POLARLAC-128` | 160.5 k | 64% | 209.2 k | 68% | 252.7 k | 62% |
| [kem-30](../kem-30/perf_x86_1.md) | PolarLAC | `POLARLAC-256` | 285.9 k | 61% | 398.5 k | 65% | 496.0 k | 58% |
| [kem-30](../kem-30/perf_x86_1.md) | PolarLAC | `POLARLAC-512` | 980.5 k | 72% | 1.32 M | 73% | 1.60 M | 67% |
| [kem-30](../kem-30/perf_x86_1.md) | PolarLAC | `POLARLAC-512-Star` | 1.07 M | 65% | 1.42 M | 68% | 1.70 M | 64% |
| [kem-30](../kem-30/perf_x86_1.md) | PolarLAC | `POLARLAC-Light` | 149.0 k | 61% | 195.5 k | 66% | 237.9 k | 60% |
| [kem-31](../kem-31/perf_x86_1.md) | QIMEN-PIKE | `NGCC-1` | 391.07 M | 0.0% | 129.56 M | 0.0% | 200.66 M | 0.0% |
| [kem-31](../kem-31/perf_x86_1.md) | QIMEN-PIKE | `NGCC-2` | 1.28 G | 0.0% | 409.71 M | 0.0% | 638.67 M | 0.0% |
| [kem-31](../kem-31/perf_x86_1.md) | QIMEN-PIKE | `NGCC-3` | 8.51 G | 0.0% | 3.13 G | 0.0% | 4.79 G | 0.0% |
| [kem-32](../kem-32/perf_x86_1.md) | Quasi-Cyclic Twisted McEliece Key Encapsulation Mechanism | `QCTM128` | 53.85 G (n=65) | 0.0% | 18.43 M | 0.0% | 5.90 G | 0.0% |
| [kem-32](../kem-32/perf_x86_1.md) | Quasi-Cyclic Twisted McEliece Key Encapsulation Mechanism | `QCTM256` | 132.38 G (n=10) | 0.0% | 53.10 M | 0.0% | 29.11 G (n=60) | 0.0% |
| [kem-32](../kem-32/perf_x86_1.md) | Quasi-Cyclic Twisted McEliece Key Encapsulation Mechanism | `QCTM512` | 793.78 G (n=2) | 0.0% | 211.05 M | 0.0% | 204.27 G (n=5) | 0.0% |
| [kem-33](../kem-33/perf_x86_1.md) | QUBE | `qube-128` ⚠ KAT MISMATCH | 616.9 k | 55% | 657.8 k | 62% | 1.18 M | 49% |
| [kem-33](../kem-33/perf_x86_1.md) | QUBE | `qube-192` ⚠ KAT NOKAT | 1.41 M | 49% | 1.48 M | 56% | 2.83 M | 41% |
| [kem-33](../kem-33/perf_x86_1.md) | QUBE | `qube-256` ⚠ KAT MISMATCH | 2.89 M | 47% | 2.92 M | 53% | 5.95 M | 35% |
| [kem-33](../kem-33/perf_x86_1.md) | QUBE | `qube-384` ⚠ KAT MISMATCH | 7.21 M | 38% | 7.17 M | 48% | 13.37 M | 40% |
| [kem-33](../kem-33/perf_x86_1.md) | QUBE | `qube-512` ⚠ KAT MISMATCH | 19.03 M | 51% | 18.67 M | 60% | 29.26 M | 49% |
| [kem-34](../kem-34/perf_x86_1.md) | Rudraksh2 | `lwekem128` | 3.19 M | 92% | 3.13 M | 93% | 3.17 M | 91% |
| [kem-34](../kem-34/perf_x86_1.md) | Rudraksh2 | `lwekem256` | 6.31 M | 92% | 6.25 M | 93% | 6.33 M | 92% |
| [kem-34](../kem-34/perf_x86_1.md) | Rudraksh2 | `lwekem512` | 19.96 M | 96% | 19.99 M | 96% | 20.15 M | 95% |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | `Scloudplus-128-AES-packed10` | 41.90 M | 0.0% | 42.02 M | 0.0% | 42.02 M | 0.0% |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | `Scloudplus-128-SHAKE-avx2` (AVX2) | 1.68 M | – | 1.73 M | – | 1.64 M | – |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | `Scloudplus-128-SHAKE-packed10` | 6.31 M | 0.0% | 6.43 M | 0.0% | 6.44 M | 0.0% |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | `Scloudplus-128-SM3-packed10` | 23.68 M | 92% | 23.93 M | 92% | 23.78 M | 92% |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | `Scloudplus-192-AES-packed10` | 77.94 M | 0.0% | 78.49 M | 0.0% | 78.61 M | 0.0% |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | `Scloudplus-192-SHAKE-packed10` | 10.50 M | 0.0% | 11.04 M | 0.0% | 11.28 M | 0.0% |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | `Scloudplus-192-SM3-packed10` | 44.44 M | 93% | 45.14 M | 92% | 45.03 M | 91% |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | `Scloudplus-256-AES-packed10` | 158.93 M | 0.0% | 159.85 M | 0.0% | 159.98 M | 0.0% |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | `Scloudplus-256-SHAKE-packed10` | 23.56 M | 0.0% | 24.61 M | 0.0% | 24.83 M | 0.0% |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | `Scloudplus-256-SM3-packed10` | 90.93 M | 91% | 92.25 M | 91% | 92.03 M | 90% |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | `Scloudplus-384-AES-packed10` | 315.05 M | 0.0% | 316.43 M | 0.0% | 317.13 M | 0.0% |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | `Scloudplus-384-SHAKE-packed10` | 46.78 M | 0.0% | 48.27 M | 0.0% | 49.53 M | 0.0% |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | `Scloudplus-384-SM3-packed10` | 179.31 M | 90% | 182.22 M | 90% | 181.76 M | 89% |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | `Scloudplus-512-AES-packed10` | 656.92 M | 0.0% | 657.55 M | 0.0% | 658.67 M | 0.0% |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | `Scloudplus-512-SHAKE-packed10` | 99.62 M | 0.0% | 101.20 M | 0.0% | 102.35 M | 0.0% |
| [kem-35](../kem-35/perf_x86_1.md) | Scloud+ | `Scloudplus-512-SM3-packed10` | 376.23 M | 89% | 379.05 M | 89% | 377.95 M | 89% |
| [kem-36](../kem-36/perf_x86_1.md) | TRIKE | `TRIKE-2` | 101.46 M | 0.0% | 9.36 M | 4.7% | 51.33 M | 0.8% |
| [kem-36](../kem-36/perf_x86_1.md) | TRIKE | `TRIKE-5` | 740.74 M | 0.0% | 69.36 M | 1.4% | 203.28 M | 0.5% |
| [kem-36](../kem-36/perf_x86_1.md) | TRIKE | `TRIKE-7` | 2.41 G | 0.0% | 203.56 M | 0.9% | 598.79 M | 0.3% |
| [kem-36](../kem-36/perf_x86_1.md) | TRIKE | `TRIKE-9` | 3.04 G | 0.0% | 206.80 M | 1.5% | 1.17 G | 0.3% |
| [kem-37](../kem-37/perf_x86_1.md) | TriQ-KEM | `TriQ-KEM-128` | 3.92 M | 12% | 7.41 M | 6.1% | 11.21 M | 4.6% |
| [kem-37](../kem-37/perf_x86_1.md) | TriQ-KEM | `TriQ-KEM-256` | 21.48 M | 4.1% | 42.49 M | 2.9% | 63.63 M | 2.3% |
| [kem-37](../kem-37/perf_x86_1.md) | TriQ-KEM | `TriQ-KEM-384` | 57.31 M | 2.9% | 113.81 M | 2.0% | 171.18 M | 1.9% |
| [kem-37](../kem-37/perf_x86_1.md) | TriQ-KEM | `TriQ-KEM-512` | 122.30 M | 3.7% | 242.32 M | 2.6% | 362.24 M | 2.2% |
| [kem-38](../kem-38/perf_x86_1.md) | UVW Key Encapsulation Mechanism | `UVW-KEM-128` | 627.34 M | 0.0% | 987.6 k | 14% | 1.36 G | 0.0% |
| [kem-38](../kem-38/perf_x86_1.md) | UVW Key Encapsulation Mechanism | `UVW-KEM-256` | 4.82 G | 0.0% | 2.88 M | 9.5% | 9.76 G | 0.0% |
| [kem-38](../kem-38/perf_x86_1.md) | UVW Key Encapsulation Mechanism | `UVW-KEM-512` | 37.96 G (n=45) | 0.0% | 18.93 M | 3.9% | 62.33 G (n=30) | 0.0% |
| [kem-39](../kem-39/perf_x86_1.md) | Weaver | `WeaverKEM-128` | 545.1 k | 82% | 585.8 k | 81% | 610.9 k | 78% |
| [kem-39](../kem-39/perf_x86_1.md) | Weaver | `WeaverKEM-256` | 845.7 k | 76% | 952.3 k | 71% | 956.1 k | 68% |
| [kem-39](../kem-39/perf_x86_1.md) | Weaver | `WeaverKEM-512` | 2.74 M | 82% | 3.18 M | 77% | 3.23 M | 76% |
| [kem-40](../kem-40/perf_x86_1.md) | YuanYang.KEM | `yuanyang-512` | 505.6 k | 8.1% | 288.3 k | 42% | 433.4 k | 21% |
| [kem-40](../kem-40/perf_x86_1.md) | YuanYang.KEM | `yuanyang-1024` | 1.07 M | 7.2% | 495.2 k | 38% | 808.6 k | 15% |
| [kem-40](../kem-40/perf_x86_1.md) | YuanYang.KEM | `yuanyang-2048` | 2.06 M | 7.5% | 991.5 k | 34% | 1.68 M | 12% |
| [kem-41](../kem-41/perf_x86_1.md) | ZEN | `ZEN_128` | 222.8 k | 29% | 143.8 k | 67% | 191.9 k | 49% |
| [kem-41](../kem-41/perf_x86_1.md) | ZEN | `ZEN_256` | 391.5 k | 36% | 200.6 k | 47% | 327.4 k | 28% |
| [kem-41](../kem-41/perf_x86_1.md) | ZEN | `ZEN_512` | 970.2 k | 46% | 501.9 k | 57% | 788.0 k | 34% |

## Digital signatures

| id | algorithm | instance | keygen | sym % | sign | sym % | verify | sym % |
|---|---|---|---|---|---|---|---|---|
| [sign-01](../sign-01/perf_x86_1.md) | Aigis-Sig+ | `Aigis-sig1` | 610.8 k | 7.4% | 10.50 M | 64% | 531.0 k | 11% |
| [sign-01](../sign-01/perf_x86_1.md) | Aigis-Sig+ | `Aigis-sig2` | 1.91 M | 4.4% | 7.97 M | 55% | 1.79 M | 5.7% |
| [sign-01](../sign-01/perf_x86_1.md) | Aigis-Sig+ | `Aigis-sig3` | 6.37 M | 5.0% | 8.89 M | 28% | 6.22 M | 5.9% |
| [sign-02](../sign-02/perf_x86_1.md) | BIT: Bimodal Triangular distribution based lattice signatures | `BiT-128` | 460.7 k | 74% | 2.25 M | 58% | 443.8 k | 72% |
| [sign-02](../sign-02/perf_x86_1.md) | BIT: Bimodal Triangular distribution based lattice signatures | `BiT-128-avx2` (AVX2) | 383.4 k | – | 1.60 M | – | 340.5 k | – |
| [sign-02](../sign-02/perf_x86_1.md) | BIT: Bimodal Triangular distribution based lattice signatures | `BiT-256` | 1.24 M | 81% | 2.71 M | 65% | 1.28 M | 79% |
| [sign-02](../sign-02/perf_x86_1.md) | BIT: Bimodal Triangular distribution based lattice signatures | `BiT-256-avx2` (AVX2) | 1.07 M | – | 2.12 M | – | 1.07 M | – |
| [sign-02](../sign-02/perf_x86_1.md) | BIT: Bimodal Triangular distribution based lattice signatures | `BiT-512` | 3.59 M | 88% | 10.97 M | 70% | 3.54 M | 85% |
| [sign-02](../sign-02/perf_x86_1.md) | BIT: Bimodal Triangular distribution based lattice signatures | `BiT-512-avx2` (AVX2) | 3.28 M | – | 9.37 M | – | 3.16 M | – |
| [sign-03](../sign-03/perf_x86_1.md) | CEDRUS+C | `CEDRUSC-160f` | 14.36 M | 98% | 513.49 M | 98% | 15.34 M | 98% |
| [sign-03](../sign-03/perf_x86_1.md) | CEDRUS+C | `CEDRUSC-160s` | 583.25 M | 98% | 8.65 G | 98% | 20.99 M | 98% |
| [sign-03](../sign-03/perf_x86_1.md) | CEDRUS+C | `CEDRUSC-256f` | 46.43 M | 98% | 1.24 G | 98% | 21.30 M | 98% |
| [sign-03](../sign-03/perf_x86_1.md) | CEDRUS+C | `CEDRUSC-256s` | 964.78 M | 98% | 12.74 G | 98% | 35.11 M | 98% |
| [sign-03](../sign-03/perf_x86_1.md) | CEDRUS+C | `CEDRUSC-384f` | 656.21 M | 99% | 12.48 G | 99% | 125.86 M | 99% |
| [sign-03](../sign-03/perf_x86_1.md) | CEDRUS+C | `CEDRUSC-384s` | 3.27 G | 99% | 48.20 G (n=35) | 99% | 53.33 M | 99% |
| [sign-03](../sign-03/perf_x86_1.md) | CEDRUS+C | `CEDRUSC-512f` | 1.76 G | 99% | 24.73 G (n=75) | 99% | 157.20 M | 99% |
| [sign-03](../sign-03/perf_x86_1.md) | CEDRUS+C | `CEDRUSC-512s` | 7.00 G | 99% | 86.78 G (n=20) | 99% | 115.31 M | 99% |
| [sign-04](../sign-04/perf_x86_1.md) | CEDRUSɑ | `CEDRUSALPHA-160f` | 16.05 M | 98% | 570.59 M | 98% | 17.73 M | 98% |
| [sign-04](../sign-04/perf_x86_1.md) | CEDRUSɑ | `CEDRUSALPHA-160s` | 523.56 M | 98% | 7.78 G | 98% | 19.14 M | 98% |
| [sign-04](../sign-04/perf_x86_1.md) | CEDRUSɑ | `CEDRUSALPHA-256f` | 52.40 M | 98% | 1.35 G | 98% | 24.20 M | 97% |
| [sign-04](../sign-04/perf_x86_1.md) | CEDRUSɑ | `CEDRUSALPHA-256s` | 793.87 M | 98% | 12.06 G | 98% | 29.24 M | 98% |
| [sign-04](../sign-04/perf_x86_1.md) | CEDRUSɑ | `CEDRUSALPHA-384f` | 637.31 M | 99% | 12.46 G | 99% | 123.74 M | 99% |
| [sign-04](../sign-04/perf_x86_1.md) | CEDRUSɑ | `CEDRUSALPHA-384s` | 4.10 G | 99% | 44.24 G (n=40) | 99% | 68.37 M | 99% |
| [sign-04](../sign-04/perf_x86_1.md) | CEDRUSɑ | `CEDRUSALPHA-512f` | 1.60 G | 99% | 21.00 G (n=85) | 99% | 145.58 M | 99% |
| [sign-04](../sign-04/perf_x86_1.md) | CEDRUSɑ | `CEDRUSALPHA-512s` | 7.68 G | 99% | 88.57 G (n=20) | 99% | 128.14 M | 99% |
| [sign-05](../sign-05/perf_x86_1.md) | Chinith | `sm4th_d3_128f_loose` | 12.0 k | 0.0% | 125.86 M | 2.7% | 83.72 M | 3.0% |
| [sign-05](../sign-05/perf_x86_1.md) | Chinith | `sm4th_d3_128f_tight` | 11.9 k | 0.0% | 194.81 M | 5.9% | 120.51 M | 8.3% |
| [sign-05](../sign-05/perf_x86_1.md) | Chinith | `sm4th_d3_128s_loose` | 12.0 k | 0.0% | 354.25 M | 11% | 296.38 M | 5.3% |
| [sign-05](../sign-05/perf_x86_1.md) | Chinith | `sm4th_d3_128s_tight` | 11.9 k | 0.0% | 422.51 M | 21% | 338.39 M | 22% |
| [sign-05](../sign-05/perf_x86_1.md) | Chinith | `sm4th_em_d2_128f_loose` | 11.9 k | 0.0% | 29.92 M | 11% | 28.37 M | 8.4% |
| [sign-05](../sign-05/perf_x86_1.md) | Chinith | `sm4th_em_d2_128f_tight` | 11.9 k | 0.0% | 34.15 M | 31% | 32.63 M | 30% |
| [sign-05](../sign-05/perf_x86_1.md) | Chinith | `sm4th_em_d2_128s_loose` | 11.9 k | 0.0% | 196.83 M | 14% | 186.07 M | 8.3% |
| [sign-05](../sign-05/perf_x86_1.md) | Chinith | `sm4th_em_d2_128s_tight` | 11.9 k | 0.0% | 232.02 M | 36% | 220.22 M | 34% |
| [sign-05](../sign-05/perf_x86_1.md) | Chinith | `ublockith_d3_256f` | 14.6 k | 0.0% | 351.34 M | 6.7% | 407.09 M | 5.7% |
| [sign-05](../sign-05/perf_x86_1.md) | Chinith | `ublockith_d3_256s` | 14.6 k | 0.0% | 1.08 G | 16% | 1.14 G | 15% |
| [sign-05](../sign-05/perf_x86_1.md) | Chinith | `ublockith_em_d3_256f` | 14.7 k | 0.0% | 267.51 M | 8.8% | 310.14 M | 7.2% |
| [sign-05](../sign-05/perf_x86_1.md) | Chinith | `ublockith_em_d3_256s` | 14.7 k | 0.0% | 897.43 M | 21% | 923.48 M | 18% |
| [sign-05](../sign-05/perf_x86_1.md) | Chinith | `vistrutith_d3_512f` | 15.9 k | 0.0% | 6.37 G | 1.7% | 5.27 G | 2.0% |
| [sign-05](../sign-05/perf_x86_1.md) | Chinith | `vistrutith_d3_512s` | 15.9 k | 0.0% | 11.79 G | 6.6% | 10.70 G | 7.2% |
| [sign-06](../sign-06/perf_x86_1.md) | COMPASS-SIG | `COMPASS-SIG-128` | 1.41 M | 93% | 1.81 M | 88% | 1.37 M | 93% |
| [sign-06](../sign-06/perf_x86_1.md) | COMPASS-SIG | `COMPASS-SIG-256` | 5.22 M | 95% | 6.81 M | 89% | 5.10 M | 95% |
| [sign-06](../sign-06/perf_x86_1.md) | COMPASS-SIG | `COMPASS-SIG-384` | 3.87 M | 90% | 5.58 M | 77% | 3.51 M | 88% |
| [sign-06](../sign-06/perf_x86_1.md) | COMPASS-SIG | `COMPASS-SIG-512` | 5.97 M | 91% | 8.24 M | 79% | 5.54 M | 90% |
| [sign-07](../sign-07/perf_x86_1.md) | CS | `CS-128` | 546.7 k | 4.7% | 4.42 M | 56% | 593.9 k | 6.3% |
| [sign-07](../sign-07/perf_x86_1.md) | CS | `CS-256` | 896.1 k | 10% | 13.25 M | 49% | 1.13 M | 11% |
| [sign-07](../sign-07/perf_x86_1.md) | CS | `CS-512` | 2.88 M | 14% | 52.45 M | 62% | 3.62 M | 16% |
| [sign-08](../sign-08/perf_x86_1.md) | DARTS | `DARTS128` | 953.3 k | 46% | 45.51 M | 88% | 353.5 k | 64% |
| [sign-08](../sign-08/perf_x86_1.md) | DARTS | `DARTS256` | 1.24 M | 64% | 33.85 M | 87% | 875.1 k | 72% |
| [sign-08](../sign-08/perf_x86_1.md) | DARTS | `DARTS512` | 2.08 M | 62% | 10.74 M | 87% | 1.64 M | 77% |
| [sign-09](../sign-09/perf_x86_1.md) | DOVE | `dove_classic_128` | 101.87 M | 19% | 4.72 M | 0.4% | 4.36 M | 0.1% |
| [sign-09](../sign-09/perf_x86_1.md) | DOVE | `dove_classic_256` | 2.16 G | 10% | 49.56 M | 0.1% | 43.98 M | 0.0% |
| [sign-09](../sign-09/perf_x86_1.md) | DOVE | `dove_classic_512` | 48.53 G (n=35) | 5.0% | 529.87 M | 0.0% | 478.61 M | 0.0% |
| [sign-09](../sign-09/perf_x86_1.md) | DOVE | `dove_pkc_skc_128` | 89.58 M | 7.8% | 27.89 M | 25% | 11.21 M | 61% |
| [sign-09](../sign-09/perf_x86_1.md) | DOVE | `dove_pkc_skc_256` | 2.02 G | 3.7% | 409.22 M | 18% | 118.08 M | 63% |
| [sign-09](../sign-09/perf_x86_1.md) | DOVE | `dove_pkc_skc_512` | 46.96 G (n=35) | 1.8% | 6.12 G | 14% | 1.30 G | 63% |
| [sign-10](../sign-10/perf_x86_1.md) | Facto-DSA | `Facto-DSA-128` | 7.34 M | 11% | 2.10 M | 0.5% | 983.9 k | 87% |
| [sign-10](../sign-10/perf_x86_1.md) | Facto-DSA | `Facto-DSA-256` | 107.58 M | 9.2% | 11.72 M | 0.1% | 11.19 M | 87% |
| [sign-10](../sign-10/perf_x86_1.md) | Facto-DSA | `Facto-DSA-512` ⚠ KAT NOKAT | 2.24 G | 5.5% | 124.35 M | 0.0% | 140.34 M | 88% |
| [sign-11](../sign-11/perf_x86_1.md) | FlexTree | `Flextree-160f` | 14.52 M | 98% | 563.57 M | 92% | 15.46 M | 98% |
| [sign-11](../sign-11/perf_x86_1.md) | FlexTree | `Flextree-160s` | 593.29 M | 98% | 8.29 G | 98% | 21.34 M | 98% |
| [sign-11](../sign-11/perf_x86_1.md) | FlexTree | `Flextree-256f` | 46.80 M | 98% | 975.63 M | 98% | 25.49 M | 98% |
| [sign-11](../sign-11/perf_x86_1.md) | FlexTree | `Flextree-256s` | 488.82 M | 98% | 9.24 G | 98% | 39.41 M | 98% |
| [sign-11](../sign-11/perf_x86_1.md) | FlexTree | `Flextree-384f` | 652.08 M | 99% | 12.33 G | 99% | 125.64 M | 99% |
| [sign-11](../sign-11/perf_x86_1.md) | FlexTree | `Flextree-384s` | 3.27 G | 99% | 44.66 G (n=40) | 99% | 53.95 M | 98% |
| [sign-11](../sign-11/perf_x86_1.md) | FlexTree | `Flextree-512f` | 1.76 G | 99% | 24.80 G (n=75) | 99% | 158.24 M | 98% |
| [sign-11](../sign-11/perf_x86_1.md) | FlexTree | `Flextree-512s` | 6.99 G | 99% | 84.54 G (n=20) | 99% | 117.82 M | 97% |
| [sign-12](../sign-12/perf_x86_1.md) | Galas Signature Scheme | `Galas-160F` ⚠ KAT MISMATCH | 22.14 M | 0.0% | 1.88 G | 4.1% | 1.20 G | 6.3% |
| [sign-12](../sign-12/perf_x86_1.md) | Galas Signature Scheme | `Galas-160S` ⚠ KAT MISMATCH | 22.13 M | 0.0% | 2.39 G | 23% | 1.68 G | 30% |
| [sign-12](../sign-12/perf_x86_1.md) | Galas Signature Scheme | `Galas-256F` ⚠ KAT MISMATCH | 57.79 M | 0.0% | 7.73 G | 3.1% | 4.89 G | 4.7% |
| [sign-12](../sign-12/perf_x86_1.md) | Galas Signature Scheme | `Galas-256S` ⚠ KAT MISMATCH | 57.82 M | 0.0% | 12.12 G | 33% | 9.06 G | 46% |
| [sign-12](../sign-12/perf_x86_1.md) | Galas Signature Scheme | `Galas-384F` ⚠ KAT MISMATCH | 136.91 M | 0.0% | 29.61 G (n=60) | 2.8% | 17.90 G | 4.9% |
| [sign-12](../sign-12/perf_x86_1.md) | Galas Signature Scheme | `Galas-384S` ⚠ KAT MISMATCH | 137.02 M | 0.0% | 38.44 G (n=50) | 23% | 26.58 G (n=70) | 34% |
| [sign-12](../sign-12/perf_x86_1.md) | Galas Signature Scheme | `Galas-512F` ⚠ KAT MISMATCH | 254.11 M | 0.0% | 75.51 G (n=25) | 2.0% | 44.76 G (n=40) | 3.5% |
| [sign-12](../sign-12/perf_x86_1.md) | Galas Signature Scheme | `Galas-512S` ⚠ KAT TIMEOUT | 254.15 M | 0.0% | 92.54 G (n=20) | 18% | 61.40 G (n=30) | 28% |
| [sign-13](../sign-13/perf_x86_1.md) | GreatWall Signature Algorithm | `GreatWall128f` | 5.88 M | 0.0% | 137.40 M | 0.0% | 101.83 M | 0.0% |
| [sign-13](../sign-13/perf_x86_1.md) | GreatWall Signature Algorithm | `GreatWall128s` | 5.89 M | 0.0% | 632.05 M | 0.0% | 538.77 M | 0.0% |
| [sign-13](../sign-13/perf_x86_1.md) | GreatWall Signature Algorithm | `GreatWall192f` | 13.49 M | 0.0% | 450.19 M | 0.0% | 311.50 M | 0.0% |
| [sign-13](../sign-13/perf_x86_1.md) | GreatWall Signature Algorithm | `GreatWall192s` | 13.54 M | 0.0% | 1.95 G | 0.0% | 1.81 G | 0.0% |
| [sign-13](../sign-13/perf_x86_1.md) | GreatWall Signature Algorithm | `GreatWall256f` | 27.35 M | 0.0% | 1.04 G | 0.0% | 699.87 M | 0.0% |
| [sign-13](../sign-13/perf_x86_1.md) | GreatWall Signature Algorithm | `GreatWall256s` | 27.36 M | 0.0% | 3.65 G | 0.0% | 3.30 G | 0.0% |
| [sign-13](../sign-13/perf_x86_1.md) | GreatWall Signature Algorithm | `GreatWall512f` | 121.94 M | 0.0% | 9.92 G | 0.0% | 5.91 G | 0.0% |
| [sign-13](../sign-13/perf_x86_1.md) | GreatWall Signature Algorithm | `GreatWall512s` | 121.91 M | 0.0% | 24.65 G (n=75) | 0.0% | 20.69 G (n=90) | 0.0% |
| [sign-14](../sign-14/perf_x86_1.md) | Lynxer | `Lynxer-160f` | 28.80 M | 80% | 533.63 M | 14% | 470.80 M | 6.2% |
| [sign-14](../sign-14/perf_x86_1.md) | Lynxer | `Lynxer-160s` | 28.78 M | 80% | 3.82 G | 3.4% | 3.73 G | 1.9% |
| [sign-14](../sign-14/perf_x86_1.md) | Lynxer | `Lynxer-256f` | 174.01 M | 99% | 1.55 G | 35% | 1.18 G | 16% |
| [sign-14](../sign-14/perf_x86_1.md) | Lynxer | `Lynxer-256s` | 174.00 M | 99% | 10.78 G | 6.3% | 10.37 G | 3.0% |
| [sign-14](../sign-14/perf_x86_1.md) | Lynxer | `Lynxer-384f` | 741.32 M | 99% | 5.16 G | 44% | 3.64 G | 22% |
| [sign-14](../sign-14/perf_x86_1.md) | Lynxer | `Lynxer-384s` | 740.93 M | 99% | 30.11 G (n=60) | 10% | 28.34 G (n=65) | 4.1% |
| [sign-14](../sign-14/perf_x86_1.md) | Lynxer | `Lynxer-512f` | 2.15 G | 99% | 6.77 G | 96% | 2.48 G | 91% |
| [sign-14](../sign-14/perf_x86_1.md) | Lynxer | `Lynxer-512s` | 2.15 G | 99% | 9.33 G | 83% | 4.74 G | 67% |
| [sign-15](../sign-15/perf_x86_1.md) | MORNING-ATLAS | `lwrdsa128` ⚠ KAT OVERFLOW | 2.78 M | 83% | 3.89 M | 70% | 2.88 M | 81% |
| [sign-15](../sign-15/perf_x86_1.md) | MORNING-ATLAS | `lwrdsa192` ⚠ KAT OVERFLOW | 6.61 M | 83% | 8.80 M | 71% | 6.81 M | 82% |
| [sign-15](../sign-15/perf_x86_1.md) | MORNING-ATLAS | `lwrdsa256` ⚠ KAT OVERFLOW | 4.23 M | 61% | 12.39 M | 35% | 4.44 M | 58% |
| [sign-15](../sign-15/perf_x86_1.md) | MORNING-ATLAS | `lwrdsa512` ⚠ KAT OVERFLOW | 12.34 M | 58% | 43.40 M | 46% | 12.96 M | 55% |
| [sign-16](../sign-16/perf_x86_1.md) | Octarine | `Octarine-128` | 767.9 k | 60% | 2.09 M | 52% | 879.7 k | 51% |
| [sign-16](../sign-16/perf_x86_1.md) | Octarine | `Octarine-256` | 1.48 M | 57% | 4.58 M | 53% | 1.71 M | 50% |
| [sign-16](../sign-16/perf_x86_1.md) | Octarine | `Octarine-512` | 3.79 M | 53% | 17.20 M | 55% | 4.35 M | 47% |
| [sign-17](../sign-17/perf_x86_1.md) | OPS Digital Signature Algorithm | `OPSsig-128` | 2.31 M | 91% | 2.63 M | 89% | 2.16 M | 86% |
| [sign-17](../sign-17/perf_x86_1.md) | OPS Digital Signature Algorithm | `OPSsig-256` | 3.90 M | 92% | 5.14 M | 88% | 3.64 M | 89% |
| [sign-17](../sign-17/perf_x86_1.md) | OPS Digital Signature Algorithm | `OPSsig-512` | 7.56 M | 92% | 10.68 M | 87% | 7.14 M | 89% |
| [sign-18](../sign-18/perf_x86_1.md) | Origami | `Origami-128` | 2.53 M | 98% | 405.85 M | 91% | 25.87 M | 83% |
| [sign-18](../sign-18/perf_x86_1.md) | Origami | `Origami-256` | 88.77 M | 100% | 1.51 G | 81% | 1.38 G | 82% |
| [sign-18](../sign-18/perf_x86_1.md) | Origami | `Origami-384` | 306.15 M | 100% | 19.85 G (n=25) | 81% | 6.48 G | 81% |
| [sign-18](../sign-18/perf_x86_1.md) | Origami | `Origami-512` | 499.54 M | 100% | 13.08 G | 79% | 11.92 G | 81% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SHAKE-128f` | 9.77 M | 0.0% | 186.43 M | 0.0% | 4.99 M | 0.0% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SHAKE-128s` | 307.13 M | 0.0% | 3.27 G | 0.0% | 12.11 M | 0.0% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SHAKE-192f` | 14.64 M | 0.0% | 290.69 M | 0.0% | 7.53 M | 0.0% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SHAKE-192s` | 538.45 M | 0.0% | 5.59 G | 0.0% | 19.20 M | 0.0% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SHAKE-256f` | 29.75 M | 0.0% | 576.55 M | 0.0% | 14.99 M | 0.0% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SHAKE-256s` | 387.92 M | 0.0% | 5.15 G | 0.0% | 33.58 M | 0.0% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SHAKE-384f` | 65.91 M | 0.0% | 2.05 G | 0.0% | 36.17 M | 0.0% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SHAKE-384s` | 651.57 M | 0.0% | 9.03 G | 0.0% | 57.15 M | 0.0% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SHAKE-512f` | 231.73 M | 0.0% | 5.34 G | 0.0% | 123.82 M | 0.0% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SHAKE-512s` | 2.41 G | 0.0% | 22.26 G (n=80) | 0.0% | 39.06 M | 0.0% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SM3-128f` ⚠ KAT MISMATCH | 10.80 M | 0.0% | 219.91 M | 4.1% | 6.08 M | 1.3% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SM3-128s` ⚠ KAT MISMATCH | 343.22 M | 0.0% | 3.90 G | 5.3% | 13.88 M | 0.5% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SM3-192f` ⚠ KAT MISMATCH | 29.84 M | 0.0% | 587.62 M | 0.3% | 15.70 M | 0.7% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SM3-192s` ⚠ KAT MISMATCH | 1.11 G | 0.0% | 11.52 G | 0.9% | 39.76 M | 0.2% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SM3-256f` ⚠ KAT MISMATCH | 59.14 M | 0.0% | 1.12 G | 2.0% | 30.04 M | 0.5% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SM3-256s` ⚠ KAT MISMATCH | 777.96 M | 0.0% | 10.54 G | 12% | 67.56 M | 0.2% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SM3-384f` ⚠ KAT MISMATCH | 124.61 M | 0.0% | 3.55 G | 0.0% | 67.63 M | 0.3% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SM3-384s` ⚠ KAT MISMATCH | 1.22 G | 0.0% | 16.64 G | 2.0% | 106.66 M | 0.2% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SM3-512f` ⚠ KAT MISMATCH | 248.00 M | 0.0% | 6.03 G | 4.8% | 133.86 M | 0.2% |
| [sign-19](../sign-19/perf_x86_1.md) | Phoenix | `Phoenix-SM3-512s` ⚠ KAT MISMATCH | 2.58 G | 0.0% | 25.75 G (n=70) | 8.1% | 43.19 M | 0.5% |
| [sign-20](../sign-20/perf_x86_1.md) | Qing Luan | `QingLuan-128` | 272.2 k | 69% | 16.41 M | 62% | 7.15 M | 66% |
| [sign-20](../sign-20/perf_x86_1.md) | Qing Luan | `QingLuan-256` | 1.67 M | 82% | 103.95 M | 72% | 45.53 M | 77% |
| [sign-20](../sign-20/perf_x86_1.md) | Qing Luan | `QingLuan-384` | 3.58 M | 82% | 257.81 M | 72% | 115.85 M | 79% |
| [sign-20](../sign-20/perf_x86_1.md) | Qing Luan | `QingLuan-512` | 8.80 M | 88% | 612.04 M | 77% | 274.42 M | 83% |
| [sign-21](../sign-21/perf_x86_1.md) | ReSolveD-ɑ | `ReSolveD-alpha-160f` | 14.25 M | 34% | 677.96 M | 2.5% | 639.43 M | 1.8% |
| [sign-21](../sign-21/perf_x86_1.md) | ReSolveD-ɑ | `ReSolveD-alpha-160s` | 14.26 M | 34% | 4.66 G | 1.4% | 4.61 G | 1.2% |
| [sign-21](../sign-21/perf_x86_1.md) | ReSolveD-ɑ | `ReSolveD-alpha-256f` | 32.73 M | 39% | 1.39 G | 3.0% | 1.33 G | 2.1% |
| [sign-21](../sign-21/perf_x86_1.md) | ReSolveD-ɑ | `ReSolveD-alpha-256s` | 32.74 M | 39% | 13.08 G | 1.4% | 12.98 G | 1.1% |
| [sign-21](../sign-21/perf_x86_1.md) | ReSolveD-ɑ | `ReSolveD-alpha-384f` | 80.53 M | 36% | 3.77 G | 3.0% | 3.61 G | 2.2% |
| [sign-21](../sign-21/perf_x86_1.md) | ReSolveD-ɑ | `ReSolveD-alpha-384s` | 80.50 M | 36% | 33.60 G (n=55) | 1.7% | 33.31 G (n=55) | 1.4% |
| [sign-21](../sign-21/perf_x86_1.md) | ReSolveD-ɑ | `ReSolveD-alpha-512f` | 133.32 M | 72% | 802.75 M | 38% | 640.49 M | 33% |
| [sign-21](../sign-21/perf_x86_1.md) | ReSolveD-ɑ | `ReSolveD-alpha-512s` | 133.37 M | 72% | 3.82 G | 39% | 3.28 G | 35% |
| [sign-22](../sign-22/perf_x86_1.md) | Rhyme | `Rhyme-SHAKE-128` | 813.50 M | 0.0% | 2.18 M | 0.0% | 191.2 k | 0.0% |
| [sign-22](../sign-22/perf_x86_1.md) | Rhyme | `Rhyme-SHAKE-256` | 1.86 G | 0.0% | 9.75 M | 0.0% | 433.3 k | 0.0% |
| [sign-22](../sign-22/perf_x86_1.md) | Rhyme | `Rhyme-SHAKE-384` | 7.40 G | 0.0% | 4.97 M | 0.0% | 788.2 k | 0.0% |
| [sign-22](../sign-22/perf_x86_1.md) | Rhyme | `Rhyme-SHAKE-512` | 10.49 G (n=75) | 0.0% | 9.88 M | 0.0% | 1.18 M | 0.0% |
| [sign-22](../sign-22/perf_x86_1.md) | Rhyme | `Rhyme-SM3-128` | 867.63 M | 0.3% | 4.27 M | 75% | 338.8 k | 55% |
| [sign-22](../sign-22/perf_x86_1.md) | Rhyme | `Rhyme-SM3-256` | 2.32 G | 0.4% | 15.55 M | 77% | 870.9 k | 59% |
| [sign-22](../sign-22/perf_x86_1.md) | Rhyme | `Rhyme-SM3-384` | 6.54 G | 0.2% | 23.32 M | 74% | 1.60 M | 59% |
| [sign-22](../sign-22/perf_x86_1.md) | Rhyme | `Rhyme-SM3-512` | 6.87 G | 0.3% | 32.58 M | 76% | 2.22 M | 55% |
| [sign-23](../sign-23/perf_x86_1.md) | Shuttle | `SHUTTLE-128` | 8.65 M | 0.0% | 4.51 M | 0.0% | 1.11 M | 0.0% |
| [sign-23](../sign-23/perf_x86_1.md) | Shuttle | `SHUTTLE-256` | 9.11 M | 0.0% | 7.15 M | 0.0% | 1.51 M | 0.0% |
| [sign-23](../sign-23/perf_x86_1.md) | Shuttle | `SHUTTLE-512` | 20.92 M | 0.0% | 14.60 M | 0.0% | 2.83 M | 0.0% |
| [sign-24](../sign-24/perf_x86_1.md) | Sigurd | `Sigurd-128` | 21.21 M | 21% | 37.45 M | 31% | 15.26 M | 43% |
| [sign-24](../sign-24/perf_x86_1.md) | Sigurd | `Sigurd-256` | 113.63 M | 32% | 325.62 M | 57% | 110.82 M | 49% |
| [sign-24](../sign-24/perf_x86_1.md) | Sigurd | `Sigurd-512` | 564.66 M | 40% | 2.97 G | 62% | 931.31 M | 34% |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | `SQISign2Dsquare-Level1-eff_compressed` | 48.79 M | 0.0% | 162.12 M | 0.5% | 34.65 M | 1.2% |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | `SQISign2Dsquare-Level1-eff_uncompressed` | 25.31 M | 0.0% | 139.10 M | 0.4% | 28.48 M | 1.4% |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | `SQISign2Dsquare-Level1-sec_compressed` | 67.27 M | 0.0% | 223.10 M | 0.0% | 46.29 M | 0.0% |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | `SQISign2Dsquare-Level1-sec_uncompressed` | 38.91 M | 0.0% | 217.06 M | 0.0% | 45.58 M | 0.0% |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | `SQISign2Dsquare-Level2-eff_compressed` | 53.82 M | 0.0% | 177.99 M | 2.6% | 41.99 M | 15% |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | `SQISign2Dsquare-Level2-eff_uncompressed` ⚠ KAT CRYPTOFAIL | 28.88 M | 0.0% | 168.46 M | 2.4% | 38.76 M | 17% |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | `SQISign2Dsquare-Level2-sec_compressed` | 122.46 M | 0.0% | 394.31 M | 0.0% | 98.08 M | 0.0% |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | `SQISign2Dsquare-Level2-sec_uncompressed` | 60.07 M | 0.0% | 330.40 M | 0.0% | 71.94 M | 0.0% |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | `SQISign2Dsquare-Level3-eff_compressed` | 263.66 M | 0.0% | 899.01 M | 1.0% | 202.48 M | 6.4% |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | `SQISign2Dsquare-Level3-eff_uncompressed` | 141.90 M | 0.0% | 844.61 M | 1.0% | 189.07 M | 6.9% |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | `SQISign2Dsquare-Level3-sec_compressed` | 371.43 M | 0.0% | 1.19 G | 0.0% | 264.35 M | 0.0% |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | `SQISign2Dsquare-Level3-sec_uncompressed` | 198.03 M | 0.0% | 1.13 G | 0.0% | 246.60 M | 0.0% |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | `SQISign2Dsquare-Level5-eff_compressed` | 1.92 G | 0.0% | 6.25 G | 0.1% | 1.37 G | 0.7% |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | `SQISign2Dsquare-Level5-eff_uncompressed` | 1.01 G | 0.0% | 5.67 G | 0.1% | 1.20 G | 0.8% |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | `SQISign2Dsquare-Level5-sec_compressed` | 2.50 G | 0.0% | 7.95 G | 0.0% | 1.77 G | 0.0% |
| [sign-25](../sign-25/perf_x86_1.md) | SQIsign2D2 | `SQISign2Dsquare-Level5-sec_uncompressed` | 1.32 G | 0.0% | 7.23 G | 0.0% | 1.52 G | 0.0% |
| [sign-26](../sign-26/perf_x86_1.md) | SQIsign2D-push1/2 | `SQIsign2D-lvl1` | 558.85 M | 0.0% | 619.25 M | 0.0% | 135.94 M | 0.0% |
| [sign-26](../sign-26/perf_x86_1.md) | SQIsign2D-push1/2 | `SQIsign2D-lvl2` | 1.85 G | 0.0% | 3.29 G | 0.0% | 438.06 M | 0.0% |
| [sign-26](../sign-26/perf_x86_1.md) | SQIsign2D-push1/2 | `SQIsign2D-lvl3` ⚠ KAT MISMATCH | 5.57 G | 0.0% | 5.32 G | 0.0% | 1.33 G | 0.0% |
| [sign-26](../sign-26/perf_x86_1.md) | SQIsign2D-push1/2 | `SQIsign2D-lvl4` | 44.58 G (n=40) | 0.0% | 39.28 G (n=45) | 0.0% | 9.78 G | 0.0% |
| [sign-27](../sign-27/perf_x86_1.md) | SQIsignTriangle | `SQIsignTriangle_lvl1` | 108.98 M | 0.0% | 203.28 M | 1.6% | 19.98 M | 3.4% |
| [sign-27](../sign-27/perf_x86_1.md) | SQIsignTriangle | `SQIsignTriangle_lvl2` | 164.50 M | 0.0% | 373.20 M | 3.4% | 32.79 M | 0.4% |
| [sign-27](../sign-27/perf_x86_1.md) | SQIsignTriangle | `SQIsignTriangle_lvl5` | 533.79 M | 0.0% | 1.06 G | 4.7% | 155.70 M | 39% |
| [sign-27](../sign-27/perf_x86_1.md) | SQIsignTriangle | `SQIsignTriangle_lvl6` | 4.16 G | 0.0% | 10.05 G | 1.7% | 3.31 G | 83% |
| [sign-28](../sign-28/perf_x86_1.md) | SYDO | `sydo_160f` | 901.2 k | 1.3% | 443.76 M | 2.1% | 449.76 M | 2.1% |
| [sign-28](../sign-28/perf_x86_1.md) | SYDO | `sydo_160s` | 901.6 k | 1.3% | 1.12 G | 5.3% | 1.11 G | 4.5% |
| [sign-28](../sign-28/perf_x86_1.md) | SYDO | `sydo_256f` | 1.60 M | 1.1% | 967.48 M | 2.5% | 1.00 G | 2.5% |
| [sign-28](../sign-28/perf_x86_1.md) | SYDO | `sydo_256s` | 1.60 M | 1.1% | 2.40 G | 5.5% | 2.43 G | 5.4% |
| [sign-28](../sign-28/perf_x86_1.md) | SYDO | `sydo_512f` | 577.0 k | 12% | 2.49 G | 7.8% | 2.65 G | 7.4% |
| [sign-28](../sign-28/perf_x86_1.md) | SYDO | `sydo_512s` | 570.3 k | 11% | 4.30 G | 26% | 4.36 G | 24% |
| [sign-29](../sign-29/perf_x86_1.md) | Tins | `Tins128` ⚠ KAT CRYPTOFAIL | 1.71 M | 0.0% | 1.35 G | 20% | 1.25 G | 20% |
| [sign-29](../sign-29/perf_x86_1.md) | Tins | `Tins256` | 9.67 M | 0.0% | 4.77 G | 37% | 4.64 G | 39% |
| [sign-29](../sign-29/perf_x86_1.md) | Tins | `Tins512` | 62.90 M | 0.0% | 20.33 G (n=90) | 54% | 20.14 G (n=90) | 55% |
| [sign-30](../sign-30/perf_x86_1.md) | TRINE | `TRINE-128-Balanced` | 9.54 M | 64% | 39.46 G (n=45) | 16% | 25.46 G (n=70) | 16% |
| [sign-30](../sign-30/perf_x86_1.md) | TRINE | `TRINE-128-ShortSig` | 19.87 M | 35% | 18.23 G (n=95) | 16% | 8.77 G | 16% |
| [sign-30](../sign-30/perf_x86_1.md) | TRINE | `TRINE-256-Balanced` ⚠ KAT TIMEOUT | 56.62 M | 46% | 534.99 G (n=3) | 7.1% | 329.94 G (n=5) | 6.8% |
| [sign-30](../sign-30/perf_x86_1.md) | TRINE | `TRINE-256-ShortSig` | 125.49 M | 25% | 158.21 G (n=10) | 9.2% | 58.42 G (n=30) | 8.8% |
| [sign-30](../sign-30/perf_x86_1.md) | TRINE | `TRINE-512-Balanced` ⚠ KAT TIMEOUT | 991.87 M | 57% | 8385.08 G (n=1) | 2.5% | 5525.78 G (n=1) | 2.5% |
| [sign-30](../sign-30/perf_x86_1.md) | TRINE | `TRINE-512-ShortSig` ⚠ KAT TIMEOUT | 2.25 G | 27% | 3367.79 G (n=1) | 2.5% | 1560.87 G (n=1) | 2.5% |
| [sign-31](../sign-31/perf_x86_1.md) | TSUOV | `TSUOV_128` | 10.52 M | 77% | 14.54 M | 56% | 11.83 M | 69% |
| [sign-31](../sign-31/perf_x86_1.md) | TSUOV | `TSUOV_256` | 67.40 M | 75% | 94.37 M | 54% | 79.44 M | 64% |
| [sign-31](../sign-31/perf_x86_1.md) | TSUOV | `TSUOV_512` | 918.12 M | 74% | 862.97 M | 79% | 898.63 M | 75% |
| [sign-32](../sign-32/perf_x86_1.md) | UVW signature | `UVW-128` ⚠ KAT CRYPTOFAIL | 78.68 G (n=20) | 0.0% | 30.29 G (n=95) | 0.0% | 340.31 M | 1.0% |
| [sign-32](../sign-32/perf_x86_1.md) | UVW signature | `UVW-256` ⚠ KAT CRYPTOFAIL | 1048.15 G (n=1) | 0.0% | 253.22 G (n=5) | 0.0% | 1.96 G | 0.2% |
| [sign-32](../sign-32/perf_x86_1.md) | UVW signature | `UVW-512` ⚠ KAT CRYPTOFAIL | 11676.24 G (n=1) | 0.0% | 1935.27 G (n=1) | 0.0% | 23.49 G (n=80) | 0.0% |
| [sign-33](../sign-33/perf_x86_1.md) | VDOO: Vinegar-Diagonal-Oil-Oil | `vdoo_128` | 1.20 G | 0.0% | 219.78 M | 0.0% | 2.36 M | 0.3% |
| [sign-33](../sign-33/perf_x86_1.md) | VDOO: Vinegar-Diagonal-Oil-Oil | `vdoo_256` | 39.28 G (n=45) | 0.0% | 271.44 M | 0.0% | 7.77 M | 0.1% |
| [sign-33](../sign-33/perf_x86_1.md) | VDOO: Vinegar-Diagonal-Oil-Oil | `vdoo_512` ⚠ KAT TIMEOUT | 308.01 G (n=5) | 0.0% | 1.69 G | 0.0% | 28.78 M | 0.1% |
| [sign-34](../sign-34/perf_x86_1.md) | YuanYang.DSA | `yuanyang-512` | 17.05 M | 0.0% | 9.00 M | 1.9% | 210.7 k | 59% |
| [sign-34](../sign-34/perf_x86_1.md) | YuanYang.DSA | `yuanyang-1024` | 19.76 M | 0.0% | 14.65 M | 1.8% | 461.1 k | 54% |
| [sign-34](../sign-34/perf_x86_1.md) | YuanYang.DSA | `yuanyang-2048` | 88.03 M | 0.0% | 46.36 M | 1.7% | 1.02 M | 49% |

## Key exchange

| id | algorithm | instance | exchange | sym % |
|---|---|---|---|---|
| [kex-01](../kex-01/perf_x86_1.md) | ADKEX (Authenticated Ding Key Exchange) | `ADKEX-128` | 1.52 M | 63% |
| [kex-01](../kex-01/perf_x86_1.md) | ADKEX (Authenticated Ding Key Exchange) | `ADKEX-256` | 4.05 M | 69% |
| [kex-01](../kex-01/perf_x86_1.md) | ADKEX (Authenticated Ding Key Exchange) | `ADKEX-512` | 13.97 M | 81% |
| [kex-02](../kex-02/perf_x86_1.md) | AFS-KEX | `AFS_KEX_C128` | 2.81 M | 63% |
| [kex-02](../kex-02/perf_x86_1.md) | AFS-KEX | `AFS_KEX_C256` | 6.52 M | 73% |
| [kex-02](../kex-02/perf_x86_1.md) | AFS-KEX | `AFS_KEX_C512` | 22.17 M | 76% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-K2K-PLAC128` | 1.99 M | 68% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-K2K-PLAC256` | 4.05 M | 66% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-K2K-PLAC512` | 14.18 M | 74% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-K2K-PLAC512Star` | 15.43 M | 70% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-K2K-ZEN128` | 1.91 M | 46% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-K2K-ZEN256` | 3.55 M | 46% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-K2K-ZEN512` | 9.55 M | 57% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-K2S-PLAC128-BiT128` | 4.40 M | 64% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-K2S-PLAC256-BiT256` | 8.04 M | 71% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-K2S-PLAC512-BiT512` | 26.97 M | 77% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-K2S-ZEN128-BiT128` | 4.26 M | 59% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-K2S-ZEN256-BiT256` | 7.88 M | 66% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-K2S-ZEN512-BiT512` | 24.31 M | 74% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-S2K-BiT128-PLAC128` | 4.45 M | 64% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-S2K-BiT128-ZEN128` | 4.49 M | 58% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-S2K-BiT256-PLAC256` | 8.34 M | 71% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-S2K-BiT256-ZEN256` | 8.13 M | 64% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-S2K-BiT512-PLAC512` | 29.73 M | 76% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-S2K-BiT512-ZEN512` | 25.76 M | 72% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-S2S-BiT128-ePLAC128` | 6.97 M | 63% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-S2S-BiT128-eZEN128` | 7.02 M | 61% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-S2S-BiT256-ePLAC256` | 12.50 M | 72% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-S2S-BiT256-eZEN256` | 12.64 M | 69% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-S2S-BiT512-ePLAC512` | 41.88 M | 78% |
| [kex-03](../kex-03/perf_x86_1.md) | CreTAKE | `CreTAKE-S2S-BiT512-eZEN512` | 43.97 M | 75% |
| [kex-04](../kex-04/perf_x86_1.md) | DKEX (Ding Key Exchange) | `DKEX-128` | 3.84 M | 12% |
| [kex-04](../kex-04/perf_x86_1.md) | DKEX (Ding Key Exchange) | `DKEX-256` | 8.70 M | 14% |
| [kex-04](../kex-04/perf_x86_1.md) | DKEX (Ding Key Exchange) | `DKEX-512` | 12.24 M | 36% |
| [kex-05](../kex-05/perf_x86_1.md) | Loom | `LoomKEX-128` | 30.90 M | 3.1% |
| [kex-05](../kex-05/perf_x86_1.md) | Loom | `LoomKEX-256` | 38.83 M | 3.4% |
| [kex-05](../kex-05/perf_x86_1.md) | Loom | `LoomKEX-512` | 81.64 M | 6.2% |
| [kex-06](../kex-06/perf_x86_1.md) | MAMBA-NIKE | `MAMBA-NIKE-128` | 6.09 M | 0.0% |
| [kex-06](../kex-06/perf_x86_1.md) | MAMBA-NIKE | `MAMBA-NIKE-192` | 6.14 M | 0.0% |
| [kex-06](../kex-06/perf_x86_1.md) | MAMBA-NIKE | `MAMBA-NIKE-256` | 6.20 M | 0.0% |
| [kex-06](../kex-06/perf_x86_1.md) | MAMBA-NIKE | `MAMBA-NIKE-384` | 12.94 M | 0.0% |
| [kex-06](../kex-06/perf_x86_1.md) | MAMBA-NIKE | `MAMBA-NIKE-512` | 13.11 M | 0.0% |
| [kex-07](../kex-07/perf_x86_1.md) | NEV-AKE | `NEV_AKE_512_769` | 889.2 k | 45% |
| [kex-07](../kex-07/perf_x86_1.md) | NEV-AKE | `NEV_AKE_512_769_C` | 847.7 k | 42% |
| [kex-07](../kex-07/perf_x86_1.md) | NEV-AKE | `NEV_AKE_512_1409` | 1.08 M | 52% |
| [kex-07](../kex-07/perf_x86_1.md) | NEV-AKE | `NEV_AKE_1024_769` | 1.83 M | 42% |
| [kex-07](../kex-07/perf_x86_1.md) | NEV-AKE | `NEV_AKE_1024_769_C` | 1.76 M | 38% |
| [kex-07](../kex-07/perf_x86_1.md) | NEV-AKE | `NEV_AKE_1024_1409` | 2.03 M | 45% |
| [kex-07](../kex-07/perf_x86_1.md) | NEV-AKE | `NEV_AKE_2048_769` | 5.18 M | 55% |
| [kex-07](../kex-07/perf_x86_1.md) | NEV-AKE | `NEV_AKE_2048_769_C` | 4.87 M | 51% |
| [kex-07](../kex-07/perf_x86_1.md) | NEV-AKE | `NEV_AKE_2048_1409` | 5.75 M | 53% |
| [kex-08](../kex-08/perf_x86_1.md) | NIIKE | `NIIKE-lv128` | 52.91 G (n=35) | 0.0% |
| [kex-08](../kex-08/perf_x86_1.md) | NIIKE | `NIIKE-lv256` | 935.98 G (n=1) | 0.0% |
| [kex-09](../kex-09/perf_x86_1.md) | TriQ-KEX | `TriQ-KEX-128` | 60.66 M | 7.0% |
| [kex-09](../kex-09/perf_x86_1.md) | TriQ-KEX | `TriQ-KEX-256` | 343.23 M | 3.6% |
| [kex-09](../kex-09/perf_x86_1.md) | TriQ-KEX | `TriQ-KEX-384` | 934.75 M | 4.4% |
| [kex-09](../kex-09/perf_x86_1.md) | TriQ-KEX | `TriQ-KEX-512` | 1.96 G | 3.8% |

## Hash functions

| id | algorithm | instance | 32 B (cycles) | 64 KiB (cycles) |
|---|---|---|---|---|
| [hash-01](../hash-01/perf_x86_1.md) | AFS-TrEDM | `AFS-TrEDM-512` | 23.7 k | 12.08 M |
| [hash-01](../hash-01/perf_x86_1.md) | AFS-TrEDM | `AFS-TrEDM-768` | 39.4 k | 26.80 M |
| [hash-01](../hash-01/perf_x86_1.md) | AFS-TrEDM | `AFS-TrEDM-1024` | 46.9 k | 48.01 M |
| [hash-02](../hash-02/perf_x86_1.md) | AXIS: Advanced eXpandable Iterative Stream-based Hash | `AXIS-512` | 58.7 k | 2.45 M |
| [hash-02](../hash-02/perf_x86_1.md) | AXIS: Advanced eXpandable Iterative Stream-based Hash | `AXIS-768` | 72.6 k | 5.96 M |
| [hash-02](../hash-02/perf_x86_1.md) | AXIS: Advanced eXpandable Iterative Stream-based Hash | `AXIS-1024` | 96.3 k | 3.88 M |
| [hash-03](../hash-03/perf_x86_1.md) | C Hash | `CHash_512` | 190.3 k | 67.98 M |
| [hash-03](../hash-03/perf_x86_1.md) | C Hash | `CHash_1024` | 190.4 k | 68.14 M |
| [hash-04](../hash-04/perf_x86_1.md) | CHAMP | `CHAMP-512` | 66.9 k | 33.76 M |
| [hash-04](../hash-04/perf_x86_1.md) | CHAMP | `CHAMP-1024` | 369.9 k | 93.70 M |
| [hash-05](../hash-05/perf_x86_1.md) | Cryptographic Hash Algorithm uHash | `uHash-512` | 58.0 k | 39.38 M |
| [hash-05](../hash-05/perf_x86_1.md) | Cryptographic Hash Algorithm uHash | `uHash-768` | 86.7 k | 88.11 M |
| [hash-05](../hash-05/perf_x86_1.md) | Cryptographic Hash Algorithm uHash | `uHash-1024` | 230.6 k | 235.53 M |
| [hash-06](../hash-06/perf_x86_1.md) | Cuishen | `Cuishen-512` | 2294 | 1.17 M |
| [hash-06](../hash-06/perf_x86_1.md) | Cuishen | `Cuishen-768` | 3119 | 1.62 M |
| [hash-06](../hash-06/perf_x86_1.md) | Cuishen | `Cuishen-1024` | 3214 | 1.63 M |
| [hash-07](../hash-07/perf_x86_1.md) | Dragon Hash Family | `Dragon-512` | 2436 | 1.17 M |
| [hash-07](../hash-07/perf_x86_1.md) | Dragon Hash Family | `Dragon-768` | 2418 | 1.57 M |
| [hash-07](../hash-07/perf_x86_1.md) | Dragon Hash Family | `Dragon-1024` | 2424 | 2.37 M |
| [hash-07](../hash-07/perf_x86_1.md) | Dragon Hash Family | `Dragon-XOF-256` | 9860 | 1.20 M |
| [hash-07](../hash-07/perf_x86_1.md) | Dragon Hash Family | `Dragon-XOF-384` | 9114 | 1.57 M |
| [hash-07](../hash-07/perf_x86_1.md) | Dragon Hash Family | `Dragon-XOF-512` | 8367 | 2.38 M |
| [hash-08](../hash-08/perf_x86_1.md) | Duet | `Duet-512` | 6249 | 8.40 M |
| [hash-08](../hash-08/perf_x86_1.md) | Duet | `Duet-768` | 29.4 k | 14.02 M |
| [hash-08](../hash-08/perf_x86_1.md) | Duet | `Duet-1024` | 29.3 k | 19.85 M |
| [hash-09](../hash-09/perf_x86_1.md) | Eijen Hash Function | `Eijen-256` | 2165 | 623.2 k |
| [hash-09](../hash-09/perf_x86_1.md) | Eijen Hash Function | `Eijen-384` | 2219 | 664.0 k |
| [hash-09](../hash-09/perf_x86_1.md) | Eijen Hash Function | `Eijen-512` | 2150 | 735.5 k |
| [hash-09](../hash-09/perf_x86_1.md) | Eijen Hash Function | `Eijen-768` | 2211 | 892.5 k |
| [hash-09](../hash-09/perf_x86_1.md) | Eijen Hash Function | `Eijen-1024` | 2185 | 1.12 M |
| [hash-10](../hash-10/perf_x86_1.md) | FEILIAN | `FEILIAN512` | 2014 | 962.6 k |
| [hash-10](../hash-10/perf_x86_1.md) | FEILIAN | `FEILIAN768` | 2125 | 960.4 k |
| [hash-10](../hash-10/perf_x86_1.md) | FEILIAN | `FEILIAN1024` | 2175 | 961.1 k |
| [hash-11](../hash-11/perf_x86_1.md) | Garnet | `Garnet_512_Cap512` | 18.6 k | 5.61 M |
| [hash-11](../hash-11/perf_x86_1.md) | Garnet | `Garnet_512_Cap640` | 19.0 k | 4.58 M |
| [hash-11](../hash-11/perf_x86_1.md) | Garnet | `Garnet_512_Cap768` | 18.6 k | 3.74 M |
| [hash-11](../hash-11/perf_x86_1.md) | Garnet | `Garnet_512_Cap896` | 18.6 k | 3.22 M |
| [hash-11](../hash-11/perf_x86_1.md) | Garnet | `Garnet_512_Cap1024` | 11.3 k | 1.70 M |
| [hash-11](../hash-11/perf_x86_1.md) | Garnet | `Garnet_768` | 10.9 k | 3.29 M |
| [hash-11](../hash-11/perf_x86_1.md) | Garnet | `Garnet_1024` | 48.4 k | 8.63 M |
| [hash-11](../hash-11/perf_x86_1.md) | Garnet | `Garnet_1024_DM4x4` ⚠ KAT MISMATCH | – | – |
| [hash-12](../hash-12/perf_x86_1.md) | Iphe | `Iphe-512` | 18.5 k | 5.40 M |
| [hash-12](../hash-12/perf_x86_1.md) | Iphe | `Iphe-768` | 17.7 k | 6.48 M |
| [hash-12](../hash-12/perf_x86_1.md) | Iphe | `Iphe-1024` | 17.1 k | 8.11 M |
| [hash-13](../hash-13/perf_x86_1.md) | JuziHash | `JuziHash-512` | 132.9 k | 22.84 M |
| [hash-13](../hash-13/perf_x86_1.md) | JuziHash | `JuziHash-1024` | 133.4 k | 22.81 M |
| [hash-14](../hash-14/perf_x86_1.md) | Laurus | `Laurus-512` | 4178 | 2.15 M |
| [hash-14](../hash-14/perf_x86_1.md) | Laurus | `Laurus-768` | 4068 | 2.63 M |
| [hash-14](../hash-14/perf_x86_1.md) | Laurus | `Laurus-1024` | 4081 | 4.25 M |
| [hash-14](../hash-14/perf_x86_1.md) | Laurus | `Laurus-XOF` | 8147 | 2.15 M |
| [hash-15](../hash-15/perf_x86_1.md) | Litchi | `litchi_512` | 4129 | 2.06 M |
| [hash-15](../hash-15/perf_x86_1.md) | Litchi | `litchi_768` | 4162 | 2.74 M |
| [hash-15](../hash-15/perf_x86_1.md) | Litchi | `litchi_1024` | 4111 | 4.01 M |
| [hash-15](../hash-15/perf_x86_1.md) | Litchi | `litchi_xof` | 4291 | 3.53 M |
| [hash-16](../hash-16/perf_x86_1.md) | LLH | `LLH-256` | 2006 | 2.14 M |
| [hash-16](../hash-16/perf_x86_1.md) | LLH | `LLH-512` | 2993 | 1.62 M |
| [hash-16](../hash-16/perf_x86_1.md) | LLH | `LLH-768` | 10.3 k | 3.68 M |
| [hash-16](../hash-16/perf_x86_1.md) | LLH | `LLH-1024` | 10.3 k | 2.74 M |
| [hash-17](../hash-17/perf_x86_1.md) | MasterCube | `MasterCube-512` | 15.4 k | 4.19 M |
| [hash-17](../hash-17/perf_x86_1.md) | MasterCube | `MasterCube-768` | 22.9 k | 5.69 M |
| [hash-17](../hash-17/perf_x86_1.md) | MasterCube | `MasterCube-1024` | 30.6 k | 8.93 M |
| [hash-18](../hash-18/perf_x86_1.md) | Megascon Hash Function | `MEGASCON-384` | 3021 | 1.19 M |
| [hash-18](../hash-18/perf_x86_1.md) | Megascon Hash Function | `MEGASCON-384-XOF-256` | 3279 | 1.27 M |
| [hash-18](../hash-18/perf_x86_1.md) | Megascon Hash Function | `MEGASCON-384-XOF-1024` | 3487 | 1.27 M |
| [hash-18](../hash-18/perf_x86_1.md) | Megascon Hash Function | `MEGASCON-384-XOF-2048` | 6552 | 1.27 M |
| [hash-18](../hash-18/perf_x86_1.md) | Megascon Hash Function | `MEGASCON-512` | 3016 | 1.48 M |
| [hash-18](../hash-18/perf_x86_1.md) | Megascon Hash Function | `MEGASCON-512-XOF-256` | 3235 | 1.56 M |
| [hash-18](../hash-18/perf_x86_1.md) | Megascon Hash Function | `MEGASCON-512-XOF-1024` | 3438 | 1.56 M |
| [hash-18](../hash-18/perf_x86_1.md) | Megascon Hash Function | `MEGASCON-512-XOF-2048` | 6505 | 1.56 M |
| [hash-18](../hash-18/perf_x86_1.md) | Megascon Hash Function | `MEGASCON-768` | 3266 | 1.35 M |
| [hash-18](../hash-18/perf_x86_1.md) | Megascon Hash Function | `MEGASCON-1024` | 3264 | 1.70 M |
| [hash-19](../hash-19/perf_x86_1.md) | MoFang Hash Function | `MoFang-256` | 2439 | 1.05 M |
| [hash-19](../hash-19/perf_x86_1.md) | MoFang Hash Function | `MoFang-256-XOF` | 2504 | 1.01 M |
| [hash-19](../hash-19/perf_x86_1.md) | MoFang Hash Function | `MoFang-512` | 2554 | 1.05 M |
| [hash-19](../hash-19/perf_x86_1.md) | MoFang Hash Function | `MoFang-768` | 4309 | 1.86 M |
| [hash-19](../hash-19/perf_x86_1.md) | MoFang Hash Function | `MoFang-768-XOF` | 4728 | 1.86 M |
| [hash-19](../hash-19/perf_x86_1.md) | MoFang Hash Function | `MoFang-1024` | 4421 | 1.85 M |
| [hash-20](../hash-20/perf_x86_1.md) | Mozi Hash Function | `MOZI-384` | 3139 | 1.23 M |
| [hash-20](../hash-20/perf_x86_1.md) | Mozi Hash Function | `MOZI-384-XOF-256` | 3323 | 1.28 M |
| [hash-20](../hash-20/perf_x86_1.md) | Mozi Hash Function | `MOZI-384-XOF-1024` | 3535 | 1.28 M |
| [hash-20](../hash-20/perf_x86_1.md) | Mozi Hash Function | `MOZI-384-XOF-2048` | 6711 | 1.28 M |
| [hash-20](../hash-20/perf_x86_1.md) | Mozi Hash Function | `MOZI-512` | 3108 | 1.53 M |
| [hash-20](../hash-20/perf_x86_1.md) | Mozi Hash Function | `MOZI-512-XOF-256` | 3351 | 1.58 M |
| [hash-20](../hash-20/perf_x86_1.md) | Mozi Hash Function | `MOZI-512-XOF-1024` | 3475 | 1.58 M |
| [hash-20](../hash-20/perf_x86_1.md) | Mozi Hash Function | `MOZI-512-XOF-2048` | 6604 | 1.58 M |
| [hash-20](../hash-20/perf_x86_1.md) | Mozi Hash Function | `MOZI-768` | 3621 | 1.50 M |
| [hash-20](../hash-20/perf_x86_1.md) | Mozi Hash Function | `MOZI-1024` | 3611 | 1.89 M |
| [hash-21](../hash-21/perf_x86_1.md) | Neulaser | `Neulaser-512` | 16.7 k | 7.72 M |
| [hash-21](../hash-21/perf_x86_1.md) | Neulaser | `Neulaser-768` | 21.5 k | 7.94 M |
| [hash-21](../hash-21/perf_x86_1.md) | Neulaser | `Neulaser-1024` | 26.6 k | 7.92 M |
| [hash-22](../hash-22/perf_x86_1.md) | Pavelor: A Highly Secure Hash Algorithm for Software Implementation | `Pavelor-512` | 37.8 k | 12.64 M |
| [hash-22](../hash-22/perf_x86_1.md) | Pavelor: A Highly Secure Hash Algorithm for Software Implementation | `Pavelor-768` | 37.9 k | 19.02 M |
| [hash-22](../hash-22/perf_x86_1.md) | Pavelor: A Highly Secure Hash Algorithm for Software Implementation | `Pavelor-1024` | 74.5 k | 37.78 M |
| [hash-23](../hash-23/perf_x86_1.md) | QILIN | `QILIN-512` | 12.7 k | 3.12 M |
| [hash-23](../hash-23/perf_x86_1.md) | QILIN | `QILIN-768` | 14.7 k | 4.76 M |
| [hash-23](../hash-23/perf_x86_1.md) | QILIN | `QILIN-1024` | 16.8 k | 7.96 M |
| [hash-24](../hash-24/perf_x86_1.md) | QuantaSylva Hash | `QSH-512` | 81.8 k | 15.73 M |
| [hash-24](../hash-24/perf_x86_1.md) | QuantaSylva Hash | `QSH-768` | 160.5 k | 15.55 M |
| [hash-24](../hash-24/perf_x86_1.md) | QuantaSylva Hash | `QSH-1024` | 160.3 k | 15.54 M |
| [hash-25](../hash-25/perf_x86_1.md) | TaiChi | `TaiChi-512` | 23.7 k | 7.95 M |
| [hash-25](../hash-25/perf_x86_1.md) | TaiChi | `TaiChi-768` | 23.1 k | 9.71 M |
| [hash-25](../hash-25/perf_x86_1.md) | TaiChi | `TaiChi-1024` | 44.2 k | 12.54 M |
| [hash-26](../hash-26/perf_x86_1.md) | The Hash Function CHIME | `CHIME-512` | 2248 | 2.24 M |
| [hash-26](../hash-26/perf_x86_1.md) | The Hash Function CHIME | `CHIME-1024` | 3030 | 3.42 M |
| [hash-27](../hash-27/perf_x86_1.md) | The Vedak Hash Function Family | `Vedak-512` | 24.7 k | 10.10 M |
| [hash-27](../hash-27/perf_x86_1.md) | The Vedak Hash Function Family | `Vedak-768` | 24.6 k | 14.07 M |
| [hash-27](../hash-27/perf_x86_1.md) | The Vedak Hash Function Family | `Vedak-1024` | 47.6 k | 25.93 M |
| [hash-28](../hash-28/perf_x86_1.md) | The XRH-1 Hash Function | `XRH-1-512` | 2665 | 1.88 M |
| [hash-28](../hash-28/perf_x86_1.md) | The XRH-1 Hash Function | `XRH-1-768` | 5073 | 2.97 M |
| [hash-28](../hash-28/perf_x86_1.md) | The XRH-1 Hash Function | `XRH-1-1024` | 17.2 k | 6.92 M |
| [hash-29](../hash-29/perf_x86_1.md) | The XRH-2 Hash Function | `XRH-2-512` | 2721 | 1.95 M |
| [hash-29](../hash-29/perf_x86_1.md) | The XRH-2 Hash Function | `XRH-2-768` | 5292 | 3.07 M |
| [hash-29](../hash-29/perf_x86_1.md) | The XRH-2 Hash Function | `XRH-2-1024` | 17.2 k | 6.92 M |
| [hash-30](../hash-30/perf_x86_1.md) | The ZC-DM Hash Function | `ZC-DM-1280-512` | 1219 | 442.1 k |
| [hash-30](../hash-30/perf_x86_1.md) | The ZC-DM Hash Function | `ZC-DM-1280-768` | 1570 | 691.9 k |
| [hash-30](../hash-30/perf_x86_1.md) | The ZC-DM Hash Function | `ZC-DM-1280-1024` | 4305 | 1.59 M |
| [hash-30](../hash-30/perf_x86_1.md) | The ZC-DM Hash Function | `ZC-DM-1536-512` | 1915 | 581.9 k |
| [hash-30](../hash-30/perf_x86_1.md) | The ZC-DM Hash Function | `ZC-DM-1536-768` | 2675 | 786.4 k |
| [hash-30](../hash-30/perf_x86_1.md) | The ZC-DM Hash Function | `ZC-DM-1536-1024` | 3433 | 1.24 M |
| [hash-31](../hash-31/perf_x86_1.md) | The ZC-DMC Hash Function | `ZC-DMC-1280-512` | 5167 | 442.6 k |
| [hash-31](../hash-31/perf_x86_1.md) | The ZC-DMC Hash Function | `ZC-DMC-1280-512-avx2` (AVX2) | 3779 | 326.5 k |
| [hash-31](../hash-31/perf_x86_1.md) | The ZC-DMC Hash Function | `ZC-DMC-1280-768` | 7239 | 696.1 k |
| [hash-31](../hash-31/perf_x86_1.md) | The ZC-DMC Hash Function | `ZC-DMC-1280-768-avx2` (AVX2) | 5141 | 515.5 k |
| [hash-31](../hash-31/perf_x86_1.md) | The ZC-DMC Hash Function | `ZC-DMC-1280-1024` | 9852 | 1.62 M |
| [hash-31](../hash-31/perf_x86_1.md) | The ZC-DMC Hash Function | `ZC-DMC-1280-1024-avx2` (AVX2) | 7150 | 1.19 M |
| [hash-31](../hash-31/perf_x86_1.md) | The ZC-DMC Hash Function | `ZC-DMC-1536-512` | 9099 | 593.3 k |
| [hash-31](../hash-31/perf_x86_1.md) | The ZC-DMC Hash Function | `ZC-DMC-1536-512-avx2` (AVX2) | 12.3 k | 825.0 k |
| [hash-31](../hash-31/perf_x86_1.md) | The ZC-DMC Hash Function | `ZC-DMC-1536-768` | 12.9 k | 808.9 k |
| [hash-31](../hash-31/perf_x86_1.md) | The ZC-DMC Hash Function | `ZC-DMC-1536-768-avx2` (AVX2) | 17.7 k | 1.15 M |
| [hash-31](../hash-31/perf_x86_1.md) | The ZC-DMC Hash Function | `ZC-DMC-1536-1024` | 16.7 k | 1.26 M |
| [hash-31](../hash-31/perf_x86_1.md) | The ZC-DMC Hash Function | `ZC-DMC-1536-1024-avx2` (AVX2) | 23.2 k | 1.76 M |
| [hash-32](../hash-32/perf_x86_1.md) | The ZC-EDMC Hash Function | `ZC-EDMC-1280-512` | 1235 | 431.8 k |
| [hash-32](../hash-32/perf_x86_1.md) | The ZC-EDMC Hash Function | `ZC-EDMC-1280-768` | 1539 | 679.1 k |
| [hash-32](../hash-32/perf_x86_1.md) | The ZC-EDMC Hash Function | `ZC-EDMC-1280-1024` | 4252 | 1.59 M |
| [hash-32](../hash-32/perf_x86_1.md) | The ZC-EDMC Hash Function | `ZC-EDMC-1536-512` | 1939 | 594.6 k |
| [hash-32](../hash-32/perf_x86_1.md) | The ZC-EDMC Hash Function | `ZC-EDMC-1536-768` | 2715 | 809.0 k |
| [hash-32](../hash-32/perf_x86_1.md) | The ZC-EDMC Hash Function | `ZC-EDMC-1536-1024` | 3472 | 1.27 M |
| [hash-33](../hash-33/perf_x86_1.md) | Thunder Hash Family | `Thunder-512` | 4276 | 2.13 M |
| [hash-33](../hash-33/perf_x86_1.md) | Thunder Hash Family | `Thunder-768` | 4240 | 2.84 M |
| [hash-33](../hash-33/perf_x86_1.md) | Thunder Hash Family | `Thunder-1024` | 4266 | 4.24 M |
| [hash-33](../hash-33/perf_x86_1.md) | Thunder Hash Family | `Thunder-XOF-256` | 11.4 k | 2.14 M |
| [hash-33](../hash-33/perf_x86_1.md) | Thunder Hash Family | `Thunder-XOF-384` | 10.7 k | 2.84 M |
| [hash-33](../hash-33/perf_x86_1.md) | Thunder Hash Family | `Thunder-XOF-512` | 9996 | 4.22 M |
| [hash-34](../hash-34/perf_x86_1.md) | WChain Hash Function | `WChain-V1-512` | 2099 | 433.6 k |
| [hash-34](../hash-34/perf_x86_1.md) | WChain Hash Function | `WChain-V2-1024` | 6691 | 746.0 k |
| [hash-35](../hash-35/perf_x86_1.md) | Wish Hash Function | `Wish512` | 245.8 k | 311.51 M |
| [hash-35](../hash-35/perf_x86_1.md) | Wish Hash Function | `Wish1024` | 763.8 k | 414.04 M |

