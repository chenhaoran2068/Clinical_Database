# AmsterdamUMCdb-1.0.2 Layer 1 Manifest

This database skeleton follows the shared Layer 1 contract:

- `raw_original`
- `raw_unpacked`
- `source_supplied_derived`
- `local_converted_parquet`
- `docs_manifest`

`raw_unpacked` is the intended ETL input layer.
`local_converted_parquet` is reserved for locally regenerated performance copies.

If a user has official AmsterdamUMCdb access, they should place the delivered files into `raw_original` and the unpacked source tables into `raw_unpacked`.
