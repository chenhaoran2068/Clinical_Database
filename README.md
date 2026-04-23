# Clinical Database

车同轨，书同文，行同伦。

This repository is the public method repository for the clinical database standardization project.

It provides:

- directory contracts
- policy-registry contracts
- database-specific critical semantics contracts
- database lineage and version tracking
- onboarding playbooks
- public workflow entrypoints
- release governance and release-note surfaces
- generated public exports and coverage summaries
- GitHub-safe public variable-card contracts
- public database scaffolding entrypoints
- reusable scripts
- Layer 1 database skeletons
- public tutorials
- detailed public review checklists

It does not provide:

- raw database files
- local parquet copies
- patient-level Layer 2 to Layer 5 outputs

## Start Here

1. Read [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md).
2. Check [`docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md`](docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md).
3. Install dependencies with `pip install -r requirements.txt`.
4. Place your officially obtained source data into the expected sibling local-work path `Methods/Clinical_Database/local_work/Layer 1/<database>/...` outside this public repository.
5. Run the public workflow entrypoints in [`scripts/public_workflow.py`](scripts/public_workflow.py).
6. Use `prepare-release` and `check-public-repository` to keep the public release surface coherent.

## Main References

- [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md)
- [`docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md`](docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md)
- [`docs/database_catalog.json`](docs/database_catalog.json)
- [`docs/release_safe_manifest.json`](docs/release_safe_manifest.json)
- [`docs/PUBLIC_INVENTORY.md`](docs/PUBLIC_INVENTORY.md)
- [`docs/PUBLIC_REPOSITORY_DETAILED_REVIEW_CHECKLIST.md`](docs/PUBLIC_REPOSITORY_DETAILED_REVIEW_CHECKLIST.md)
- [`docs/public_exports/README.md`](docs/public_exports/README.md)
- [`docs/onboarding/README.md`](docs/onboarding/README.md)
- [`docs/onboarding/families/README.md`](docs/onboarding/families/README.md)
- [`docs/tutorials/README.md`](docs/tutorials/README.md)
- [`docs/NEXT_STAGE_PUBLIC_METHOD_REPOSITORY_CHECKLIST.md`](docs/NEXT_STAGE_PUBLIC_METHOD_REPOSITORY_CHECKLIST.md)
- [`Framework_Guideline/Layer1_Directory_Contract.md`](Framework_Guideline/Layer1_Directory_Contract.md)
- [`Framework_Guideline/CrossDatabase_Variable_Harmonization_Contract.md`](Framework_Guideline/CrossDatabase_Variable_Harmonization_Contract.md)
- [`Framework_Guideline/Database_Critical_Semantics_Contract.md`](Framework_Guideline/Database_Critical_Semantics_Contract.md)
- [`Framework_Guideline/Database_Family_NewVersion_Admission_Contract.md`](Framework_Guideline/Database_Family_NewVersion_Admission_Contract.md)
- [`Framework_Guideline/AmsterdamUMCdb_TimeSemantics_Contract.md`](Framework_Guideline/AmsterdamUMCdb_TimeSemantics_Contract.md)
- [`Framework_Guideline/ID_Normalization_Contract.md`](Framework_Guideline/ID_Normalization_Contract.md)
- [`Framework_Guideline/MIMICIV_SourcePackageAndModuleBoundary_Contract.md`](Framework_Guideline/MIMICIV_SourcePackageAndModuleBoundary_Contract.md)
- [`Framework_Guideline/Layer5_PublicVariableCard_Contract.md`](Framework_Guideline/Layer5_PublicVariableCard_Contract.md)
- [`Framework_Guideline/PolicyRegistry_Contract.md`](Framework_Guideline/PolicyRegistry_Contract.md)
- [`Framework_Guideline/ReleaseSafe_Manifest_ReleaseGovernance_Contract.md`](Framework_Guideline/ReleaseSafe_Manifest_ReleaseGovernance_Contract.md)
- [`Framework_Guideline/Script_Placement_Contract.md`](Framework_Guideline/Script_Placement_Contract.md)
- [`docs/std_variable_cards/README.md`](docs/std_variable_cards/README.md)
- [`docs/RELEASE_CHANGELOG.md`](docs/RELEASE_CHANGELOG.md)
- [`docs/releases/README.md`](docs/releases/README.md)
- [`requirements.txt`](requirements.txt)
- [`scripts/public_workflow.py`](scripts/public_workflow.py)
- [`scripts/check_public_repository.py`](scripts/check_public_repository.py)
- [`scripts/export_public_metadata.py`](scripts/export_public_metadata.py)
- [`scripts/prepare_public_release.py`](scripts/prepare_public_release.py)
- [`scripts/scaffold_public_database.py`](scripts/scaffold_public_database.py)
- [`scripts/layer5/check_local_id_semantics.py`](scripts/layer5/check_local_id_semantics.py)
- [`scripts/layer1/convert_amsterdam_raw_unpacked_to_parquet.py`](scripts/layer1/convert_amsterdam_raw_unpacked_to_parquet.py)
- [`scripts/generate_layer4_layer5_excel_templates.py`](scripts/generate_layer4_layer5_excel_templates.py)
- [`scripts/layer1/download_mimic_note_to_layer1.py`](scripts/layer1/download_mimic_note_to_layer1.py)
- [`scripts/layer1/reconstruct_mimic_note_raw_unpacked_from_parquet.py`](scripts/layer1/reconstruct_mimic_note_raw_unpacked_from_parquet.py)
- [`scripts/layer1/unpack_mimic_raw_original_to_raw_unpacked.py`](scripts/layer1/unpack_mimic_raw_original_to_raw_unpacked.py)
- [`scripts/layer1/convert_mimic_raw_unpacked_to_parquet.py`](scripts/layer1/convert_mimic_raw_unpacked_to_parquet.py)
- [`scripts/layer1/unpack_mimic_echo_raw_original_to_raw_unpacked.py`](scripts/layer1/unpack_mimic_echo_raw_original_to_raw_unpacked.py)
- [`scripts/layer1/convert_mimic_echo_raw_unpacked_to_parquet.py`](scripts/layer1/convert_mimic_echo_raw_unpacked_to_parquet.py)
- [`scripts/layer4/validate_policy_registry.py`](scripts/layer4/validate_policy_registry.py)
- [`scripts/layer5/export_layer3_filtered_preview.py`](scripts/layer5/export_layer3_filtered_preview.py)
- [`scripts/layer5/summarize_layer3_numeric_asset.py`](scripts/layer5/summarize_layer3_numeric_asset.py)
