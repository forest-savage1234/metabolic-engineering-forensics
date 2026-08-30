# Initial Comparative Audit

**Status:** provisional; no case is considered end-to-end reconstructed until T6 is explicitly passed.

This document records the first comparative pass under `methodology/verification-protocol.md`. It describes the publicly available evidentiary package, not the biological truth of any published result.

| Case | Bounded claim | Public evidence strength | Current strongest finding | Current verdict direction |
|---|---|---|---|---|
| Kim et al. 2019 | 50.2 g/L FFA | Strong: publisher exposes raw fed-batch XLSX plus model-reaction XLSX and SI | Five independent ROP1_34 runs are reported; source-data replay still required | Positive reconstruction candidate |
| Cho et al. 2026 | 141.5 g/L 1,3-PDO; 2.95 g/L/h | Very strong: article/SI, 30 fermentation datasets, 37 statistical datasets, Figshare deposit, genome accession, public GEM | Publication state changed by a later author correction; current evidentiary state is unusually rich | Strongest positive reconstruction candidate |
| Park et al. 2022 | 218.0 mg/L lutein; 5.01 mg/L/h | Strong: figure source data and supplementary XLSX files | Final strain/process is identifiable; source-data replay still required | Positive reconstruction candidate |
| Decembrino et al. 2021 | 196 µM / 78 mg/L DPT; 98% yield | Moderate: detailed article/SI, but key raw analytical/calibration evidence is not publicly deposited in the audited package | Versioned identifier inconsistency (`KT390173.1` vs `KT390173.12`) plus incomplete public derivation of 196 µM | Integrity conflict + incomplete reconstruction |

## Case 1 — Kim et al. 2019

**Citation:** Kim HM, Chae TU, Choi SY, Kim WJ, Lee SY. *Engineering of an oleaginous bacterium for the production of fatty acids and fuels.* Nature Chemical Biology 15, 721–729 (2019). DOI: 10.1038/s41589-019-0295-5.

The publication explicitly reports 50.2 g/L free fatty acids from an engineered *Rhodococcus opacus* strain. Nature exposes Supplementary Dataset 1 as “Raw data of fed-batch fermentations” and Supplementary Dataset 2 as the metabolic reactions used for genome-scale modeling. The supplementary information reports five independent ROP1_34 fed-batch FFA titers: 50.2, 47.2, 46.7, 49.2 and 50.1 g/L.

The important unresolved question is whether the released fed-batch dataset is sufficient to replay the complete analytical transformation that produced the concentration observations, or whether it begins from already processed concentration values. The project therefore does not yet equate “raw fed-batch data” with raw instrument evidence.

## Case 2 — Cho et al. 2026

**Citation:** Cho JS et al. *High-titer, antibiotic-free, pilot-scale production of 1,3-propanediol by engineered Corynebacterium.* Nature Chemical Engineering 3, 272–285 (2026). DOI: 10.1038/s44286-026-00389-w.

The article reports 141.5 g/L 1,3-PDO at 2.95 g/L/h without antibiotics. Its public provenance surface is unusually extensive: article and supplementary information, source data, Figshare DOI 10.6084/m9.figshare.29264624, 30 named fermentation datasets, 37 statistical supplementary datasets, SC97 genome accession JBSORY000000000 / BioProject PRJNA1370509, and a public SC97 genome-scale metabolic model repository.

The study also has a documented publication-state transition: an author correction was published on 21 May 2026 after the 12 May 2026 version of record. The correction states that the altered wording did not affect experimental data, results, or conclusions. This is useful as a non-adversarial example of why an evidentiary system should pin the exact publication state even where the bounded claim is unaffected.

## Case 3 — Park et al. 2022

**Citation:** Park et al. *Metabolic engineering of Escherichia coli with electron channelling for the production of natural products.* Nature Catalysis (2022). DOI: 10.1038/s41929-022-00820-4.

The bounded result is 218.0 mg/L lutein at 5.01 mg/L/h from the final LUT5MH1 fed-batch process. Figure-level source data and supplementary XLSX datasets are exposed by the publisher. This case is valuable because it couples a natural-product system with a multistage engineering history involving electron channelling, enzyme-partner state, metabolic engineering and process optimization.

The current audit has not yet replayed the Fig. 7 source dataset or independently recomputed the final titer/productivity.

## Case 4 — Decembrino et al. 2021

**Citation:** Decembrino D et al. *Synthesis of (−)-deoxypodophyllotoxin and (−)-epipodophyllotoxin via a multi-enzyme cascade in E. coli.* Microbial Cell Factories 20, 183 (2021). DOI: 10.1186/s12934-021-01673-5.

The bounded result is 196 µM deoxypodophyllotoxin, reported as 78 mg/L and 98% theoretical yield from 200 µM matairesinol. Two downstream calculations independently reconstruct:

- `196 µmol/L × 398.40 g/mol = 78.0864 mg/L`, consistent with 78 mg/L after rounding.
- `196 / 200 × 100 = 98%`, consistent with the reported theoretical yield under the stated 1:1 molar interpretation.

The public article/SI package does not expose the raw LC/MS or peak-area observations and the calibration observations/fitted parameters needed to replay the upstream derivation of 196 µM. The paper instead states that raw data/materials will be made available to scientists for non-commercial use. This is recorded as an incomplete public evidence chain, not evidence that the result is incorrect.

An independent identifier-integrity finding is also present: the main article gives deoxypodophyllotoxin synthase / 2-ODD as GenBank `KT390173.1`, whereas the supplementary sequence heading gives `KT390173.12`. The project treats this as an evidentiary inconsistency requiring explicit review, likely typographical, and does not infer a sequence or biological error from it.

## Current interpretation

The four cases already span distinct forensic states:

1. rich released data that should permit positive reconstruction;
2. versioned publication and computational state that can be pinned;
3. a natural-product workflow with figure-level source data; and
4. a partially reconstructable claim with both missing public derivation evidence and an internal identifier inconsistency.

The next decisive step is byte-level artifact acquisition plus replay. Until that is complete, the project deliberately leaves T6 unresolved for all four cases.
