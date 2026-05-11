# Layer 3 Directory Contract

Last updated: `2026-05-09`

Layer 3 is the retained standardized-data layer. It stores formal standardized assets and stable helper products that downstream analyses may read.

## Canonical Layout

All new Layer 3 assets must use a database-scoped path:

```text
Methods/Clinical_Database/local_work/Layer 3/<database_id>/<semantic_folder>/<std_variable_id>/<std_variable_id>_long.parquet
```

Examples:

```text
Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/vital_signs/std_heart_rate/std_heart_rate_long.parquet
Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/vital_signs/std_heart_rate/std_heart_rate_long.parquet
Methods/Clinical_Database/local_work/Layer 3/eICU-CRD-2.0/vital_signs/std_heart_rate/std_heart_rate_long.parquet
Methods/Clinical_Database/local_work/Layer 3/Zigong-1.1/vital_signs/std_heart_rate/std_heart_rate_long.parquet
```

The `<database_id>` segment must match a `database_id` in `docs/database_catalog.json`.

## Why Database Scope Is Required

The same standard variable can be implemented in multiple source databases. Physical Layer 3 paths must not mix database ownership under one shared semantic folder.

Cross-database identity belongs in:

- Layer 5 Global indexes
- public standard-variable cards
- mapping specs
- variable-class contracts

It does not belong in physical co-location under `Layer 3/<semantic_folder>/`.

## Legacy Exception

Historical MIMIC-IV-3.1 assets may still appear directly under root-level semantic folders:

```text
Methods/Clinical_Database/local_work/Layer 3/<semantic_folder>/<std_variable_id>/<std_variable_id>_long.parquet
```

This is a legacy exception only. It exists because earlier MIMIC retained assets, Layer 5 manifests, runtime evidence, and review notes were created before the multi-database Layer 3 convention was locked.

Do not extend this exception to new databases.

Do not move existing MIMIC root-level assets casually. A MIMIC Layer 3 migration requires a formal path-migration manifest and synchronized updates to:

- builder scripts
- mapping specs
- runtime evidence
- Layer 5 asset manifests
- public variable cards
- generated public exports
- reproducibility checks

## New-Asset Rule

For every new database and every newly generated retained asset, the output path must be database-scoped.

Allowed:

```text
Methods/Clinical_Database/local_work/Layer 3/SICdb-1.0.5/vital_signs/std_heart_rate/std_heart_rate_long.parquet
```

Not allowed:

```text
Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/vital_signs/std_heart_rate/std_heart_rate_long.parquet
```

## Machine Policy

The machine-readable companion policy is:

```text
docs/layer3_directory_policy.json
```

The validator is:

```text
scripts/validate_layer3_layout_policy.py
```

The public workflow entrypoint is:

```text
python scripts/public_workflow.py validate-layer3-layout
```

The public repository checker must include this validator so that newly published mapping specs and runtime evidence do not silently create non-database-scoped Layer 3 references.
