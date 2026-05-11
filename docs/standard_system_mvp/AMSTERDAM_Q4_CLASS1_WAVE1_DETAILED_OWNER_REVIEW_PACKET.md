# Amsterdam Q4 Class1 Wave1 Detailed Owner Review Packet

Last updated: 2026-05-08

Status: reviewed_approved_by_owner

Owner approval note: the project owner explicitly approved all ten variables on 2026-05-08. This packet now records both the technical review and the owner approval decision. Caveat-bearing variables remain approved but must carry their documented caveats in downstream review.

The review follows the active `VARIABLE_REVIEW_REPORTING_STANDARD.md`: Amsterdam distribution, approved MIMIC comparison, official/source alignment, external clinical or epidemiologic plausibility, risk/boundary review, and explicit technical recommendation.

## Technical Recommendation Summary

| variable | technical recommendation | unit | Amsterdam kept | MIMIC kept | reason |
| --- | --- | --- | ---: | ---: | --- |
| `std_anion_gap` | technical_review_recommend_approve_with_caveat | `mEq/L` | 464,116 | 3,925,396 | Direct Amsterdam blood anion-gap source is locked and scale is plausible; Amsterdam center is lower than MIMIC, consistent with formula/analyzer and albumin-sensitive anion-gap behavior, so keep a distribution caveat. |
| `std_amylase` | technical_review_recommend_approve | `IU/L` | 36,730 | 96,248 | Blood/plasma amylase itemids and IU/L-equivalent source units are specific; other-fluid amylase families remain excluded and the distribution matches the approved MIMIC order of magnitude. |
| `std_lipase` | technical_review_recommend_approve | `IU/L` | 3,436 | 293,090 | Blood lipase source is specific, E/L is IU/L-equivalent, and the heavy pancreatitis tail is clinically expected without source-scale conflict. |
| `std_ferritin` | technical_review_recommend_approve_with_caveat | `ng/mL` | 993 | 189,400 | Blood ferritin source and ug/L-to-ng/mL equivalence are direct; the Amsterdam set is sparse and selected with an inflammatory high tail, so keep a sparse/high-tail caveat. |
| `std_haptoglobin` | technical_review_recommend_approve_with_caveat | `mg/dL` | 375 | 47,962 | Blood haptoglobin source and g/L-to-mg/dL conversion are direct; the Amsterdam set is sparse, so the recommendation carries a sparse-source caveat. |
| `std_magnesium` | technical_review_recommend_approve | `mg/dL` | 131,729 | 2,932,480 | Blood/serum magnesium itemids and mmol/L-to-mg/dL conversion are direct; urine, dialysate, other-fluid, and medication rows remain excluded. |
| `std_phosphate` | technical_review_recommend_approve | `mg/dL` | 143,890 | 2,813,857 | Blood/serum phosphate itemids and mmol/L-to-mg/dL conversion are direct; urine, timed urine, and medication phosphate rows remain excluded. |
| `std_osmolality_measured` | technical_review_recommend_approve_with_caveat | `mOsm/kg` | 4,805 | 52,878 | Measured blood osmolality source is specific and scale is correct; the Amsterdam set is sparse with a selected hyperosmolar tail, so keep a sparse-source caveat. |
| `std_total_cholesterol` | technical_review_recommend_approve | `mg/dL` | 2,391 | 322,532 | Blood/serum total cholesterol source is specific, mmol/L-to-mg/dL conversion is correct, and distribution sits in the expected clinical scale. |
| `std_troponin_t` | technical_review_recommend_approve_with_caveat | `ng/mL` | 24,321 | 191,554 | Blood troponin T sources and ug/L-to-ng/mL equivalence are direct; Amsterdam values are heavily positive/ICU-selected, so keep a high-acuity distribution caveat. |

## Distribution Review

| variable | Amsterdam rows | kept | outliers | patients | stays | Amsterdam p50 | Amsterdam p99 | MIMIC p50 | MIMIC p99 | interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `std_anion_gap` | 464,208 | 464,116 | 92 | 15,423 | 17,378 | 8 | 20 | 14 | 24 | Amsterdam p50 8 is lower than MIMIC p50 14, while Amsterdam p99 20 remains in a plausible ICU high-tail range. This looks like formula/analyzer/cohort variation rather than source mismatch because the retained source is a direct blood anion-gap item. |
| `std_amylase` | 36,754 | 36,730 | 24 | 9,258 | 10,613 | 73 | 1,135 | 64 | 676.53 | Amsterdam p50 73 and p99 1,135 are in the same clinical order of magnitude as MIMIC p50 64 and p99 676.53, with differences explainable by database mix and testing practice. |
| `std_lipase` | 3,436 | 3,436 | 0 | 1,920 | 2,105 | 31 | 2,277.9 | 33 | 1,194 | Amsterdam p50 31 and p99 2,277.9 are in the same clinical order of magnitude as MIMIC p50 33 and p99 1,194, with differences explainable by database mix and testing practice. |
| `std_ferritin` | 1,001 | 993 | 8 | 806 | 898 | 344 | 13,038.84 | 115 | 5,711 | Amsterdam has a smaller, indication-driven measured set than MIMIC. The center/tail difference is plausible for selective ICU testing and does not contradict the locked source identity. |
| `std_haptoglobin` | 375 | 375 | 0 | 261 | 287 | 130 | 441.86 | 156 | 520 | Amsterdam has a smaller, indication-driven measured set than MIMIC. The center/tail difference is plausible for selective ICU testing and does not contradict the locked source identity. |
| `std_magnesium` | 131,779 | 131,729 | 50 | 18,607 | 21,112 | 2.1 | 3.8 | 2 | 3 | Amsterdam p50 2.1 and p99 3.8 are in the same clinical order of magnitude as MIMIC p50 2 and p99 3, with differences explainable by database mix and testing practice. |
| `std_phosphate` | 143,927 | 143,890 | 37 | 18,045 | 20,463 | 3.3 | 8.4 | 3.4 | 7.6 | Amsterdam p50 3.3 and p99 8.4 are in the same clinical order of magnitude as MIMIC p50 3.4 and p99 7.6, with differences explainable by database mix and testing practice. |
| `std_osmolality_measured` | 4,816 | 4,805 | 11 | 2,433 | 2,620 | 300 | 390.96 | 294 | 363 | Amsterdam has a smaller, indication-driven measured set than MIMIC. The center/tail difference is plausible for selective ICU testing and does not contradict the locked source identity. |
| `std_total_cholesterol` | 2,392 | 2,391 | 1 | 1,928 | 2,062 | 135.3 | 305.5 | 182 | 310 | Amsterdam p50 135.3 and p99 305.5 are in the same clinical order of magnitude as MIMIC p50 182 and p99 310, with differences explainable by database mix and testing practice. |
| `std_troponin_t` | 24,401 | 24,321 | 80 | 8,121 | 8,942 | 0.149 | 13 | 0.09 | 6.46 | Amsterdam has a smaller, indication-driven measured set than MIMIC. The center/tail difference is plausible for selective ICU testing and does not contradict the locked source identity. |

## Official Source Alignment

AmsterdamUMCdb official documentation describes measurement/observation data as including lab results, and the legacy dictionary is the native item source for version 1.0.2. The reviewed candidate rows below are locked to Amsterdam numericitems itemids, labels, and units. MIMIC comparison uses already reviewed-approved MIMIC-IV-3.1 assets and their retained source anchors.

- `std_anion_gap`: Amsterdam sources 9559 Anion-Gap (bloed) (mmol/l, ucum mmol/L) contributes 464,208 rows with 464,116 kept and 92 outliers. Conversion lock: 9559: source unit mmol/l, factor 1.0, rule direct_value
- `std_amylase`: Amsterdam sources 11986 Amylase (bloed) (E/l, ucum U/L) contributes 35,727 rows with 35,711 kept and 16 outliers; 6845 Plasma Amylase (E/l, ucum U/L) contributes 1,027 rows with 1,019 kept and 8 outliers. Conversion lock: 11986: source unit E/l, factor 1.0, rule direct_value; 6845: source unit E/l, factor 1.0, rule direct_value
- `std_lipase`: Amsterdam sources 12043 Lipase (bloed) (E/l, ucum U/L) contributes 3,436 rows with 3,436 kept and 0 outliers. Conversion lock: 12043: source unit E/l, factor 1.0, rule direct_value
- `std_ferritin`: Amsterdam sources 10162 Ferritine (bloed) (µg/l, ucum ug/L) contributes 999 rows with 991 kept and 8 outliers; 6971 Ferritine (ng/ml, ucum ng/mL) contributes 2 rows with 2 kept and 0 outliers. Conversion lock: 10162: source unit µg/l, factor 1.0, rule ferritin_ug_per_l_to_ng_per_ml_equivalent; 6971: source unit ng/ml, factor 1.0, rule direct_value
- `std_haptoglobin`: Amsterdam sources 10129 Haptoglobine (bloed) (g/l, ucum g/L) contributes 375 rows with 375 kept and 0 outliers. Conversion lock: 10129: source unit g/l, factor 100.0, rule haptoglobin_g_per_l_to_mg_per_dl
- `std_magnesium`: Amsterdam sources 9952 Magnesium (bloed) (mmol/l, ucum mmol/L) contributes 127,345 rows with 127,330 kept and 15 outliers; 6839 Magnesium (mmol/l, ucum mmol/L) contributes 4,434 rows with 4,399 kept and 35 outliers. Conversion lock: 6839: source unit mmol/l, factor 2.4305, rule magnesium_mmol_per_l_to_mg_per_dl; 9952: source unit mmol/l, factor 2.4305, rule magnesium_mmol_per_l_to_mg_per_dl
- `std_phosphate`: Amsterdam sources 9935 Fosfaat (bloed) (mmol/l, ucum mmol/L) contributes 139,031 rows with 139,022 kept and 9 outliers; 6828 Fosfaat (mmol/l, ucum mmol/L) contributes 4,896 rows with 4,868 kept and 28 outliers. Conversion lock: 6828: source unit mmol/l, factor 3.096, rule phosphate_mmol_per_l_to_mg_per_dl; 9935: source unit mmol/l, factor 3.096, rule phosphate_mmol_per_l_to_mg_per_dl
- `std_osmolality_measured`: Amsterdam sources 11918 Osmolaliteit (bloed) (mosmol/kg, ucum mosm/kg) contributes 4,816 rows with 4,805 kept and 11 outliers. Conversion lock: 11918: source unit mosmol/kg, factor 1.0, rule direct_value
- `std_total_cholesterol`: Amsterdam sources 9954 Cholesterol (bloed) (mmol/l, ucum mmol/L) contributes 2,386 rows with 2,385 kept and 1 outliers; 6820 Cholesterol (mmol/l, ucum mmol/L) contributes 6 rows with 6 kept and 0 outliers. Conversion lock: 6820: source unit mmol/l, factor 38.67, rule cholesterol_mmol_per_l_to_mg_per_dl; 9954: source unit mmol/l, factor 38.67, rule cholesterol_mmol_per_l_to_mg_per_dl
- `std_troponin_t`: Amsterdam sources 10407 TroponineT (bloed) (µg/l, ucum ug/L) contributes 23,805 rows with 23,730 kept and 75 outliers; 8115 Troponine (ng/ml, ucum ng/mL) contributes 596 rows with 591 kept and 5 outliers. Conversion lock: 10407: source unit µg/l, factor 1.0, rule troponin_t_ug_per_l_to_ng_per_ml_equivalent; 8115: source unit ng/ml, factor 1.0, rule direct_value

## Per-Variable Review Blocks

### `std_anion_gap`

- Identity: Class 1 event-level numeric laboratory measurement in AmsterdamUMCdb-1.0.2; canonical unit `mEq/L`; cleaned field `std_anion_gap_meq_per_l_cleaned`; cleaned range [-5.0, 60.0]; mapping is a database-specific same-name/bounded-source owner-review candidate.
- Reviewed database distribution: source rows 464,208, kept 464,116, outliers 92, patients 15,423, stays 17,378; zero kept 601, negative raw 1,659, raw low/high outliers 2/90; pre/post ICU rows 52,886/111; exact duplicate kept rows 0.
- Raw and cleaned distribution: raw min -8, p01 1, p50 8, p95 -, p99 20, max 12,474; cleaned min -5, p01 1, p50 8, p95 14.7, p99 20, max 58.5; first-stay measurement count 17,378, first p50 9, first p95 18, first p99 26.
- Source-level detail: 9559 Anion-Gap (bloed) (mmol/l, ucum mmol/L) contributes 464,208 rows with 464,116 kept and 92 outliers
- Comparison with approved databases: Approved MIMIC has 3,925,396 kept rows, p50 14, p95 20, p99 24, max 60, mean 13.792. MIMIC retained source anchor: -; unit counts {'mEq/L': 3925590}. Amsterdam p50 8 is lower than MIMIC p50 14, while Amsterdam p99 20 remains in a plausible ICU high-tail range. This looks like formula/analyzer/cohort variation rather than source mismatch because the retained source is a direct blood anion-gap item.
- Official/source alignment: Amsterdam dictionary itemids {'9559': 'Anion-Gap (bloed)'} are retained from numericitems with locked source units {'9559': 'mmol/l'}. Amsterdam Anion-Gap (bloed) numericitems rows are retained as the direct blood anion-gap source; non-anion calcium/procalcitonin false-positive rows from the broad Q4 scan are excluded.
- Clinical/literature plausibility: External check: anion gap is a calculated mEq/L or mmol/L measure; modern ion-selective-electrode ranges can be near 3-11 mEq/L, and ICU literature emphasizes albumin correction. Amsterdam p50 8.0 is therefore low versus MIMIC but not a scale failure.
- Risks and boundaries: Risk: anion gap is calculated and formula/analyzer dependent; future derived anion-gap variants must not be mixed silently with this direct source item.
- Owner approval decision: `reviewed_approved`. Technical recommendation: `technical_review_recommend_approve_with_caveat`. Owner approval was recorded on `2026-05-08`; caveats remain active where listed.

### `std_amylase`

- Identity: Class 1 event-level numeric laboratory measurement in AmsterdamUMCdb-1.0.2; canonical unit `IU/L`; cleaned field `std_amylase_iu_per_l_cleaned`; cleaned range [1.0, 5000.0]; mapping is a database-specific same-name/bounded-source owner-review candidate.
- Reviewed database distribution: source rows 36,754, kept 36,730, outliers 24, patients 9,258, stays 10,613; zero kept 0, negative raw 0, raw low/high outliers 7/17; pre/post ICU rows 5,047/61; exact duplicate kept rows 111.
- Raw and cleaned distribution: raw min 0, p01 11, p50 73, p95 -, p99 1,151.47, max 102,187; cleaned min 2, p01 11, p50 73, p95 433, p99 1,135, max 4,902; first-stay measurement count 10,610, first p50 66, first p95 356.55, first p99 998.28.
- Source-level detail: 11986 Amylase (bloed) (E/l, ucum U/L) contributes 35,727 rows with 35,711 kept and 16 outliers; 6845 Plasma Amylase (E/l, ucum U/L) contributes 1,027 rows with 1,019 kept and 8 outliers
- Comparison with approved databases: Approved MIMIC has 96,248 kept rows, p50 64, p95 250, p99 676.53, max 4,938, mean 96.622. MIMIC retained source anchor: -; unit counts {'IU/L': 96286}. Amsterdam p50 73 and p99 1,135 are in the same clinical order of magnitude as MIMIC p50 64 and p99 676.53, with differences explainable by database mix and testing practice.
- Official/source alignment: Amsterdam dictionary itemids {'11986': 'Amylase (bloed)', '6845': 'Plasma Amylase'} are retained from numericitems with locked source units {'11986': 'E/l', '6845': 'E/l'}. Amsterdam blood/plasma amylase rows are retained and E/L is treated as IU/L; urine, drain, ascites, pleural, and generic other-fluid amylase rows are excluded from this blood/plasma same-name candidate.
- Clinical/literature plausibility: External check: MedlinePlus gives blood amylase normal results around 40-140 U/L, while pancreatitis and other abdominal disease can produce large elevations. Amsterdam p50 73.0 and p99 1135.0 are clinically plausible for selected ICU testing.
- Risks and boundaries: Risk: urine, ascites, pleural, drain, and other-fluid amylase are adjacent variables and remain excluded.
- Owner approval decision: `reviewed_approved`. Technical recommendation: `technical_review_recommend_approve`. Owner approval was recorded on `2026-05-08`; caveats remain active where listed.

### `std_lipase`

- Identity: Class 1 event-level numeric laboratory measurement in AmsterdamUMCdb-1.0.2; canonical unit `IU/L`; cleaned field `std_lipase_iu_per_l_cleaned`; cleaned range [1.0, 20000.0]; mapping is a database-specific same-name/bounded-source owner-review candidate.
- Reviewed database distribution: source rows 3,436, kept 3,436, outliers 0, patients 1,920, stays 2,105; zero kept 0, negative raw 0, raw low/high outliers 0/0; pre/post ICU rows 854/3; exact duplicate kept rows 0.
- Raw and cleaned distribution: raw min 4, p01 6, p50 31, p95 -, p99 2,277.9, max 16,420; cleaned min 4, p01 6, p50 31, p95 640.25, p99 2,277.9, max 16,420; first-stay measurement count 2,105, first p50 24, first p95 490.4, first p99 2,569.08.
- Source-level detail: 12043 Lipase (bloed) (E/l, ucum U/L) contributes 3,436 rows with 3,436 kept and 0 outliers
- Comparison with approved databases: Approved MIMIC has 293,090 kept rows, p50 33, p95 214, p99 1,194, max 19,540, mean 89.861. MIMIC retained source anchor: hosp.labevents itemid 50956; unit counts {'IU/L': 293108}. Amsterdam p50 31 and p99 2,277.9 are in the same clinical order of magnitude as MIMIC p50 33 and p99 1,194, with differences explainable by database mix and testing practice.
- Official/source alignment: Amsterdam dictionary itemids {'12043': 'Lipase (bloed)'} are retained from numericitems with locked source units {'12043': 'E/l'}. Amsterdam Lipase (bloed) numericitems rows are retained and E/L is treated as IU/L; other-fluid, ascites, drain, and no-unit legacy lipase rows are excluded.
- Clinical/literature plausibility: External check: MedlinePlus gives lipase normal results around 0-160 U/L. Amsterdam p50 31.0 is normal-range centered and p99 2277.9 is compatible with severe pancreatic disease.
- Risks and boundaries: Risk: body-fluid and no-unit legacy lipase rows remain excluded; future inclusion needs a separate source-boundary review.
- Owner approval decision: `reviewed_approved`. Technical recommendation: `technical_review_recommend_approve`. Owner approval was recorded on `2026-05-08`; caveats remain active where listed.

### `std_ferritin`

- Identity: Class 1 event-level numeric laboratory measurement in AmsterdamUMCdb-1.0.2; canonical unit `ng/mL`; cleaned field `std_ferritin_ng_per_ml_cleaned`; cleaned range [0.5, 50000.0]; mapping is a database-specific same-name/bounded-source owner-review candidate.
- Reviewed database distribution: source rows 1,001, kept 993, outliers 8, patients 806, stays 898; zero kept 0, negative raw 0, raw low/high outliers 0/8; pre/post ICU rows 765/1; exact duplicate kept rows 0.
- Raw and cleaned distribution: raw min 5, p01 10, p50 351, p95 -, p99 32,725, max 106,352; cleaned min 5, p01 10, p50 344, p95 3,145.6, p99 13,038.84, max 42,656; first-stay measurement count 895, first p50 313, first p95 2,447.9, first p99 9,513.46.
- Source-level detail: 10162 Ferritine (bloed) (µg/l, ucum ug/L) contributes 999 rows with 991 kept and 8 outliers; 6971 Ferritine (ng/ml, ucum ng/mL) contributes 2 rows with 2 kept and 0 outliers
- Comparison with approved databases: Approved MIMIC has 189,400 kept rows, p50 115, p95 1,655, p99 5,711, max 49,983, mean 468.551. MIMIC retained source anchor: hosp.labevents itemid 50924; unit counts {'ng/mL': 189548}. Amsterdam has a smaller, indication-driven measured set than MIMIC. The center/tail difference is plausible for selective ICU testing and does not contradict the locked source identity.
- Official/source alignment: Amsterdam dictionary itemids {'10162': 'Ferritine (bloed)', '6971': 'Ferritine'} are retained from numericitems with locked source units {'10162': 'µg/l', '6971': 'ng/ml'}. Amsterdam blood ferritin rows are retained; ug/L and ng/mL are numerically equivalent for ferritin concentration.
- Clinical/literature plausibility: External check: Mayo Clinic reports typical ferritin ranges in micrograms/L, numerically equivalent to ng/mL, and lists inflammatory, liver, malignancy, transfusion, and iron-overload causes of high values. Amsterdam p50 344.0 and high tail are plausible in ICU selected testing.
- Risks and boundaries: Risk: sparse selected testing and extreme inflammatory tail; monitor future row additions for unit changes or non-blood specimen leakage.
- Owner approval decision: `reviewed_approved`. Technical recommendation: `technical_review_recommend_approve_with_caveat`. Owner approval was recorded on `2026-05-08`; caveats remain active where listed.

### `std_haptoglobin`

- Identity: Class 1 event-level numeric laboratory measurement in AmsterdamUMCdb-1.0.2; canonical unit `mg/dL`; cleaned field `std_haptoglobin_mg_per_dl_cleaned`; cleaned range [5.0, 700.0]; mapping is a database-specific same-name/bounded-source owner-review candidate.
- Reviewed database distribution: source rows 375, kept 375, outliers 0, patients 261, stays 287; zero kept 0, negative raw 0, raw low/high outliers 374/0; pre/post ICU rows 178/0; exact duplicate kept rows 0.
- Raw and cleaned distribution: raw min 0.06, p01 0.06, p50 1.3, p95 -, p99 4.419, max 5.1; cleaned min 6, p01 6, p50 130, p95 353, p99 441.86, max 510; first-stay measurement count 287, first p50 150, first p95 367.3, first p99 455.6.
- Source-level detail: 10129 Haptoglobine (bloed) (g/l, ucum g/L) contributes 375 rows with 375 kept and 0 outliers
- Comparison with approved databases: Approved MIMIC has 47,962 kept rows, p50 156, p95 407, p99 520, max 699, mean 177.982. MIMIC retained source anchor: hosp.labevents itemid 50935; unit counts {'mg/dL': 48016}. Amsterdam has a smaller, indication-driven measured set than MIMIC. The center/tail difference is plausible for selective ICU testing and does not contradict the locked source identity.
- Official/source alignment: Amsterdam dictionary itemids {'10129': 'Haptoglobine (bloed)'} are retained from numericitems with locked source units {'10129': 'g/l'}. Amsterdam Haptoglobine (bloed) rows are retained and converted from g/L to mg/dL.
- Clinical/literature plausibility: External check: Mayo Clinic Laboratories gives haptoglobin serum reference values of 30-200 mg/dL. Amsterdam p50 130.0 is centered in range and p99 441.86 is plausible for acute-phase elevation.
- Risks and boundaries: Risk: sparse selected testing; low haptoglobin hemolysis-tail behavior should be revisited if a larger source family is admitted.
- Owner approval decision: `reviewed_approved`. Technical recommendation: `technical_review_recommend_approve_with_caveat`. Owner approval was recorded on `2026-05-08`; caveats remain active where listed.

### `std_magnesium`

- Identity: Class 1 event-level numeric laboratory measurement in AmsterdamUMCdb-1.0.2; canonical unit `mg/dL`; cleaned field `std_magnesium_mg_per_dl_cleaned`; cleaned range [0.1, 10.0]; mapping is a database-specific same-name/bounded-source owner-review candidate.
- Reviewed database distribution: source rows 131,779, kept 131,729, outliers 50, patients 18,607, stays 21,112; zero kept 0, negative raw 0, raw low/high outliers 18/22; pre/post ICU rows 13,218/191; exact duplicate kept rows 199.
- Raw and cleaned distribution: raw min 0, p01 0.52, p50 0.85, p95 -, p99 1.58, max 150; cleaned min 0.1, p01 1.3, p50 2.1, p95 3.1, p99 3.8, max 10; first-stay measurement count 21,105, first p50 2, first p95 3.3, first p99 4.
- Source-level detail: 9952 Magnesium (bloed) (mmol/l, ucum mmol/L) contributes 127,345 rows with 127,330 kept and 15 outliers; 6839 Magnesium (mmol/l, ucum mmol/L) contributes 4,434 rows with 4,399 kept and 35 outliers
- Comparison with approved databases: Approved MIMIC has 2,932,480 kept rows, p50 2, p95 2.5, p99 3, max 10, mean 2.025. MIMIC retained source anchor: hosp.labevents itemid 50960; unit counts {'mg/dL': 2932689}. Amsterdam p50 2.1 and p99 3.8 are in the same clinical order of magnitude as MIMIC p50 2 and p99 3, with differences explainable by database mix and testing practice.
- Official/source alignment: Amsterdam dictionary itemids {'9952': 'Magnesium (bloed)', '6839': 'Magnesium'} are retained from numericitems with locked source units {'9952': 'mmol/l', '6839': 'mmol/l'}. Amsterdam blood/serum magnesium rows are retained and converted from mmol/L to mg/dL; urine, dialysate, other-fluid, and medication magnesium rows are excluded.
- Clinical/literature plausibility: External check: MedlinePlus encyclopedia gives blood magnesium normal range around 1.7-2.2 mg/dL. Amsterdam p50 2.1 and p99 3.8 are plausible in ICU monitoring and treatment.
- Risks and boundaries: Risk: medication magnesium and urine/dialysate magnesium are adjacent but excluded; source unit conversion must stay item-specific.
- Owner approval decision: `reviewed_approved`. Technical recommendation: `technical_review_recommend_approve`. Owner approval was recorded on `2026-05-08`; caveats remain active where listed.

### `std_phosphate`

- Identity: Class 1 event-level numeric laboratory measurement in AmsterdamUMCdb-1.0.2; canonical unit `mg/dL`; cleaned field `std_phosphate_mg_per_dl_cleaned`; cleaned range [0.1, 20.0]; mapping is a database-specific same-name/bounded-source owner-review candidate.
- Reviewed database distribution: source rows 143,927, kept 143,890, outliers 37, patients 18,045, stays 20,463; zero kept 0, negative raw 0, raw low/high outliers 7/24; pre/post ICU rows 13,304/150; exact duplicate kept rows 316.
- Raw and cleaned distribution: raw min 0, p01 0.38, p50 1.07, p95 -, p99 2.72, max 169; cleaned min 0.3, p01 1.2, p50 3.3, p95 6, p99 8.4, max 19.6; first-stay measurement count 20,460, first p50 3.1, first p95 6.2, first p99 9.6.
- Source-level detail: 9935 Fosfaat (bloed) (mmol/l, ucum mmol/L) contributes 139,031 rows with 139,022 kept and 9 outliers; 6828 Fosfaat (mmol/l, ucum mmol/L) contributes 4,896 rows with 4,868 kept and 28 outliers
- Comparison with approved databases: Approved MIMIC has 2,813,857 kept rows, p50 3.4, p95 5.5, p99 7.6, max 20, mean 3.56. MIMIC retained source anchor: hosp.labevents itemid 50970; unit counts {'mg/dL': 2813952}. Amsterdam p50 3.3 and p99 8.4 are in the same clinical order of magnitude as MIMIC p50 3.4 and p99 7.6, with differences explainable by database mix and testing practice.
- Official/source alignment: Amsterdam dictionary itemids {'9935': 'Fosfaat (bloed)', '6828': 'Fosfaat'} are retained from numericitems with locked source units {'9935': 'mmol/l', '6828': 'mmol/l'}. Amsterdam blood/serum phosphate rows are retained and converted from mmol/L to mg/dL; urine, 24-hour urine, and medication phosphate rows are excluded.
- Clinical/literature plausibility: External check: MedlinePlus gives adult phosphorus/phosphate blood normal values around 2.8-4.5 mg/dL. Amsterdam p50 3.3 and p99 8.4 are plausible in ICU kidney/metabolic illness.
- Risks and boundaries: Risk: urine/timed urine and medication phosphate are adjacent but excluded; source unit conversion must stay item-specific.
- Owner approval decision: `reviewed_approved`. Technical recommendation: `technical_review_recommend_approve`. Owner approval was recorded on `2026-05-08`; caveats remain active where listed.

### `std_osmolality_measured`

- Identity: Class 1 event-level numeric laboratory measurement in AmsterdamUMCdb-1.0.2; canonical unit `mOsm/kg`; cleaned field `std_osmolality_measured_mosm_per_kg_cleaned`; cleaned range [100.0, 450.0]; mapping is a database-specific same-name/bounded-source owner-review candidate.
- Reviewed database distribution: source rows 4,816, kept 4,805, outliers 11, patients 2,433, stays 2,620; zero kept 0, negative raw 0, raw low/high outliers 1/10; pre/post ICU rows 1,471/19; exact duplicate kept rows 0.
- Raw and cleaned distribution: raw min 7, p01 246, p50 300, p95 -, p99 397.85, max 477; cleaned min 181, p01 246, p50 300, p95 350, p99 390.96, max 450; first-stay measurement count 2,619, first p50 300, first p95 357, first p99 398.
- Source-level detail: 11918 Osmolaliteit (bloed) (mosmol/kg, ucum mosm/kg) contributes 4,816 rows with 4,805 kept and 11 outliers
- Comparison with approved databases: Approved MIMIC has 52,878 kept rows, p50 294, p95 334, p99 363, max 449, mean 295.401. MIMIC retained source anchor: hosp.labevents itemid 50964; unit counts {'mOsm/kg': 52885}. Amsterdam has a smaller, indication-driven measured set than MIMIC. The center/tail difference is plausible for selective ICU testing and does not contradict the locked source identity.
- Official/source alignment: Amsterdam dictionary itemids {'11918': 'Osmolaliteit (bloed)'} are retained from numericitems with locked source units {'11918': 'mosmol/kg'}. Amsterdam Osmolaliteit (bloed) rows are retained as measured blood osmolality; urine, stool, other-fluid, nutrition product, and no-unit legacy osmolality rows are excluded.
- Clinical/literature plausibility: External check: StatPearls reports normal serum osmolality around 275-295 mOsm/kg and values above 300 in hyperosmolar states. Amsterdam p50 300.0 and p99 390.96 are plausible for selected ICU osmolality testing.
- Risks and boundaries: Risk: urine, stool, nutrition-product, and calculated-osmolality concepts are adjacent but excluded; this approval is measured blood osmolality only.
- Owner approval decision: `reviewed_approved`. Technical recommendation: `technical_review_recommend_approve_with_caveat`. Owner approval was recorded on `2026-05-08`; caveats remain active where listed.

### `std_total_cholesterol`

- Identity: Class 1 event-level numeric laboratory measurement in AmsterdamUMCdb-1.0.2; canonical unit `mg/dL`; cleaned field `std_total_cholesterol_mg_per_dl_cleaned`; cleaned range [1.0, 500.0]; mapping is a database-specific same-name/bounded-source owner-review candidate.
- Reviewed database distribution: source rows 2,392, kept 2,391, outliers 1, patients 1,928, stays 2,062; zero kept 0, negative raw 0, raw low/high outliers 38/0; pre/post ICU rows 1,220/0; exact duplicate kept rows 0.
- Raw and cleaned distribution: raw min 0.1, p01 0.8, p50 3.5, p95 -, p99 7.9, max 14.9; cleaned min 3.9, p01 30.9, p50 135.3, p95 243.6, p99 305.5, max 464; first-stay measurement count 2,061, first p50 139.2, first p95 247.5, first p99 307.06.
- Source-level detail: 9954 Cholesterol (bloed) (mmol/l, ucum mmol/L) contributes 2,386 rows with 2,385 kept and 1 outliers; 6820 Cholesterol (mmol/l, ucum mmol/L) contributes 6 rows with 6 kept and 0 outliers
- Comparison with approved databases: Approved MIMIC has 322,532 kept rows, p50 182, p95 263, p99 310, max 497, mean 185.033. MIMIC retained source anchor: hosp.labevents itemid 50907; unit counts {'mg/dL': 322725}. Amsterdam p50 135.3 and p99 305.5 are in the same clinical order of magnitude as MIMIC p50 182 and p99 310, with differences explainable by database mix and testing practice.
- Official/source alignment: Amsterdam dictionary itemids {'9954': 'Cholesterol (bloed)', '6820': 'Cholesterol'} are retained from numericitems with locked source units {'9954': 'mmol/l', '6820': 'mmol/l'}. Amsterdam blood/serum cholesterol rows are retained and converted from mmol/L to mg/dL; broad Q4 false-positive total-volume and bilirubin rows are excluded.
- Clinical/literature plausibility: External check: CDC describes total cholesterol in mg/dL and notes values above 200 mg/dL may be high. Amsterdam p50 135.3 and p99 305.5 are clinically plausible for ICU lipid measurements.
- Risks and boundaries: Risk: HDL, LDL, triglyceride, ratio, and pleural/body-fluid cholesterol variables must remain split from total blood cholesterol.
- Owner approval decision: `reviewed_approved`. Technical recommendation: `technical_review_recommend_approve`. Owner approval was recorded on `2026-05-08`; caveats remain active where listed.

### `std_troponin_t`

- Identity: Class 1 event-level numeric laboratory measurement in AmsterdamUMCdb-1.0.2; canonical unit `ng/mL`; cleaned field `std_troponin_t_ng_per_ml_cleaned`; cleaned range [0.0, 30.0]; mapping is a database-specific same-name/bounded-source owner-review candidate.
- Reviewed database distribution: source rows 24,401, kept 24,321, outliers 80, patients 8,121, stays 8,942; zero kept 0, negative raw 0, raw low/high outliers 0/80; pre/post ICU rows 6,705/14; exact duplicate kept rows 21.
- Raw and cleaned distribution: raw min 0.003, p01 0.004, p50 0.15, p95 -, p99 15.7, max 113; cleaned min 0.003, p01 0.004, p50 0.149, p95 4.8, p99 13, max 30; first-stay measurement count 8,941, first p50 0.047, first p95 1.5, first p99 5.7.
- Source-level detail: 10407 TroponineT (bloed) (µg/l, ucum ug/L) contributes 23,805 rows with 23,730 kept and 75 outliers; 8115 Troponine (ng/ml, ucum ng/mL) contributes 596 rows with 591 kept and 5 outliers
- Comparison with approved databases: Approved MIMIC has 191,554 kept rows, p50 0.09, p95 2.11, p99 6.46, max 25, mean 0.466. MIMIC retained source anchor: -; unit counts {'ng/mL': 459872}. Amsterdam has a smaller, indication-driven measured set than MIMIC. The center/tail difference is plausible for selective ICU testing and does not contradict the locked source identity.
- Official/source alignment: Amsterdam dictionary itemids {'10407': 'TroponineT (bloed)', '8115': 'Troponine'} are retained from numericitems with locked source units {'10407': 'µg/l', '8115': 'ng/ml'}. Amsterdam blood troponin T rows are retained; ug/L and ng/mL are numerically equivalent. The single other-fluid troponin row is excluded.
- Clinical/literature plausibility: External check: Mayo Clinic Laboratories high-sensitivity troponin T reference values are sex-specific in ng/L, where 0.010-0.015 ng/mL is the same scale after unit conversion. Amsterdam p50 0.149 ng/mL is high but plausible because ICU troponin testing is indication-driven.
- Risks and boundaries: Risk: troponin T must not be merged with troponin I or high-sensitivity ng/L variants without explicit conversion and assay review.
- Owner approval decision: `reviewed_approved`. Technical recommendation: `technical_review_recommend_approve_with_caveat`. Owner approval was recorded on `2026-05-08`; caveats remain active where listed.

## Owner Approval Action

Owner approval was recorded on `2026-05-08` for all ten variables in this packet.

- Amsterdam mapping specs: `artifact_status=reviewed_approved_public_mapping_lock`, `approval_status=reviewed_approved`.
- Local Amsterdam Layer 5 master-index rows and asset manifests: `current_status=reviewed_approved`.
- Public cross-database cards should list AmsterdamUMCdb-1.0.2 after approved runtime evidence is rerun.

## References

- https://github.com/AmsterdamUMC/AmsterdamUMCdb
- https://www.nature.com/articles/s41597-022-01899-x
- https://pmc.ncbi.nlm.nih.gov/articles/PMC2644323/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC3681403/
- https://medlineplus.gov/ency/article/003464.htm
- https://medlineplus.gov/ency/article/003465.htm
- https://www.mayoclinic.org/tests-procedures/ferritin-test/about/pac-20384928
- https://www.mayocliniclabs.com/test-catalog/Overview/800043
- https://medlineplus.gov/ency/article/003487.htm
- https://medlineplus.gov/ency/article/003478.htm
- https://www.ncbi.nlm.nih.gov/books/NBK567764/
- https://www.cdc.gov/cholesterol/about/index.html
- https://www.mayocliniclabs.com/test-catalog/download-setup?format=pdf&unit_code=65832
