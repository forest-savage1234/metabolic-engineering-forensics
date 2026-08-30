# Metabolic Engineering Forensics

**Author: Forest Savage**

An open-source research project testing whether consequential metabolic-engineering claims can be independently reconstructed, internally validated, and traced to their supporting experimental and computational evidence.

## Research question

Can digital-forensic verification principles strengthen metabolic-engineering reproducibility by detecting incomplete provenance, inconsistent dependencies, silent state drift, and non-reconstructable claim-to-evidence chains?

## Design

One verification protocol is applied consistently across three primary case studies:

1. Kim et al. (2019), *Engineering of an oleaginous bacterium for the production of fatty acids and fuels*.
2. Cho et al. (2026), 1,3-propanediol systems metabolic engineering case study.
3. Park et al. (2022), *Metabolic engineering of Escherichia coli with electron channelling for the production of natural products*.

A 2021 podophyllotoxin multi-enzyme cascade study is retained as a benchmark case.

## Verification principle

A publication is not treated as defective merely because an artifact is unavailable, and a biological result is never treated as incorrect without evidence. The verifier reports what can and cannot be established from the available evidence and fails closed when a required dependency is unresolved.

### Core states

- `VERIFIED` — the bounded claim and required derivation can be reconstructed from identified evidence.
- `INCOMPLETE` — one or more required dependencies are unavailable or absent.
- `INCONSISTENT` — identified artifacts contain a material contradiction requiring review.
- `UNVERIFIABLE` — available evidence is insufficient to test the bounded claim.

## Evaluation dimensions

- claim reconstruction
- dependency closure
- identifier integrity
- source-state integrity
- transformation traceability
- controlled drift detection
- failure attribution
- verification overhead

## Research integrity

The project distinguishes published source artifacts from derived analysis, records uncertainty explicitly, avoids silent normalization of conflicting evidence, and does not characterize missing provenance as evidence that an underlying scientific result is false.

## Status

Initial research implementation for ME2026. Results remain provisional until each case has been independently reconstructed and validated.
