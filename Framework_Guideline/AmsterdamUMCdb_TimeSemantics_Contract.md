# AmsterdamUMCdb Time Semantics Contract

This note records a critical timing rule for AmsterdamUMCdb standardization.

## Core rule

- Raw offset fields such as `admittedat`, `dischargedat`, `start`, `stop`, `measuredat`, and `registeredat` should be treated as the timing truth.
- `lengthofstay` should be treated as a source-supplied summary duration, typically reported in whole hours.

## What this means

- Use raw offsets plus an admission anchor to align events on the time axis.
- Do not use `lengthofstay` as the default precise boundary for event filtering, censoring, or time-to-event work.

## Default pattern

Use:

```text
relative_time_minutes = (event_time_ms - anchor_time_ms_raw) / 60000
```

Do not assume:

```text
stay_end_minutes = lengthofstay * 60
```

as the precise timing truth.

## Why this note exists

In AmsterdamUMCdb opening review, `lengthofstay` behaved like a reported whole-hour field, while raw offset columns preserved finer timing detail.
Future builders should preserve this distinction.
