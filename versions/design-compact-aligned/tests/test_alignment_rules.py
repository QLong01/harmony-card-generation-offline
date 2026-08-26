from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_DIR / "scripts" / "validate_card.py"
FIXTURES = SKILL_DIR / "tests" / "fixtures"


def read_messages(name: str) -> list[dict]:
    path = FIXTURES / name
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_messages(path: Path, messages: list[dict]) -> None:
    path.write_text(
        "\n".join(json.dumps(item, ensure_ascii=False) for item in messages) + "\n",
        encoding="utf-8",
    )


def run_validator(dsl: Path, cardspec: Path, *, aesthetic: bool = True) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        "-X",
        "utf8",
        str(VALIDATOR),
        "--dsl",
        str(dsl),
        "--cardspec",
        str(cardspec),
        "--fail-on-error",
        "--strict",
        "--format",
        "json",
    ]
    if aesthetic:
        command.append("--enable-aesthetic")
    return subprocess.run(
        command,
        cwd=SKILL_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def four_action_hub_messages() -> list[dict]:
    actions: list[dict] = []
    for index in range(4):
        action_id = f"action_{index + 1}"
        label_id = f"action_label_{index + 1}"
        actions.extend(
            [
                {
                    "id": action_id,
                    "component": "Row",
                    "children": [label_id],
                    "onClick": [
                        {
                            "call": "clickToApi",
                            "args": {"intentName": "CleanRAMMemory", "params": {}},
                        }
                    ],
                    "styles": {
                        "width": 142,
                        "height": 48,
                        "justifyContent": "center",
                        "alignItems": "center",
                    },
                },
                {
                    "id": label_id,
                    "component": "Text",
                    "content": f"动作{index + 1}",
                    "styles": {
                        "width": 142,
                        "height": 48,
                        "fontSize": 14,
                        "fontWeight": 500,
                        "fontColor": "#E5000000",
                        "maxLines": 1,
                        "textAlign": "center",
                    },
                },
            ]
        )
    components = [
        {
            "id": "root",
            "component": "Column",
            "children": ["header", "action_grid"],
            "itemMargin": 8,
            "styles": {
                "width": "matchParent",
                "height": "matchParent",
                "padding": 12,
                "borderRadius": 18,
                "clip": True,
                "backgroundColor": "#FFF5F7F9",
                "justifyContent": "center",
                "alignItems": "center",
            },
        },
        {
            "id": "header",
            "component": "Text",
            "content": "快捷动作",
            "styles": {
                "width": 296,
                "height": 20,
                "fontSize": 16,
                "fontWeight": 700,
                "fontColor": "#E5000000",
                "maxLines": 1,
                "textAlign": "start",
            },
        },
        {
            "id": "action_grid",
            "component": "Column",
            "children": ["action_row_1", "action_row_2"],
            "itemMargin": 8,
            "styles": {
                "width": 296,
                "height": 104,
                "justifyContent": "center",
                "alignItems": "start",
            },
        },
        {
            "id": "action_row_1",
            "component": "Row",
            "children": ["action_1", "action_2"],
            "itemMargin": 8,
            "styles": {
                "width": 296,
                "height": 48,
                "justifyContent": "center",
                "alignItems": "center",
            },
        },
        {
            "id": "action_row_2",
            "component": "Row",
            "children": ["action_3", "action_4"],
            "itemMargin": 8,
            "styles": {
                "width": 296,
                "height": 48,
                "justifyContent": "center",
                "alignItems": "center",
            },
        },
        *actions,
    ]
    return [
        {
            "version": "v0.9",
            "createSurface": {
                "surfaceId": "hub",
                "catalogId": "ohos.a2ui.extended.catalog.form",
            },
        },
        {
            "version": "v0.9",
            "updateComponents": {
                "surfaceId": "hub",
                "root": "root",
                "components": components,
            },
        },
        {
            "version": "v0.9",
            "updateDataModel": {
                "surfaceId": "hub",
                "path": "/",
                "value": {"state": {"ready": True}},
            },
        },
    ]


class AlignmentRulesTest(unittest.TestCase):
    def test_aligned_fixtures_pass_with_cardspec(self) -> None:
        for stem in ("aligned_2x2_metric", "aligned_2x4_agenda"):
            result = run_validator(
                FIXTURES / f"{stem}.genui.jsonl",
                FIXTURES / f"{stem}.cardspec.json",
            )
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_root_shell_fields_are_hard_requirements(self) -> None:
        base = read_messages("aligned_2x2_metric.genui.jsonl")
        cardspec = FIXTURES / "aligned_2x2_metric.cardspec.json"
        mutations = (
            ("dimensions", ("width", "height")),
            ("padding", ("padding",)),
            ("shape", ("borderRadius", "clip")),
            ("background", ("linearGradient",)),
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            for label, fields in mutations:
                messages = copy.deepcopy(base)
                root = messages[1]["updateComponents"]["components"][0]
                for field in fields:
                    root["styles"].pop(field, None)
                dsl = temp_root / f"missing_{label}.jsonl"
                write_messages(dsl, messages)
                result = run_validator(dsl, cardspec, aesthetic=False)
                self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_root_background_must_be_valid_and_opaque(self) -> None:
        base = read_messages("aligned_2x2_metric.genui.jsonl")
        cardspec = FIXTURES / "aligned_2x2_metric.cardspec.json"
        invalid_backgrounds = (
            {"backgroundColor": False},
            {"backgroundColor": "#00FFFFFF"},
            {
                "linearGradient": {
                    "direction": "Right",
                    "colors": [["#FFFFFFFF", 0], ["#00FFFFFF", 1]],
                }
            },
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            for index, background in enumerate(invalid_backgrounds):
                messages = copy.deepcopy(base)
                root_styles = messages[1]["updateComponents"]["components"][0]["styles"]
                root_styles.pop("linearGradient", None)
                root_styles.update(background)
                dsl = Path(temp_dir) / f"invalid_background_{index}.jsonl"
                write_messages(dsl, messages)
                result = run_validator(dsl, cardspec, aesthetic=False)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("STYLE_ROOT_BACKGROUND_REQUIRED", result.stdout)

    def test_free_outer_layout_fails_fixed_skeleton_check(self) -> None:
        messages = read_messages("aligned_2x2_metric.genui.jsonl")
        for component in messages[1]["updateComponents"]["components"]:
            if component["id"] in {"header", "hero", "support"}:
                component["styles"]["height"] = 30
        with tempfile.TemporaryDirectory() as temp_dir:
            dsl = Path(temp_dir) / "free_layout.jsonl"
            write_messages(dsl, messages)
            result = run_validator(
                dsl,
                FIXTURES / "aligned_2x2_metric.cardspec.json",
                aesthetic=False,
            )
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertIn("DESIGN_COMPACT_FIXED_SKELETON_MISMATCH", result.stdout)

    def test_root_cross_axis_overflow_fails_hard(self) -> None:
        messages = read_messages("aligned_2x2_metric.genui.jsonl")
        for component in messages[1]["updateComponents"]["components"]:
            if component["id"] == "header":
                component["styles"]["width"] = 200
        with tempfile.TemporaryDirectory() as temp_dir:
            dsl = Path(temp_dir) / "cross_axis_overflow.jsonl"
            write_messages(dsl, messages)
            result = run_validator(
                dsl,
                FIXTURES / "aligned_2x2_metric.cardspec.json",
                aesthetic=False,
            )
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertIn("DESIGN_COMPACT_ROOT_CROSS_AXIS_OVERFLOW", result.stdout)

    def test_four_action_hub_requires_exact_internal_grid(self) -> None:
        messages = four_action_hub_messages()
        cardspec_data = {
            "title": "快捷动作",
            "description": "四项快捷操作",
            "suggestSize": "2x4",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            cardspec = temp_root / "hub.cardspec.json"
            cardspec.write_text(
                json.dumps(cardspec_data, ensure_ascii=False), encoding="utf-8"
            )
            valid_dsl = temp_root / "valid_hub.jsonl"
            write_messages(valid_dsl, messages)
            valid = run_validator(valid_dsl, cardspec, aesthetic=False)
            self.assertEqual(valid.returncode, 0, valid.stdout)

            invalid_messages = copy.deepcopy(messages)
            for component in invalid_messages[1]["updateComponents"]["components"]:
                if component["id"].startswith("action_") and not component["id"].startswith("action_label") and not component["id"].startswith("action_row"):
                    component["styles"]["width"] = 40
                if component["id"].startswith("action_row"):
                    component["itemMargin"] = 4
            invalid_dsl = temp_root / "invalid_hub.jsonl"
            write_messages(invalid_dsl, invalid_messages)
            invalid = run_validator(invalid_dsl, cardspec, aesthetic=False)
            self.assertNotEqual(invalid.returncode, 0, invalid.stdout)
            self.assertIn("DESIGN_COMPACT_ACTION_LIMIT_EXCEEDED", invalid.stdout)

    def test_reliable_theme_override_is_review_not_strict_failure(self) -> None:
        messages = read_messages("aligned_2x2_metric.genui.jsonl")
        root = messages[1]["updateComponents"]["components"][0]
        root["styles"]["linearGradient"]["colors"] = [
            ["#FFF0F8FF", 0],
            ["#FFFFFFFF", 1],
        ]
        for component in messages[1]["updateComponents"]["components"]:
            if component["id"] == "battery_icon":
                component["styles"]["fillColor"] = "#FF3366CC"
        with tempfile.TemporaryDirectory() as temp_dir:
            dsl = Path(temp_dir) / "theme_override.jsonl"
            write_messages(dsl, messages)
            result = run_validator(
                dsl, FIXTURES / "aligned_2x2_metric.cardspec.json"
            )
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("DESIGN_COMPACT_THEME_", result.stdout)

    def test_cross_family_theme_gradient_still_fails_strict(self) -> None:
        messages = read_messages("aligned_2x2_metric.genui.jsonl")
        root = messages[1]["updateComponents"]["components"][0]
        root["styles"]["linearGradient"]["colors"] = [
            ["#FFFFEEEE", 0],
            ["#FFEEEEFF", 1],
        ]
        with tempfile.TemporaryDirectory() as temp_dir:
            dsl = Path(temp_dir) / "cross_family_gradient.jsonl"
            write_messages(dsl, messages)
            result = run_validator(
                dsl, FIXTURES / "aligned_2x2_metric.cardspec.json"
            )
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertIn("DESIGN_COMPACT_GRADIENT_PAIR_NOT_ALLOWED", result.stdout)


if __name__ == "__main__":
    unittest.main()
