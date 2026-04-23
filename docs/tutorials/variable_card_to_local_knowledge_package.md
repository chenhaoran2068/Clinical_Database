# From Public Variable Card To Local Knowledge Package

## Why both objects exist

The repository intentionally splits one standardized variable into two layers of documentation:

- the public variable card
- the local knowledge package

They are related, but they do not serve the same job.

## What the public variable card answers

A public card tells an external reader:

- what the variable is called
- what it means
- what unit, type, and grain it uses
- what the default display rule is
- what the cross-database caution surface looks like

This is the GitHub-safe summary layer.

## What the local knowledge package answers

A local knowledge package tells the execution team:

- which source tables and fields were used
- what the cleaned and normalized value columns are
- which database-specific exceptions were approved
- what the build evidence and preview outputs looked like
- what the grouped review decided

This is the execution-evidence layer.

## The practical reading order

When reviewing one variable, use this sequence:

1. read the public card to lock the cross-database intent
2. read the local knowledge package to understand the implementation
3. read the grouped review or audit note if a database-specific risk needs context

## What should stay public

Keep these in the public repository:

- standardized variable name
- definition
- unit
- type
- grain
- default display rule
- stable global cautions

## What should stay local

Keep these in local work:

- source-table bindings
- source-field bindings
- build logs
- patient-level preview extracts
- database-specific review evidence
- local approval traces

## Rule of thumb

If a detail teaches the shared standard, it is a good candidate for the public card.

If a detail proves how one database produced the asset, it belongs in the local knowledge package.
