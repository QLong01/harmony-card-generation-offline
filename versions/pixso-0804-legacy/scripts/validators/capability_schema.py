from __future__ import annotations

from typing import Any


def contains_binding(value: Any) -> bool:
    if isinstance(value, str):
        return "{{" in value or "}}" in value or "${" in value
    if isinstance(value, dict):
        if set(value.keys()) == {"path"} or value.get("call") == "formatString":
            return True
        return any(contains_binding(child) for child in value.values())
    if isinstance(value, list):
        return any(contains_binding(child) for child in value)
    return False


def schema_errors(
    value: Any,
    schema: Any,
    path: str = "",
    *,
    dynamic_paths: set[str] | None = None,
) -> list[str]:
    if not isinstance(schema, dict):
        return []
    dynamic_paths = dynamic_paths or set()
    if path in dynamic_paths and contains_binding(value):
        return []
    errors: list[str] = []
    label = path or "/"
    if "const" in schema and value != schema["const"]:
        errors.append(f"{label}: must equal {schema['const']!r}")
    if isinstance(schema.get("enum"), list) and value not in schema["enum"]:
        errors.append(f"{label}: must be one of {schema['enum']!r}")
    expected_type = schema.get("type")
    type_ok = {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }.get(expected_type, True)
    if not type_ok:
        errors.append(f"{label}: expected {expected_type}")
        return errors
    if expected_type == "object":
        properties = schema.get("properties", {})
        properties = properties if isinstance(properties, dict) else {}
        required = schema.get("required", [])
        required = required if isinstance(required, list) else []
        for key in required:
            if key not in value:
                errors.append(f"{label}: missing {key}")
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{label}: unexpected {key}")
        for key, child in value.items():
            if key not in properties:
                continue
            child_path = f"{path}/{key}" if path else f"/{key}"
            errors.extend(
                schema_errors(
                    child,
                    properties[key],
                    child_path,
                    dynamic_paths=dynamic_paths,
                )
            )
    elif expected_type == "array" and isinstance(schema.get("items"), dict):
        for index, child in enumerate(value):
            child_path = f"{path}/{index}" if path else f"/{index}"
            errors.extend(
                schema_errors(
                    child,
                    schema["items"],
                    child_path,
                    dynamic_paths=dynamic_paths,
                )
            )
    elif expected_type == "string":
        if isinstance(schema.get("minLength"), int) and len(value) < schema["minLength"]:
            errors.append(f"{label}: shorter than minLength {schema['minLength']}")
    elif expected_type in {"integer", "number"}:
        if isinstance(schema.get("minimum"), (int, float)) and value < schema["minimum"]:
            errors.append(f"{label}: below minimum {schema['minimum']}")
        if isinstance(schema.get("maximum"), (int, float)) and value > schema["maximum"]:
            errors.append(f"{label}: above maximum {schema['maximum']}")
    return errors
