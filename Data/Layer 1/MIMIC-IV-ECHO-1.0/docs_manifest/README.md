# MIMIC-IV-ECHO-1.0 Layer 1 Manifest

This database skeleton follows the shared Layer 1 contract:

- `raw_original`
- `raw_unpacked`
- `source_supplied_derived`
- `local_converted_parquet`
- `docs_manifest`

`MIMIC-IV-ECHO v1.0` is staged as a sibling module, not as a permanent child of `MIMIC-IV-3.1`.

`raw_unpacked/ECHO-1.0` is the intended ETL input layer.
`local_converted_parquet` is reserved for locally regenerated performance copies.
