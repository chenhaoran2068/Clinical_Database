# std_apacheii_reconstructed_first24h Owner Approval Record

- status: `reviewed_approved`
- approved database: `MIMIC-IV-3.1`
- approved variable identity: `std_apacheii_reconstructed_first24h`
- approval date: `2026-05-09`
- owner: `ChenHR`
- processor: `Codex`

## Approved Route

`std_apacheii_reconstructed_first24h` is approved as the MIMIC-IV-3.1 first-24h APACHE II reconstruction route.

The approved main score is:

- `std_apacheii_reconstructed_total_missing_normal_with_strict_chronic_proxy`

The approved main route uses:

- first ICU 24h component reconstruction, clipped at ICU outtime;
- APACHE II component scoring from first-day worst values;
- oxygen missing-normal scoring with explicit any-support and severe-support guardrails;
- strict chronic-health proxy;
- strict acute renal failure creatinine doubling using KDIGO stage 2/3 or first-day RRT, excluding chronic dialysis-only overlap;
- medication-only strict immunosuppression whitelist excluding low-dose rheumatology/IBD drugs and common TNF-alpha inhibitors unless strict ICD evidence is also present.

## Approved Boundaries

This approval is bounded to MIMIC-IV-3.1 and the documented reconstruction rule lock.

The following are retained as sensitivity/reference fields, not as the approved main score:

- strict-complete APACHE II;
- broad chronic proxy totals;
- no-chronic totals;
- KDIGO stage >=1/RRT broad acute kidney injury reference;
- oxygen any-support and severe-support indeterminate flags.

The legacy sparse observed charted APACHE II route (`std_apacheii` / `std_apacheii_observed_charted`) has been retired and deleted. APACHE II should now be represented by the owner-approved reconstructed first-24h route unless a future owner decision reopens an observed-source route.

## Review Evidence

- Rule lock: `docs/standard_system_mvp/STD_APACHEII_MIMIC_RECONSTRUCTION_RULE_LOCK_PROPOSAL.md`
- Final audit: `docs/standard_system_mvp/STD_APACHEII_MIMIC_FINAL_AUDIT.md`
- Local distribution summary: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_apacheii_reconstructed_first24h/query_summary/std_apacheii_reconstructed_first24h_distribution_summary.json`
- Local final audit summary: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_apacheii_reconstructed_first24h/query_summary/std_apacheii_reconstructed_first24h_final_audit_summary.json`

## Decision

Owner approval is granted for `std_apacheii_reconstructed_first24h` as a reviewed-approved MIMIC-IV-3.1 score variable under the approved route and boundaries above.
