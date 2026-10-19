# Metabolic Engineering Forensics

Research by Forest Savage on reconstructing bounded metabolic-engineering claims from their published evidence. This repository contains the original comparative protocol, four case manifests, a Python verifier, and the initial findings.

[Open Claim Review](https://forest-savage1234.github.io/casefile-provenance-demo/claim-review/) · [Read the findings](results/initial-audit.md) · [Run the verifier](#run-the-manifest-verifier) · [Verification protocol](methodology/verification-protocol.md)

## Start here

| Resource | What it contains |
|---|---|
| [Claim Review 0.3.2](https://forest-savage1234.github.io/casefile-provenance-demo/claim-review/) | A separate public browser companion for source-bound calculation replay, condition checks, and replicate statistics. Includes a released Cho study workbook and clearly labeled synthetic examples. |
| [Original comparative audit](results/initial-audit.md) | The provisional findings across four publications, including completed artifact acquisition and remaining reconstruction requirements. |
| [Public-evidence probe](results/public-evidence-probe.md) | Source identities, byte hashes, and bounded structural observations from the August 30, 2026 acquisition run. |
| [Protocol](methodology/verification-protocol.md), [case manifests](cases/), and [verifier](verifier/verify.py) | The original research method and executable checks on recorded dependency availability, supplied hashes, and declared findings. |

Claim Review is hosted in a separate repository: [browser source and notices](https://github.com/forest-savage1234/casefile-provenance-demo/tree/main/claim-review). Its published-study example replays a declared productivity calculation from the Cho Figure 4 workbook while keeping unresolved measurement and experimental-context requirements visible.

The browser calculation is later work. The original case manifests and audit here retain their earlier research state; the browser's numerical replay does not update these records or establish complete experimental verification.

## Research question and design

Can digital-forensic verification principles strengthen metabolic-engineering reproducibility by detecting incomplete provenance, inconsistent dependencies, silent state drift, and non-reconstructable claim-to-evidence chains?

One protocol applies the same tests and state semantics across four cases:

1. [Kim et al. (2019)](cases/kim-2019/claim.json), *Engineering of an oleaginous bacterium for the production of fatty acids and fuels*.
2. [Cho et al. (2026)](cases/cho-2026/claim.json), *High-titer, antibiotic-free, pilot-scale production of 1,3-propanediol by engineered Corynebacterium*.
3. [Park et al. (2022)](cases/park-2022/claim.json), *Metabolic engineering of Escherichia coli with electron channelling for the production of natural products*.
4. [Decembrino et al. (2021)](cases/decembrino-2021/claim.json), *Synthesis of (−)-deoxypodophyllotoxin and (−)-epipodophyllotoxin via a multi-enzyme cascade in E. coli*.

Positive reconstruction, partial reconstruction, and failure are all reportable outcomes. Cases are assessed for scientific informativeness rather than the number of defects found.

## What the original audit established

These are the bounded findings recorded in the [initial comparative audit](results/initial-audit.md), not a new assessment of the publications.

| Case | Recorded evidence | Remaining requirement in the original audit |
|---|---|---|
| Kim 2019 | A hash-pinned fed-batch workbook contains five ROP1_34 summary titers and run-level fermentation/GC sheets. | Trace the analytical transformation to the concentration observations. |
| Cho 2026 | A hash-pinned source archive contains 42 workbooks and the reported concentration neighborhood. | Replay the exact titer/productivity derivation and pin the publication state. |
| Park 2022 | A hash-pinned Figure 7 workbook contains the final fed-batch lutein time profile. | Replay the titer and productivity from the released series and time basis. |
| Decembrino 2021 | Downstream mass-conversion and yield arithmetic reconstruct; the article and supplement contain a versioned identifier inconsistency. | Resolve the identifier and obtain the raw analytical/calibration evidence needed for the concentration derivation. |

The original audit leaves the end-to-end reconstruction test, **T6**, unresolved for all four cases. This describes that study record; it does not erase the later bounded calculation available in Claim Review. An identifier inconsistency or incomplete public evidence chain does not establish an incorrect biological result.

## Run the manifest verifier

The verifier uses the Python standard library. CI runs it with Python 3.12.

```sh
git clone https://github.com/forest-savage1234/metabolic-engineering-forensics.git
cd metabolic-engineering-forensics
python verifier/verify.py cases/cho-2026/claim.json
```

The command prints a JSON status, blockers, and generated findings. For the current Cho manifest, the expected status is `INCOMPLETE`: the required `claim-derivation` dependency remains unresolved.

This command evaluates the recorded manifest. It does not download a paper or workbook, perform the biological experiment, or execute the separate browser calculation. Hash checking requires both a local `source` path and a `sha256` in a dependency record; `--root PATH` changes the base directory for those paths.

The original case manifests still contain acquisition-pending notes and null source/hash fields. The later [public-evidence probe](results/public-evidence-probe.md) records successful acquisition and hashes for three artifacts. Read that report for the acquisition result; running these manifests does not repeat it.

To run the existing tests:

```sh
python -m pip install pytest
python -m pytest -q
```

[Tests](tests/test_verify.py) cover missing dependencies, absent reconstruction, explicit reconstruction findings, digest drift, identifier conflicts, and verdict precedence. Passing them establishes software behavior within those tests.

## Verification principles

A publication is not treated as defective merely because an artifact is unavailable, and a biological result is never treated as incorrect without evidence. The verifier reports what can and cannot be established from the available evidence and fails closed when a required dependency is unresolved.

| State | Meaning |
|---|---|
| `VERIFIED` | The bounded claim and required derivation can be reconstructed from identified evidence. |
| `INCOMPLETE` | One or more required dependencies are unavailable or absent. |
| `INCONSISTENT` | Identified artifacts contain a material contradiction requiring review. |
| `UNVERIFIABLE` | Available evidence is insufficient to test the bounded claim. |

The Python implementation combines recorded availability, any supplied hash checks, and declared findings. A `VERIFIED` output depends on a declared T6 pass; the program does not independently perform that scientific reconstruction.

The [full protocol](methodology/verification-protocol.md) covers claim reconstruction, dependency closure, identifier integrity, source-state integrity, transformation traceability, controlled drift detection, failure attribution, and verification overhead.

## Research integrity and status

This is the initial research implementation for ME2026. Its original study findings remain provisional. Published source artifacts are distinguished from derived analysis; uncertainty is recorded explicitly, and conflicting evidence is not silently normalized.

Synthetic perturbations evaluate verifier sensitivity only after the unmodified publication artifacts have been assessed. They are never represented as defects in the source work. Missing provenance is not evidence that an underlying scientific result is false.

For citation metadata, see [CITATION.cff](CITATION.cff).
