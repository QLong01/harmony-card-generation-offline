from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class RuleRegistry:
    """Loads all rule JSON under ``scripts/rules/``.

    The validator is closed against ``scripts/`` for static mode: config,
    capability manifests, allowlists and diagnostics all live under
    ``scripts/rules/``. External data
    (dynamic ``effectiveCapabilities`` or ``capabilities_dir``) is only
    consumed through the ``validate_card`` call sites, never read from disk
    outside the scripts directory.
    """

    def __init__(self, skill_dir: Path) -> None:
        self.skill_dir = skill_dir
        self.rules_dir = skill_dir / "scripts" / "rules"
        self.config_dir = self.rules_dir / "config"
        self.protocol = self._load_json(self.config_dir / "protocol.json", {})
        self.layout = self._load_json(self.config_dir / "layout.json", {})
        self.style = self._load_json(self.config_dir / "style.json", {})
        self.asset = self._load_json(self.config_dir / "asset.json", {})
        self.expression = self._load_json(self.config_dir / "expression.json", {})
        self.diagnostics = self._load_json(self.config_dir / "diagnostics.zh-CN.json", {})
        self.capability_profile = self._load_json(
            self.config_dir / "capabilities.json", {}
        )
        self.capability_bundle_dir = self._capability_bundle_dir()
        self.data_capabilities = self._load_capability_list("dataManifest")
        self.event_capabilities = self._load_capability_list("eventManifest")
        self.asset_capabilities = self._load_capability_list("assetManifest")
        self.capabilities = self._load_capabilities()
        self.allowed_components = set(self.protocol.get("allowedComponents", []))
        manifest_assets = {
            item.get("src")
            for item in self.asset_capabilities
            if isinstance(item.get("src"), str) and item.get("src")
        }
        self.asset_allowlist = manifest_assets or set(self.asset.get("allowlist", []))

    def _load_json(self, path: Path, fallback: Any) -> Any:
        if not path.exists():
            return fallback
        return json.loads(path.read_text(encoding="utf-8"))

    def _capability_bundle_dir(self) -> Path | None:
        relative = self.capability_profile.get("bundleDirectory")
        if not isinstance(relative, str) or not relative:
            return None
        candidate = (self.skill_dir / relative).resolve()
        rules_root = self.rules_dir.resolve()
        try:
            candidate.relative_to(rules_root)
        except ValueError:
            raise ValueError("capability bundleDirectory must stay under scripts/rules")
        return candidate

    def _load_capability_list(self, manifest_key: str) -> list[dict[str, Any]]:
        if self.capability_bundle_dir is None:
            return []
        filename = self.capability_profile.get(manifest_key)
        if not isinstance(filename, str) or not filename:
            return []
        manifest_path = self.capability_bundle_dir / filename
        expected_hashes = self.capability_profile.get("sha256", {})
        expected_hash = (
            expected_hashes.get(filename) if isinstance(expected_hashes, dict) else None
        )
        if isinstance(expected_hash, str):
            actual_hash = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
            if actual_hash.lower() != expected_hash.lower():
                raise ValueError(f"capability manifest checksum mismatch: {filename}")
        data = self._load_json(manifest_path, [])
        if not isinstance(data, list):
            return []
        return [item for item in data if isinstance(item, dict)]

    def _load_capabilities(self) -> dict[str, Any]:
        capabilities: dict[str, Any] = {}
        for item in self.data_capabilities:
            capability_id = item.get("id")
            if not isinstance(capability_id, str) or not capability_id:
                continue
            normalized = dict(item)
            normalized["capabilityId"] = capability_id
            normalized["preferredWriteResultTo"] = item.get("defaultWriteResultTo")
            normalized["_source"] = str(
                self.capability_bundle_dir
                / self.capability_profile.get("dataManifest", "data_capabilities.json")
            )
            capabilities[capability_id] = normalized
        return capabilities
