# Variable Review Reporting Standard

Last updated: 2026-05-29

Status: active owner-review reporting rule

This document records the mandatory reporting structure for all standard-variable
reviews. It applies to oral reports, written owner-review packets, formal approval
reviews, candidate reviews, database-specific reviews, and batch closure notes.

A short dashboard count is never enough for owner review. Every variable that is
being reviewed must expose its evidence chain, semantic boundary, temporal rule,
system-level blind spots, downstream-use contract, and final decision.

## Non-Negotiable Rule

Do not mark a variable owner-approved until the owner explicitly approves it after
the review report.

Build success, reproducibility pass, technical recommendation, and Codex review
are not owner approval.

Every owner-facing report must end with one of these states:

- `reviewed_approved`: approved under the stated contract.
- `reviewed_approved_restricted_partial`: approved only for the stated partial or restricted interpretation.
- `reviewed_approved_unavailable`: reviewed and approved as unavailable/not safely constructible.
- `blocked`: blocked by unresolved source, semantic, timing, or reconstruction risk.
- `pending_owner_decision`: reviewed, but owner approval has not yet been given.

## Required Seven-Part Review Structure

Each reviewed variable must be reported with the following seven sections unless
the variable class makes a subsection irrelevant. If a subsection is irrelevant,
state why rather than silently skipping it.

### I. Asset Identity & Final Verdict

This is the owner-facing signature block. It must be stated first.

Report:

- `std_variable_id`.
- Plain-language meaning.
- Variable class and physical grain: point event, active interval, measurement, summary, bridge, endpoint, or evidence layer.
- Database(s) reviewed and database version(s).
- Lineage: exact source tables, source fields, itemids, concept codes, status labels, and parent assets.
- Materialization state: parquet present/absent, row count, subject/admission/stay coverage as appropriate.
- Core distribution: value or duration median, P25/P75, min/max, missingness, and major extreme tails.
- Final verdict by database: approved, restricted partial, unavailable, blocked, or pending.
- One-sentence interpretation: what this asset can be used for, and what it cannot represent.

Class adjustment:

- Event variables must report event count and unique subjects/admissions/stays.
- Active intervals must report interval count, coverage, duration distribution, overlap/merge burden, short intervals, and long intervals.
- Numeric measurements must report raw and cleaned distributions, unit conversions, outliers, and source contribution.
- Endpoints must report numerator, denominator, missingness, censoring, and whether `0`, `1`, and `NA` are all source-supported.

### II. Clinical Semantics & Physical Boundaries

This section defines the indication and contraindication of the asset.

Report:

- Positive semantic claim: what the asset means clinically.
- Negative firewall: adjacent concepts it does not mean.
- Physical form: point event, active interval, state flag, longitudinal measurement, or derived summary.
- Whether the output has true clinical duration or only documentation duration.
- Whether absence of a row can ever be interpreted as clinical absence.
- Threshold and inclusion floor for composite concepts.

Mandatory examples of boundary checks:

- HFNC must state whether it is label-defined or requires numeric flow/FiO2 thresholds.
- NIV/CPAP must state whether chronic/home/OSA CPAP is excluded, retained, or unresolved.
- Tracheostomy must state whether it is treated as an interface, a procedure, or an active support state.
- FiO2, oxygen flow, and oxygen device rows must not be treated as respiratory support intervals unless a reconstruction rule approves them.

### III. Temporal Mechanics & Reconstruction Rules

This section is mandatory for all time-aware assets.

Report:

- Time anchor: ICU admission, hospital admission, randomization, source admission, procedure start, chart time, or discharge.
- For point events: the single valid event timestamp and whether any end time is clinically meaningful.
- For intervals: start/end source fields, duration field, and whether intervals are source-supplied or reconstructed.
- Gap rule: exact threshold for merging versus splitting intervals.
- Overlap rule: whether overlapping intervals are unioned, prioritized, split, or kept as collisions.
- Carry-forward rule if point evidence is converted to interval evidence.
- Right-censoring rule, especially ICU discharge and hospital discharge clipping.
- Pre-ICU, post-ICU, and negative-relative-time handling.
- Extreme-tail interpretation: short intervals, long intervals, impossible times, and source-order conflicts.

Default rule:

- If no explicit carry-forward or state-machine rule exists, point events must remain point events.
- If no explicit gap rule exists, interval stitching is not approved.

### IV. Conflicts, Hierarchy & System-Level Blind Spots

This section records the data-ecosystem risks that ordinary row counts miss.

Report:

- State hierarchy when same-family states collide, such as `IMV > NIV > HFNC > ordinary oxygen`.
- Whether the asset is mutually exclusive mode evidence or binary any-state evidence.
- Interface versus support-mode distinction, such as tracheostomy or ETT versus invasive ventilation.
- Systematic false negatives caused by workflow split, such as OR procedure, billing, ICD, HCPCS, bedside charting, and respiratory-therapy table separation.
- Mixed-label contamination, such as extubation mixed with decannulation or acute NIV mixed with home CPAP.
- Cross-variable linkage needed for interpretation.
- Any official logic that conflicts with local Layer 5 assumptions.

The report must explicitly say when a database-specific source surface is only a
partial view of the clinical reality.

### V. Downstream Usage Contract & Red Lines

This section is written for the analyst who will later use the asset.

Report:

- Permitted use cases.
- Prohibited use cases.
- Mandatory study-window clipping, if needed.
- Missingness interpretation.
- Whether missing rows can be treated as negative. In most positive-only assets, they cannot.
- Whether the asset is eligible for primary analysis, sensitivity analysis, adjudication only, or unavailable.
- Required flags or filters for default analysis.
- Whether downstream must report availability, missingness, selection bias, or exposure-window sensitivity.

Hard red lines:

- Do not treat absence of a positive-only row as clinical absence unless the approval contract explicitly allows it.
- Do not infer a child concept by subtracting one approved asset from another, such as broad ventilation minus invasive ventilation equals noninvasive ventilation.
- Do not convert point events into active intervals without a reviewed reconstruction rule.
- Do not use procedure events as treatment-duration evidence unless the approval contract says so.
- Do not use foundation active-support assets directly as free-day outcomes; free-day outcomes require separate death and censoring rules.
- Do not silently merge direct evidence, proxy evidence, and unavailable evidence under the same interpretation.

### VI. Official, External, And Cross-Database Plausibility Check

This section explains whether the result is coherent outside the local build.

Report:

- Official SQL, dictionary, concept, item, code, or documentation alignment.
- Whether the local source labels and units match the official/source-native meaning.
- Comparison with already processed approved databases.
- Comparison with source-design expectations, case mix, or published database documentation when available.
- Whether prevalence, duration, missingness, value distribution, or extreme tails are clinically plausible.
- Whether differences are explained by database design, cohort, source frequency, unit, timing, or collection practice.

External benchmarks support the review. They do not replace source-level proof.

### VII. Evidence Chain, Reproducibility & Archival Closure

This section makes the review executable and auditable.

Report:

- Layer 3 parquet path or explicit no-parquet status.
- Layer 5 review/audit document path.
- Extract/build code path.
- Query summary, preview, runtime log, validation report, and audit JSON paths when present.
- MasterIndex status after review.
- SchemaRegistry status after review.
- AvailabilityMatrix status after review.
- Public/GitHub method documentation status when relevant.
- Whether old pending or contradictory status labels remain.
- Owner approval date and exact approved wording.

After owner approval, the closure step must update all relevant registries and
review files in the same round. If a file is deliberately not updated because it
is a historical runtime artifact, state that explicitly.

## Compact Owner-Report Template

Use this template for each variable in oral or written review.

```text
Variable: <std_variable_id>

I. Asset identity and final verdict
- class/grain:
- lineage:
- materialization:
- row/subject/admission/stay coverage:
- core distribution:
- final database statuses:
- one-sentence verdict:

II. Clinical semantics and physical boundaries
- positive meaning:
- negative firewall:
- physical form:
- threshold/inclusion floor:

III. Temporal mechanics and reconstruction rules
- timestamp or start/end rule:
- gap/carry-forward/reconstruction rule:
- short/long/pre-ICU/post-ICU handling:

IV. Conflicts, hierarchy, and blind spots
- hierarchy/collision rule:
- false-negative risks:
- mixed-label contamination:
- cross-variable dependencies:

V. Downstream usage contract and red lines
- allowed use:
- forbidden use:
- missingness rule:
- mandatory filters or time-window clipping:

VI. Official/external/cross-database plausibility
- official alignment:
- cross-database comparison:
- clinical plausibility:

VII. Evidence chain and archival closure
- local evidence paths:
- registry/matrix status:
- GitHub/public status:
- owner approval state:
```

## Batch Reporting Rule

A batch review may start with a short verdict table, but it must not stop there.

Acceptable batch structure:

1. Batch verdict table.
2. Per-variable seven-part review block.
3. Cross-variable dependency and collision notes.
4. Final approval/hold/unavailable list.
5. Registry and archival closure checklist.

If time is limited, report fewer variables in full detail rather than many
variables as shallow counts.

## Amendment Rule

This standard is the current minimum. When a later review exposes a missing
check, update this document in the same round and cite the reason.

Examples of required amendments:

- a new class-specific temporal rule is discovered;
- a source-family false-negative mechanism is found;
- an anti-subtraction failure occurs;
- an official definition conflicts with the local build;
- an approval was previously marked before explicit owner confirmation.

The standard exists to prevent forgotten caveats and unenforced review rules.
