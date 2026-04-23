# Standard Variable Public Cards

This folder is reserved for GitHub-safe public summaries of standardized variables.

These public cards should expose only the stable metadata subset that is safe and useful to publish in the method repository.

They should not be treated as replacements for the full local Layer 5 knowledge packages stored under:

- `Methods/Clinical_Database/local_work/Layer 5/<database>/<std_variable_id>/`

Preferred long-term rule:

- generate public cards from local canonical metadata rather than maintaining two independent hand-edited copies
- let the exporter suppress local-only implementation detail rather than mirroring local execution prose unchanged

Current publication-boundary rule:

- public cards may keep stable definitions, units, value types, grain, display rules, and public-safe cautions
- public cards should not mirror raw source tables, source fields, itemids, local thresholds, or build-review artifact detail

Current export script:

- `scripts/layer5/export_public_variable_card.py`

Example:

```text
python scripts/layer5/export_public_variable_card.py \
  --workspace-root <workspace-root> \
  --std-variable-id std_hospital_history_comorbidity_charlson_index
```

If a variable already has more than one reviewed-approved database asset, the script requires:

```text
--database-id <database-id>
```

Or, when you want one merged public card for a cross-database standardized variable:

```text
python scripts/layer5/export_public_variable_card.py \
  --workspace-root <workspace-root> \
  --std-variable-id std_heart_rate \
  --cross-database
```

Batch export all currently reviewed-approved variables:

```text
python scripts/layer5/export_public_variable_card.py \
  --workspace-root <workspace-root> \
  --all-reviewed-approved \
  --cross-database \
  --overwrite
```

Batch export only missing cards without touching existing ones:

```text
python scripts/layer5/export_public_variable_card.py \
  --workspace-root <workspace-root> \
  --all-reviewed-approved \
  --cross-database \
  --only-missing
```

Batch export while preferring one database as the publication basis for variables that currently have multiple approved database assets:

```text
python scripts/layer5/export_public_variable_card.py \
  --workspace-root <workspace-root> \
  --all-reviewed-approved \
  --database-id MIMIC-IV-3.1 \
  --overwrite
```
