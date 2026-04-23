import argparse
import json
from pathlib import Path


REQUIRED_TOP_LEVEL = {
    "registry_metadata": dict,
    "shared_defaults": dict,
    "policies": list,
}

REQUIRED_METADATA_KEYS = {
    "registry_name": str,
    "registry_version": str,
    "database_name": str,
    "layer_scope": str,
    "registry_status": str,
    "contract_name": str,
    "contract_version": str,
    "execution_mode": str,
    "runtime_model_interpretation_allowed": bool,
    "created_at": str,
    "source_review_artifacts": list,
}

REQUIRED_SHARED_DEFAULT_KEYS = {
    "default_grain": str,
    "default_anchor_asset": str,
    "default_relative_time_formula": str,
    "default_boundary_truth_fields": list,
    "disallowed_default_boundary_fields": list,
}

REQUIRED_POLICY_KEYS = {
    "policy_id": str,
    "policy_family": str,
    "policy_version": str,
    "status": str,
    "applies_to_assets": list,
    "intent": str,
    "trigger_conditions": dict,
    "classification_outputs": list,
    "default_actions": dict,
    "rule_blocks": list,
    "notes": list,
}

ALLOWED_STATUSES = {
    "draft",
    "built_pending_user_review",
    "reviewed_approved",
    "deprecated",
}


def _check_required(container, required_map, label, errors):
    for key, expected_type in required_map.items():
        if key not in container:
            errors.append(f"{label}: missing required key '{key}'")
            continue
        if not isinstance(container[key], expected_type):
            actual = type(container[key]).__name__
            expected = expected_type.__name__
            errors.append(
                f"{label}: key '{key}' expected {expected}, got {actual}"
            )


def validate_registry(path: Path):
    errors = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"JSON decode error: {exc}"]

    _check_required(data, REQUIRED_TOP_LEVEL, "top_level", errors)
    if errors:
        return errors

    _check_required(data["registry_metadata"], REQUIRED_METADATA_KEYS, "registry_metadata", errors)
    _check_required(data["shared_defaults"], REQUIRED_SHARED_DEFAULT_KEYS, "shared_defaults", errors)

    registry_status = data["registry_metadata"].get("registry_status")
    if registry_status not in ALLOWED_STATUSES:
        errors.append(
            f"registry_metadata: registry_status '{registry_status}' is not in {sorted(ALLOWED_STATUSES)}"
        )

    policies = data["policies"]
    if not policies:
        errors.append("policies: registry must contain at least one policy")
        return errors

    seen_ids = set()
    for index, policy in enumerate(policies, start=1):
        label = f"policy[{index}]"
        if not isinstance(policy, dict):
            errors.append(f"{label}: expected object, got {type(policy).__name__}")
            continue

        _check_required(policy, REQUIRED_POLICY_KEYS, label, errors)
        policy_id = policy.get("policy_id")
        if isinstance(policy_id, str):
            if policy_id in seen_ids:
                errors.append(f"{label}: duplicate policy_id '{policy_id}'")
            else:
                seen_ids.add(policy_id)

        status = policy.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(
                f"{label}: status '{status}' is not in {sorted(ALLOWED_STATUSES)}"
            )

        assets = policy.get("applies_to_assets")
        if isinstance(assets, list) and not assets:
            errors.append(f"{label}: applies_to_assets must not be empty")

        outputs = policy.get("classification_outputs")
        if isinstance(outputs, list):
            for output_index, output in enumerate(outputs, start=1):
                if not isinstance(output, dict):
                    errors.append(
                        f"{label}.classification_outputs[{output_index}]: expected object"
                    )
                    continue
                if "field" not in output:
                    errors.append(
                        f"{label}.classification_outputs[{output_index}]: missing 'field'"
                    )

        rule_blocks = policy.get("rule_blocks")
        if isinstance(rule_blocks, list) and not rule_blocks:
            errors.append(f"{label}: rule_blocks must not be empty")
        if isinstance(rule_blocks, list):
            for rule_index, rule in enumerate(rule_blocks, start=1):
                if not isinstance(rule, dict):
                    errors.append(f"{label}.rule_blocks[{rule_index}]: expected object")
                    continue
                for required_rule_key in ("rule_id", "when", "emit"):
                    if required_rule_key not in rule:
                        errors.append(
                            f"{label}.rule_blocks[{rule_index}]: missing '{required_rule_key}'"
                        )

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate a machine-readable policy registry JSON file."
    )
    parser.add_argument(
        "--registry",
        required=True,
        help="Path to the policy registry JSON file.",
    )
    args = parser.parse_args()

    path = Path(args.registry)
    if not path.exists():
        raise SystemExit(f"Registry not found: {path}")

    errors = validate_registry(path)
    if errors:
        print("Policy registry validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    data = json.loads(path.read_text(encoding="utf-8"))
    print("Policy registry validation passed.")
    print(f"Registry: {data['registry_metadata']['registry_name']}")
    print(f"Version: {data['registry_metadata']['registry_version']}")
    print(f"Policies: {len(data['policies'])}")
    print("Policy IDs:")
    for policy in data["policies"]:
        print(f"- {policy['policy_id']}")


if __name__ == "__main__":
    main()
