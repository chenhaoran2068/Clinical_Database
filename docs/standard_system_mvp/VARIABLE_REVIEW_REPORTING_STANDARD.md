# Variable Review Reporting Standard

Last updated: 2026-05-04

Status: active reporting rule; may be amended when review practice improves

## Purpose

This note defines how a standard-variable review must be reported after the evidence review is completed.

A batch-level closure note is not enough.

For every reviewed variable, the report must give the human reviewer enough information to decide whether the approval decision is correct.

This standard applies to:

- formal approval reviews
- candidate reviews
- class-closure reviews
- database same-name admission reviews
- any oral or written post-review summary given to the project owner

User-facing review reports are part of the review artifact. A detailed file plus a short chat summary is not enough when the user is acting as the reviewer; the chat/oral report must also expose the evidence chain for each variable.

## Core Rule

Every reviewed variable needs an explicit per-variable review block.

The block must include at least:

- the variable identity and approved semantic boundary
- the reviewed database's standardized distribution
- comparison with already processed approved databases
- official source or dictionary alignment
- clinical, epidemiologic, or high-quality publication plausibility
- risks, caveats, and adjacent variables that were excluded
- final decision and reason

Do not report only a count such as "7 approved, 2 held" when the user is asking for variable review.

Counts are useful for a dashboard, but they are not sufficient for review.

## Required Per-Variable Sections

Each variable review block should use the following sections unless the variable class makes one section irrelevant.

### 1. Variable Identity

Report:

- `std_variable_id`
- standard meaning in plain language
- variable class and semantic grain
- reviewed database and database version
- canonical unit
- cleaned-value field and cleaned range
- whether the reviewed mapping is same-name, database-specific, derived, broader, narrower, or candidate-only

The reviewer must be able to see what semantic claim is being made before seeing the numbers.

### 2. Reviewed Database Distribution

Report the standardized distribution in the reviewed database.

Minimum numeric fields for event-level numeric variables:

- total source or output rows
- kept rows
- rows nullified or excluded by cleaning/outlier rule
- unique patients or subjects
- unique admissions or stays
- raw min, p01, p50, p95, p99, max when available
- cleaned min, p01, p50, p95, p99, max when available
- zero rows, negative rows, and extreme-tail rows when relevant
- missingness, duplicate handling, and same-time tie handling when relevant

For multi-source variables, also report source-level detail:

- source table
- source item/code
- source label
- source unit
- source row contribution
- source-specific conversion
- source-specific distribution if it affects approval

For non-numeric classes, replace these with the class-appropriate burden and distribution fields, such as episode count, duration distribution, state prevalence, category counts, route counts, or entity counts.

### 3. Comparison With Already Processed Databases

Compare the reviewed database with already processed approved databases whenever a same-name or sibling anchor exists.

Report:

- approved comparison databases
- their row burden and core distribution
- whether p50, p95, p99, prevalence, duration, or burden are in the same clinical order of magnitude
- whether differences can be explained by database structure, cohort, source frequency, unit, or collection practice
- whether a difference suggests source-scale failure or semantic mismatch

The comparison does not require identical distributions.

It does require a clear explanation for material differences.

### 4. Official Source Alignment

Report the official or database-native source evidence.

Include when available:

- official source table
- source item/code IDs
- official labels
- official units
- official category or table family
- LOINC, SNOMED CT, ICD, item concept, or database concept anchor
- official documentation statement or local dictionary field supporting the mapping
- inclusion reason for each retained source family
- exclusion reason for adjacent source families

If official evidence is ambiguous, say so.

Do not approve by name similarity alone when unit, specimen, route, timing, or grain remains ambiguous.

### 5. Clinical And Literature Plausibility

Compare the standardized result with appropriate external knowledge.

Use the best available source type for the variable:

- official database documentation
- official clinical reference ranges or laboratory interpretation pages
- high-quality ICU, epidemiology, or database papers
- established clinical scores or trial definitions when the variable feeds those constructs
- widely used database concept definitions such as MIMIC concept SQL when appropriate

Report:

- expected normal or clinical range when useful
- expected ICU or disease-cohort range when available
- whether the reviewed distribution center and tail are plausible
- whether external literature supports the unit and scale
- whether a mismatch is acceptable cohort variation or a likely standardization error

External sources are supporting evidence, not replacements for source-level proof.

### 6. Risk And Boundary Review

Report risks explicitly.

Common risk categories:

- same-name but different semantic grain
- raw event versus baseline or summary confusion
- measured value versus treatment target or device setting
- specimen confusion, such as arterial versus venous or blood versus other fluid
- monitor value versus lab value confusion
- unit label versus observed distribution conflict
- medication/order/process evidence mixed into physiologic measurement
- grouped proxy evidence presented as exact same-name evidence
- derived value hidden inside a primary-source variable
- sparse source family with unstable tail

For every important adjacent source or sibling variable, say whether it was included, excluded, or deferred.

### 7. Decision

Use one of the current decision labels, or define a more precise label if the class requires it:

- `reviewed_approved`
- `reviewed_approved_with_caveat`
- `not_approved_keep_candidate`
- `reject_or_split_identity_needed`
- `blocked_pending_source_evidence`

The decision must include one short reason stating why the evidence is enough or why it is not enough.

## Recommended Compact Template

Use this template for each variable in a written or oral review summary:

```text
Variable: <std_variable_id>

Identity:
- meaning:
- class/grain:
- reviewed database:
- canonical unit/range:

Reviewed database distribution:
- rows / kept / outliers:
- patients / admissions or stays:
- raw distribution:
- cleaned distribution:
- source-level notes:

Comparison with approved databases:
- comparison database(s):
- distribution comparison:
- interpretation:

Official/source alignment:
- retained source codes:
- labels/units:
- included and excluded adjacent sources:
- match judgment:

Clinical/literature plausibility:
- external range or published benchmark:
- match judgment:

Risks:
- remaining caveats:
- future-review trigger:

Decision:
- verdict:
- reason:
```

## Batch Reporting Rule

A batch review may start with a verdict table, but it must not stop there.

Acceptable batch structure:

1. short verdict table
2. one per-variable review block for every reviewed variable
3. cross-variable boundary notes
4. final approval and hold list

If time is limited, report fewer variables in full detail rather than reporting many variables only as a count.

When the project owner asks for an audit/review report, do not compress each variable to one sentence. For every variable covered in that response, include the reviewed database distribution, already-approved database comparison, official-source alignment, clinical/literature plausibility, risks or boundaries, and the decision.

## Amendment Rule

This reporting standard is allowed to improve.

When a later review reveals a missing check, update this document and cite the reason.

Examples of future amendments:

- add a class-specific reporting subsection for binary episodes
- add a reporting rule for first-day summary variables
- add stricter evidence requirements for external terminology mapping
- add automated fields that must be generated from runtime manifests

Do not treat this document as final forever.

Treat it as the current minimum standard.
