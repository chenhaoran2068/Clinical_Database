# Public Repository Tests And Fixtures

This directory stores public-safe fixtures and test-support files for the GitHub repository.

Current fixture purpose:

- prove that the public variable-card parser expects a stable contract shape
- keep the checker from depending only on the current production card set

Current fixture areas:

- `fixtures/public_cards/`

Current usage:

- `scripts/check_public_repository.py`
- `.github/workflows/public-smoke.yml`
