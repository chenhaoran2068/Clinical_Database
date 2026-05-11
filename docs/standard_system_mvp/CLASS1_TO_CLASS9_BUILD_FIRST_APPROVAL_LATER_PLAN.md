# Class 1-9 Build-First Approval-Later Execution Plan

Last updated: 2026-05-04

Status: active execution-order rule; owner approval intentionally deferred

## Purpose

This note records the revised execution strategy requested by the project owner.

The project owner is not approving the current Class 1 review batch yet. The preferred strategy is to first complete the buildable work across Class 1-9, classify the non-buildable or unsafe variables clearly, and then run owner approval on larger, better-contextualized review packets.

The governing idea is:

- build what can be built directly
- preserve evidence for every build
- hold variables when source, unit, specimen, or semantic identity is unsafe
- defer variables that require already approved upstream variables
- approve later in structured owner-review waves

## Core Interpretation

Build completion is not the same as owner approval.

Technical review recommendation is not the same as owner approval.

Public synchronization is allowed for GitHub-safe artifacts, but public coverage must not overclaim owner-approved status for variables that are only built, technically reviewed, held, or deferred.

The current Amsterdam Class 1 Batch2 review should therefore be read as a technical evidence review and approval recommendation for its approved subset, not as final project-owner approval.

## Working Status Labels

Use these labels while executing the new strategy:

| status | meaning |
| --- | --- |
| `not_started` | variable has not entered governed build work |
| `direct_build_queue` | source identity looks direct enough to build without upstream approval dependencies |
| `built_runtime_repro_pass` | governed build, first execution, rerun, and reproducibility evidence exist |
| `technical_review_recommend_approve` | reviewer evidence supports approval, but owner approval is still pending |
| `technical_review_recommend_approve_with_caveat` | reviewer evidence supports approval with an explicit caveat, but owner approval is still pending |
| `hold_candidate_problem_found` | build or review found a source, unit, specimen, grain, or distribution problem; keep candidate evidence but do not approve |
| `deferred_pending_approved_parent` | variable needs one or more upstream variables to be owner-approved first |
| `split_identity_needed` | Amsterdam has useful data, but not under the current same-name variable identity |
| `blocked_current_source_surface` | current Amsterdam opening source surface does not support a safe build |
| `owner_approved` | project owner has explicitly approved after review |

## Current Audit Surface

The current Amsterdam audit denominator is `465` public variables.

Generated execution queue:

- `docs/standard_system_mvp/CLASS1_TO_CLASS9_EXECUTION_QUEUE.md`
- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_class1_to_class9_execution_queue.csv`
- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_class1_to_class9_execution_queue.json`

Generated Q4/Q3-Q7 execution registers:

- `docs/standard_system_mvp/AMSTERDAM_Q4_BOUNDED_CANDIDATE_BATCH_BUILD_REGISTER.md`
- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_q4_bounded_candidate_batch_build_register.csv`
- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_q4_bounded_candidate_source_item_hits.csv`
- `docs/standard_system_mvp/AMSTERDAM_Q4_CLASS1_WAVE1_RUNTIME_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_q4_class1_wave1_runtime_plan.json`
- `docs/standard_system_mvp/AMSTERDAM_Q3_Q5_Q6_Q7_FREEZE_DEPENDENCY_SPLIT_REGISTER.md`
- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_q3_q5_q6_q7_freeze_dependency_split_register.csv`

Current bucket counts from the coverage audit:

| Class | Total | same-name ready | split identity needed | bounded candidate only | blocked |
| --- | ---: | ---: | ---: | ---: | ---: |
| Class 1: event-level numeric primary-source | 296 | 33 | 0 | 153 | 110 |
| Class 2: baseline/summary/window numeric | 21 | 6 | 8 | 7 | 0 |
| Class 3: binary state/active flag/episode | 23 | 9 | 0 | 14 | 0 |
| Class 4: treatment/device/input-output event stream | 30 | 2 | 0 | 23 | 5 |
| Class 5: episode/interval/follow-up bridge | 30 | 2 | 4 | 24 | 0 |
| Class 6: ordinal/text/semiquantitative result | 18 | 0 | 0 | 18 | 0 |
| Class 7: diagnosis/admin/demographic/id-map | 17 | 4 | 3 | 0 | 10 |
| Class 8: score/phenotype/composite derived | 27 | 0 | 0 | 27 | 0 |
| Class 9: microbiology multi-entity family | 3 | 0 | 0 | 0 | 3 |

These buckets are execution guidance, not approval decisions.

## Execution Queue Policy

### Queue A: Direct Same-Name Builds First

Build variables first when all of the following are true:

- same-name identity appears plausible
- source table and source item/code family are direct
- unit conversion is deterministic
- cleaning range is already class-compatible or can be justified from source evidence
- no upstream approved variable is required
- no major specimen, route, interval, or grain conflict is visible

Preferred order inside Queue A:

1. remaining direct Class 1 event-level numeric variables
2. direct Class 7 demographic/admin/id-map variables with stable grain
3. direct Class 6 ordinal or semiquantitative result variables with finite source result domains
4. direct Class 3 active-state variables with explicit active intervals or status rows
5. direct Class 4 treatment/device/input-output event streams with source-faithful event rows
6. direct Class 5 interval variables where the source itself provides start and end boundaries

For each variable, produce:

- governed variable directory or approved extension path
- mapping spec
- `execution.py`
- first execution runtime evidence
- rerun reproducibility evidence
- source/distribution review packet
- GitHub-safe public-card or metadata update without overclaiming owner approval

### Queue B: Bounded Candidates With Real Evidence

Build bounded candidates when the data are useful but require careful review.

Examples:

- multiple candidate item families with ambiguous source boundary
- blood versus other-fluid or arterial versus venous uncertainty
- monitor measurement versus lab measurement risk
- source unit label versus observed distribution conflict
- direct source exists but sparse tail or mixed-scale behavior needs adjudication

Queue B output should usually be:

- `built_runtime_repro_pass`
- `hold_candidate_problem_found`, or
- `technical_review_recommend_approve_with_caveat`

Do not force a candidate into approval just because it can be built.

### Queue C: Dependency-Driven Derived Variables

Defer variables that require upstream owner-approved parents before a safe final build.

This includes:

- Class 2 baseline, summary, first-day, daily, or follow-up window variables derived from event streams
- Class 5 free-day or follow-up bridge variables requiring approved support episodes
- Class 8 scores, phenotypes, onset definitions, helper variables, and composite criteria packages
- any ratio or calculation that depends on upstream standardized components

Candidate dry-runs may be useful for engineering, but approval-facing builds should wait until required parents are owner-approved or explicitly marked acceptable as bounded upstream inputs.

### Queue D: Split Identity Or Local Proxy Route

Use this queue when Amsterdam has useful information but same-name identity would be false.

Examples:

- grouped age rather than exact age
- grouped or proxy body weight rather than exact measured weight
- ICU/MCU local timing rather than hospital-admission timing
- source-bounded support family rather than full cross-database support identity

The correct output is a split variable identity, local proxy identity, or explicit non-approval note, not a forced same-name mapping.

### Queue E: Blocked Current Source Surface

Do not spend build time on variables whose required source family is absent from the current Amsterdam opening surface.

Keep them in the audit as blocked, with a short reason and any future source that could reopen them.

## Approval Wave Policy

Owner approval should happen after enough variables have been built and reviewed to make the context visible.

Recommended owner-review waves:

1. Class 1 direct numeric completion wave
2. Class 6 and Class 7 direct low-dependency wave
3. Class 3 direct active-state wave
4. Class 4 and Class 5 direct treatment/interval wave
5. Class 2 dependent summary/baseline wave after parent approval
6. Class 8 score/phenotype/composite wave after all required components are approved
7. Class 9 microbiology wave only after Amsterdam source hierarchy proves parent/branch/leaf equivalence

Each approval wave must include:

- an approve-ready list
- a hold list
- a deferred-dependency list
- a split-identity list
- a blocked list
- per-variable review blocks following `VARIABLE_REVIEW_REPORTING_STANDARD.md`

## Immediate Execution Order

Use this order for the next work cycle:

1. Freeze current no-owner-approval state.
   - Amsterdam Class 1 Batch2 remains technical review evidence, not final owner approval.
   - Do not spend the next round trying to get owner approval for those variables.

2. Build or update the full Class 1-9 queue table from the audit CSV.
   - Columns must include class, bucket, dependency status, direct-build status, current runtime status, review status, and owner-approval status.

3. Start Queue A direct builds.
   - Prefer variables already marked `same_name_ready`.
   - Within the same class, prioritize high downstream reuse and simple source identity.

4. During each build, immediately classify problems.
   - If a problem appears, move the variable to Queue B, D, or E.
   - Do not stall the whole campaign on one problematic variable.

5. Keep derived variables in Queue C until parents are approved.
   - Do not approve Class 2 or Class 8 variables that require unapproved upstream components.

6. After a meaningful group is ready, prepare an owner-review packet.
   - The packet should be detailed enough for approval, but approval happens only when the project owner explicitly approves.

7. After owner approval, sync final public coverage.
   - Refresh public metadata.
   - Rerun coverage audit.
   - Run `check_public_repository.py`.

## Practical Consequence

The campaign should no longer be blocked by unresolved variables such as Amsterdam `std_pt` or arterial blood-gas oxygen saturation.

Those should remain visible hold candidates while direct-buildable variables in Class 1-9 continue moving forward.

The goal is a complete map of:

- what is built and ready for owner approval
- what is built but held
- what is deferred because approved parents are required
- what needs a split identity
- what is blocked under the current source surface

Only then should the owner approve in structured batches.
