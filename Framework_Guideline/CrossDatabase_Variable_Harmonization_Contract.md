# Cross-Database Variable Harmonization Contract

This document defines how the project keeps standard variables consistent across databases.

The goal is not only to make field names look similar.
The goal is:

- same name means same meaning
- same meaning means same extraction contract
- same extraction contract means same standard unit and same default display rule

## Core rule

If two source variables from different databases truly represent the same standardized variable, they must share the same:

- `std_variable_id`
- standard English name
- standard Chinese name
- standard unit
- value type
- semantic definition
- default display rule

If they do not satisfy that level of equivalence, they must not be forced into the same standard variable.

## What must be harmonized

For any cross-database standardized variable, the following must be treated as global contracts rather than database-local preferences:

1. Identity
   - the same `std_variable_id`
   - the same standardized naming family
2. Meaning
   - the same clinical or operational definition
   - the same positive/negative semantics
   - the same event or stay grain expectation
3. Value contract
   - the same value type such as numeric, categorical, boolean, interval, or evidence flag
   - the same standard unit when numeric
   - the same categorical label set when categorical
4. Time contract
   - the same relative-time semantics when the variable is event-level
   - the same default time unit for retained standardized outputs when feasible
5. Display contract
   - the same default display precision
   - the same default presentation style for percentages, rates, counts, and durations

## Storage precision vs display precision

These two ideas must be kept separate.

- storage precision should preserve enough numeric fidelity for downstream analysis
- display precision should define how the value is shown by default in metadata, summaries, previews, and user-facing tables

Therefore:

- do not round away useful source precision only because a human-facing table prefers fewer decimals
- do define a default display precision so that the same variable is shown consistently across databases

Example:

- a laboratory measurement may be stored as a high-precision float
- the same variable may still have a default display rule such as 1 or 2 decimal places

## When two source variables may share one standardized variable

They may share one standardized variable only when all of the following are true:

- the underlying concept is the same
- the source-level differences can be resolved by unit conversion or controlled normalization
- the retained value after normalization still means the same thing clinically
- the resulting variable can follow one common metadata contract without hidden database-specific caveats

## When they must not be merged

Do not merge two variables into the same `std_variable_id` if any of the following is true:

- one is a setting and the other is an observed measurement
- one is invasive and the other is noninvasive, and that distinction matters by default
- one is summary-level and the other is event-level
- one database only offers a proxy while another offers the direct measurement
- the time anchor or event timing semantics are meaningfully different
- the unit conversion would still leave residual semantic mismatch

In these cases, use one of the following:

- create separate standardized variables
- create child variables under a shared family
- keep one as a future bridge or sensitivity-only derivative rather than the default main variable

## Required metadata for each standardized variable

Each standardized variable should eventually have globally stable metadata that is not database-specific in its core definition.

At minimum, the project should maintain:

- `std_variable_id`
- `std_variable_name_en`
- `std_variable_name_cn`
- if available, `std_variable_name_jp`
- semantic folder
- standard unit
- value type
- default display precision
- default relative-time unit when relevant
- grain definition
- short semantic definition
- known non-equivalence warnings if some databases only provide approximations

## Database-specific work is still allowed

Database-specific builders may differ in:

- raw source tables
- source itemids or concept codes
- unit-conversion logic
- cleaning thresholds
- linkage strategy
- lineage fields

But these database-specific implementation details must terminate in the same standardized output contract when the variable is declared equivalent.

## Approval rule for new databases

When opening a new database:

1. first test whether a candidate variable truly matches an existing standardized variable contract
2. if yes, reuse the existing `std_variable_id` and its global contract
3. if not, do not force a match just for naming convenience
4. document the reason for splitting, bridging, or deferring

## Practical interpretation

The project should behave as if the standardized variable contract is global, and database builders are local adapters.

That means:

- databases adapt to the standardized variable
- the standardized variable does not drift every time a new database arrives
