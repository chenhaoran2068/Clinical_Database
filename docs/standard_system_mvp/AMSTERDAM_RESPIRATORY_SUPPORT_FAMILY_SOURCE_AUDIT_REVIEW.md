# Amsterdam Respiratory-Support Family Source Audit Review

Review date: 2026-05-02

Database: `AmsterdamUMCdb-1.0.2`

Scope: Class 3 respiratory-support family after the approved Amsterdam invasive mechanical ventilation same-name mapping.

## Decision Summary

Amsterdam respiratory-support family source audit is complete for the current third-layer scope.

The current decisions are:

- `std_noninvasive_ventilation_active`: approvable as same-name, using `processitems` itemid `10740` / `Beademen non-invasief` plus itemid `9671` / `CPAP`
- `std_tracheostomy_status_active`: approvable as same-name, using `processitems` itemid `12635` / `Tracheostoma`
- `std_high_flow_nasal_cannula_active`: not approvable under current evidence because no narrow Amsterdam HFNC / high-flow nasal cannula / Optiflow source was found
- `std_supplemental_oxygen_active`: not approvable as a Class 3 active episode under current evidence because the available oxygen evidence is event/device/flow evidence, not a governed active interval source

This source audit does not change the already approved Amsterdam invasive ventilation boundary:

- `std_invasive_mechanical_ventilation_active` remains sourced from `processitems` itemid `9328` / `Beademen`
- NIV/CPAP, oxygen-only device evidence, and tracheostomy status remain separate from invasive ventilation

## Source Surface

Primary interval source table:

- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/reviewed_unsplit/processitems_interval.parquet`

Supporting stay/patient source:

- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/reviewed_unsplit/admissions_core.parquet`

Dictionary source:

- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/reviewed_unsplit/amsterdam_item_dictionary_legacy.parquet`

Key process concepts:

- `9328` / `Beademen`: approved invasive mechanical ventilation active source
- `10740` / `Beademen non-invasief`: approved NIV source
- `9671` / `CPAP`: approved CPAP/NIV-family source
- `12635` / `Tracheostoma`: approved tracheostomy status source
- `9171`, `9176`, `9177`, `10618`: legacy no-longer-used tracheostomy process concepts, not included in the approved same-name tracheostomy output

Key oxygen/device evidence:

- `listitems` itemid `8189` / `Toedieningsweg`
- values include `O2-bril`, `Kapje`, `Non-Rebreathing masker`, `CPAP`, `Trach.stoma`, `Spreekcanule`
- `numericitems` itemid `8845` / `O2 l/min`
- procedure orders include `Zuurstofkapje geven`, `Diep nasaal zuurstof geven`, and `Neusbril geven`

Those oxygen/device rows are clinically useful, but they are not yet approved as active supplemental-oxygen episodes.

## Approved Interval Sources

`std_noninvasive_ventilation_active`:

- source rows: `4,736`
- `9671 / CPAP`: `2,953`
- `10740 / Beademen non-invasief`: `1,783`
- invalid timing rows: `0`
- output rows after same-variable overlap merge: `4,566`
- unique `subject_id`: `1,309`
- unique `stay_id`: `1,414`

`std_tracheostomy_status_active`:

- source rows: `1,940`
- `12635 / Tracheostoma`: `1,940`
- invalid timing rows: `0`
- output rows: `1,940`
- unique `subject_id`: `1,081`
- unique `stay_id`: `1,275`

## Blocked Same-Name Sources

`std_high_flow_nasal_cannula_active`:

- dictionary search found no `HFNC`, `high-flow`, `high flow`, `Optiflow`, or high-flow nasal-cannula source
- oxygen flow or route rows are not enough to infer HFNC
- `HFO-Bias-flow` is not accepted as HFNC

`std_supplemental_oxygen_active`:

- oxygen route and flow evidence exists
- current evidence is event-level or order/device evidence rather than active start-stop episode evidence
- same-name approval is blocked until a governed intervalization rule is defined and validated

## Family Boundary

The Amsterdam respiratory-support third layer is therefore closed as follows:

- approved same-name active episodes: invasive ventilation, NIV/CPAP, tracheostomy status
- blocked same-name active episodes under current evidence: HFNC, supplemental oxygen
- future work may create new event-stream variables for oxygen device/flow or later promote supplemental oxygen after a governed episode-construction rule exists

The current closure prioritizes semantic safety over forcing every MIMIC sibling into Amsterdam.
