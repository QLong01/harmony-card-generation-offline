from __future__ import annotations

import copy
import hashlib
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace


SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from validators.binding_validator import BindingValidator  # noqa: E402
from validators.api import ValidationOptions, validate_card  # noqa: E402
from validators.effective_capability_validator import EffectiveCapabilityValidator  # noqa: E402
from validators.rule_registry import RuleRegistry  # noqa: E402


class CapabilityBundleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rules = RuleRegistry(SKILL_DIR)
        cls.binding = BindingValidator()

    def test_profile_counts_ids_and_checksums(self) -> None:
        self.assertEqual(self.rules.capability_profile["profileId"], "app-11.7.5.205_rom-6.0")
        self.assertEqual(len(self.rules.data_capabilities), 7)
        self.assertEqual(len(self.rules.event_capabilities), 18)
        self.assertEqual(len(self.rules.asset_capabilities), 72)
        self.assertEqual(
            set(self.rules.capabilities),
            {
                "ViewWeather",
                "GetCalendarEvents",
                "GetCountdownDays",
                "GetAppUsageDuration",
                "GetEarphoneInfo",
                "GetPhoneBatteryInfo",
                "GetHealthAndSportSummary",
            },
        )
        for filename, expected in self.rules.capability_profile["sha256"].items():
            payload = (self.rules.capability_bundle_dir / filename).read_bytes()
            self.assertEqual(hashlib.sha256(payload).hexdigest(), expected)

    def test_data_schema_uses_remote_required_and_ranges(self) -> None:
        weather = self.rules.capabilities["ViewWeather"]
        self.assertEqual(weather["inputSchema"]["required"], ["prefectureName"])
        self.assertEqual(weather["preferredWriteResultTo"], "/data/weather")
        self.assertTrue(
            self.binding._schema_errors(
                {"prefectureName": "杭州市", "forecastDays": 6},
                weather["inputSchema"],
            )
        )
        self.assertFalse(
            self.binding._schema_errors(
                {"prefectureName": "杭州市", "forecastDays": 3},
                weather["inputSchema"],
            )
        )

    def test_effective_data_uses_resolved_manifest_schema(self) -> None:
        weather = self.rules.capabilities["ViewWeather"]
        context = SimpleNamespace(
            use_effective_capabilities=True,
            effective_data_capabilities={"ViewWeather": weather},
            cardspec={
                "dataBindings": [
                    {
                        "capabilityId": "ViewWeather",
                        "arguments": {"prefectureName": "杭州市", "forecastDays": 9},
                        "writeResultTo": "/data/weather",
                    }
                ]
            },
        )

        class Reporter:
            def __init__(self) -> None:
                self.codes: list[str] = []

            def add(self, _severity, code, *_args, **_kwargs) -> None:
                self.codes.append(code)

        reporter = Reporter()
        self.binding._check_capability_arguments(context, self.rules, reporter)
        self.assertIn("CARD_ARGUMENT_SCHEMA_INVALID", reporter.codes)

    def test_effective_id_falls_back_to_bundled_manifest(self) -> None:
        report = validate_card(
            cardspec={
                "title": "天气",
                "description": "天气概览",
                "suggestSize": "2x2",
                "dataBindings": [
                    {
                        "capabilityId": "ViewWeather",
                        "arguments": {"prefectureName": "杭州市", "forecastDays": 99},
                        "writeResultTo": "/data/weather",
                    }
                ],
            },
            effective_capabilities={"data": ["ViewWeather"]},
            options=ValidationOptions(skill_dir=SKILL_DIR),
        )
        self.assertTrue(report.has_code("CARD_ARGUMENT_SCHEMA_INVALID"))

    def test_event_templates_and_parameters_schema_are_exact(self) -> None:
        by_id = {item["id"]: item for item in self.rules.event_capabilities}
        bluetooth = by_id["event.open.settings.bluetooth"]
        exact_args = copy.deepcopy(bluetooth["actionTemplate"]["args"])
        self.assertFalse(
            self.binding._schema_errors(exact_args, bluetooth["parametersSchema"])
        )
        exact_args["uri"] = "battery"
        self.assertTrue(
            self.binding._schema_errors(exact_args, bluetooth["parametersSchema"])
        )
        self.assertEqual(
            {
                item["actionTemplate"]["call"]
                for item in self.rules.event_capabilities
            },
            {"clickToApi", "clickToDeeplink", "clickToIntent"},
        )

    def test_effective_event_allows_only_declared_dynamic_paths(self) -> None:
        by_id = {item["id"]: item for item in self.rules.event_capabilities}
        capability = by_id["event.call.phone"]
        validator = EffectiveCapabilityValidator()
        allowed = validator._event_actions([capability])
        self.assertTrue(
            validator._event_allowed(
                "clickToApi",
                {
                    "intentName": "CallPhone",
                    "params": {
                        "relationship": "{{/data/contact/relation}}",
                        "phoneNumber": "{{/data/contact/phone}}",
                    },
                },
                allowed,
            )
        )
        self.assertFalse(
            validator._event_allowed(
                "clickToApi",
                {
                    "intentName": "NotCallPhone",
                    "params": {"relationship": "母亲", "phoneNumber": "10086"},
                },
                allowed,
            )
        )

    def test_asset_allowlist_is_manifest_derived(self) -> None:
        manifest_sources = {item["src"] for item in self.rules.asset_capabilities}
        self.assertEqual(self.rules.asset_allowlist, manifest_sources)
        self.assertIn(
            "resources/base/media/icon_weather_wind.svg",
            self.rules.asset_allowlist,
        )
        self.assertNotIn(
            "resources/base/media/icon_weather1.svg",
            self.rules.asset_allowlist,
        )


if __name__ == "__main__":
    unittest.main()
