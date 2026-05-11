from __future__ import annotations

import sys
from pathlib import Path


VARIABLE_DIR = Path(__file__).resolve().parent
REPO_ROOT = VARIABLE_DIR.parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from standard_system_mvp_engine import run_diagnosis_admin_demographic_id_map


if __name__ == "__main__":
    raise SystemExit(
        run_diagnosis_admin_demographic_id_map(
            variable_dir=VARIABLE_DIR,
            execution_entrypoint_path=Path(__file__).resolve(),
        )
    )
