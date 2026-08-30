# Public Evidence Probe — 2026-08-30

## Scope

This note records the durable, provenance-only outcome of the `Public evidence probe` workflow run. Third-party source bytes were downloaded only inside the workflow and were not committed or redistributed. The durable record is limited to source identity, byte hashes, artifact structure, formulas, and bounded observations needed to assess whether later replay is feasible.

This is **not** a declaration that any case has passed T6. Artifact acquisition and structural inspection are distinct from end-to-end replay of the bounded scientific claim.

## Run result

Workflow run `33292912220` completed successfully. The `probe` job completed every step, including public-evidence acquisition and upload of the provenance-only result artifact.

The resulting artifact was named `public-evidence-probe` and had digest:

`sha256:a8fca15edce12aa1a1dd673bc3fa7ee55268b7051ed9ef4b8abd36e0bbd06695`

## Acquired public artifacts

| Case | Public artifact | HTTP | Bytes | SHA-256 | Bounded structural observation |
|---|---|---:|---:|---|---|
| Kim et al. 2019 | Supplementary Dataset 1 — raw fed-batch fermentations (XLSX) | 200 | 1,106,968 | `d8d9e6c66ec6646a74749e5a92aa584ba6e7ff95e14342d8b26b77d6c7f32be0` | Workbook contains the five ROP1_34 summary values 50.2, 47.2, 46.7, 49.2, and 50.1, plus run-level fermentation/GC sheets and formulas. |
| Park et al. 2022 | Source Data Fig. 7 — final lutein fed-batch (XLSX) | 200 | 9,870 | `c450b75846a6af5071652ffcca8ac2afa7692ad2e6896dae37455f2c26ca1cf4` | Workbook is readable and exposes the Fig. 7b fed-batch time-profile table with a `Lutein (mg/L)` series. |
| Cho et al. 2026 | Figshare source-data archive (ZIP) | 200 | 384,800 | `c936d72329b05a2a336a8419d6074d7a74c0705c9711ef701774e549847f876c` | Archive contains 42 XLSX members. Bounded inspection finds 1,3-PDO source-data tables, including values 141.517 and 141.5 in the released workbook set. |

No acquisition error was reported for any of the three probed artifacts.

## What changed in the evidentiary state

### Kim et al. 2019

The project can now distinguish a mere publisher claim that a raw-data workbook exists from successful byte-level acquisition of a specific workbook. The acquired workbook is hash-pinned and contains the five ROP1_34 titers already described in the paper/SI. It also contains run-level fermentation and GC worksheets and formulas, making a deeper replay plausible.

That does **not** yet establish that the workbook starts from raw instrument observations rather than processed analytical values. T6 remains unresolved until the complete transformation path to the bounded 50.2 g/L claim is replayed and its inputs are classified.

### Park et al. 2022

The Fig. 7 source workbook is now byte-pinned and structurally verified rather than merely linked. The relevant lutein time-profile table is present. The next step is to identify the final LUT5MH1 observations and recompute both the reported 218.0 mg/L titer and 5.01 mg/L/h productivity from the released values and stated time basis.

### Cho et al. 2026

The Figshare source-data archive is now byte-pinned and its 42 workbook members enumerated. Bounded inspection independently locates the reported final-scale concentration neighborhood: released source workbooks contain 141.517 and 141.5 values associated with 1,3-PDO data. The archive therefore materially strengthens the positive-reconstruction path.

T6 still requires reconstruction of the exact 141.5 g/L and 2.95 g/L/h claim from the correct experimental series, with the publication/correction state and calculation basis pinned.

### Decembrino et al. 2021

No new public raw analytical artifact was acquired by this probe. The prior finding therefore stands: the downstream arithmetic is reproducible, but the public evidence package remains insufficient to replay the upstream derivation of 196 µM, and the `KT390173.1` / `KT390173.12` identifier conflict remains an explicit integrity issue.

## Decision

The byte-level acquisition milestone is complete for the three public artifacts targeted by this probe. The repository should no longer describe acquisition itself as wholly pending.

The remaining scientific work is narrower and more defensible: **claim-specific replay**. T6 remains unresolved for all four cases until each bounded result is either reconstructed from the released evidence or explicitly shown to terminate at a missing evidentiary input.
