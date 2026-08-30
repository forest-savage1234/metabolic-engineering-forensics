# Initial Comparative Audit

**Status:** provisional; no case is considered end-to-end reconstructed until T6 is explicitly passed.

This document records the comparative pass under `methodology/verification-protocol.md`. It describes the publicly available evidentiary package, not the biological truth of any published result. Byte-level acquisition and bounded structural inspection of the targeted Kim, Park, and Cho public artifacts has now completed; see `results/public-evidence-probe.md`.

| Case | Bounded claim | Public evidence strength | Current strongest finding | Current verdict direction |
|---|---|---|---|---|
| Kim et al. 2019 | 50.2 g/L FFA | Strong: publisher exposes raw fed-batch XLSX plus model-reaction XLSX and SI | Hash-pinned fed-batch workbook contains five ROP1_34 values (50.2, 47.2, 46.7, 49.2, 50.1) plus run-level fermentation/GC sheets; complete analytical replay still required | Positive reconstruction candidate |
| Cho et al. 2026 | 141.5 g/L 1,3-PDO; 2.95 g/L/h | Very strong: article/SI, source-data archive, genome accession, public GEM | Hash-pinned 42-workbook source archive contains the 141.5/141.517 concentration neighborhood; exact titer/productivity replay and publication-state pinning remain | Strongest positive reconstruction candidate |
| Park et al. 2022 | 218.0 mg/L lutein; 5.01 mg/L/h | Strong: figure source data and supplementary XLSX files | Hash-pinned Fig. 7 workbook exposes the LUT5MH1 fed-batch lutein time-profile table; exact titer/productivity replay remains | Positive reconstruction candidate |
| Decembrino et al. 2021 | 196 µM / 78 mg/L DPT; 98% yield | Moderate: detailed article/SI, but key raw analytical/calibration evidence is not publicly deposited in the audited package | Versioned identifier inconsistency (`KT390173.1` vs `KT390173.12`) plus incomplete public derivation of 196 µM | Integrity conflict + incomplete reconstruction |

## Case 1 — Kim et al. 2019

**Citation:** Kim HM, Chae TU, Choi SY, Kim WJ, Lee SY. *Engineering of an oleaginous bacterium for the production of fatty acids and fuels.* Nature Chemical Biology 15, 721–729 (2019). DOI: 10.1038/s41589-019-0295-5.

The publication explicitly reports 50.2 g/L free fatty acids from an engineered *Rhodococcus opacus* strain. Nature exposes Supplementary Dataset 1 as “Raw data of fed-batch fermentations” and Supplementary Dataset 2 as the metabolic reactions used for genome-scale modeling. The supplementary information reports five independent ROP1_34 fed-batch FFA titers: 50.2, 47.2, 46.7, 49.2 and 50.1 g/L.

The public-evidence probe successfully acquired and hash-pinned Supplementary Dataset 1. Bounded workbook inspection independently locates all five ROP1_34 summary titers and shows that the workbook contains run-level fermentation/GC worksheets and formulas. This moves the case beyond link-level provenance into artifact-level inspection.

The important unresolved question is whether the released fed-batch dataset is sufficient to replay the complete analytical transformation that produced the concentration observations, or whether it begins from already processed concentration values. The project therefore does not yet equate “raw fed-batch data” with raw instrument evidence, and T6 remains unresolved.

## Case 2 — Cho et al. 2026

**Citation:** Cho JS et al. *High-titer, antibiotic-free, pilot-scale production of 1,3-propanediol by engineered Corynebacterium.* Nature Chemical Engineering 3, 272–285 (2026). DOI: 10.1038/s44286-026-00389-w.

The article reports 141.5 g/L 1,3-PDO at 2.95 g/L/h without antibiotics. Its public provenance surface is unusually extensive: article and supplementary information, source data, Figshare DOI 10.6084/m9.figshare.29264624, named fermentation/statistical datasets, SC97 genome accession JBSORY000000000 / BioProject PRJNA1370509, and a public SC97 genome-scale metabolic model repository.

The public-evidence probe successfully acquired and hash-pinned the Figshare source-data ZIP, enumerated 42 XLSX members, and located released 1,3-PDO source-data values of 141.517 and 141.5 in the workbook set. This materially strengthens the positive-reconstruction path but does not by itself prove the exact titer/productivity derivation.

The study also has a documented publication-state transition: an author correction was published on 21 May 2026 after the 12 May 2026 version of record. The correction states that the altered wording did not affect experimental data, results, or conclusions. This is useful as a non-adversarial example of why an evidentiary system should pin the exact publication state even where the bounded claim is unaffected.

T6 remains unresolved pending reconstruction of the exact 141.5 g/L and 2.95 g/L/h claim from the correct released experimental series and stated calculation basis.

## Case 3 — Park et al. 2022

**Citation:** Park et al. *Metabolic engineering of Escherichia coli with electron channelling for the production of natural products.* Nature Catalysis (2022). DOI: 10.1038/s41929-022-00820-4.

The bounded result is 218.0 mg/L lutein at 5.01 mg/L/h from the final LUT5MH1 fed-batch process. Figure-level source data and supplementary XLSX datasets are exposed by the publisher. This case is valuable because it couples a natural-product system with a multistage engineering history involving electron channelling, enzyme-partner state, metabolic engineering and process optimization.

The public-evidence probe successfully acquired and hash-pinned the Fig. 7 source workbook and verified that its Fig. 7b table contains the fed-batch time profile with a `Lutein (mg/L)` series. The remaining task is now claim-specific: identify the final LUT5MH1 observations and independently recompute the 218.0 mg/L titer and 5.01 mg/L/h productivity from the released values and the stated time basis. T6 remains unresolved until that replay is complete.

## Case 4 — Decembrino et al. 2021

**Citation:** Decembrino D et al. *Synthesis of (−)-deoxypodophyllotoxin and (−)-epipodophyllotoxin via a multi-enzyme cascade in E. coli.* Microbial Cell Factories 20, 183 (2021). DOI: 10.1186/s12934-021-01673-5.

The bounded result is 196 µM deoxypodophyllotoxin, reported as 78 mg/L and 98% theoretical yield from 200 µM matairesinol. Two downstream calculations independently reconstruct:

- `196 µmol/L × 398.40 g/mol = 78.0864 mg/L`, consistent with 78 mg/L after rounding.
- `196 / 200 × 100 = 98%`, consistent with the reported theoretical yield under the stated 1:1 molar interpretation.

The public article/SI package does not expose the raw LC/MS or peak-area observations and the calibration observations/fitted parameters needed to replay the upstream derivation of 196 µM. The paper instead states that raw data/materials will be made available to scientists for non-commercial use. This is recorded as an incomplete public evidence chain, not evidence that the result is incorrect.

An independent identifier-integrity finding is also present: the main article gives deoxypodophyllotoxin synthase / 2-ODD as GenBank `KT390173.1`, whereas the supplementary sequence heading gives `KT390173.12`. The project treats this as an evidentiary inconsistency requiring explicit review, likely typographical, and does not infer a sequence or biological error from it.

## Current interpretation

The four cases now span distinct forensic states:

1. a hash-pinned released workbook with run-level analytical structure that appears suitable for deeper reconstruction;
2. a hash-pinned, version-sensitive source-data archive with the reported concentration neighborhood directly present;
3. a hash-pinned figure-level time-series workbook awaiting exact titer/productivity replay; and
4. a partially reconstructable claim with both missing public derivation evidence and an internal identifier inconsistency.

The byte-level acquisition milestone is complete for the three targeted public artifacts. The next decisive step is claim-specific replay: reconstruct each bounded result from its released observations and calculation basis, or terminate the chain explicitly at the first missing evidentiary input. Until that is complete, the project deliberately leaves T6 unresolved for all four cases.
