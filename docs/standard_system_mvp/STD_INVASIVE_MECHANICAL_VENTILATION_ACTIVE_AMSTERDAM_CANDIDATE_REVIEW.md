# `std_invasive_mechanical_ventilation_active` Amsterdam Candidate Review

Review date: `2026-05-01`

## Formal Verdict

Formal decision:

- do not approve `AmsterdamUMCdb-1.0.2` as a same-name implementation of `std_invasive_mechanical_ventilation_active` yet
- `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/mapping_spec_amsterdamumcdb_1_0_2.json` may now exist only as a candidate mapping draft
- do not treat that candidate mapping draft as reviewed-approved
- Amsterdam candidate runtime evidence may exist only as candidate evidence
- do not treat candidate runtime evidence as reviewed-approved
- keep the current formal approval bounded to `MIMIC-IV-3.1`

This is not a rejection of Amsterdam feasibility.

It means:

- Amsterdam has a plausible interval source basis for future same-name construction
- the strongest opening candidate is `processitems` itemid `9328` / `Beademen`
- the candidate still needs source-level semantic proof that it means invasive mechanical ventilation active, not broader ventilation support
- a first local source audit has now been completed, and it supports `9328` as a promising candidate but not yet a promotable same-name mapping
- focused interval-classification and manual-review policy work now permits a candidate mapping draft, but not approval
- the candidate mapping draft has now been run once through governed execute-mode runtime evidence, but this is still not approval

Short verdict:

- source-audit started and currently promising
- not approved yet
- candidate mapping draft allowed
- candidate runtime evidence generated
- not ready for reviewed-approved same-name output yet

## What Was Reviewed

Reviewed public standard-system surface:

- `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/variable_spec.json`
- `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `docs/std_variable_cards/std_invasive_mechanical_ventilation_active.md`
- `Framework_Guideline/StandardVariableClass_BinaryStateEpisode_Contract.md`
- `Framework_Guideline/ID_Normalization_Contract.md`
- `Framework_Guideline/AmsterdamUMCdb_TimeSemantics_Contract.md`

Reviewed local Amsterdam source and foundation evidence:

- `Methods/Clinical_Database/local_work/Layer 1/AmsterdamUMCdb-1.0.2/raw_unpacked/processitems.csv`
- `Methods/Clinical_Database/local_work/Layer 1/AmsterdamUMCdb-1.0.2/raw_unpacked/listitems.csv`
- `Methods/Clinical_Database/local_work/Layer 1/AmsterdamUMCdb-1.0.2/raw_unpacked/procedureorderitems.csv`
- `Methods/Clinical_Database/local_work/Layer 1/AmsterdamUMCdb-1.0.2/source_supplied_derived/official_legacy_dictionary.csv`
- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/reviewed_unsplit/processitems_interval.parquet`
- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/reviewed_unsplit/listitems_event.parquet`
- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/reviewed_unsplit/procedureorderitems_event.parquet`
- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/logs/2026-04-19_amsterdam_opening_a03_a05_build_log.md`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_invasive_mechanical_ventilation_active_candidate_source_audit/query_summary/std_invasive_mechanical_ventilation_active_amsterdam_source_audit_summary.json`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_invasive_mechanical_ventilation_active_candidate_source_audit/risk_audit/std_invasive_mechanical_ventilation_active_amsterdam_risk_audit_summary.json`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_invasive_mechanical_ventilation_active_candidate_source_audit/classification/amsterdam_9328_candidate_interval_classification.csv`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_invasive_mechanical_ventilation_active_candidate_source_audit/classification/amsterdam_9328_candidate_interval_classification_summary.json`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_invasive_mechanical_ventilation_active_candidate_source_audit/manual_review_policy/amsterdam_9328_manual_review_policy.csv`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_invasive_mechanical_ventilation_active_candidate_source_audit/manual_review_policy/amsterdam_9328_manual_review_policy_summary.json`

Reviewed public candidate mapping draft:

- `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/mapping_spec_amsterdamumcdb_1_0_2.json`

Reviewed public candidate runtime evidence:

- `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/runtime/amsterdamumcdb_1_0_2_candidate_execution/validation_report.json`
- `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/runtime/amsterdamumcdb_1_0_2_candidate_execution/manifest.json`

Reviewed official/source context:

- AmsterdamUMCdb official repository
- AmsterdamUMCdb official legacy dictionary source
- AmsterdamUMCdb official paper
- MIMIC official ventilation concept SQL, used only as the approved same-name target boundary for the current MIMIC implementation

## Current Same-Name Contract To Match

The current `std_invasive_mechanical_ventilation_active` contract is:

- one retained row per positive invasive mechanical ventilation state episode
- ICU-stay or approved ICU stay-equivalent anchor
- retained value is always `true`
- explicit episode start time
- explicit episode end time
- explicit support duration
- no false rows emitted
- absence of a row is not universal proof of no respiratory support

The same-name variable must not mean:

- noninvasive ventilation active
- CPAP-only support active
- high-flow nasal cannula active
- supplemental oxygen active
- tracheostomy status active
- intubation event only
- extubation event only
- ventilator parameter observation only
- broader mechanical ventilation or respiratory support without invasive/noninvasive separation

## Amsterdam Source Discovery Summary

Amsterdam has several respiratory-support-related source families.

The current opening evidence supports a candidate review, but not same-name approval yet.

### Strongest interval candidate

| source table | itemid | source label | source role | dictionary count | opening interpretation |
| --- | --- | --- | --- | --- | --- |
| `processitems` | `9328` | `Beademen` | candidate primary interval source | `18,471` | strongest candidate for active ventilation episode because raw rows carry `start`, `stop`, and `duration` |

Raw source shape:

- `processitems.csv` columns include `admissionid`, `itemid`, `item`, `start`, `stop`, and `duration`
- `9328 Beademen` raw rows: `18,471`
- unique `admissionid` among `9328 Beademen` raw rows: `15,950`
- duration unit follows the Amsterdam process-items opening rule: minutes derived from millisecond offsets
- duration p50 / p90 / p95 / p99: `841 / 13,810 / 23,439 / 51,674` minutes
- short nonnegative episodes `<=60m`: `296`
- prolonged episodes `>=7d`: `2,546`
- source-edge negative-duration rows: `1`
- start offsets before ICU/MC anchor: `7`
- stop offsets before ICU/MC anchor: `4`

Interpretation:

- the interval structure is promising
- the row count and duration distribution are plausible for a critical-care ventilation interval candidate
- the single negative-duration row is a validation issue that must be handled before approval
- the label `Beademen` alone is not enough to prove same-name invasive-only scope

## First Local Source-Audit Findings

Current audit judgment:

- `9328 Beademen` is a strong candidate source
- it is not yet ready for same-name mapping approval

The source audit used these checks:

- semantic label and official dictionary context
- source table grain and interval fields
- start/stop/duration quality
- neighboring NIV/CPAP/weaning exclusion boundary
- ventilator mode/device context
- intubation/extubation order-event audit
- ID/stay normalization boundary
- MIMIC `InvasiveVent` same-name contract compatibility
- runtime-readiness and unresolved blocking issues

### Process-overlap boundary checks

| adjacent source | overlap pairs with `9328` | affected admissions | affected `9328` intervals | interpretation |
| --- | ---: | ---: | ---: | --- |
| `10740 Beademen non-invasief` | `114` | `109` | `114` | noninvasive ventilation is mostly separate, but overlap must be resolved before same-name approval |
| `9671 CPAP` | `176` | `66` | `98` | CPAP is adjacent support; overlapping rows require an explicit exclusion or precedence rule |
| `9325 Weanen` | `415` | `135` | `203` | weaning can overlap active ventilation and should be audit/context, not an automatic exclusion |

Interpretation:

- overlap counts are small relative to the full `18,471` `9328` intervals
- they are not ignorable because they are exactly the boundary cases that determine whether the same-name variable stays invasive-only
- a future mapping rule must explicitly define how to handle overlap with NIV, CPAP, and weaning records

### Intubation and extubation order-event audit

| audit source | rows | unique admissions | rows in admissions with `9328` | inside `9328` interval | near `9328` start within 6h | near `9328` end within 6h |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `9476 Intuberen` | `162` | `150` | `159` | `134` | `130` | `20` |
| `9484 Extuberen` | `510` | `499` | `503` | `183` | `64` | `441` |

Interpretation:

- intubation orders cluster near `9328` starts
- extubation orders cluster near `9328` ends
- this supports the interpretation that `9328 Beademen` behaves like an active ventilation interval
- these order events are sparse and should remain audit evidence, not the primary source

### Ventilator-mode and oxygen-delivery context

The extracted target listitem context contains `735,297` rows across ventilation-mode, device, and oxygen-delivery item families.

Major adjacent or noninvasive values include:

- `CPAP/ASB`
- `CPAP_ASB`
- `BIPAP/ASB`
- `BIPAP`
- `CPAP`
- `Bipap Vision`
- ordinary oxygen-delivery values such as `O2-bril`, `Kapje`, and `Non-Rebreathing masker`

Major invasive or controlled ventilation mode values include:

- `CPPV`
- `CPPV/ASSIST`
- `IPPV`
- `IPPV/ASSIST`
- `SIMV`
- `SIMV/ASB`
- `Pressure Controled`

Interpretation:

- mode/device context exists and is rich enough to support a final interval-classification audit
- this current note has not yet classified every `9328` interval by overlapping ventilator-mode/device evidence
- that classification is the next gate before same-name mapping

## Focused Risk Audit

A focused risk audit was then run only on:

- `9328 Beademen` intervals overlapping `10740 Beademen non-invasief`
- `9328 Beademen` intervals overlapping `9671 CPAP`
- the one negative-duration `9328 Beademen` source row

This audit did not create a formal Amsterdam same-name output.

It only created local evidence for the next mapping decision.

### Risk interval counts

| risk type | count |
| --- | ---: |
| total risky overlap intervals | `290` |
| affected admissions | `174` |
| overlap with `10740 Beademen non-invasief` | `114` |
| overlap with `9671 CPAP` | `176` |
| negative-duration `9328 Beademen` rows | `1` |

### Provisional interpretation

| provisional class | count | interpretation |
| --- | ---: | --- |
| `noninvasive_overlap_requires_exclusion_or_split_review` | `114` | NIV overlap is a blocking adjacent-state signal unless later interval-level evidence proves the `9328` segment is truly invasive |
| `cpap_overlap_without_invasive_context_requires_exclusion_or_flag` | `171` | CPAP overlap lacks enough invasive-mode context and should not silently remain in same-name output |
| `cpap_overlap_with_invasive_mode_context_possible_weaning_or_mode_transition_review_required` | `5` | a small subset may represent invasive weaning or mode transition, but still requires deterministic rule review |

### Negative-duration row

The source-edge anomaly is:

- `admissionid = 9810`
- `itemid = 9328`
- `start = 717300000`
- `stop = -1899`
- `duration = -54557891`

Interpretation:

- this row is not a valid positive ventilation episode
- current fields are not sufficient to repair it safely
- it should be excluded from any candidate output and retained in audit evidence

### Risk-handling rule from this audit

Current rule before any mapping spec:

- do not promote Amsterdam same-name mapping until risky intervals are classified by deterministic retain/exclude/review rules
- treat `10740 Beademen non-invasief` overlap as a blocking adjacent-state signal unless interval-level invasive mode or airway evidence justifies retaining the `9328` segment
- treat `9671 CPAP` overlap as adjacent-state evidence; retain only if invasive/controlled ventilator mode or airway evidence supports an invasive-weaning or invasive-mode transition interpretation
- exclude the negative-duration `9328` row from any candidate output and record it in source audit
- if a candidate output is later built, each retained `9328` row should carry explicit risk flags for NIV overlap, CPAP overlap, weaning overlap, and source-duration anomaly

Current implication:

- `9328 Beademen` remains a strong candidate
- it is still not ready for formal same-name mapping
- the next gate is a candidate interval-classification table with `retain`, `exclude`, and `manual_review` labels

## Candidate Interval Classification

A conservative interval-level classification was then generated for all `18,471` `9328 Beademen` intervals.

This classification is still candidate evidence.

It is not an approved Amsterdam same-name output.

### Classification policy

| class | rule |
| --- | --- |
| `retain_candidate` | no invalid timing, NIV overlap, or CPAP overlap detected under this audit |
| `retain_candidate_with_flag` | weaning overlap without NIV/CPAP overlap or invalid timing |
| `manual_review` | NIV overlap, CPAP overlap, or ambiguous CPAP/mode context |
| `exclude` | invalid source timing, including negative or nonpositive duration |

### Classification result

| class | interval count | interpretation |
| --- | ---: | --- |
| `retain_candidate` | `18,061` | clean opening candidate intervals |
| `retain_candidate_with_flag` | `198` | likely retainable but must carry weaning-overlap flags |
| `manual_review` | `211` | cannot be silently retained or excluded without a deterministic boundary rule |
| `exclude` | `1` | invalid source timing; do not retain |

Risk flags observed in the candidate classification:

| risk flag | count |
| --- | ---: |
| `noninvasive_or_adjacent_mode_context_present` | `922` |
| `invasive_mode_context_present` | `436` |
| `nearby_extubation_order` | `511` |
| `nearby_intubation_order` | `158` |
| `overlap_noninvasive_ventilation` | `114` |
| `overlap_cpap_without_invasive_mode_context` | `95` |
| `overlap_cpap_with_invasive_mode_context` | `2` |
| `overlap_weaning` | `198` |
| `pre_anchor_timing_present` | `8` |
| `source_time_invalid` | `1` |

Interpretation:

- the large majority of `9328 Beademen` intervals are clean enough to remain same-name candidates
- the current manual-review set is small but semantically important
- the negative-duration row is excluded
- weaning overlap is not treated as automatic exclusion, but it must remain visible as a flag
- Amsterdam is closer to a same-name mapping, but the manual-review policy must be approved first

Current readiness after classification:

- source-shape gate: passed as candidate
- negative-duration handling: rule proposed, exclude
- NIV/CPAP overlap handling: not yet approved
- interval classification table: created
- Amsterdam same-name mapping spec: ready only as a candidate draft after owner policy acceptance
- Amsterdam runtime evidence: candidate execute-mode evidence exists; formal approved evidence does not

## Manual-Review Policy

The `211` manual-review intervals were then grouped into a proposed deterministic policy.

This policy is conservative.

It prioritizes same-name semantic purity over maximum sensitivity.

### Manual-review policy result

| proposed policy | interval count | interpretation |
| --- | ---: | --- |
| `exclude_from_same_name_candidate` | `205` | do not retain in the first Amsterdam same-name candidate because NIV/CPAP boundary evidence is not compatible with a clean invasive-only interpretation |
| `manual_review_keep_possible_transition` | `6` | possible invasive weaning or support-transition intervals; do not auto-retain without separate approval |

Main policy groups:

| group | count | proposed action |
| --- | ---: | --- |
| NIV overlap, no invasive mode or airway-order support | `105` | exclude |
| CPAP overlap, no invasive mode or airway-order support | `91` | exclude |
| NIV overlap with airway-order support but no invasive mode | `8` | exclude from same-name first pass |
| both NIV and CPAP overlap, no invasive mode or airway-order support | `1` | exclude |
| CPAP overlap with airway-order support or invasive mode context | `6` | possible transition; keep out of first pass unless separately approved |

Recommended conservative first-pass policy:

- retain `retain_candidate`
- retain `retain_candidate_with_flag` with a visible `weaning_overlap` flag
- exclude the one invalid-timing row
- exclude the `205` `manual_review` rows marked `exclude_from_same_name_candidate`
- do not include the `6` possible transition rows in the first same-name mapping unless the project owner separately approves a transition-retention rule

Policy acceptance record:

- accepted by project owner on 2026-05-01
- accepted as the first-pass Amsterdam same-name candidate policy only
- this acceptance permits drafting an Amsterdam mapping spec candidate
- this acceptance does not approve Amsterdam as reviewed-approved same-name `std_invasive_mechanical_ventilation_active`

If this conservative policy is accepted, the first Amsterdam same-name candidate build would use:

- `18,061` clean candidate intervals
- plus `198` weaning-flagged candidate intervals
- total retained first-pass candidate intervals: `18,259`
- excluded invalid or boundary-risk intervals: `212`

This would be a stricter but safer Amsterdam same-name candidate.

It would still require:

- Amsterdam mapping spec
- governed execution
- validation report
- manifest
- rerun reproducibility report
- formal approval review

### Adjacent process sources that must not be silently included

| source table | itemid | source label | dictionary count | same-name decision |
| --- | --- | --- | --- | --- |
| `processitems` | `10740` | `Beademen non-invasief` | `1,783` | exclude from `std_invasive_mechanical_ventilation_active`; possible future `std_noninvasive_ventilation_active` evidence |
| `processitems` | `9671` | `CPAP` | `2,953` | exclude from invasive ventilation unless separately proven as an invasive ventilator mode under an approved rule |
| `processitems` | `9325` | `Weanen` | `374` | audit-only; weaning is not itself a same-name invasive active-state source |
| `processitems` | `9171`, `9176`, `9177`, `10618` | deprecated or old tracheostoma process labels | small counts | adjacent tracheostomy/process evidence, not same-name invasive ventilation active by itself |

Interpretation:

- Amsterdam has explicit neighboring noninvasive and CPAP process concepts
- those neighboring concepts are helpful because they may allow `9328 Beademen` to remain narrow
- but this still requires source audit, not assumption

### Ventilator-mode and device observations

Potential audit or bridge sources include:

- `listitems` itemid `6685`, `Type Beademing Evita 4`
- `listitems` itemid `9534`, `Type beademing Evita 1`
- `listitems` itemid `9652`, `Type Beademing Evita 4(2)`
- `listitems` itemid `8848`, `Beademingstoestel`

These include mode or device values such as:

- `CPPV`
- `IPPV`
- `SIMV`
- `CPAP`
- `BIPAP`
- `BIPAP/ASB`
- `Bipap Vision`

Interpretation:

- these are useful for auditing ventilation-mode context
- they should not be promoted as the primary active episode source without a rule for converting point observations into intervals
- CPAP and BIPAP values must not be silently absorbed into an invasive-only variable

### Intubation and extubation orders

Potential audit sources include:

- `procedureorderitems` itemid `9476`, `Intuberen`
- `procedureorderitems` itemid `9484`, `Extuberen`

Interpretation:

- intubation and extubation are airway events, not the same object as an active ventilation interval
- they may help audit starts or stops
- they should not replace a true episode source unless a separate bridge rule is reviewed

### Ventilator parameter observations

Potential audit or downstream parameter sources include:

- `numericitems` PEEP and CPAP-related settings
- `numericitems` expiratory minute volume
- `numericitems` inspiratory and expiratory tidal volume
- `numericitems` respiratory-rate-on-ventilator rows

Interpretation:

- ventilator parameter rows can support plausibility review
- they do not by themselves define the active state boundary
- they are better suited for `std_ventilator_parameter_event` or later audit joins

## Why Same-Name Approval Still Fails Today

Amsterdam same-name approval fails today for four reasons.

### 1. Invasive-only semantics are plausible but not fully proven

The strongest source label is `Beademen`, and Amsterdam also has a separate `Beademen non-invasief`.

That separation is encouraging.

However, approval requires proof that retained `9328 Beademen` intervals are invasive mechanical ventilation active intervals under the same-name boundary.

The current evidence supports that interpretation but does not yet fully prove it because overlapping NIV/CPAP/weaning and mode-context cases still need rule-level resolution.

### 2. Episode construction has candidate governed output but is not approved

The candidate source has interval fields and now has both a candidate mapping draft and one governed candidate execute-mode run.

The candidate run did:

- normalized `admissionid` to standard `stay_id`
- emitted `support_starttime`
- emitted `support_endtime`
- emitted `support_duration_minutes`
- emitted true-only retained rows
- enforced no false rows
- validated non-null episode boundaries
- validated duplicate keys
- handled the negative-duration source-edge row
- classified or flagged intervals with adjacent support overlap

However, no reviewed-approved same-name Amsterdam build has yet:

- been accepted by final approval review
- been promoted out of candidate-only status
- been added to the approved Amsterdam implementation surface

### 3. Adjacent support states must be explicitly excluded

The same-name variable cannot silently include:

- `Beademen non-invasief`
- `CPAP`
- BIPAP device or mode evidence
- oxygen-delivery rows
- tracheostomy-only evidence

Those may become separate variables or audit sources later.

They are not approved here.

### 4. Candidate Amsterdam runtime and rerun evidence exist, but approved runtime evidence does not

Amsterdam now has a candidate mapping draft, one governed candidate runtime evidence directory, and one candidate rerun reproducibility report.

No approved same-name package exists yet for:

- formal approval review

Candidate runtime result:

| runtime field | value |
| --- | ---: |
| source `9328` rows | `18,471` |
| retained candidate rows | `18,259` |
| retained clean rows | `18,061` |
| retained weaning-flagged rows | `198` |
| manual-policy excluded rows | `205` |
| possible transition rows withheld | `6` |
| invalid-timing rows excluded | `1` |
| unique candidate `stay_id` | `15,879` |
| runtime validation status | `pass` |
| candidate rerun reproducibility status | `pass` |
| runtime evidence status | `candidate_only_not_reviewed_approved` |

The current MIMIC runtime evidence cannot approve the Amsterdam mapping.

Candidate rerun result:

| rerun field | value |
| --- | --- |
| baseline runtime directory | `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/runtime/amsterdamumcdb_1_0_2_candidate_execution` |
| rerun runtime directory | `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/runtime/amsterdamumcdb_1_0_2_candidate_rerun_repro_check` |
| reproducibility report | `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/runtime/amsterdamumcdb_1_0_2_candidate_rerun_repro_check/reproducibility_report.json` |
| primary output signature | unchanged |
| preview output signature | unchanged |
| stable build-summary fields | unchanged |

Interpretation:

- candidate output generation is reproducible under the current candidate mapping and local reference implementation
- the primary output remains `candidate_only_not_reviewed_approved`
- reproducibility pass is necessary evidence for approval, but it is not approval by itself

## Current Candidate Decision

The correct current status is:

| candidate question | current answer |
| --- | --- |
| Is Amsterdam impossible for this same-name variable? | No |
| Is there a plausible source candidate? | Yes, `processitems` itemid `9328` / `Beademen` |
| Is same-name invasive-only semantics proven? | Partly supported, not fully proven |
| Should a mapping spec be published now? | Yes, as a candidate draft only |
| Should governed runtime evidence be generated now? | Done as candidate evidence only, not approval |
| Has candidate rerun reproducibility passed? | Yes, as candidate evidence only, not approval |
| Should Amsterdam be listed as approved for this variable? | No |

Updated after focused risk audit:

| risk decision | current answer |
| --- | --- |
| Can the negative-duration row be retained? | No |
| Can NIV-overlap intervals be silently retained? | No |
| Can CPAP-overlap intervals be silently retained? | No |
| Can non-overlapping `9328` intervals proceed toward candidate classification? | Yes |
| Is formal same-name mapping ready now? | No; only a candidate mapping draft is ready |

Updated after candidate interval classification:

| classification decision | current answer |
| --- | --- |
| Are most `9328` intervals clean candidates? | Yes, `18,061 / 18,471` are `retain_candidate` |
| Are flagged weaning-overlap rows potentially retainable? | Yes, `198` are `retain_candidate_with_flag` |
| Are unresolved boundary rows still present? | Yes, `211` are `manual_review` |
| Is any row excluded immediately? | Yes, `1` invalid timing row |
| Can mapping spec be written now? | Not until the `manual_review` policy is approved |

Updated after manual-review policy:

| policy question | current proposed answer |
| --- | --- |
| How many manual-review rows should be excluded from first same-name candidate? | `205` |
| How many manual-review rows are possible transition cases? | `6` |
| Should possible transition cases be auto-retained? | No |
| First-pass retained candidate if conservative policy is accepted | `18,259` intervals |
| First-pass excluded invalid/boundary-risk intervals | `212` intervals |
| Can mapping spec be written now? | Yes, as an Amsterdam candidate mapping spec draft, because this conservative policy has been accepted |

## Required Next Governed Review Before Approval

Before Amsterdam can advance from candidate mapping to reviewed-approved same-name output, the next governed review must answer:

1. Does `9328 Beademen` mean invasive mechanical ventilation active, or a broader ventilation process?
2. Are `10740 Beademen non-invasief` and `9671 CPAP` fully separate enough to exclude NIV/CPAP from `9328`?
3. Do `9328` intervals have reliable `start`, `stop`, and `duration` fields after Layer 2 conversion?
4. How should the single negative-duration source-edge row be handled?
5. How many intervals start before or end after the ICU/MC stay anchor?
6. How often do `9328` intervals overlap with ventilator-mode observations such as `CPPV`, `IPPV`, or `SIMV`?
7. How often do `9328` intervals overlap with noninvasive evidence such as `BIPAP`, `CPAP`, or `Bipap Vision`?
8. Do intubation and extubation order events support the episode boundaries, or are they too sparse for boundary proof?
9. Does the resulting candidate distribution remain clinically plausible after excluding adjacent support states?

Current progress against those questions:

- questions 3, 4, 5, and 8 have initial source-audit evidence
- questions 1, 2, 6, 7, and 9 remain the next decision gate
- the focused risk audit has added a preliminary handling rule for NIV overlap, CPAP overlap, and the negative-duration source row
- the candidate interval-classification table now separates clean candidate intervals, retain-with-flag intervals, manual-review intervals, and excluded invalid timing rows
- the manual-review policy now has an accepted conservative first-pass candidate boundary: retain clean and weaning-flagged intervals, exclude NIV/CPAP boundary-risk intervals, and keep possible transition cases out unless separately approved
- candidate runtime evidence and rerun reproducibility evidence now exist and pass; they remain candidate evidence, not approval

Only after those questions are answered by governed runtime evidence and final review should the project decide between:

- same-name Amsterdam `std_invasive_mechanical_ventilation_active`
- a broader variable such as mechanical ventilation active
- a separate Amsterdam-specific candidate that is not published under this same name

## Practical Outcome

For the current public repository:

- `std_invasive_mechanical_ventilation_active` remains approved for `MIMIC-IV-3.1` only
- Amsterdam is now documented as a same-name feasibility candidate
- Amsterdam now has a candidate mapping draft, not a reviewed-approved mapping
- Amsterdam now has candidate runtime and rerun reproducibility evidence, not formal approved runtime evidence
- `9328 Beademen` has passed the opening source-shape audit as a promising interval candidate
- `10740 Beademen non-invasief` and `9671 CPAP` are explicit exclusion and boundary-audit targets
- the first interval-level classification is complete
- a conservative deterministic policy for the `211` manual-review intervals has been accepted by the project owner
- the accepted first-pass policy has been translated into an Amsterdam candidate mapping spec draft
- the candidate mapping has now been run once through governed execute-mode evidence
- the candidate mapping has passed rerun reproducibility with unchanged primary output signature and stable build-summary fields
- the next work item is final approval review if the project owner chooses to promote this candidate

## Source Pointers

Official/source references:

- AmsterdamUMCdb official repository: <https://github.com/AmsterdamUMC/AmsterdamUMCdb>
- AmsterdamUMCdb official legacy dictionary source: <https://raw.githubusercontent.com/AmsterdamUMC/AmsterdamUMCdb/master/amsterdamumcdb/dictionary/legacy/dictionary.csv>
- AmsterdamUMCdb official paper: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8132908/>
- MIMIC official ventilation concept SQL: <https://github.com/MIT-LCP/mimic-code/blob/main/mimic-iv/concepts/treatment/ventilation.sql>

## Final Decision

Amsterdam should continue source-audit work for possible same-name `std_invasive_mechanical_ventilation_active`.

It should not be approved or run as a formal same-name governed output until `9328 Beademen` passes final approval review after candidate execution, validation, rerun reproducibility, and explicit exclusion or flagging of neighboring noninvasive/CPAP/tracheostomy/oxygen states by rule.

Current post-policy update:

- a candidate mapping draft now exists
- candidate execute-mode runtime evidence now exists
- candidate rerun reproducibility evidence now exists and passes
- this draft encodes the accepted conservative first-pass policy
- this draft does not approve Amsterdam as a same-name implementation
- this runtime evidence should be used only as the basis for candidate result review and final approval decision
