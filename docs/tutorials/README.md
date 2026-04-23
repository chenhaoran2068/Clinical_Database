# Representative Tutorials

These are public-safe tutorials.

They explain how to use the repository contracts and public cards without exposing restricted source data or patient-level retained outputs.

Use them in this rough order:

- repository governance and database admission first
- variable-level public/local interpretation second
- release and inventory workflow after that

Current tutorials:

- [`database_family_and_version_admission_walkthrough.md`](database_family_and_version_admission_walkthrough.md)
  - how to classify a new incoming source as a new family member, new version, or sibling module
- [`variable_card_to_local_knowledge_package.md`](variable_card_to_local_knowledge_package.md)
  - how to interpret the public variable card versus the local knowledge package
- [`std_heart_rate_cross_database_walkthrough.md`](std_heart_rate_cross_database_walkthrough.md)
  - how to compare one already standardized variable across two approved databases without dropping back into raw-table thinking
- [`minimal_variable_validation_workflow.md`](minimal_variable_validation_workflow.md)
  - the smallest reasonable review loop for one retained variable after a local asset exists
- [`public_release_governance_and_inventory_workflow.md`](public_release_governance_and_inventory_workflow.md)
  - how to keep release manifest, inventory, changelog, and release note surfaces in sync

Command interpretation rule:

- tutorial command examples assume the current shell is at the repository root unless the tutorial says otherwise
- tutorials may show workflow shape for local-only steps, but they do not publish restricted data or patient-level outputs
