# Amsterdam Class 1 Batch2 Formal Approval Review

Last updated: 2026-05-04

Status: technical_review_complete_owner_approval_pending

Owner approval note: as of 2026-05-04, the project owner explicitly deferred approval for this batch while shifting to a Class 1-9 build-first, approval-later strategy. The verdicts below are technical review recommendations and hold decisions, not final owner approval.

This review closes the first formal variable-level pass for the Amsterdam same-name-ready Batch2 Class 1 variables. The review follows four checks: local Amsterdam distribution, comparison with the already approved MIMIC-IV asset, official source/dictionary alignment, and external clinical or epidemiologic plausibility.

## Verdict Summary

| variable | verdict | reason |
| --- | --- | --- |
| `std_oxygen_partial_pressure_bg_allspecimen` | reviewed_approved | Direct Amsterdam blood-gas pO2 rows, including sparse other-specimen rows, match the all-specimen variable identity; kPa conversion is correct and distribution aligns with MIMIC and ICU blood-gas literature. |
| `std_carbon_dioxide_partial_pressure_bg_allspecimen` | reviewed_approved | Direct Amsterdam blood-gas pCO2 rows match the all-specimen variable identity; end-tidal and target rows stay excluded; distribution aligns with MIMIC and blood-gas reference ranges. |
| `std_oxygen_saturation_bg_allspecimen` | reviewed_approved | Direct Amsterdam blood-gas oxygen saturation rows match the all-specimen variable identity; monitor SpO2 and ECMO venous saturation stay excluded; source scale normalization is supported by distribution. |
| `std_oxygen_saturation_bg_arterial_specimen` | not_approved_keep_candidate | Amsterdam lacks a universal structured arterial specimen flag for these retained rows; the candidate removes only explicit venous comments and is nearly identical to the all-specimen asset, so arterial certainty is overclaimed. |
| `std_total_bilirubin` | reviewed_approved | Blood total-bilirubin rows map to total bilirubin, use the expected umol/L to mg/dL conversion, and match MIMIC plus Amsterdam sepsis-epidemiology bilirubin magnitudes. |
| `std_albumin` | reviewed_approved_with_distribution_caveat | Blood albumin rows and g/L to g/dL conversion are official and specific; the Amsterdam measured subset is much lower and smaller than MIMIC, but this is clinically plausible for selected ICU testing and not a source-identity mismatch. |
| `std_inr` | reviewed_approved | INR-unit Prothrombinetijd rows match the INR variable, separate cleanly from PT seconds, and reproduce the approved MIMIC INR distribution closely. |
| `std_pt` | not_approved_keep_candidate | Although the legacy dictionary unit is seconds, the Amsterdam distribution is INR-like, not PT-seconds-like; approving it as `std_pt` would violate cross-database same-name identity. |
| `std_aptt` | reviewed_approved | Direct APTT blood seconds rows match source identity; corrected APTT, targets, CVVH agreements, orders, and free-text inhibitor rows stay excluded; distribution is ICU-plausible and comparable to external APTT literature. |

## Distribution Review

| variable | Amsterdam rows | Amsterdam kept | Amsterdam outliers | Amsterdam p50 | Amsterdam p99 | MIMIC p50 | MIMIC p99 | interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `std_oxygen_partial_pressure_bg_allspecimen` | 688,840 | 688,744 | 96 | 93.0 | 334.0 | 99.0 | 448.0 | Similar center to MIMIC; Amsterdam has less high-tail oxygen exposure than MIMIC but stays within expected ICU blood-gas behavior. |
| `std_carbon_dioxide_partial_pressure_bg_allspecimen` | 694,287 | 694,121 | 166 | 41.0 | 76.0 | 41.0 | 86.0 | Excellent cross-database match at the center and high tail. |
| `std_oxygen_saturation_bg_allspecimen` | 677,490 | 677,276 | 214 | 98.0 | 100.0 | 94.0 | 99.0 | Amsterdam is more arterial/oxygenated in distribution; all-specimen label is still acceptable because no monitor SpO2 is merged. |
| `std_oxygen_saturation_bg_arterial_specimen` | 677,419 | 677,205 | 214 | 98.0 | 100.0 | 97.0 | 99.0 | Distribution alone is plausible, but it does not prove arterial scope because the row set differs from all-specimen by only 71 rows. |
| `std_total_bilirubin` | 58,944 | 58,943 | 1 | 0.5 | 14.9 | 0.5 | 21.7 | Strong match at median; Amsterdam high tail is clinically plausible and slightly less extreme than MIMIC. |
| `std_albumin` | 3,141 | 3,129 | 12 | 1.8 | 3.572 | 3.9 | 5.0 | Much lower and smaller Amsterdam measured subset; official source and unit are clear, so approval carries a distribution caveat. |
| `std_inr` | 193,688 | 193,671 | 17 | 1.26 | 4.41 | 1.3 | 4.8 | Strong cross-database agreement. |
| `std_pt` | 5,800 | 5,776 | 24 | 1.4 | 34.5 | 14.0 | 50.4 | Fails identity check: p50 around 1.4 is INR-like and not PT seconds. |
| `std_aptt` | 198,511 | 196,451 | 2,060 | 44.0 | 130.0 | 33.1 | 150.0 | Higher Amsterdam center is plausible in ICU/heparin-heavy cohorts and still source-consistent. |

## Official Source Alignment

Amsterdam official dictionary review confirmed that the approved rows are `numericitems` laboratory rows with expected labels, units, and source categories:

- pO2: `9996 PO2 (bloed)` and `7433 PO2` in mmHg plus `21214 PO2 (bloed) - kPa`; sparse `9997 pO2 (overig)` is retained only in the all-specimen variable.
- pCO2: `9990 pCO2 (bloed)` and `6846 PCO2` in mmHg plus `21213 PCO2 (bloed) - kPa`; sparse `9991 pCO2 (overig)` is retained only in the all-specimen variable.
- Oxygen saturation blood gas: `12311 O2-Saturatie (bloed)`, `8903 SO2`, and `11543 SO2 (Hb) (bloed)`.
- Total bilirubin: `9945 Bilirubine (bloed)` and `6813 Bili Totaal`, both total bilirubin blood/chemistry rows.
- Albumin: `6801 Albumine chemisch` and `9975 Albumine (imm.) (bloed)`, both blood/chemistry albumin rows in g/L.
- INR: `11893 Prothrombinetijd (bloed)` and `11894 Prothrombinetijd  (bloed)`, both unit `INR`.
- APTT: `11944 APTT  (bloed)` and `17982 APTT (bloed)`, both unit `sec`.

Official dictionary review also supports the two holds:

- `std_oxygen_saturation_bg_arterial_specimen`: source labels say blood/blood-gas but not universal arterial specimen. The source-row filter only removes explicit venous comments.
- `std_pt`: `6789 Protrombinetijd` carries unit `sec`, but the observed value distribution is not seconds-scale.

MIMIC official lab-item alignment remains the cross-database anchor: `50821 pO2`, `50818 pCO2`, `50817 Oxygen Saturation`, `50885 Bilirubin, Total`, `50862 Albumin`, `51237 INR(PT)`, `51274 PT`, and `51275 PTT`.

## External Plausibility Review

Blood-gas ranges and specimen cautions support the pO2, pCO2, and oxygen-saturation decisions. MedlinePlus and StatPearls report arterial blood-gas pO2, pCO2, and SaO2 reference ranges that match the retained units; StatPearls also emphasizes that arterial versus venous differences are largest for PO2 and meaningful for gas interpretation, so an arterial-only variable needs more than a weak comment filter.

Liver and coagulation references support the chemistry/coagulation decisions. Mayo Clinic liver-function guidance treats albumin, bilirubin, and PT as clinically relevant liver-function measures, while Mayo's PT discussion frames PT in seconds and INR as a separate cross-laboratory ratio. This is exactly why the Amsterdam `std_pt` candidate cannot be approved while its p50 remains around 1.4. Cleveland Clinic's PTT guidance gives a usual PTT/aPTT normal range around the low tens of seconds; Amsterdam APTT's higher ICU center is compatible with critical care and anticoagulation exposure rather than a source mismatch.

Published AmsterdamUMCdb analyses provide an additional face-validity check. A Frontiers AmsterdamUMCdb atrial-fibrillation model reports average PO2 near the same order as this build and reports average APTT around the Amsterdam p50 seen here; it also reports a "Prothrombin Time" average near 1.3 to 1.4, which reinforces that the legacy prothrombin-time source behaves like an INR-like ratio rather than PT seconds. A PLOS One AmsterdamUMCdb Sepsis-3 analysis uses PaO2 and bilirubin in expected ICU/SOFA-style magnitudes, supporting the bilirubin and blood-gas scale checks.

## Per-Variable Review Blocks

### `std_oxygen_partial_pressure_bg_allspecimen`

- Reviewed database distribution: Amsterdam has 688,840 source rows, 688,744 retained standardized rows, 96 outliers, 19,617 patients, 22,420 admissions, and 355 timestamp/source de-duplications. Raw values span -3.0 to 88,888.0 before cleaning; retained values span 1.0 to 599.0 mmHg with p01 33.0, p05 55.0, p50 93.0, p95 191.0, p99 334.0, and mean 104.62.
- Amsterdam source composition: `9996 PO2 (bloed)` contributes 654,064 rows with 653,986 kept; legacy `7433 PO2` contributes 25,372 rows with 25,360 kept; `21214 PO2 (bloed) - kPa` contributes 9,392 rows and is kept after kPa-to-mmHg conversion; sparse `9997 pO2 (overig)` contributes 12 rows, of which 6 are kept. The high raw maximum and negative raw values are removed by the standard range filter.
- Other approved database comparison: approved MIMIC `std_oxygen_partial_pressure_bg_allspecimen` has 697,418 rows, 697,301 kept rows, 71,106 subjects, p50 99.0, p95 341.0, p99 448.0, and mean 126.06. Amsterdam and MIMIC agree well at the median; MIMIC has a higher oxygenation tail, plausibly reflecting a different mix of arterial/venous/unknown specimens and oxygen therapy practice.
- Official alignment: Amsterdam dictionary rows are direct pO2 blood-gas items and include a kPa item that is unit-converted into the mmHg standard. MIMIC's official anchor is item `50821 pO2`. The Amsterdam build retains all-specimen blood-gas sources and does not merge monitor oxygen saturation, ventilator settings, targets, or other non-lab oxygen concepts.
- Clinical and literature plausibility: arterial blood-gas references place PaO2 around 75 to 100 mmHg at sea level, while ICU and all-specimen data can include venous samples and high inspired oxygen exposure. The Amsterdam median near 93.0 and broad upper tail are therefore clinically plausible. AmsterdamUMCdb publications using blood-gas variables provide face validity that pO2 appears in the expected ICU scale.
- Risk and boundary: the sparse `pO2 (overig)` source is appropriate only because this variable is explicitly all-specimen. It must not be reused as arterial-only evidence without a stronger specimen source.
- Review decision: approved for Amsterdam as `reviewed_approved`.

### `std_carbon_dioxide_partial_pressure_bg_allspecimen`

- Reviewed database distribution: Amsterdam has 694,287 source rows, 694,121 retained rows, 166 outliers, 19,647 patients, 22,462 admissions, and 353 de-duplications. Raw values span -1.0 to 3,537.0; retained values span 1.0 to 200.0 mmHg with p01 26.0, p05 30.0, p50 41.0, p95 60.0, p99 76.0, and mean 42.42.
- Amsterdam source composition: `9990 pCO2 (bloed)` contributes 659,456 rows with 659,318 kept; legacy `6846 PCO2` contributes 25,348 rows with 25,323 kept; `21213 PCO2 (bloed) - kPa` contributes 9,464 rows and is kept after kPa-to-mmHg conversion; sparse `9991 pCO2 (overig)` contributes 19 rows with 16 kept.
- Other approved database comparison: approved MIMIC `std_carbon_dioxide_partial_pressure_bg_allspecimen` has 696,693 rows, 696,676 kept rows, 71,095 subjects, p50 41.0, p95 66.0, p99 86.0, and mean 43.32. The two databases are nearly identical at the center and close in the upper tail.
- Official alignment: Amsterdam dictionary rows are direct pCO2 blood-gas items, with the kPa source converted into the standard mmHg unit. MIMIC's official anchor is item `50818 pCO2`. End-tidal CO2, ventilator settings, target CO2 values, and non-lab concepts remain excluded.
- Clinical and literature plausibility: arterial blood-gas references place PaCO2 around the high 30s to low 40s mmHg, and ICU blood-gas data should have a meaningful high tail from ventilatory and metabolic derangements. Amsterdam p50 41.0 and p99 76.0 match both MIMIC and clinical expectations.
- Risk and boundary: as with pO2, sparse `overig` rows are acceptable for all-specimen identity but not for a future arterial-only claim.
- Review decision: approved for Amsterdam as `reviewed_approved`.

### `std_oxygen_saturation_bg_allspecimen`

- Reviewed database distribution: Amsterdam has 677,490 source rows, 677,276 retained rows, 214 outliers, 19,613 patients, 22,414 admissions, and 2 de-duplications. Raw values show mixed scale and erroneous entries, spanning -0.97000003 to 8,101,208.0 with p50 0.98000002. After scale normalization and cleaning, retained values span 1.0 to 100.0 percent with p01 60.0, p05 87.0, p50 98.0, p95 99.0, p99 100.0, and mean 95.86.
- Amsterdam source composition: `12311 O2-Saturatie (bloed)` contributes 652,899 rows with 652,733 kept; `8903 SO2` contributes 24,404 rows with 24,363 kept; `11543 SO2 (Hb) (bloed)` contributes 187 rows with 180 kept. The retained data normalize fractional 0 to 1 style entries and percent-style entries into percent.
- Other approved database comparison: approved MIMIC all-specimen oxygen saturation has 239,342 rows, 239,322 kept rows, 42,284 subjects, p50 94.0, p99 99.0, and mean 83.58. MIMIC's explicit arterial version has 141,339 rows, p50 97.0, p99 99.0, and mean 95.32. Amsterdam's all-specimen distribution is closer to MIMIC arterial because the Amsterdam retained blood-gas sources appear heavily arterial/oxygenated, but that does not change the formal all-specimen identity.
- Official alignment: Amsterdam source labels are blood or blood-gas oxygen saturation concepts. MIMIC's official anchor is item `50817 Oxygen Saturation`. The Amsterdam build excludes monitor SpO2, ECMO venous oxygen saturation, target saturation, and device/therapy settings, so this is a blood-gas saturation variable rather than a bedside monitor vital sign.
- Clinical and literature plausibility: blood-gas references place arterial SaO2 near the mid-to-high 90s in normal conditions. ICU all-specimen oxygen saturation can be lower when venous or mixed samples enter, but Amsterdam's source mix plausibly yields a high median. The scale correction is supported by the raw p50 near 0.98 and the retained p50 near 98.0.
- Risk and boundary: the high oxygenated distribution should not be used as proof that every row is arterial. It supports blood-gas saturation identity and percent normalization only.
- Review decision: approved for Amsterdam as `reviewed_approved`.

### `std_oxygen_saturation_bg_arterial_specimen`

- Reviewed database distribution: Amsterdam has 677,419 source rows, 677,205 retained rows, 214 outliers, 19,613 patients, 22,414 admissions, and 73 de-duplications. Retained values span 1.0 to 100.0 percent with p01 60.0, p05 87.0, p50 98.0, p95 99.0, p99 100.0, and mean 95.86.
- Amsterdam source composition: this candidate uses the same three blood-gas saturation sources as the all-specimen variable: `12311 O2-Saturatie (bloed)`, `8903 SO2`, and `11543 SO2 (Hb) (bloed)`. It retains only 71 fewer source rows than the all-specimen build, mostly by excluding explicit venous comments rather than by applying a universal structured arterial specimen identifier.
- Other approved database comparison: MIMIC separates all-specimen and arterial oxygen saturation by explicit specimen information. MIMIC all-specimen has 239,342 rows with p50 94.0 and p01 34.0, while MIMIC arterial has 141,339 rows with p50 97.0 and p01 78.0. Amsterdam's candidate does not create a comparable source separation; it is nearly the same row set as Amsterdam all-specimen.
- Official alignment: Amsterdam dictionary labels support blood-gas oxygen saturation but do not provide universal arterial certainty for every retained row. MIMIC's approved arterial standard is anchored by explicit arterial specimen filtering around item `50817`.
- Clinical and literature plausibility: the distribution is clinically plausible for arterial SaO2, but plausibility alone is insufficient because all-specimen Amsterdam saturation is already very similar. Blood-gas references and specimen cautions make arterial/venous distinction clinically meaningful, especially for interpreting paired blood-gas panels.
- Risk and boundary: approving this candidate would overstate specimen certainty and could mislead downstream models that treat arterial and all-specimen oxygen saturation as distinct evidence.
- Review decision: not approved; keep as candidate until a stronger Amsterdam arterial specimen rule is found.

### `std_total_bilirubin`

- Reviewed database distribution: Amsterdam has 58,944 source rows, 58,943 retained rows, 1 outlier, 10,962 patients, 12,791 admissions, and 162 de-duplications. Raw values are on the Amsterdam umol/L scale and span 0.0 to 926.0. After conversion to mg/dL, retained values span 0.1 to 54.1 with p01 0.1, p05 0.2, p50 0.5, p95 4.5, p99 14.9, and mean 1.235.
- Amsterdam source composition: `9945 Bilirubine (bloed)` contributes 57,224 rows with all kept; `6813 Bili Totaal` contributes 1,720 rows with 1,719 kept. The conversion factor is the expected bilirubin umol/L-to-mg/dL conversion.
- Other approved database comparison: approved MIMIC `std_total_bilirubin` has 1,575,798 rows, 1,575,693 kept rows, 184,395 subjects, p50 0.5, p95 5.9, p99 21.7, and mean 1.496. Amsterdam and MIMIC match at the median; MIMIC has a somewhat heavier upper tail, but both are plausible ICU chemistry distributions.
- Official alignment: Amsterdam source rows are total bilirubin blood/chemistry rows, not direct/conjugated bilirubin, body-fluid bilirubin, or urine/other specimen concepts. MIMIC's official anchor is item `50885 Bilirubin, Total`.
- Clinical and literature plausibility: liver-function guidance treats bilirubin as a liver/biliary and hemolysis-related marker, and Sepsis/SOFA-style ICU studies use bilirubin on the same clinical scale. Amsterdam p50 0.5 and high-tail values are compatible with mixed ICU patients and severe liver dysfunction outliers.
- Risk and boundary: direct bilirubin and non-blood bilirubin must stay excluded. The approved variable is total bilirubin in blood only.
- Review decision: approved for Amsterdam as `reviewed_approved`.

### `std_albumin`

- Reviewed database distribution: Amsterdam has 3,141 source rows, 3,129 retained rows, 12 outliers, 895 patients, 942 admissions, and no de-duplications. Raw values are on the Amsterdam g/L scale and span 0.0 to 114.0. After conversion to g/dL, retained values span 0.5 to 6.1 with p01 0.7, p05 1.0, p50 1.8, p95 2.8, p99 3.572, and mean 1.891.
- Amsterdam source composition: `6801 Albumine chemisch` contributes 3,064 rows with 3,052 kept; `9975 Albumine (imm.) (bloed)` contributes 77 rows with all kept. Both are blood/chemistry albumin sources and are converted from g/L to g/dL.
- Other approved database comparison: approved MIMIC `std_albumin` has 1,032,266 rows, 1,032,253 kept rows, 166,448 subjects, p50 3.9, p95 4.8, p99 5.0, and mean 3.754. Amsterdam is much smaller and substantially lower at the median, so this is the main distribution caveat in the approved Batch2 set.
- Official alignment: Amsterdam dictionary labels and units support serum/blood albumin identity. MIMIC's official anchor is item `50862 Albumin`. Amsterdam albumin-drug administration, urine albumin, CSF albumin, dialysate albumin, and other body-fluid concepts are excluded.
- Clinical and literature plausibility: liver-function guidance lists albumin as a liver-related protein marker and notes low values can reflect liver, gastrointestinal, kidney-related, inflammatory, or critical illness contexts. A low Amsterdam measured subset is plausible if albumin was tested selectively or in sicker patients, but it should be visible to reviewers because it differs strongly from MIMIC.
- Risk and boundary: the source identity and unit conversion are strong, but the distribution suggests Amsterdam albumin should be reviewed again during Class 1 clinical approval, especially for whether this legacy source captures a selected subgroup rather than routine serum albumin.
- Review decision: approved for Amsterdam as `reviewed_approved_with_distribution_caveat`.

### `std_inr`

- Reviewed database distribution: Amsterdam has 193,688 source rows, 193,671 retained rows, 17 outliers, 18,915 patients, 21,560 admissions, and 2 de-duplications. Raw values span 0.0 to 159.0; retained values span 0.68 to 7.4 with p01 0.94, p05 1.0, p50 1.26, p95 2.35, p99 4.41, and mean 1.419.
- Amsterdam source composition: `11893 Prothrombinetijd (bloed)` contributes 66,847 rows with 66,845 kept; `11894 Prothrombinetijd  (bloed)` contributes 126,841 rows with 126,826 kept. Both carry INR-unit evidence in the Amsterdam dictionary and are kept as ratio-scale INR rows.
- Other approved database comparison: approved MIMIC `std_inr` has 1,767,351 rows with no outliers removed, 195,465 subjects, p50 1.3, p95 3.2, p99 4.8, and mean 1.601. Amsterdam matches MIMIC closely at the median and high tail.
- Official alignment: Amsterdam dictionary rows are prothrombin-time blood rows with unit `INR`; MIMIC's official anchor is item `51237 INR(PT)`. The build keeps these rows separate from PT seconds.
- Clinical and literature plausibility: PT/INR guidance describes INR as a ratio used to compare clotting results across laboratories, with typical non-anticoagulated values near 1 and therapeutic anticoagulation often higher. Amsterdam p50 1.26 and p99 4.41 are ICU-plausible and align with MIMIC.
- Risk and boundary: the main risk is accidental blending with seconds-scale PT fields. This review explicitly separates Amsterdam INR from the held PT candidate.
- Review decision: approved for Amsterdam as `reviewed_approved`.

### `std_pt`

- Reviewed database distribution: Amsterdam has 5,800 source rows, 5,776 retained rows, 24 outliers, 894 patients, 937 admissions, and no de-duplications. Raw values span 0.0 to 1,903.0; retained values span 1.0 to 288.0 with p01 1.0, p05 1.1, p50 1.4, p95 2.7, p99 34.5, and mean 2.846.
- Amsterdam source composition: the candidate is based on `6789 Protrombinetijd`. The Amsterdam dictionary labels the unit as seconds, but most retained values are concentrated near 1.0 to 2.0, which is ratio-like rather than PT-seconds-like.
- Other approved database comparison: approved MIMIC `std_pt` has 1,767,026 rows, 1,767,024 kept rows, 195,466 subjects, p50 14.0, p95 33.9, p99 50.4, and mean 17.386. The Amsterdam p50 1.4 is not comparable to MIMIC PT seconds; it is much closer to the Amsterdam and MIMIC INR medians.
- Official alignment: this is a conflict between dictionary metadata and observed data behavior. MIMIC's official PT anchor is `51274 PT` in seconds, while Mayo Clinic PT guidance frames PT as seconds and INR as a separate ratio. Amsterdam item `6789` therefore cannot be approved as `std_pt` solely because the legacy dictionary says `sec`.
- Clinical and literature plausibility: PT seconds usually sit around the low teens in non-anticoagulated patients. A median of 1.4 seconds is physiologically implausible for PT but clinically plausible as an INR-like ratio. Published AmsterdamUMCdb work reporting prothrombin-time-like averages near 1.3 to 1.4 reinforces the suspicion that the legacy source behaves as a ratio field.
- Risk and boundary: approving this candidate would break same-name semantics across databases and could silently mix PT seconds with INR-like values.
- Review decision: not approved; keep as candidate pending source-scale adjudication or row-level scale separation.

### `std_aptt`

- Reviewed database distribution: Amsterdam has 198,511 source rows, 196,451 retained rows, 2,060 outliers, 18,898 patients, and 21,546 admissions. Raw values span 0.0 to 240.0; retained values span 1.0 to 200.0 seconds with p01 28.0, p05 31.0, p50 44.0, p95 86.0, p99 130.0, and mean 50.78.
- Amsterdam source composition: `11944 APTT  (bloed)` contributes 130,281 rows with 128,908 kept; `17982 APTT (bloed)` contributes 68,230 rows with 67,543 kept. Corrected APTT, target APTT, CVVH agreements, procedure orders, and free-text inhibitor-related rows are excluded.
- Other approved database comparison: approved MIMIC `std_aptt` has 1,618,857 rows with no outliers removed, 190,938 subjects, p50 33.1, p95 92.8, p99 150.0, and mean 43.095. Amsterdam has a higher median but similar ICU-scale high tail.
- Official alignment: Amsterdam dictionary rows are direct APTT blood rows in seconds. MIMIC's official anchor is item `51275 PTT`. The source set is specific and does not mix in PT/INR or anticoagulation targets.
- Clinical and literature plausibility: PTT/aPTT guidance places normal values around the low tens of seconds and notes that high values can reflect heparin therapy, liver disease, clotting-factor problems, or other ICU-relevant conditions. Amsterdam p50 44.0 is elevated relative to normal outpatient ranges but plausible for a critical-care cohort.
- Risk and boundary: the high center should be flagged for clinical review but does not look like a unit or source-identity failure. Outliers above the approved ceiling are removed.
- Review decision: approved for Amsterdam as `reviewed_approved`.

## Technical Recommendation

When the owner later opens the approval wave, the technical recommendation is to promote these AmsterdamUMCdb-1.0.2 mappings and local Layer 5 assets to `reviewed_approved`:

1. `std_oxygen_partial_pressure_bg_allspecimen`
2. `std_carbon_dioxide_partial_pressure_bg_allspecimen`
3. `std_oxygen_saturation_bg_allspecimen`
4. `std_total_bilirubin`
5. `std_albumin`
6. `std_inr`
7. `std_aptt`

The technical recommendation is to keep these AmsterdamUMCdb-1.0.2 assets as candidates:

1. `std_oxygen_saturation_bg_arterial_specimen`
2. `std_pt`

## Required Follow-Up

`std_oxygen_saturation_bg_arterial_specimen` should either find a stronger structured specimen source or remain unapproved for Amsterdam 1.0.2. The current evidence is suitable for all-specimen blood-gas oxygen saturation, not for arterial certainty.

`std_pt` should not be published as PT seconds under the current mapping. The next review should decide whether itemid `6789` is a mislabeled ratio-like legacy field, a mixed-scale field requiring row-level separation, or a non-publishable local legacy item.

## References

- AmsterdamUMCdb official repository and dictionary: https://github.com/AmsterdamUMC/AmsterdamUMCdb
- AmsterdamUMCdb official dictionary file: https://raw.githubusercontent.com/AmsterdamUMC/AmsterdamUMCdb/refs/heads/master/amsterdamumcdb/dictionary/dictionary.csv
- MIMIC official lab item CodeSystem: https://mimic.mit.edu/fhir/CodeSystem-mimic-d-labitems.html
- MedlinePlus blood gases: https://medlineplus.gov/ency/article/003855.htm
- StatPearls arterial blood gas review: https://www.ncbi.nlm.nih.gov/books/NBK536919/
- Mayo Clinic liver function tests: https://www.mayoclinic.org/tests-procedures/liver-function-tests/about/pac-20394595
- Mayo Clinic prothrombin time test: https://www.mayoclinic.org/tests-procedures/prothrombin-time/about/pac-20384661
- Cleveland Clinic partial thromboplastin time: https://my.clevelandclinic.org/health/diagnostics/25101-partial-thromboplastin-time
- Frontiers AmsterdamUMCdb atrial-fibrillation model: https://www.frontiersin.org/articles/10.3389/fcvm.2022.897709/full
- PLOS One AmsterdamUMCdb Sepsis-3 epidemiology: https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0304133
