# Amsterdam Class 1 Batch1 Formal Approval Review

Last updated: 2026-05-03

Status: reviewed_approved

This review records the approved source boundaries and runtime evidence for the Amsterdam same-name-ready Batch1 variables. All variables below completed governed first execution, rerun, and reproducibility validation.

## Batch Scope

| variable | canonical unit | retained Amsterdam source itemids | approval boundary |
| --- | --- | --- | --- |
| `std_map` | `mmHg` | `6642 ABP gemiddeld, 6679 Niet invasieve bloeddruk gemiddeld, 8843 ABP gemiddeld II` | `Amsterdam has direct invasive and non-invasive mean arterial pressure numericitems; IABP augmentation and target-pressure rows remain excluded.` |
| `std_sbp` | `mmHg` | `6641 ABP systolisch, 6678 Niet invasieve bloeddruk systolisch, 8841 ABP systolisch II` | `Amsterdam direct invasive and non-invasive systolic blood-pressure rows are retained; IABP and target-pressure rows are excluded.` |
| `std_dbp` | `mmHg` | `6643 ABP diastolisch, 6680 Niet invasieve bloeddruk diastolisch, 8842 ABP diastolisch II` | `Amsterdam direct invasive and non-invasive diastolic blood-pressure rows are retained; IABP and target-pressure rows are excluded.` |
| `std_respiratory_rate` | `breaths_per_minute` | `12266 Ademfreq., 8874 Ademfrequentie Monitor, 12577 Ademfreq. Spontaan nieuw, 12348 Ademfreq.(2)` | `Amsterdam patient respiratory-rate measurement and monitor rows are retained; ventilator-set frequency rows are excluded.` |
| `std_spo2` | `percent` | `6709 Saturatie (Monitor)` | `Amsterdam monitor SpO2 is retained; blood oxygen saturation, target SpO2, and ECMO venous saturation rows are excluded.` |
| `std_temp` | `degrees_celsius` | `13060 Temp Axillair, 8658 Temp Bloed, 8662 Temperatuur Perifeer 1, 13059 Temp Lies, 13062 Temp Oor, 16110 Temp Oesophagus, 13063 Temp Huid, 13058 Temp Rectaal, 8659 Temperatuur Perifeer 2, 13952 Temp Blaas, 14047 PiCCO Tb blood temperature, 13061 Temp Oraal, 9546 Cerebrale temp.` | `Amsterdam direct patient body-temperature site rows are retained; target temperature, warmer settings, ventilator humidifier temperature, and APACHE summary rows are excluded.` |
| `std_glucose` | `mg/dL` | `9947 Glucose (bloed), 6833 Glucose Bloed` | `Amsterdam blood chemistry glucose rows are retained and converted from mmol/L to mg/dL; Astrup blood-gas glucose and non-blood fluids remain excluded from this routine-chemistry variable.` |
| `std_sodium` | `mEq/L` | `10284 Na (onv.ISE) (bloed), 9924 Natrium (bloed), 6840 Natrium` | `Amsterdam blood/serum sodium chemistry rows are retained; urine, other-fluid, APACHE, and Astrup-only rows are excluded.` |
| `std_potassium` | `mEq/L` | `10285 K (onv.ISE) (bloed), 9927 Kalium (bloed), 6835 Kalium` | `Amsterdam blood/serum potassium chemistry rows are retained; urine, other-fluid, APACHE, and ventilator-pressure false-positive rows are excluded.` |
| `std_chloride` | `mEq/L` | `9930 Chloor (bloed), 6819 Chloor` | `Amsterdam blood/serum chloride chemistry rows are retained; Astrup, urine, other-fluid, and 24-hour rows are excluded from this routine-chemistry variable.` |
| `std_creatinine` | `mg/dL` | `9941 Kreatinine (bloed), 6836 Kreatinine, 14216 KREAT enzym. (bloed)` | `Amsterdam serum/blood creatinine rows are retained and converted from umol/L-scale values to mg/dL; urine, clearance, other-fluid, and APACHE rows are excluded.` |
| `std_lactate_bg` | `mmol/L` | `9580 Laktaat Astrup` | `Amsterdam Astrup lactate is retained as the blood-gas lactate same-name source; routine chemistry lactate rows are intentionally excluded.` |
| `std_paco2` | `mmHg` | `9990 pCO2 (bloed), 6846 PCO2, 21213 PCO2 (bloed) - kPa` | `Amsterdam blood-gas pCO2 rows are retained, kPa rows are converted to mmHg, and rows explicitly commented as venous are excluded.` |
| `std_pao2` | `mmHg` | `9996 PO2 (bloed), 7433 PO2, 21214 PO2 (bloed) - kPa` | `Amsterdam blood-gas pO2 rows are retained, kPa rows are converted to mmHg, and rows explicitly commented as venous are excluded.` |
| `std_bicarbonate_bg` | `mmol/L` | `9992 Act.HCO3 (bloed), 6810 HCO3` | `Amsterdam blood-gas bicarbonate rows are retained; other-fluid bicarbonate rows are excluded.` |
| `std_bun` | `mg/dL` | `9943 Ureum (bloed), 6850 Ureum` | `Amsterdam blood/serum urea rows are retained and converted to BUN mg/dL; urine, other-fluid, and 24-hour rows are excluded.` |
| `std_hemoglobin` | `g/dL` | `10286 Hb(v.Bgs) (bloed), 9960 Hb (bloed), 9553 CtHB Astrup, 6778 Hemoglobine` | `Amsterdam hemoglobin rows are retained and converted from mmol/L to g/dL; Hb fractions, HbA1c, targets, other-fluid, and ECMO device rows are excluded.` |
| `std_hematocrit` | `%` | `11545 Ht(v.Bgs) (bloed), 11423 Ht (bloed), 6777 Hematocriet` | `Amsterdam hematocrit fraction-scale rows are retained and converted to percent; APACHE summary and non-blood-fluid rows are excluded.` |
| `std_platelet_count` | `10^3/uL` | `9964 Thrombo's (bloed), 6797 Thrombocyten, 10409 Thrombo's citr. bloed (bloed)` | `Amsterdam platelet count rows are retained on the same numeric scale as 10^3/uL; CD61 flow, target threshold, coagulation-test, and other-fluid rows are excluded.` |
| `std_wbc_count` | `10^3/uL` | `9965 Leuco's (bloed), 6779 Leucocyten` | `Amsterdam blood WBC count rows are retained on the same numeric scale as 10^3/uL; CSF, urine sediment, other-fluid, and APACHE rows are excluded.` |

## Runtime Evidence

Runtime evidence is stored under each variable directory at:

- `runtime/amsterdamumcdb_1_0_2_first_real_execution`
- `runtime/amsterdamumcdb_1_0_2_rerun_repro_check`

| variable | first validation | rerun validation | reproducibility | source rows | retained rows | outlier rows | patients | admissions | first value p50 |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `std_map` | pass | pass | pass | 33,589,290 | 33,588,258 | 1,032 | 20,101 | 23,087 | 76.0 |
| `std_sbp` | pass | pass | pass | 33,587,613 | 33,587,120 | 493 | 20,101 | 23,087 | 113.0 |
| `std_dbp` | pass | pass | pass | 33,577,960 | 33,577,359 | 601 | 20,101 | 23,087 | 58.0 |
| `std_respiratory_rate` | pass | pass | pass | 39,494,208 | 39,492,870 | 1,338 | 20,001 | 22,971 | 16.0 |
| `std_spo2` | pass | pass | pass | 36,411,768 | 36,411,658 | 110 | 20,074 | 23,058 | 98.0 |
| `std_temp` | pass | pass | pass | 6,633,139 | 6,572,246 | 60,893 | 19,908 | 22,811 | 36.1 |
| `std_glucose` | pass | pass | pass | 828,343 | 828,264 | 79 | 20,015 | 22,944 | 121.0 |
| `std_sodium` | pass | pass | pass | 761,306 | 761,073 | 233 | 20,054 | 22,999 | 139.0 |
| `std_potassium` | pass | pass | pass | 765,676 | 765,494 | 182 | 20,053 | 22,997 | 4.1 |
| `std_chloride` | pass | pass | pass | 180,001 | 179,381 | 620 | 10,992 | 12,528 | 107.0 |
| `std_creatinine` | pass | pass | pass | 202,223 | 202,103 | 120 | 20,010 | 22,935 | 0.97 |
| `std_lactate_bg` | pass | pass | pass | 917 | 916 | 1 | 256 | 262 | 1.5 |
| `std_paco2` | pass | pass | pass | 694,197 | 694,034 | 163 | 19,647 | 22,462 | 40.0 |
| `std_pao2` | pass | pass | pass | 688,758 | 688,668 | 90 | 19,617 | 22,420 | 109.0 |
| `std_bicarbonate_bg` | pass | pass | pass | 682,347 | 681,987 | 360 | 19,646 | 22,461 | 24.0 |
| `std_bun` | pass | pass | pass | 110,551 | 110,494 | 57 | 15,428 | 18,007 | 18.0 |
| `std_hemoglobin` | pass | pass | pass | 737,056 | 736,236 | 820 | 20,066 | 23,017 | 13.2 |
| `std_hematocrit` | pass | pass | pass | 699,544 | 666,411 | 33,133 | 20,051 | 22,993 | 39.0 |
| `std_platelet_count` | pass | pass | pass | 221,226 | 221,209 | 17 | 20,018 | 22,940 | 238.0 |
| `std_wbc_count` | pass | pass | pass | 197,179 | 197,178 | 1 | 20,000 | 22,922 | 9.3 |

## Boundary Review Notes

Amsterdam blood-pressure rows are approved only for direct invasive and non-invasive arterial pressure measurements. IABP augmentation rows and therapeutic target rows are excluded because they are adjacent device or goal states, not observed patient blood pressure.

Blood-pressure manual review addendum: the opening same-name approval retains the core Amsterdam monitor families `ABP`, non-invasive blood pressure, and `ABP II`. Adjacent numericitems found during manual review remain excluded from this Batch1 approval: IABP pressure/device rows (`8649`, `8655`, `12441`, `12442`, `12443`), target-pressure rows (`14736`, `15277`, `15278`, `15279`), pulmonary artery pressure rows (`6644`, `6645`, `6646`), PiCCO arterial pressure rows (`14056`, `14057`, `14058`), and sparse/opaque arterial-pressure abbreviations (`13093`, `14454`, `16612`). The PiCCO rows are physiologically adjacent and small-volume, but they are device-specific hemodynamic-module rows rather than the core ABP/NIBP monitor family used for the opening same-name spine; adding them later should be a governed source-boundary extension, not an implicit merge.

Amsterdam respiratory rate is approved only for patient or monitor respiratory-rate observations. Ventilator-set frequency rows remain excluded because they are treatment settings, not observed respiratory rate.

Amsterdam `std_spo2` is approved only from monitor SpO2. Blood-gas oxygen saturation, target SpO2, and ECMO venous saturation rows remain outside this same-name mapping.

Amsterdam temperature is approved only from direct body-temperature site rows. Target temperature, warmer settings, ventilator humidifier temperature, APACHE summary fields, and lab measurement temperature rows remain excluded.

Routine chemistry variables intentionally exclude Astrup blood-gas rows unless the standard variable is explicitly a blood-gas variable. This keeps routine chemistry and blood-gas families from silently merging.

Blood-gas pCO2 and pO2 retain blood-gas rows, convert kPa rows to mmHg, and exclude rows explicitly commented as venous. Amsterdam does not expose a universal structured arterial/venous specimen flag for every retained source row, so `std_paco2` and `std_pao2` are approved with this source-boundary note rather than overclaiming full arterial certainty.

Unit conversions are governed in the mapping specs and runtime manifests. Creatinine, glucose, urea-to-BUN, hemoglobin, hematocrit, and kPa blood-gas sources are normalized before validation and outlier checks.

## Approval Verdict

Approve Amsterdam same-name Batch1 for all 20 variables listed above.

This approval covers AmsterdamUMCdb 1.0.2 governed extraction, runtime validation, rerun evidence, and reproducibility evidence. It does not approve split-identity variables, all-specimen blood-gas variants, oxygen-saturation blood-gas variants, coagulation variables, or derived support-state composites; those remain in later batches.
