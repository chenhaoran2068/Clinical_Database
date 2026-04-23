# ID Normalization Contract

This contract defines the canonical identifier naming rules used by the clinical database standardization project.

The goal is the same as for standardized variables:

- same canonical ID name means the same semantic layer
- canonical ID naming is decided by meaning, not by source spelling
- source-system naming should remain visible in lineage, but it should not control the cross-database standard vocabulary

## Core rule

Canonical identifier names must be assigned by semantic level, not by whichever raw column name happens to exist in one database.

That means:

- `subject_id` means one patient-level identifier
- `hadm_id` means one hospital-admission-level identifier
- `stay_id` means one ICU-stay-level or ICU-semantic critical-care-stay-level identifier

If a database does not expose one of those semantic layers cleanly, do not invent that canonical ID by default.

## Canonical identifier dictionary

### `subject_id`

Use `subject_id` only when the identifier semantically represents one patient across encounters.

### `hadm_id`

Use `hadm_id` only when the identifier semantically represents one hospital admission or one hospital-level encounter.

Do not use `hadm_id` for:

- ICU stays
- ICU-semantic admission rows
- procedure episodes
- module-specific study records

### `stay_id`

Use `stay_id` when the identifier semantically represents:

- one ICU stay
- or one ICU-semantic critical-care stay equivalent under the current approved contract

This rule allows a database-specific local key to map to `stay_id` even if the raw source column is not literally named `stay_id`, as long as the approved semantic layer is the ICU-stay layer.

## What must not happen

Do not assign canonical ID names by convenience alone.

Examples of prohibited behavior:

- mapping every raw `admissionid` to `hadm_id` just because the source column contains the word `admission`
- mapping a stay-level key to `hadm_id` in one database and to `stay_id` in another
- inventing a hospital-admission canonical identifier for a database that has not yet published a real hospital-admission bridge

## Source naming still matters

The raw source name should still remain visible in:

- source schema review
- Layer 2 review notes
- Layer 5 knowledge packages
- lineage fields
- audit summaries

Canonical ID naming does not erase source provenance.

It standardizes the cross-database semantic vocabulary.

## Current database examples

### MIMIC-IV-3.1

Current direct semantic mapping:

- raw `subject_id` -> canonical `subject_id`
- raw `hadm_id` -> canonical `hadm_id`
- raw `stay_id` -> canonical `stay_id`

This is the straightforward case where raw naming already matches the canonical cross-database vocabulary.

### AmsterdamUMCdb-1.0.2

Current opening semantic mapping:

- raw `patientid` -> canonical `subject_id`
- raw `admissionid` -> canonical `stay_id`

Reason:

- the current Amsterdam opening contracts treat `admissionid` as one ICU/MC admission record in the source table
- under the current ICU-semantic retained-variable surface, that row acts as the local stay-equivalent key

Current non-mapping rule:

- do not publish raw `admissionid` as canonical `hadm_id` by default

Reason:

- the current public Amsterdam opening surface has not yet published a separate hospital-admission canonical layer

## Rule for future database admission

When a new database or module is onboarded:

1. identify whether the source exposes patient, hospital-admission, and ICU-stay layers separately
2. map canonical IDs by semantic layer
3. leave a canonical layer absent if it is not yet truly available
4. document the source-to-canonical mapping in the database onboarding playbook
5. document any stay-equivalent approximation or caveat explicitly

## Practical interpretation

The project should behave as if canonical identifier naming is a shared cross-database dictionary.

That means:

- databases adapt to the canonical identifier vocabulary
- the canonical vocabulary does not drift every time a new raw schema arrives
- future users should not need a different top-level identifier dictionary for every database
