# APACHE II Reconstruction Final Audit

Generated at: 2026-05-09T07:45:36Z

Status: reviewed_approved. Owner approval recorded on 2026-05-09.

## Medication Audit

Medication-only strict immunosuppression remains whitelist-only. The allowed prescription evidence was rebuilt with the same inclusion and exclusion regex used by the main APACHE II reconstruction.

- candidate medication evidence rows: 5019
- ICD plus medication rows: 4332
- medication-only rows: 687
- scoped allowed medication stays reconstructed by audit: 5019
- scoped allowed medication-only stays reconstructed by audit: 687
- allowed medication order rows after scope filtering: 129387
- included excluded-term hits among retained allowed medication evidence: {}

Top medication-only allowed keywords:

| keyword | stay count | order rows |
| --- | ---: | ---: |
| mycophenolate | 429 | 1494 |
| tacrolimus | 150 | 2282 |
| cyclosporine | 61 | 222 |
| carboplatin | 48 | 62 |
| rituximab | 40 | 85 |
| paclitaxel | 33 | 40 |
| fluorouracil | 26 | 39 |
| sirolimus | 24 | 62 |
| cyclophosphamide | 22 | 63 |
| etoposide | 18 | 24 |

Excluded clinical medication terms found in scoped source prescriptions are documented below for transparency; they do not trigger medication-only strict chronic-health points.

| excluded term | scoped stays | scoped med-only-without-strict-ICD stays | order rows |
| --- | ---: | ---: | ---: |
| methotrexate | 784 | 116 | 3390 |
| hydroxychloroquine | 755 | 418 | 3177 |
| azathioprine | 577 | 125 | 3498 |
| sulfasalazine | 204 | 122 | 1554 |
| infliximab | 107 | 60 | 408 |
| etanercept | 70 | 2 | 213 |
| adalimumab | 6 | 3 | 6 |
| golimumab | 1 | 1 | 1 |
| certolizumab | 0 | 0 | 0 |

## Severe-Support Exclusion Sensitivity

The severe-support oxygen guardrail marks rows with missing scorable oxygenation plus invasive/noninvasive ventilation, HFNC, tracheostomy, high ventilator-setting FiO2, or low SpO2 evidence.

- severe-support rows: 20798 (22.02%)
- any-support rows: 43111 (45.64%)
- legacy oxygen indeterminate flag equals severe-support flag: True
- full-cohort median: 17.0
- median after excluding severe-support rows: 17.0
- median shift after excluding severe-support rows: 0.0
- mean shift after excluding severe-support rows: -0.07618494281336652

| group | rows | row percent | main median | main mean | hospital mortality percent |
| --- | ---: | ---: | ---: | ---: | ---: |
| full_cohort | 94458 | 100.0 | 17.0 | 18.033475195324908 | 12.02 |
| exclude_severe_support_indeterminate | 73660 | 77.98 | 17.0 | 17.95729025251154 | 10.68 |
| severe_support_indeterminate_only | 20798 | 22.02 | 18.0 | 18.303298394076354 | 16.75 |
| exclude_any_support_indeterminate_reference | 51347 | 54.36 | 18.0 | 18.664907394784507 | 12.75 |
| any_support_indeterminate_only_reference | 43111 | 45.64 | 17.0 | 17.281413096425506 | 11.14 |

## Files

- JSON summary: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_apacheii_reconstructed_first24h/query_summary/std_apacheii_reconstructed_first24h_final_audit_summary.json`
- severe-support sensitivity CSV: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_apacheii_reconstructed_first24h/query_summary/std_apacheii_reconstructed_first24h_severe_support_exclusion_sensitivity.csv`
- medication top names, all med rows: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_apacheii_reconstructed_first24h/query_summary/std_apacheii_reconstructed_first24h_medication_top_drug_names_all.csv`
- medication top names, med-only rows: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_apacheii_reconstructed_first24h/query_summary/std_apacheii_reconstructed_first24h_medication_top_drug_names_med_only.csv`
- medication top keywords, all med rows: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_apacheii_reconstructed_first24h/query_summary/std_apacheii_reconstructed_first24h_medication_top_keywords_all.csv`
- medication top keywords, med-only rows: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_apacheii_reconstructed_first24h/query_summary/std_apacheii_reconstructed_first24h_medication_top_keywords_med_only.csv`
- medication-only stay audit preview: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_apacheii_reconstructed_first24h/preview/std_apacheii_reconstructed_first24h_medication_med_only_stay_audit.csv`
