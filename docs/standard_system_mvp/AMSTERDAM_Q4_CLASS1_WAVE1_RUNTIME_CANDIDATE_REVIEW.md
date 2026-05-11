# Amsterdam Q4 Class1 Wave1 Runtime Candidate Review

Last updated: 2026-05-04

Status: built-first candidate runtime evidence; owner approval not requested and not implied

## Scope

This packet covers the first high-confidence Q4 Class1 numeric bounded-candidate wave. Variables were selected only when the Amsterdam item label, source unit, specimen scope, and deterministic unit conversion were clear enough for runtime construction.

Excluded from this wave: specimen/body-fluid variables with unresolved modifier boundaries, broad alias false positives, and variables needing parent/component approval.

## Candidate Runtime Summary

| variable | unit | runtime status | rows | kept | stays | raw p50 | raw p99 | kept p50 | kept p99 | rows by item | retained Amsterdam source boundary | candidate caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `std_anion_gap` | `mEq/L` | `runtime_and_rerun_repro_pass` | `464208.0` | `464116.0` | `17378.0` | `8.0` | `20.0` | `8.0` | `20.0` | `9559=464208` | 9559 Anion-Gap (bloed) (mmol/l; factor=1.0) | Amsterdam Anion-Gap (bloed) numericitems rows are retained as the direct blood anion-gap source; non-anion calcium/procalcitonin false-positive rows from the broad Q4 scan are excluded. |
| `std_amylase` | `IU/L` | `runtime_and_rerun_repro_pass` | `36754.0` | `36730.0` | `10613.0` | `73.0` | `1151.4700000000012` | `73.0` | `1135.0` | `6845=1027; 11986=35727` | 11986 Amylase (bloed) (E/l; factor=1.0); 6845 Plasma Amylase (E/l; factor=1.0) | Amsterdam blood/plasma amylase rows are retained and E/L is treated as IU/L; urine, drain, ascites, pleural, and generic other-fluid amylase rows are excluded from this blood/plasma same-name candidate. |
| `std_lipase` | `IU/L` | `runtime_and_rerun_repro_pass` | `3436.0` | `3436.0` | `2105.0` | `31.0` | `2277.9000000000005` | `31.0` | `2277.9000000000005` | `12043=3436` | 12043 Lipase (bloed) (E/l; factor=1.0) | Amsterdam Lipase (bloed) numericitems rows are retained and E/L is treated as IU/L; other-fluid, ascites, drain, and no-unit legacy lipase rows are excluded. |
| `std_ferritin` | `ng/mL` | `runtime_and_rerun_repro_pass` | `1001.0` | `993.0` | `898.0` | `351.0` | `32725.0` | `344.0` | `13038.840000000058` | `6971=2; 10162=999` | 10162 Ferritine (bloed) (µg/l; factor=1.0); 6971 Ferritine (ng/ml; factor=1.0) | Amsterdam blood ferritin rows are retained; ug/L and ng/mL are numerically equivalent for ferritin concentration. |
| `std_haptoglobin` | `mg/dL` | `runtime_and_rerun_repro_pass` | `375.0` | `375.0` | `287.0` | `1.3` | `4.418599925999999` | `130.0` | `441.8599999999999` | `10129=375` | 10129 Haptoglobine (bloed) (g/l; factor=100.0) | Amsterdam Haptoglobine (bloed) rows are retained and converted from g/L to mg/dL. |
| `std_magnesium` | `mg/dL` | `runtime_and_rerun_repro_pass` | `131779.0` | `131729.0` | `21112.0` | `0.85000002` | `1.58` | `2.1` | `3.8` | `6839=4434; 9952=127345` | 9952 Magnesium (bloed) (mmol/l; factor=2.4305); 6839 Magnesium (mmol/l; factor=2.4305) | Amsterdam blood/serum magnesium rows are retained and converted from mmol/L to mg/dL; urine, dialysate, other-fluid, and medication magnesium rows are excluded. |
| `std_phosphate` | `mg/dL` | `runtime_and_rerun_repro_pass` | `143927.0` | `143890.0` | `20463.0` | `1.0700001` | `2.72` | `3.3` | `8.4` | `6828=4896; 9935=139031` | 9935 Fosfaat (bloed) (mmol/l; factor=3.096); 6828 Fosfaat (mmol/l; factor=3.096) | Amsterdam blood/serum phosphate rows are retained and converted from mmol/L to mg/dL; urine, 24-hour urine, and medication phosphate rows are excluded. |
| `std_osmolality_measured` | `mOsm/kg` | `runtime_and_rerun_repro_pass` | `4816.0` | `4805.0` | `2620.0` | `300.0` | `397.85000000000036` | `300.0` | `390.96000000000004` | `11918=4816` | 11918 Osmolaliteit (bloed) (mosmol/kg; factor=1.0) | Amsterdam Osmolaliteit (bloed) rows are retained as measured blood osmolality; urine, stool, other-fluid, nutrition product, and no-unit legacy osmolality rows are excluded. |
| `std_total_cholesterol` | `mg/dL` | `runtime_and_rerun_repro_pass` | `2392.0` | `2391.0` | `2062.0` | `3.5` | `7.9000001` | `135.3` | `305.5` | `6820=6; 9954=2386` | 9954 Cholesterol (bloed) (mmol/l; factor=38.67); 6820 Cholesterol (mmol/l; factor=38.67) | Amsterdam blood/serum cholesterol rows are retained and converted from mmol/L to mg/dL; broad Q4 false-positive total-volume and bilirubin rows are excluded. |
| `std_troponin_t` | `ng/mL` | `runtime_and_rerun_repro_pass` | `24401.0` | `24321.0` | `8942.0` | `0.15000001` | `15.7` | `0.149` | `13.0` | `8115=596; 10407=23805` | 10407 TroponineT (bloed) (µg/l; factor=1.0); 8115 Troponine (ng/ml; factor=1.0) | Amsterdam blood troponin T rows are retained; ug/L and ng/mL are numerically equivalent. The single other-fluid troponin row is excluded. |

## Approval Boundary

These rows are candidate runtime evidence only. Detailed owner-facing review still needs the full per-variable distribution comparison, source-document agreement, and cross-database/epidemiology plausibility check required by `VARIABLE_REVIEW_REPORTING_STANDARD.md`.
