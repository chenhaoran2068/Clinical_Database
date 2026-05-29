# SICdb `std_aado2` Sparse-Source Firewall Review

- Finalized: 2026-05-29
- Variable: `std_aado2`
- Database: `SICdb-1.0.8`
- Final status: `reviewed_approved_unavailable`
- Core usable row count: `0`
- Audit-only source rows: `5`

## Final Verdict

SICdb direct `std_aado2` is owner-approved unavailable. The reviewed SICdb source surface contains a direct-looking candidate, `LaboratoryID 679 pO2 (A-a) (T) (BGA)`, but it has only five numeric rows and is treated as a structural device/interface sparse artifact rather than a usable population-level laboratory asset.

The five candidate rows are retained only in the local inactive audit stub:

`Methods/Clinical_Database/local_work/Layer 3/SICdb-1.0.8/laboratory/std_aado2/sparse_audit_stub.json`

They do not enter the core Layer 5 feature matrix.

## Source Boundary

Accepted as audit-only evidence:

- `LaboratoryID 679`
- label: `pO2 (A-a) (T) (BGA)`
- unit: `mmHg`
- source rows: `5`
- value range: `27.4` to `209.7` mmHg
- median: `103.2` mmHg

Permanently excluded adjacent source:

- `LaboratoryID 680`
- label: `pO2 (A/a) (T) (BGA)`
- reason: `A/a` ratio semantics are not equivalent to `A-a` oxygen-gradient semantics; the LOINC metadata points to arterial pO2 and conflicts with the local label.

## Timing Finding

SICdb laboratory offsets are second offsets. For candidate `679`:

- strict ICU stay window: `1/5`
- peri-admission `[-6h, ICU discharge]`: `4/5`
- post-ICU long tail: `1/5`

The peri-admission rows are compatible with ED/OR or pre-ICU blood-gas documentation, but the source remains too sparse to support a governed direct variable.

## Downstream Contract

- Direct SICdb `std_aado2` must return an empty unavailable/blocked asset.
- The audit-only rows must not be used in default clinical exposure analyses.
- Missing SICdb `std_aado2` rows must not be interpreted as normal oxygenation or absence of A-a gradient measurement.
- SICdb A-aDO2 analyses must use a separately approved formula-derived `std_aado2_calc` asset.
- Do not substitute PaO2/FiO2 ratio or PaO2 for A-aDO2.

## Cross-Database Context

MIMIC-IV has 13,744 retained direct arterial A-aDO2 rows from its direct analyzer source. SICdb has only five direct-looking rows despite rich PaO2 and PaCO2 blood-gas surfaces. This contrast supports treating the SICdb direct source as a reporting/interface artifact, not as a usable direct source.
