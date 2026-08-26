# Harmony Card Generation Offline

一个用于离线生成、修复、评审和解释 HarmonyOS A2UI Form 服务卡片的 Codex skill。

项目根据 Pixso 0804 设计规范生成可渲染的 `genui` JSONL，并通过 CardSpec 描述端侧数据能力。新卡片使用 2×2 画布，遵循既定的布局、字体、颜色、素材、事件和数据绑定约束。

## 主要能力

- 根据用户需求直接生成 Form DSL，不依赖预制视觉模板。
- 支持天气、日程、倒计时、应用时长、耳机、手机电量、健康运动和系统内存等能力。
- 支持专注、日程、防沉迷、耳机、低电、清理、晴天关怀、雨天出行、赛事倒计时和睡眠等视觉场景。
- 支持本地素材、已声明点击事件以及严格的 DataModel / CardSpec 对齐。
- 提供离线校验器，用于检查协议、组件、表达式、能力契约和资源路径。

## 项目结构

```text
.
├── SKILL.md                     # Skill 入口与执行规则
├── agents/openai.yaml           # Agent 配置
├── reference/                   # 设计、协议和能力文档
│   ├── capability/              # 数据能力、事件能力与 CardSpec
│   ├── design/                  # Pixso 规范、颜色、布局和素材库
│   └── protocol/                # Form 协议、组件目录与数据绑定
└── scripts/                     # 离线校验器和规则配置
    ├── validate_card.py
    ├── rules/
    └── validators/
```

## 使用方式

将项目放入支持 Codex skill 的目录后，根据 `SKILL.md` 中的规则使用。

单独校验一份 DSL：

```bash
python scripts/validate_card.py --dsl example.genui.jsonl --fail-on-error
```

同时校验 DSL 和 CardSpec：

```bash
python scripts/validate_card.py \
  --dsl example.genui.jsonl \
  --cardspec example.cardspec.json \
  --fail-on-error
```

更多参数和 Python API 用法见 [`scripts/README.md`](scripts/README.md)。

## 输出格式

每张卡片的 DSL 固定为三行 JSONL，顺序为：

1. `createSurface`
2. `updateComponents`
3. `updateDataModel`

动态卡片还可以配套输出一个 CardSpec JSON，用于声明数据能力及其写入路径。
