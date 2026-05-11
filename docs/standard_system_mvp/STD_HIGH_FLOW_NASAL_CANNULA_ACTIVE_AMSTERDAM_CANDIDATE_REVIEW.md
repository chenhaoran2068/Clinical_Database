# std_high_flow_nasal_cannula_active Amsterdam Candidate Review

Review date: 2026-05-02

Status: not_approved_candidate_blocked

Database: `AmsterdamUMCdb-1.0.2`

Standard variable: `std_high_flow_nasal_cannula_active`

## Decision

AmsterdamUMCdb is not approved for same-name `std_high_flow_nasal_cannula_active` under the current evidence.

The blocker is source identity:

- no narrow Amsterdam item was found for `HFNC`
- no narrow Amsterdam item was found for `high-flow nasal cannula`
- no narrow Amsterdam item was found for `Optiflow`
- oxygen-flow or oxygen-device evidence is not sufficient to infer HFNC

## Source Audit Result

Dictionary search across current public/local Amsterdam item metadata found no accepted HFNC source labels for:

- `HFNC`
- `high flow`
- `high-flow`
- `Optiflow`
- `high-flow nasal cannula`

Observed oxygen-adjacent evidence includes:

- `numericitems` itemid `8845` / `O2 l/min`
- `listitems` itemid `8189` / `Toedieningsweg`
- oxygen-route values such as `O2-bril`, `Kapje`, and `Non-Rebreathing masker`

Those are oxygen delivery or flow records, not narrow HFNC active episodes.

`HFO-Bias-flow` is not accepted as HFNC.

## Boundary

Not approved:

- `std_high_flow_nasal_cannula_active` on AmsterdamUMCdb
- mapping oxygen flow to HFNC
- mapping oxygen route/device values to HFNC
- inferring HFNC from generic ventilator or oxygen settings

Future approval requires a narrow source item or a formally reviewed source-combination rule that can distinguish HFNC from ordinary supplemental oxygen and NIV/CPAP.

## Conclusion

This candidate is closed as blocked under current Amsterdam evidence. It should remain absent from the Amsterdam same-name approved mapping surface.
