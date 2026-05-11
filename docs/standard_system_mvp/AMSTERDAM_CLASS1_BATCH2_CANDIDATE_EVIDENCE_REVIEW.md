# Amsterdam Class 1 Batch2 Candidate Evidence Review

Last updated: 2026-05-04

Status: candidate_evidence_superseded_by_formal_review

This note records the candidate source boundaries for the Amsterdam same-name-ready Batch2 Class 1 variables. It is intentionally not a formal approval review. Variable-level approval is reserved for the next review pass.

Formal review result: see `docs/standard_system_mvp/AMSTERDAM_CLASS1_BATCH2_FORMAL_APPROVAL_REVIEW.md`. That review promotes seven variables to `reviewed_approved` and keeps `std_oxygen_saturation_bg_arterial_specimen` plus `std_pt` as candidates.

## Batch Scope

| variable | canonical unit | retained Amsterdam source itemids | candidate boundary |
| --- | --- | --- | --- |
| `std_oxygen_partial_pressure_bg_allspecimen` | `mmHg` | `7433 PO2, 9996 PO2 (bloed), 9997 pO2 (overig), 21214 PO2 (bloed) - kPa` | `Amsterdam blood-gas pO2 blood and other-specimen numericitems are retained for the all-specimen candidate; kPa rows are converted to mmHg; monitor SpO2 and target oxygen rows are excluded.` |
| `std_carbon_dioxide_partial_pressure_bg_allspecimen` | `mmHg` | `6846 PCO2, 9990 pCO2 (bloed), 9991 pCO2 (overig), 21213 PCO2 (bloed) - kPa` | `Amsterdam blood-gas pCO2 blood and other-specimen numericitems are retained for the all-specimen candidate; kPa rows are converted to mmHg; end-tidal CO2 and target CO2 rows are excluded.` |
| `std_oxygen_saturation_bg_allspecimen` | `percent` | `8903 SO2, 11543 SO2 (Hb) (bloed), 12311 O2-Saturatie (bloed)` | `Amsterdam blood-gas oxygen-saturation rows are retained; O2-Saturatie fraction-scale rows are converted to percent; monitor SpO2, target SpO2, and ECMO venous saturation rows are excluded.` |
| `std_oxygen_saturation_bg_arterial_specimen` | `percent` | `8903 SO2, 11543 SO2 (Hb) (bloed), 12311 O2-Saturatie (bloed)` | `Amsterdam blood-gas oxygen-saturation arterial-specimen candidate retains blood-gas SO2 rows while excluding rows explicitly commented as venous; the absence of a universal structured specimen flag must remain visible during review.` |
| `std_total_bilirubin` | `mg/dL` | `6813 Bili Totaal, 9945 Bilirubine (bloed)` | `Amsterdam total bilirubin blood/chemistry rows are retained and converted from umol/L scale to mg/dL; conjugated, urine, ascites, drain, and other-fluid bilirubin rows are excluded.` |
| `std_albumin` | `g/dL` | `6801 Albumine chemisch, 9975 Albumine (imm.) (bloed)` | `Amsterdam blood/chemistry albumin rows are retained and converted from g/L to g/dL; liquor, urine, dialysate, and drug albumin rows are excluded.` |
| `std_inr` | `unitless` | `11893 Prothrombinetijd (bloed), 11894 Prothrombinetijd  (bloed)` | `Amsterdam Prothrombinetijd rows with INR unit are retained for std_inr; PT seconds rows, medication rows, and target/process rows are excluded.` |
| `std_pt` | `sec` | `6789 Protrombinetijd` | `Amsterdam legacy Protrombinetijd rows are the only seconds-labeled candidate source for std_pt, but their distribution is INR-like and must be reviewed before approval.` |
| `std_aptt` | `sec` | `11944 APTT  (bloed), 17982 APTT (bloed)` | `Amsterdam direct APTT blood seconds rows are retained; corrected APTT, target APTT, CVVH treatment targets, procedure orders, and free-text inhibitor comments are excluded.` |

## Runtime Evidence

Runtime evidence is stored under each variable directory at:

- `runtime/amsterdamumcdb_1_0_2_first_candidate_execution`
- `runtime/amsterdamumcdb_1_0_2_rerun_repro_check`

All nine variables completed governed first execution, rerun execution, and reproducibility comparison. This candidate evidence is now interpreted through the formal review file linked above.

| variable | first validation | rerun validation | reproducibility | source rows | retained rows | outlier rows | patients | admissions | kept p50 | kept p99 |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `std_oxygen_partial_pressure_bg_allspecimen` | pass | pass | pass | 689,195 | 688,744 | 96 | 19,617 | 22,420 | 93.0 | 334.0 |
| `std_carbon_dioxide_partial_pressure_bg_allspecimen` | pass | pass | pass | 694,640 | 694,121 | 166 | 19,647 | 22,462 | 41.0 | 76.0 |
| `std_oxygen_saturation_bg_allspecimen` | pass | pass | pass | 677,492 | 677,276 | 214 | 19,613 | 22,414 | 98.0 | 100.0 |
| `std_oxygen_saturation_bg_arterial_specimen` | pass | pass | pass | 677,492 | 677,205 | 214 | 19,613 | 22,414 | 98.0 | 100.0 |
| `std_total_bilirubin` | pass | pass | pass | 59,106 | 58,943 | 1 | 10,962 | 12,791 | 0.5 | 14.9 |
| `std_albumin` | pass | pass | pass | 3,141 | 3,129 | 12 | 895 | 942 | 1.8 | 3.572 |
| `std_inr` | pass | pass | pass | 193,690 | 193,671 | 17 | 18,915 | 21,560 | 1.26 | 4.41 |
| `std_pt` | pass | pass | pass | 5,800 | 5,776 | 24 | 894 | 937 | 1.4 | 34.5 |
| `std_aptt` | pass | pass | pass | 198,511 | 196,451 | 2,060 | 18,898 | 21,546 | 44.0 | 130.0 |

## Review Notes

Blood-gas all-specimen candidates intentionally include blood-gas blood rows and the sparse Amsterdam `overig` rows where present. They do not merge monitor SpO2, end-tidal CO2, target oxygen/CO2 rows, or device/ECMO saturation rows.

`std_oxygen_saturation_bg_allspecimen` and `std_oxygen_saturation_bg_arterial_specimen` use source-specific scale normalization: `O2-Saturatie (bloed)` is treated as fraction scale and converted to percent, while `SO2` and `SO2 (Hb) (bloed)` are treated as percent-scale sources. The arterial-specimen candidate excludes rows explicitly commented as venous, but Amsterdam does not expose a universal structured specimen flag in these rows; this must be reviewed before approval.

`std_total_bilirubin` and `std_albumin` preserve routine blood/chemistry identity and exclude urine, liquor, drain, ascites, dialysate, drug, and other-fluid neighboring rows.

`std_inr` is separated from `std_pt`: INR-unit `Prothrombinetijd` rows are retained for `std_inr`, while the legacy seconds-labeled `Protrombinetijd` rows are retained only as a `std_pt` candidate. The `std_pt` distribution is INR-like despite the seconds unit label and should be treated as the highest-risk Batch2 review item.

`std_aptt` retains direct blood APTT seconds rows only. Corrected APTT, target APTT, CVVH treatment targets, procedure orders, and free-text inhibitor comments remain outside the candidate mapping.

## Approval Gate

The formal review has now closed the first variable-level pass. Only the seven variables explicitly listed as `reviewed_approved` in `AMSTERDAM_CLASS1_BATCH2_FORMAL_APPROVAL_REVIEW.md` may be promoted. `std_oxygen_saturation_bg_arterial_specimen` and `std_pt` must remain candidates until their source-boundary problems are resolved.
