# Verification Protocol v0.1

Author: Forest Savage

## Purpose

Evaluate bounded published metabolic-engineering claims using a common forensic protocol. The protocol is fixed across cases before comparative conclusions are drawn.

## Unit of analysis

A **bounded claim** is one quantitative or mechanistic published assertion selected before reconstruction begins. Each claim is represented as a directed dependency graph from source evidence through transformations to the published assertion.

## Evidence classes

1. Source observation — raw or minimally processed experimental measurement.
2. Identity assertion — organism, strain, gene, enzyme, metabolite, construct, reaction, instrument, software, or model identity.
3. State assertion — version, genotype, configuration, parameter set, environmental condition, or computational state.
4. Transformation — calibration, normalization, conversion, preprocessing, model execution, statistical operation, or other derivation.
5. Derived observation — value produced by an explicit transformation.
6. Scientific assertion — interpretation or conclusion supported by preceding evidence.

## Required provenance fields

Where applicable, record:

- persistent source identifier or citation
- retrieval date
- artifact filename/path
- cryptographic digest when bytes are available
- asserted entity identifier and version
- producing activity/transformation
- transformation parameters
- software/model/reference state
- inputs and outputs
- units
- uncertainty/replication information
- relationship to the bounded claim

## Verification tests

### T1 — Claim identity
Can the exact claim being tested be located and represented without interpretive ambiguity?

### T2 — Dependency closure
Can every dependency necessary to derive the claim be identified?

### T3 — Identifier integrity
Are material biological, chemical, computational, and experimental entities identified consistently across artifacts?

### T4 — Source-state integrity
Can the exact relevant state of each mutable dependency be established?

### T5 — Transformation traceability
Can each consequential transformation between source observation and claim be identified, including parameters and required reference state?

### T6 — Reconstruction
Can the bounded claim be independently recomputed or otherwise reconstructed from the released evidence to a prespecified tolerance?

### T7 — Controlled drift detection
When a recorded dependency is intentionally changed in a controlled test, does verification detect that the evidentiary state no longer matches the reference state?

### T8 — Attribution
Can the verifier localize the dependency or transformation responsible for the detected divergence?

### T9 — Fail-closed behavior
Does unresolved evidence yield an explicit unresolved state rather than an implicit pass?

### T10 — Overhead
What additional storage, metadata, computation, and human annotation are required by the verification layer?

## Outcome states

`VERIFIED`: required evidence is available and the bounded derivation satisfies the applicable verification tests.

`INCOMPLETE`: the derivation is identifiable but at least one required dependency is absent or unavailable.

`INCONSISTENT`: material artifacts disagree about a dependency or state and the contradiction cannot be resolved without an explicit adjudication step.

`UNVERIFIABLE`: the available evidence is insufficient to conduct the required verification.

States describe the **public evidentiary package**, not the truth or validity of the underlying biological result.

## Anti-cherry-picking rule

The same tests and state semantics are applied to all primary cases. A case is not excluded because it reconstructs successfully, contains no interesting defect, or contradicts the motivating hypothesis. Positive reconstruction, partial reconstruction, and failure are all reportable outcomes.

## Perturbation rule

Synthetic perturbations are clearly labeled and never represented as defects in the source publication. Perturbations test verifier sensitivity and attribution only after the unmodified case has been evaluated.

## Reporting rule

Every reported finding must include the source artifact, observed fact, verification test, resulting state, and the narrowest defensible interpretation. Claims about downstream biological or pharmaceutical safety remain hypotheses unless directly evaluated.
