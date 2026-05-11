# std_supplemental_oxygen_active Amsterdam Candidate Review

Review date: 2026-05-02

Status: not_approved_candidate_blocked

Database: `AmsterdamUMCdb-1.0.2`

Standard variable: `std_supplemental_oxygen_active`

## Decision

AmsterdamUMCdb is not approved for same-name `std_supplemental_oxygen_active` as a Class 3 active episode under the current evidence.

The blocker is representation:

- Amsterdam has oxygen route, device, flow, and order evidence
- the current reviewed source surface does not yet prove active supplemental-oxygen start-stop episodes
- converting point/device/flow rows into active intervals would require a separate governed intervalization rule

## Source Audit Result

Relevant oxygen evidence includes:

- `listitems` itemid `8189` / `Toedieningsweg`
- `8189` value `O2-bril`: `338,421`
- `8189` value `Kapje`: `52,649`
- `8189` value `Non-Rebreathing masker`: `36,844`
- `numericitems` itemid `8845` / `O2 l/min`: `656,405`
- `procedureorderitems` itemid `9497` / `Zuurstofkapje geven`: `32`
- `procedureorderitems` itemid `9498` / `Diep nasaal zuurstof geven`: `7`
- `procedureorderitems` itemid `9516` / `Neusbril geven`: `80`

These are clinically meaningful oxygen-support signals, but they are not by themselves a governed active episode source.

## Boundary

Not approved:

- `std_supplemental_oxygen_active` on AmsterdamUMCdb
- treating every oxygen device row as a start-stop episode
- using oxygen flow rows as proof of continuous oxygen-active state without a continuity rule
- mixing NIV/CPAP, HFNC, tracheostomy, or invasive ventilation into ordinary supplemental oxygen

Future approval requires one of:

- a source-proven oxygen active interval table
- a formally reviewed episode-construction rule from oxygen route/device/flow event streams
- a split event-stream variable such as oxygen device/flow events before episode derivation

## Conclusion

This candidate is closed as blocked for same-name Class 3 active-episode approval under current Amsterdam evidence. It should not be forced into the approved Amsterdam respiratory-support surface yet.
