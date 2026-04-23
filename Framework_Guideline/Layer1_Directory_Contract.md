# Layer 1 Directory Contract

Layer 1 is the source-ingestion layer. It separates official source files from local convenience copies.

## Required buckets

### `raw_original`

- preserves the original delivered package or file set
- should remain as close as possible to the source delivery
- should not be manually edited

### `raw_unpacked`

- stores official source files after unpacking only
- is the canonical Layer 1 input for ETL
- should not be semantically edited

### `source_supplied_derived`

- stores official companion resources supplied by the source project
- examples include official dictionaries, mappings, or source-provided derived files
- does not replace `raw_unpacked` as the main ETL input

### `local_converted_parquet`

- stores local performance copies converted from `raw_unpacked`
- is reproducible and disposable
- should not contain semantic cleaning or derived columns

### `docs_manifest`

- stores human-readable provenance, folder-role notes, and expected source file lists

## Contract summary

The most important boundary is:

- official source files live in `raw_original` or `raw_unpacked`
- locally generated convenience copies live in `local_converted_parquet`

This prevents format-conversion artifacts from being mistaken for official source truth.
