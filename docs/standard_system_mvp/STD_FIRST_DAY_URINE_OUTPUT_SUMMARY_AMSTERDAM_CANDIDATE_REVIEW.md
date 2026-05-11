# std_first_day_urine_output_summary Amsterdam Candidate Review

Last updated: 2026-04-25

## Review Verdict

Formal decision:

- do not approve `AmsterdamUMCdb-1.0.2` as a same-name implementation of `std_first_day_urine_output_summary` yet

Practical outcome:

- no Amsterdam same-name approval should be claimed for this variable at this time
- no Amsterdam governed execute-mode runtime evidence should be treated as approved for this same-name variable until a summary-specific build is generated from the approved upstream urine-event layer
- the current public approval remains `MIMIC-IV-3.1` only

This is not a rejection of Amsterdam feasibility.

It means:

- Amsterdam has a plausible official source basis for future same-name construction
- Amsterdam now has the governed upstream `std_icu_urine_output_event` asset and runtime evidence required as the prerequisite
- the next correct step is to derive Amsterdam `std_first_day_urine_output_summary` from that approved event stream and then review the summary-specific mapping, window logic, runtime evidence, and rerun evidence

Short verdict:

- eligible to build next
- not approved yet

## What Was Reviewed

Reviewed public standard-system surface:

- `docs/standard_system_mvp/std_first_day_urine_output_summary/variable_spec.json`
- `docs/standard_system_mvp/std_first_day_urine_output_summary/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_FORMAL_APPROVAL_REVIEW.md`
- `docs/std_variable_cards/std_first_day_urine_output_summary.md`
- `docs/standard_system_mvp/CLASS2_CURRENT_APPROVAL_CLOSURE.md`

Reviewed local Amsterdam source and foundation evidence:

- `Methods/Clinical_Database/local_work/Layer 1/AmsterdamUMCdb-1.0.2/raw_unpacked/numericitems.csv`
- `Methods/Clinical_Database/local_work/Layer 1/AmsterdamUMCdb-1.0.2/source_supplied_derived/official_legacy_dictionary.csv`
- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/reviewed_unsplit/numericitems_event.parquet`
- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/reviewed_unsplit/admissions_core.parquet`
- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/time_anchor/icu_admission_anchor.parquet`
- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/logs/2026-04-19_amsterdam_opening_a03_a05_build_log.md`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/TEMP_2026-04-20_amsterdam_remaining_variable_backlog_and_sequence.md`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/2026-04-22_amsterdam_admissionid_to_stayid_consistency_audit.md`

Reviewed official/source context:

- AmsterdamUMCdb official repository and wiki
- AmsterdamUMCdb official legacy dictionary source
- MIMIC official urine-output and first-day urine-output concept SQL for cross-database boundary comparison

## Current Same-Name Contract To Match

The current `std_first_day_urine_output_summary` contract is:

- one retained row per ICU stay or approved ICU stay-equivalent target
- first-day ICU urine-output total in `mL`
- window start: ICU admission time or ICU-semantic local stay entry time
- window end: ICU admission time plus 24 hours
- aggregation: sum all approved urine-output event rows inside that first-day window
- no-source-row behavior: retain the stay row with `first_day_urine_output_ml = NULL`
- output is a Class-2 `window_summary`

The same-name variable must not mean:

- raw urine-output event rows
- total intake-output balance
- all body-fluid output
- non-urine drain output
- dialysis or CRRT fluid removal
- urine-output rate normalized by body weight or time
- zero-filled missingness
- a calendar-day ICU-day summary instead of an ICU-admission-relative first-24-hour summary

## Amsterdam Source Basis

Amsterdam has a real source basis for future construction.

The raw `numericitems.csv` header includes:

- `admissionid`
- `itemid`
- `item`
- `value`
- `unit`
- `measuredat`
- `registeredat`
- `updatedat`
- `fluidout`

The current Layer 2 `numericitems_event` foundation records:

- row count: `977,625,612`
- anchor missing rows: `0`
- null primary time rows: `0`
- event-time preference: `measuredat -> registeredat -> updatedat`

The already reviewed ID interpretation is:

- Amsterdam raw `admissionid` is the local ICU/MC admission identifier
- under the public standard naming rule, that role maps to standardized `stay_id`
- this is a stay-equivalent structural key, not a patient identifier

This means Amsterdam can plausibly support a first-day stay-level urine-output summary after the urine-event layer is governed.

## Official Dictionary Candidate Urine Sources

The Amsterdam official legacy dictionary contains explicit numeric urine-output items in `mL`.

Candidate urine-output item family:

| itemid | item | English/source meaning | External anchor | Category | Unit | Count |
| --- | --- | --- | --- | --- | --- | --- |
| `8794` | `UrineCAD` | urine output from indwelling urinary catheter | LOINC `9187-6` | `VB-Urine` | `mL` | `1,632,547` |
| `8796` | `UrineSupraPubis` | urine output | LOINC `9187-6` | `VB-Urine` | `mL` | `16,184` |
| `8798` | `UrineSpontaan` | spontaneous urine output | LOINC `9197-5` | `VB-Urine` | `mL` | `14,683` |
| `8800` | `UrineIncontinentie` | urine output | LOINC `9187-6` | `VB-Urine` | `mL` | `2,916` |
| `8803` | `UrineUP` | urine output from urostomy | LOINC `9187-6` | `VB-Urine` | `mL` | `6,668` |
| `10743` | `Nefrodrain li Uit` | urine output from left-sided nephrostomy | LOINC `79549-2` | `VB-Nefrodrains` | `mL` | `3,301` |
| `10745` | `Nefrodrain re Uit` | urine output from right-sided nephrostomy | LOINC `79549-2` | `VB-Nefrodrains` | `mL` | `4,261` |
| `19921` | `UrineSplint Li` | urine output from left-sided ureteral splint | LOINC `9187-6` | `VB-Urine` | `mL` | `503` |
| `19922` | `UrineSplint Re` | urine output from right-sided ureteral splint | LOINC `9187-6` | `VB-Urine` | `mL` | `810` |

Total dictionary count for these candidate urine-output rows:

- `1,681,873`

Interpretation:

- the source basis is strong enough to justify a future Amsterdam build
- the source-code list is now approved for the upstream Amsterdam `std_icu_urine_output_event` event layer
- the same source boundary should be inherited by the first-day summary through the approved upstream event stream rather than reselected directly from raw `numericitems`
- the nephrostomy and ureteral-splint rows are included in the event layer with explicit route flags, so any summary-level downstream sensitivity should remain route-aware

## Sources That Must Not Be Accidentally Included

Amsterdam also has many `mL` fluid-output rows that are not same-name urine-output rows.

Examples include:

- thorax drain output
- wound drain output
- GI output such as gastric output, vomiting, stoma output, and stool output
- blood loss
- ventricular, lumbar, pericardial, pleural, biliary, spinal, and other drain output
- CVVH or dialysis removal
- irrigation input/output families that require separate sign and balance logic

Therefore, a future Amsterdam mapping must not use a broad rule such as:

- all `fluidout` rows
- all `mL` output rows
- all `VB-*` output rows

It must use an approved urine-output source-code set.

## Why Same-Name Summary Approval Still Fails Today

Amsterdam same-name approval still fails because the summary-specific governed layer has not yet been built.

### 1. Upstream event prerequisite is now satisfied, but summary-specific evidence is still missing

The MIMIC implementation derives the first-day summary from an already governed upstream urine-output event stream.

Amsterdam now has an approved same-name upstream event package with:

- machine-readable variable spec
- Amsterdam mapping spec
- governed `execution.py`
- execute-mode runtime evidence
- rerun reproducibility evidence
- formal approval review

However, the first-day summary itself still does not yet have:

- Amsterdam `mapping_spec_amsterdamumcdb_1_0_2.json`
- Amsterdam summary execution
- Amsterdam summary runtime validation
- Amsterdam summary rerun reproducibility evidence
- Amsterdam summary formal approval review

Therefore, the prerequisite is complete, but the same-name summary implementation is not yet approved.

### 2. First-day window translation still needs summary execution proof

The Amsterdam event layer is event-level.

The summary contract is stay-level.

The next build must prove:

- the first 24-hour window starts at the approved ICU/MC local admission anchor
- event rows are included only if they fall inside that first-day window
- the retained target grain is one row per standardized `stay_id`
- boundary inclusion rules match the public contract

### 3. NULL versus zero behavior is not yet proven at the summary layer

The MIMIC contract explicitly preserves official-style `NULL` when no qualifying first-day urine row exists.

Amsterdam must separately prove:

- no-source first-day rows are retained
- no-source rows are represented as `NULL`, not zero
- zero values are treated as real charted zero only when they are actual source rows that pass validation

### 4. No Amsterdam execute/rerun evidence exists for this summary variable

There is no public Amsterdam mapping spec and no Amsterdam runtime evidence for this same-name summary variable.

Therefore, the standard-system chain is incomplete:

- variable spec exists
- MIMIC mapping exists
- MIMIC execution and runtime evidence exist
- Amsterdam upstream event mapping and runtime evidence now exist
- Amsterdam summary mapping does not yet exist
- Amsterdam summary execution and runtime evidence do not yet exist

## What Is Still Acceptable

Amsterdam is acceptable as a future candidate because:

- official dictionary rows support urine-output semantics
- source units are already `mL`
- Layer 2 has a large event foundation with explicit time preference
- local `admissionid` can be normalized to standardized `stay_id`
- a previous local backlog already identified the correct order:
- `std_icu_output_event`
- `std_icu_urine_output_event`
- `std_first_day_urine_output_summary`

Amsterdam is not acceptable yet as:

- an approved same-name mapping for `std_first_day_urine_output_summary`
- a dual-database approval for the current variable
- a public runtime-evidence claim
- a direct shortcut from raw `numericitems` into the first-day summary without a governed urine-event layer

## Required Preconditions For Same-Name Approval

Before Amsterdam can be approved for `std_first_day_urine_output_summary`, complete the following in order:

1. Use the approved Amsterdam `std_icu_urine_output_event` as the upstream source.
2. Confirm the standardized event timestamp and first-24-hour ICU/MC stay-equivalent window.
3. Define no-source-row `NULL` behavior and zero-row behavior.
4. Add Amsterdam `mapping_spec_amsterdamumcdb_1_0_2.json` for the summary variable.
5. Run governed Amsterdam `execution.py` for first execution.
6. Run post-run runtime validation.
7. Run rerun reproducibility validation.
8. Update the public card and class-2 closure only if all checks pass.

Already satisfied upstream preconditions:

- Amsterdam `std_icu_urine_output_event` is built and formally approved.
- The urine-output source-code set is locked for the event layer.
- Non-urine drains, GI output, blood loss, CVVH, hemodialysis, peritoneal dialysis, and intake-output balance rows are excluded from the event-layer urine numerator.
- `fluidout` / `value` behavior is governed by the approved event-layer mapping and cleaning rule.

## Recommended Next Action

Recommended next action:

- build Amsterdam `std_first_day_urine_output_summary` from the approved upstream `std_icu_urine_output_event` event stream

Do not start by writing:

- Amsterdam public-card approval claim
- a direct raw-`numericitems` summary that bypasses the approved event stream
- a zero-filled missingness version under the same variable identity

The correct dependency is:

- event layer approved
- first-day summary build next

## Final Decision

Formal conclusion:

- `std_first_day_urine_output_summary` remains approved only for `MIMIC-IV-3.1`
- `AmsterdamUMCdb-1.0.2` is eligible to build next
- Amsterdam is not approved yet because the same-name summary mapping, execution, runtime evidence, and rerun evidence do not yet exist

This review should be treated as a candidate/eligibility review, not as a mapping approval.

## Source Pointers

Public official/source references used in this review:

- AmsterdamUMCdb official repository README: <https://github.com/AmsterdamUMC/AmsterdamUMCdb>
- AmsterdamUMCdb official `numericitems` wiki: <https://github.com/AmsterdamUMC/AmsterdamUMCdb/wiki/numericitems>
- AmsterdamUMCdb official legacy dictionary source: <https://raw.githubusercontent.com/AmsterdamUMC/AmsterdamUMCdb/master/amsterdamumcdb/dictionary/legacy/dictionary.csv>
- MIMIC official `first_day_urine_output.sql` concept: <https://raw.githubusercontent.com/MIT-LCP/mimic-code/main/mimic-iv/concepts_postgres/firstday/first_day_urine_output.sql>
- MIMIC official `urine_output.sql` concept: <https://raw.githubusercontent.com/MIT-LCP/mimic-code/main/mimic-iv/concepts_postgres/measurement/urine_output.sql>
