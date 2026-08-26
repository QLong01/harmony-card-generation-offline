# Harmony Card Generation Offline

一个用于离线生成、修复、评审和解释 HarmonyOS A2UI Form 服务卡片的 Codex skill。

项目保留完整的 `genui` Form JSONL、DataModel、事件能力和 CardSpec 协议，同时把任务收敛、信息与动作预算、2x2/2x4 固定骨架、字体、间距、色板、图表和素材规则对齐到 CreateMyCard `design-compact-dsl` 的远程 Prompt。

## 主要能力

- 根据 query 与能力清单自由生成内容，不依赖带固定文案或数据的视觉模板。
- 支持 `2x2` 与 `2x4`，分别使用经过预算的固定关系骨架。
- 支持天气、日程、倒计时、应用时长、耳机、手机电量、健康运动和系统内存等数据能力。
- 支持本地素材、已声明点击事件以及严格的 DataModel / CardSpec 对齐。
- 提供离线校验器，检查协议、组件、表达式、能力契约、布局、色板和资源路径。

## 对齐基线

- 上游文件：`widget_service/cloud/data/protocol_profiles/design-compact-dsl/PROMPT.md`
- 上游分支：`dev`
- 对齐提交：`91e8be400099189756f3c9d7d0f6614387d40c02`
- 对齐范围：除极简协议表示法与 few-shot 内容外的任务选择、骨架、布局、视觉、事件、素材和自检规则。

本项目不会输出上游的 compact component arrays 或 TaskSpec；这些规则会映射为本项目的完整 Form 组件和 CardSpec 能力契约。

## 项目结构

```text
.
├── SKILL.md
├── agents/openai.yaml
├── reference/
│   ├── capability/
│   ├── design/
│   └── protocol/
└── scripts/
    ├── validate_card.py
    ├── rules/
    └── validators/
```

## 使用方式

将项目放入支持 Codex skill 的目录后，根据 `SKILL.md` 使用。

```bash
python scripts/validate_card.py --dsl example.genui.jsonl --fail-on-error
```

```bash
python scripts/validate_card.py \
  --dsl example.genui.jsonl \
  --cardspec example.cardspec.json \
  --enable-aesthetic \
  --fail-on-error
```

更多参数和 Python API 用法见 [`scripts/README.md`](scripts/README.md)。

运行对齐回归（包含 root 负例、自由骨架负例、主题色 review，以及 2x2/2x4 DSL + CardSpec）：

```bash
python -X utf8 -m unittest discover -s tests -p "test_*.py" -v
```

## 输出格式

每张卡片的 DSL 固定为三行 JSONL：`createSurface`、`updateComponents`、`updateDataModel`。每张卡片同时输出一个 CardSpec JSON；动态卡片用 `dataBindings` 声明端侧数据能力及其写入路径。
