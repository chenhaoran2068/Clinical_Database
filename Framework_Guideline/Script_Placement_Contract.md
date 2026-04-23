# Script Placement Contract

Last updated: 2026-04-21

## Why this contract exists

Script placement is now governed by responsibility, not by convenience.

This contract exists to prevent the script trees from drifting back into a mixed state where:

- shared cross-project tools
- public GitHub-safe `Clinical_Database` method scripts
- local production scripts

are stored together without a clear boundary.

## Canonical split

The canonical script split is:

- `Shared/scripts`
  - only truly shared cross-project or cross-method tools
- `Github/Clinical_Database/scripts`
  - only GitHub-safe scripts that belong to the `Clinical_Database` method stack
- `Methods/Clinical_Database/local_work/scripts`
  - local production, local admin, database-specific, one-off, semi-one-off, and not-yet-GitHub-safe scripts

These are workspace-relative tree locations, not machine-specific absolute paths.

## Public path-writing rule

When public GitHub-facing docs or contracts mention project paths, they should:

1. avoid machine-specific absolute paths
2. prefer forward-slash relative paths
3. use workspace-relative paths such as `Methods/Clinical_Database/local_work/...` for sibling local-work references
4. reserve shell-native path syntax for executable command examples only

## Placement rules

1. Place by responsibility, not by author and not by temporary convenience.
2. New `Clinical_Database` scripts default to `Methods/Clinical_Database/local_work/scripts`.
3. A script may be promoted into `Github/Clinical_Database/scripts` only if it is:
   - GitHub-safe
   - reasonably reusable
   - not dependent on restricted data access or local-only execution assumptions
4. `Shared/scripts` has the highest bar.
   - A script belongs there only if it is genuinely useful beyond the `Clinical_Database` method family.
5. Do not keep the same script as a long-term duplicated copy in multiple trees.
   - once promoted or relocated, one location must become the clear primary home
6. If a script directly serves `Methods/Clinical_Database/local_work`, it belongs in the local-work tree unless there is a strong reason otherwise.

## Promotion and demotion rule

The normal script lifecycle is:

1. draft and prove locally in `Methods/Clinical_Database/local_work/scripts`
2. harden path handling, inputs, and documentation
3. promote to `Github/Clinical_Database/scripts` if it becomes public and reusable

If a script later becomes local-only again, it should be moved back rather than leaving a misleading public copy in place.

## Documentation rule

Whenever a new script is added, renamed, moved, or retired, the maintainer should update the relevant inventory README.

At minimum, the documentation should make clear:

- what the script is for
- what it reads
- what it writes
- whether it touches restricted or local-only data
- why it belongs in this tree instead of the other two

## Health-check rule

After a cleanup or migration pass, run a minimal script-tree health check:

1. verify the directory split still matches this contract
2. update active README or entry-point docs
3. run parse or compile checks on active Python scripts
4. remove temporary byproducts such as `__pycache__`

## Historical note

Older logs may still mention the previous mixed `Shared/scripts` layout.

Those references should be interpreted as historical only and superseded by this contract.
