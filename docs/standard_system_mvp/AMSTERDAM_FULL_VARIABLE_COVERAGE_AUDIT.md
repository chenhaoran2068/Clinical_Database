# Amsterdam Full Variable Coverage Audit

Last generated: 2026-05-03T22:58:30Z

## Purpose

This audit assigns the current public standard-variable universe to Class 1-9 and labels each variable with an AmsterdamUMCdb-1.0.2 feasibility bucket.

The four Amsterdam buckets are:

- `same_name_ready`: same-name route ready or already approved
- `split_identity_needed`: Amsterdam needs a split/proxy/local critical-care identity
- `bounded_candidate_only`: source evidence exists, but approval requires bounded source review
- `not_supported_or_blocked`: not supported or blocked under current Amsterdam source evidence

Machine-readable outputs:

- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_variable_coverage_audit.csv`
- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_variable_coverage_audit.json`

Build-first / approval-later execution queue generated from this audit:

- `docs/standard_system_mvp/CLASS1_TO_CLASS9_EXECUTION_QUEUE.md`
- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_class1_to_class9_execution_queue.csv`
- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_class1_to_class9_execution_queue.json`

## Source Surface Scanned

- `admissions_core`: ICU/MCU admission rows, gender, grouped age/weight/height, origin/destination, stay boundary, and date-of-death fields.
- `numericitems_event`: high-volume bedside numeric observations, blood gases, routine labs, device settings, and numeric intake/output records.
- `listitems_event`: categorical/ordinal bedside states, admission context, retrospective score/admin fields, and selected support or assessment states.
- `drugitems_event`: medication and continuous infusion records, including vasoactive support and fluid inputs.
- `processitems_interval`: start-stop process/device intervals, including ventilation/RRT/tracheostomy-adjacent states.
- `procedureorderitems_event`: procedure/order workflow records, not a full hospital CPOE equivalent.
- `freetextitems_event`: free-text events, useful for bounded review only.
- `amsterdam_item_dictionary_legacy`: official legacy item dictionary mirror used for item-level source search.

## Headline Counts

- public variable denominator: `465`
- already public-covered in Amsterdam: `41`
- `same_name_ready`: `56`
- `split_identity_needed`: `15`
- `bounded_candidate_only`: `266`
- `not_supported_or_blocked`: `128`

## Counts By Class

| Class | Total | same_name_ready | split_identity_needed | bounded_candidate_only | not_supported_or_blocked |
| --- | ---: | ---: | ---: | ---: | ---: |
| Class 1: event-level numeric primary-source | `296` | `33` | `0` | `153` | `110` |
| Class 2: baseline/summary/window numeric | `21` | `6` | `8` | `7` | `0` |
| Class 3: binary state/active flag/episode | `23` | `9` | `0` | `14` | `0` |
| Class 4: treatment/device/input-output event stream | `30` | `2` | `0` | `23` | `5` |
| Class 5: episode/interval/follow-up bridge | `30` | `2` | `4` | `24` | `0` |
| Class 6: ordinal/text/semiquantitative result | `18` | `0` | `0` | `18` | `0` |
| Class 7: diagnosis/admin/demographic/id-map | `17` | `4` | `3` | `0` | `10` |
| Class 8: score/phenotype/composite derived | `27` | `0` | `0` | `27` | `0` |
| Class 9: microbiology multi-entity family | `3` | `0` | `0` | `0` | `3` |

## Immediate Same-Name High-Yield Batch

These are not yet approvals. They are the recommended next governed Amsterdam candidate batch because they are direct ICU numeric event variables with high downstream reuse.

| Order | Variable | Class | Source scan | Rationale |
| ---: | --- | --- | --- | --- |

## Interpretation

`same_name_ready` means Amsterdam can enter governed candidate execution under the current standard variable identity, or is already approved. It is not a blanket approval.

`split_identity_needed` means Amsterdam has useful data, but using the MIMIC same name would mix hospital-level, exact-measurement, or other incompatible semantics.

`bounded_candidate_only` means source evidence exists but the row family, item set, unit, interval, or parent-link rule still needs focused review before approval.

`not_supported_or_blocked` means the current Amsterdam opening source surface does not support the required same-name source structure.

## Immediate Recommendation

Start with the high-yield Class 1 batch above, then rerun this audit after each approved batch so Amsterdam coverage moves from source-ready to governed-approved in controlled waves.
