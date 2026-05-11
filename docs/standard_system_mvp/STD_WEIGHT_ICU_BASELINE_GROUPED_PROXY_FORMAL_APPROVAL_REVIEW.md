# std_weight_icu_baseline_grouped_proxy Formal Approval Review

Last updated: 2026-04-25

## Approval Verdict

Formal decision:

- `std_weight_icu_baseline_grouped_proxy` is approved as a governed `AmsterdamUMCdb-1.0.2` class-2 variable under the current `baseline_summary_window_numeric` approval standard

Blocking-findings judgment:

- no blocking Amsterdam semantic finding remains after splitting it away from `std_weight_admission_baseline`
- no blocking Amsterdam runtime-evidence finding remains
- no blocking public-card publication issue remains

This approval intentionally creates a separate grouped/proxy variable.

It does not approve the Amsterdam candidate as the same variable as:

- `std_weight_admission_baseline`
- `std_weight_icu_baseline`

## Scope

This review covers:

- `docs/standard_system_mvp/std_weight_icu_baseline_grouped_proxy/variable_spec.json`
- `docs/standard_system_mvp/std_weight_icu_baseline_grouped_proxy/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_weight_icu_baseline_grouped_proxy/execution.py`
- current governed runtime evidence on `AmsterdamUMCdb-1.0.2`
- `docs/std_variable_cards/std_weight_icu_baseline_grouped_proxy.md`
- local reviewed-approved Amsterdam Layer 5 evidence for `std_weight_icu_baseline_grouped_proxy`

## Current Approved Meaning

The approved current meaning is:

- one retained row per Amsterdam ICU/MCU local admission encounter
- ICU/MCU admission-context baseline body-weight proxy
- canonical unit: `kg`
- current storage/display rule: `round(2)`
- primary source: `admissions_core.weightgroup`
- primary value semantics: grouped bucket mapped to a kilogram proxy
- repair-only fallback: one near-admission `std_weight_event` row within `+/-360` minutes only when `weightgroup` is missing
- unresolved rows are retained with null `std_weight_kg_baseline`

This variable is:

- a grouped/proxy numeric variable
- useful for coarse adjustment, stratification, descriptive summaries, and transparent Amsterdam baseline body-size context

This variable is not:

- exact continuous measured body weight
- hospital-admission baseline weight
- a replacement for event-level `std_weight_event`
- a same-name cross-database equivalent of MIMIC `std_weight_icu_baseline`

## Current Amsterdam Implementation Reviewed

Current approved implementation:

- primary source table: `admissions_core`
- primary source field: `weightgroup`
- source-context field: `weightsource`
- source-context fallback: `listitems_event` itemid `10697`
- repair-only event source: `std_weight_event`
- repair window: `+/-360` minutes relative to local admission
- local retained key: `admissionid`
- local patient key: `patientid`

Current bucket-to-proxy mapping:

- `59- -> 59.0`
- `60-69 -> 64.5`
- `70-79 -> 74.5`
- `80-89 -> 84.5`
- `90-99 -> 94.5`
- `100-109 -> 104.5`
- `110+ -> 110.0`

Interpretation:

- closed buckets use midpoint proxies
- open boundary buckets use conservative boundary proxies
- open boundary buckets are not hidden averages

Current retained output summary:

- `total_rows = 23,106`
- `unique_patientid = 20,109`
- `unique_admissionid = 23,106`
- `nonnull_baseline_rows = 22,206`
- `null_baseline_rows = 900`
- `admissions_weightgroup_proxy_rows = 22,160`
- `event_fallback_rows = 46`
- `unresolved_rows = 900`
- p25 / p50 / p75 = `70.0 / 74.5 / 84.5 kg`

Current representation summary:

- closed bucket midpoint proxy rows: `19,397`
- open lower boundary rows: `1,845`
- open upper boundary rows: `918`
- exact near-admission event fallback rows: `46`
- unresolved rows: `900`

Current source-context summary:

- measured context rows: `1,771`
- anamnestic context rows: `10,235`
- estimated context rows: `6,142`
- unknown context rows: `4,958`
- source-context discordance rows: `611`

Current governed runtime status:

- first execute-mode runtime validator: `pass`
- rerun execute-mode runtime validator: `pass`
- rerun reproducibility gate: `pass`

Stable rerun evidence:

- `primary_output_asset` signature is invariant across reruns
- `preview_csv` signature is invariant across reruns
- stable build-summary fields match across reruns
- process-batch IDs differ as expected between first run and rerun

## Official-Source Alignment Review

Current official-alignment judgment: acceptable for this proxy variable.

The Amsterdam official source surface supports this split because:

- the official `admissions` table is an ICU/MCU admission table
- `admissionid` is the local ICU admission identifier
- `weightgroup` is categorized weight at admission in kg
- `weightsource` records whether the weight was measured, estimated, or asked/anamnestic

Interpretation:

- Amsterdam's source is naturally grouped/proxy, not exact continuous weight
- Amsterdam's local admission context is ICU/MCU admission, not a separately verified hospital admission
- this new variable name and contract preserve those official semantics instead of hiding them

## Public Plausibility Review

Current plausibility judgment: acceptable.

The retained distribution:

- p25 / p50 / p75 = `70.0 / 74.5 / 84.5 kg`

This is plausible for adult ICU/MCU baseline body-size context and is exactly shaped by the official grouped buckets.

The key plausibility check is not whether this matches exact continuous MIMIC weight.

The key check is whether:

- grouped bucket midpoints appear in the expected values
- open boundary buckets remain visible as proxy classes
- event fallback remains rare and repair-only
- unresolved rows remain explicit

Those checks pass.

## Public-Card Review

Current judgment:

- the public card is publication-safe
- the public card correctly states Amsterdam-only approval
- the public card warns that this is grouped/proxy, not exact continuous bedside measurement
- the public card warns that event fallback is repair-only
- the public card warns that open boundary groups require caution

## Final Approval Decision

`std_weight_icu_baseline_grouped_proxy` now satisfies the current approval bar for an Amsterdam-only class-2 governed MVP:

- machine-readable variable lock present
- reviewed Amsterdam mapping spec present
- governed `execution.py` present
- execute-mode runtime evidence present on `AmsterdamUMCdb-1.0.2`
- rerun reproducibility evidence present on `AmsterdamUMCdb-1.0.2`
- public interpretation acceptable
- official-source alignment acceptable
- public plausibility acceptable
- same-name boundary against exact baseline-weight variables is explicit

Formal conclusion:

- approve `std_weight_icu_baseline_grouped_proxy` as the Amsterdam grouped/proxy baseline-weight variable split out from the rejected same-name `std_weight_admission_baseline` candidate

## Boundary Of This Approval

This note does not claim:

- that grouped/proxy weight equals exact measured weight
- that `59-` and `110+` are true means
- that this variable should be used for precise dose calculations without sensitivity analysis
- that this variable is a hospital-admission baseline variable
- that this variable is a cross-database equivalent of MIMIC `std_weight_icu_baseline`

This note does claim:

- the current Amsterdam grouped/proxy asset is valid under its own explicit variable identity
- the proxy transformation is transparent and reproducible
- users can use it when grouped baseline body-size context is acceptable

## Source Pointers

Public official/source references used in this review:

- AmsterdamUMCdb official repository README: <https://github.com/AmsterdamUMC/AmsterdamUMCdb>
- AmsterdamUMCdb official `admissions` wiki: <https://github.com/AmsterdamUMC/AmsterdamUMCdb/wiki/admissions>
- AmsterdamUMCdb official `listitems` wiki: <https://github.com/AmsterdamUMC/AmsterdamUMCdb/wiki/listitems>
- AmsterdamUMCdb official paper: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8132908/>
