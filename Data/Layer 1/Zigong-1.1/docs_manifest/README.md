# Zigong-1.1 Layer 1 Manifest

This database skeleton follows the shared Layer 1 contract:

- `raw_original`
- `raw_unpacked`
- `source_supplied_derived`
- `local_converted_parquet`
- `docs_manifest`

The current local intake stages the Zigong 1.1 CSV delivery under `raw_original`.

Restricted raw CSV files must remain outside this public repository. Public files here are only the data-free skeleton and documentation.

The local `raw_original` intake includes 8 source CSV files plus `LICENSE.txt` and `SHA256SUMS.txt`.

The checksum manifest references the upstream `DataTables.zip` package and `LICENSE.txt`; it does not provide per-CSV checksums for the unzipped CSV files staged locally.

The retained `LICENSE.txt` matches the SHA256 value listed in `SHA256SUMS.txt`. `DataTables.zip` is not present in the Layer 1 raw-original directory, so that package-level checksum cannot be verified against the staged files.

Layer 2 opening is intentionally deferred until the current multi-database intake wave is ready for a coordinated opening pass.
