from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = SKILL_DIR / "scripts" / "rules" / "config" / "capabilities.json"

DATA_FILES = {
    "ViewWeather": "weather.md",
    "GetCalendarEvents": "calendar.md",
    "GetCountdownDays": "countdown-days.md",
    "GetAppUsageDuration": "app-usage.md",
    "GetEarphoneInfo": "blutoothearphone-status.md",
    "GetPhoneBatteryInfo": "phone-battery.md",
    "GetHealthAndSportSummary": "healthy-sport.md",
}

DATA_SCENES = {
    "ViewWeather": "天气、空气质量、温湿度、未来预报与天气提醒",
    "GetCalendarEvents": "今日/未来日程、会议、日历提醒与赛事日程",
    "GetCountdownDays": "指定日期倒数日、纪念日、节日、考试或截止日期",
    "GetAppUsageDuration": "指定应用今日使用时长",
    "GetEarphoneInfo": "蓝牙耳机连接、电量与左右耳/耳机盒状态",
    "GetPhoneBatteryInfo": "手机电量、充电状态、电池健康、温度、电流与电压",
    "GetHealthAndSportSummary": "睡眠、步数、热量、距离、最近运动与心率",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def markdown_cell(value: object) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ")


def package_names(item: dict[str, Any]) -> list[str]:
    dependencies = item.get("dependencies", {})
    packages = dependencies.get("requiredPackages", []) if isinstance(dependencies, dict) else []
    return [
        package.get("packageName")
        for package in packages
        if isinstance(package, dict) and isinstance(package.get("packageName"), str)
    ]


def source_note(config: dict[str, Any], manifest_name: str, relative_link: str) -> str:
    return (
        f"能力源：[`{manifest_name}`]({relative_link})，来源提交 "
        f"`{config['sourceCommit']}`，profile `{config['profileId']}`。"
    )


def write_data_docs(config: dict[str, Any], data_items: list[dict[str, Any]]) -> None:
    target_dir = SKILL_DIR / "reference" / "capability" / "data-capability"
    target_dir.mkdir(parents=True, exist_ok=True)
    manifest_link = (
        "../../../scripts/rules/capabilities/"
        f"{config['profileId']}/{config['dataManifest']}"
    )
    rows: list[str] = []
    for item in data_items:
        capability_id = item.get("id")
        if capability_id not in DATA_FILES:
            raise ValueError(f"Unmapped data capability: {capability_id}")
        filename = DATA_FILES[capability_id]
        required = item.get("inputSchema", {}).get("required", [])
        packages = package_names(item)
        output_properties = item.get("outputSchema", {}).get("properties", {})
        output_paths = [
            f"`{item.get('defaultWriteResultTo')}/{name}`"
            for name in output_properties
        ] if isinstance(output_properties, dict) else []
        content = [
            f"# {capability_id}",
            "",
            source_note(config, config["dataManifest"], manifest_link),
            "",
            markdown_cell(item.get("description")),
            "",
            "## 生成规则",
            "",
            f"- `capabilityId`: `{capability_id}`",
            f"- 推荐 `writeResultTo`: `{item.get('defaultWriteResultTo')}`",
            f"- 必填入参：{', '.join(f'`{name}`' for name in required) if required else '无'}",
            f"- 依赖包：{', '.join(f'`{name}`' for name in packages) if packages else '无'}",
            "- `arguments` 只能使用下方 `inputSchema.properties`；类型、枚举、范围和必填项必须原样遵守。",
            "- UI 只能访问 `writeResultTo + outputSchema` 可推导路径；初始化数据必须是 outputSchema 的合法投影。",
            f"- 顶层输出路径：{', '.join(output_paths) if output_paths else '无'}",
            "",
            "## 原始能力声明",
            "",
            "```json",
            json.dumps(item, ensure_ascii=False, indent=2),
            "```",
            "",
        ]
        (target_dir / filename).write_text("\n".join(content), encoding="utf-8")
        rows.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(DATA_SCENES[capability_id]),
                    f"[`{filename}`]({filename})",
                    f"`{capability_id}`",
                    f"`{item.get('defaultWriteResultTo')}`",
                ]
            )
            + " |"
        )

    index = [
        "# 数据能力索引",
        "",
        source_note(config, config["dataManifest"], manifest_link),
        "",
        "先按 query 命中最多 1–2 个必要能力，再读取对应文件。清单外能力不得编造；静态卡片不写 `dataBindings`。",
        "",
        "| 用户意图 | 读取文件 | 能力 ID | 推荐 `writeResultTo` |",
        "| --- | --- | --- | --- |",
        *rows,
        "",
        "## 共通约束",
        "",
        "- CardSpec `arguments` 必须满足原始 `inputSchema`；UI/DataModel 必须满足 `outputSchema`。",
        "- 多个 `writeResultTo` 不得相同、互为父子或彼此覆盖。",
        "- 依赖包不可用时不得假装能力可执行；改用静态降级或说明能力边界。",
        "- 事件参数引用数据时，该字段必须存在于命中 data capability 的 `outputSchema`。",
        "",
    ]
    (target_dir / "index.md").write_text("\n".join(index), encoding="utf-8")


def write_event_doc(config: dict[str, Any], event_items: list[dict[str, Any]]) -> None:
    target = SKILL_DIR / "reference" / "capability" / "event-capability" / "click-event.md"
    manifest_link = (
        "../../../scripts/rules/capabilities/"
        f"{config['profileId']}/{config['eventManifest']}"
    )
    rows: list[str] = []
    for item in event_items:
        template = item.get("actionTemplate", {})
        dynamic = item.get("dynamicArguments", [])
        paths = [entry.get("path") for entry in dynamic if isinstance(entry, dict)]
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{item.get('id')}`",
                    f"`{template.get('call')}`",
                    f"`{item.get('targetScene')}`",
                    markdown_cell(", ".join(path for path in paths if isinstance(path, str)) or "—"),
                    markdown_cell(", ".join(package_names(item)) or "—"),
                    markdown_cell(item.get("description")),
                ]
            )
            + " |"
        )
    content = [
        "# 点击事件能力",
        "",
        source_note(config, config["eventManifest"], manifest_link),
        "",
        "只使用下表声明的事件。DSL `onClick` 仍写单元素 EventHandler 数组；复制命中能力的 `actionTemplate.call/args`，只替换 `dynamicArguments` 指定路径，并让最终值满足 `parametersSchema`。",
        "",
        "| 能力 ID | call | targetScene | 动态参数路径 | 依赖包 | 用途 |",
        "| --- | --- | --- | --- | --- | --- |",
        *rows,
        "",
        "## 约束",
        "",
        "- 未命中能力时删除点击与动作外观，不编造 call、intentName、URI、bundleName 或 params。",
        "- `actionTemplate` 中未列为动态参数的常量不得改写；动态表达式必须能从 DataModel 推导。",
        "- 依赖包不可用时不得选择该事件；同一交互只绑定一个 onClick。",
        "- 完整 actionTemplate、dynamicArguments 和 parametersSchema 以原始 manifest 为准。",
        "",
    ]
    target.write_text("\n".join(content), encoding="utf-8")


def write_asset_doc(config: dict[str, Any], asset_items: list[dict[str, Any]]) -> None:
    target = SKILL_DIR / "reference" / "design" / "asset-library.md"
    manifest_link = (
        "../../scripts/rules/capabilities/"
        f"{config['profileId']}/{config['assetManifest']}"
    )
    visual_authority = (
        "`design-compact-aligned-spec.md`"
        if (SKILL_DIR / "reference" / "design" / "design-compact-aligned-spec.md").exists()
        else "`pixso-0804-spec.md`"
    )
    rows = [
        "| "
        + " | ".join(
            [
                f"`{item.get('id')}`",
                f"`{item.get('src')}`",
                markdown_cell(", ".join(item.get("sceneTags", [])) or "—"),
                markdown_cell(item.get("description")),
                f"`{item.get('minXiaoyiVersion')}`",
            ]
        )
        + " |"
        for item in asset_items
    ]
    content = [
        "# 素材能力索引",
        "",
        source_note(config, config["assetManifest"], manifest_link),
        "",
        "## 选择规则",
        "",
        "- 只使用下表/原始 manifest 中存在的 `id` 与 `src`，不得猜测文件名或替换目录。",
        "- 按 description、sceneTags 和实际内容职责选择最少必要素材；没有语义职责时不为填空使用素材。",
        f"- 数量、尺寸、布局、染色和背景策略服从当前版本的视觉规范 {visual_authority}。",
        "- SVG 只有在描述与素材结构允许时染色；PNG、品牌、多色、渐变或要求保留原色的素材不染色。",
        "- `Image` 必须显式声明 width、height、objectFit；依赖版本不满足 `minXiaoyiVersion` 时不得使用。",
        "",
        "## 素材清单",
        "",
        "| 能力 ID | src | sceneTags | description | 最低小艺版本 |",
        "| --- | --- | --- | --- | --- |",
        *rows,
        "",
    ]
    target.write_text("\n".join(content), encoding="utf-8")


def main() -> None:
    config = load_json(CONFIG_PATH)
    bundle = SKILL_DIR / config["bundleDirectory"]
    data_items = load_json(bundle / config["dataManifest"])
    event_items = load_json(bundle / config["eventManifest"])
    asset_items = load_json(bundle / config["assetManifest"])
    if not (len(data_items) == 7 and len(event_items) == 18 and len(asset_items) == 72):
        raise ValueError("Unexpected capability bundle counts")
    write_data_docs(config, data_items)
    write_event_doc(config, event_items)
    write_asset_doc(config, asset_items)


if __name__ == "__main__":
    main()
