# APACHE II MIMIC First-24h Reconstruction Rule Lock

Generated at: 2026-05-09T07:49:12Z

Status: reviewed_approved. Owner approval recorded on 2026-05-09.

## Owner-Accepted Rule Decisions

- Main reconstructed variable identity: `std_apacheii_reconstructed_first24h`.
- Legacy sparse charted `std_apacheii` route has been retired and deleted; APACHE II is represented by the owner-approved reconstructed first-24h route.
- Output should keep two clearly separated totals: strict complete and missing-normal.
- Missing-normal rows must carry an explicit imputation flag and missing-component list.
- FiO2 should be supplemented from respiratory/ventilator settings when possible; room air assumption is allowed only when no first-24h respiratory support or oxygen-delivery evidence exists.
- Acute renal failure creatinine doubling should use a strict proxy: KDIGO stage 2/3 or first-day RRT, excluding chronic dialysis-only rows.
- Chronic health should use a strict proxy for main analysis; broad ICD/Charlson chronic disease evidence is retained as a reference comparator.
- Strict immunosuppression medication-only evidence should use a narrow whitelist. Low-dose methotrexate, azathioprine, hydroxychloroquine, sulfasalazine, and common TNF-alpha inhibitors do not trigger chronic-health points unless separate strict ICD evidence is present.
- Oxygen missing-normal is the main full-cohort route. Guardrails are split into any-support and severe-support flags; the severe flag covers invasive/noninvasive ventilation, HFNC, tracheostomy, high ventilator FiO2, or low SpO2 without scorable ABG oxygenation.

## Purpose

This rule lock keeps one APACHE II route for MIMIC-IV-3.1:

- `std_apacheii_reconstructed_first24h`: owner-approved reconstructed APACHE II from first-24h component measurements.

The legacy sparse observed charted `std_apacheii` route has been retired and deleted because it covered only a tiny source-charted subset and should not compete with the approved cohort-level APACHE II reconstruction.

## Approved Extraction Logic

- Window: ICU `intime` through the first 24 hours, clipped at ICU `outtime`.
- Vitals/labs/GCS: use MIMIC first-day derived tables.
- Component scoring: score min and max values where APACHE II has high and low abnormal ranges, then retain the higher point score.
- Oxygenation: use arterial blood gas rows in the first 24h; use ABG-row FiO2 when present, otherwise nearest prior ventilator-setting FiO2 within 6h, otherwise assume room-air FiO2 21% only when no first-24h respiratory support or oxygen-delivery evidence exists. If FiO2 is at least 50%, score A-aDO2; otherwise score PaO2.
- Acid-base: use arterial pH when available; if no arterial pH is available, use bicarbonate as the optional APACHE II substitute.
- Age: use `admission_age`.
- Chronic health: main strict proxy from dialysis-dependent renal disease, decompensated liver disease, AIDS/transplant/hematologic malignancy/chemotherapy or strong immunosuppression, and only strict cardiopulmonary evidence. Medication-only strict immunosuppression is limited to transplant-grade immunosuppression and strong cytotoxic/antineoplastic therapy; low-dose rheumatology/IBD drugs and TNF-alpha inhibitors are excluded unless separate strict ICD evidence is present. Chronic-positive elective postoperative proxy rows receive 2 points; other chronic-positive rows receive 5 points. Broad chronic and no-chronic totals are retained as references.
- Acute renal failure creatinine doubling: main rule uses first-24h KDIGO stage >=2 or first-day RRT when strict chronic dialysis evidence is absent. KDIGO stage >=1/RRT is retained as a reference comparator.

## Coverage

| component | available stays | available percent | missing stays |
| --- | ---: | ---: | ---: |
| `apacheii_age_score` | 94458 | 100.0% | 0 |
| `apacheii_temperature_score` | 91758 | 97.14% | 2700 |
| `apacheii_map_score` | 94245 | 99.77% | 213 |
| `apacheii_heart_rate_score` | 94355 | 99.89% | 103 |
| `apacheii_respiratory_rate_score` | 94212 | 99.74% | 246 |
| `apacheii_oxygenation_score` | 31355 | 33.19% | 63103 |
| `apacheii_acid_base_score` | 93442 | 98.92% | 1016 |
| `apacheii_sodium_score` | 93259 | 98.73% | 1199 |
| `apacheii_potassium_score` | 93228 | 98.7% | 1230 |
| `apacheii_creatinine_score_with_strict_arf_double` | 93478 | 98.96% | 980 |
| `apacheii_hematocrit_score` | 93411 | 98.89% | 1047 |
| `apacheii_wbc_score` | 93353 | 98.83% | 1105 |
| `apacheii_gcs_score` | 93809 | 99.31% | 649 |

Strict all-12-component coverage: 29053 / 94458 (30.76%).

Oxygenation remains the main bottleneck: 31355 stays have a scorable first-24h arterial oxygenation component under the current FiO2/Pao2/A-aDO2 rule.

Strict chronic health proxy positive rows: 31769 / 94458 (33.63%). Score-2 elective postoperative proxy rows: 2338; score-5 nonoperative/emergency-or-uncertain rows: 29431. Evidence came from prior hospitalizations in 18642 rows and from current/pre-ICU/chronic-status evidence in 27314 rows.

Strict chronic health category counts are: dialysis-dependent renal 6008; decompensated liver 8360; strict respiratory 7189; strict cardiovascular 1274; strict immunocompromised/chemo 18520; strict immunosuppression medication evidence 5019.

Strict immunosuppression medication-only evidence uses a narrow whitelist. Methotrexate, azathioprine, hydroxychloroquine, sulfasalazine, and common TNF-alpha inhibitors are excluded from medication-only triggers unless separate strict ICD evidence supports immunocompromised/chemo status.

Broad chronic reference positive rows: 51191 / 94458 (54.19%). Broad category counts are: renal/CKD-or-dialysis 23729; severe liver 10351; severe respiratory 15988; severe cardiovascular 1274; immunocompromised-or-malignancy 26173. Broad Charlson CHF and chronic pulmonary flags are retained as evidence fields but are not sufficient by themselves for strict chronic-health scoring.

Oxygen missing-normal guardrail: 43111 rows have any respiratory support/oxygen delivery without scorable oxygenation, and 20798 rows meet the stricter severe-support/high-FiO2/low-SpO2 indeterminate rule. The legacy `apacheii_oxygen_missing_normal_indeterminate_flag` aliases the severe-support rule.

## Approved Distributions

Strict complete sensitivity version, with strict chronic health proxy and strict ARF creatinine doubling:

| metric | value |
| --- | ---: |
| count | 29053 |
| min | 1.0 |
| p25 | 16.0 |
| median | 20.0 |
| mean | 21.249199738409114 |
| p75 | 26.0 |
| max | 58.0 |

Main missing-normal version, with strict chronic health proxy and strict ARF creatinine doubling:

| metric | value |
| --- | ---: |
| count | 94458 |
| min | 0.0 |
| p25 | 13.0 |
| median | 17.0 |
| mean | 18.033475195324908 |
| p75 | 22.0 |
| max | 58.0 |

Reference distributions:

| route | count | median | mean | p75 | max |
| --- | ---: | ---: | ---: | ---: | ---: |
| strict complete broad-chronic reference | 29053 | 21.0 | 22.34192682339173 | 27.0 | 58.0 |
| missing-normal broad-chronic reference | 94458 | 19.0 | 19.23720595396896 | 24.0 | 58.0 |
| strict complete no-chronic reference | 29053 | 19.0 | 19.81420163150105 | 24.0 | 53.0 |
| missing-normal no-chronic reference | 94458 | 16.0 | 16.426083550361007 | 20.0 | 53.0 |

## Official And External Rule Comparison

The APACHE II source definition is a sum of 12 acute physiology component scores, age points, and chronic health points. The original Knaus 1985 paper states that APACHE II uses 12 routine physiologic measurements, age, and previous health status. Merck Manual summarizes the same 0-71 score range and the acute physiology plus age plus chronic health structure.

eICU is useful as an architectural comparator: its APACHE tables are one row per ICU stay and store worst first-APACHE-day component variables, including worst GCS, WBC, temperature, respiratory rate, sodium, potassium, heart rate, mean BP, pH, hematocrit, creatinine, PaO2, FiO2, and related inputs. eICU public outputs are APACHE IV/IVa rather than direct APACHE II, so it should guide structure rather than be copied as a scoring authority.

References:

- PubMed Knaus 1985: https://pubmed.ncbi.nlm.nih.gov/3928249/
- Merck Manual APACHE II table: https://www.merckmanuals.com/professional/multimedia/table/acute-physiologic-assessment-and-chronic-health-evaluation-apache-ii-scoring-system
- MedicalCriteria APACHE II chronic health definitions: https://medicalcriteria.com/web/utiapache/
- George Institute Fluid TRIPS data dictionary: https://www.georgeinstitute.org/sites/default/files/documents/fluidtrips_datadictionary_v2_300414_final.pdf
- eICU apacheApsVar table: https://eicu.mit.edu/eicutables/apacheapsvar/

## Chronic Health Meaning

In APACHE II, chronic health is not the same thing as a general comorbidity index. It is an extra APACHE II add-on for severe pre-existing organ insufficiency or immunocompromised state before this acute ICU admission. The point value also depends on admission/operation context: historically 5 points for nonoperative or emergency postoperative patients, and 2 points for elective postoperative patients.

In MIMIC, this is hard because no single field says "APACHE II chronic health positive." This approved route separates a strict main proxy from the older broad proxy. Every row keeps strict/broad category flags, evidence scope, operative/elective proxy, no-chronic reference totals, and oxygen missing-normal guardrail flags.

## Post-Approval Boundaries

1. Approval is bounded to MIMIC-IV-3.1 and this documented reconstruction route.
2. The main analysis route is `missing-normal` oxygen scoring with explicit oxygen guardrails; strict-complete remains a sensitivity version.
3. Broad chronic and KDIGO stage >=1/RRT variants remain reference comparators, not the approved main score.
4. The legacy sparse observed charted APACHE II route has been deleted; do not reintroduce it as `std_apacheii` without a new owner decision.
