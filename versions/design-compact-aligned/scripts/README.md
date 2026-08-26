# Datamodel-First 卡片校验器

`scripts` 目录用于校验 HarmonyOS A2UI Form 卡片产物（三行 `genui` JSONL + `cardspec` JSON）。

## 默认运行姿态

CLI 与 Python API 默认按以下设定运行，让本地测试和接口调用不阻塞主流程：

- **只校验 DSL**：`--cardspec` 是可选项。缺少 CardSpec 时校验器只跑 DSL 相关规则，不追加 CardSpec 必填错误。
- **面向模型输出**：`--format` 默认 `model`（紧凑修复清单），而不是 `text`（长报告）或 `json`（结构化）。
- **永远非阻塞**：不管发现多少 error / warning，退出码固定 0。加 `--fail-on-error` 才恢复历史"有 error 就退出 1"的行为；`--strict` 只在 `--fail-on-error` 打开时把 warning 也算作 error。

Python API 提供两个入口：

- `validate_dsl(dsl_text) -> str`：DSL only 便捷入口，直接返回 `render_model` 字符串，把 CardSpec-only 诊断从结果里剔除。用于其它工具、Agent 或服务接接口。
- `validate_card(...) -> Reporter`：功能全集入口，返回 `Reporter` 对象，可以进一步渲染、结构化处理，或按需打开 CardSpec / effectiveCapabilities 校验。

需要更详细报告或 CI 阻塞时显式覆盖：`--format text|json`、`--strict`、`--fail-on-error`、`--cardspec`、`--enable-aesthetic` 等。

下文命令默认在 `skills/harmony-card-generation-offline/` 目录下运行；如果在仓库根目录运行，把 `python scripts/validate_card.py` 替换为 `python skills/harmony-card-generation-offline/scripts/validate_card.py`。

校验分两类：

- **静态校验**：按 `scripts/rules/` 中的静态配置和 schema 校验，默认模式。
- **动态 effective 校验**：在同一套静态规则基础上，把数据/事件/素材三类能力的白名单替换为本次运行传入的 `effectiveCapabilities`。

两者共用协议、组件、CardSpec、表达式、列表循环/绑定路径、跨文件一致、颜色等规则；区别只在数据/事件/素材能力的来源不同。

## 一、静态校验

### 1. JSONL + CardSpec

```bash
python scripts/validate_card.py --dsl out.genui.jsonl --cardspec out.cardspec.json
```

也可以传入同时包含两个 fenced code block 的草稿：

```bash
python scripts/validate_card.py draft.md
```

草稿格式：

````md
```genui
{"version":"v0.9","createSurface":{}}
{"version":"v0.9","updateComponents":{}}
{"version":"v0.9","updateDataModel":{}}
```
```cardspec
{"title":"天气","description":"今日天气","suggestSize":"2x4","dataBindings":[]}
```
````

### 2. 只传 JSONL

```bash
python scripts/validate_card.py --dsl out.genui.jsonl
```

只检查 JSONL 语法、协议行顺序、组件结构、表达式、素材基础安全等；缺少 CardSpec 时跨文件一致性和数据能力 schema 推导会受限。

### 3. 只传 CardSpec

```bash
python scripts/validate_card.py --cardspec out.cardspec.json
```

只检查 CardSpec 必填字段、尺寸、`dataBindings` 基础形态和 `writeResultTo` 冲突。

## 二、动态 effective 校验

动态校验运行在 semantic 阶段。默认 `--stage all` 会覆盖它；如果指定 `--stage hard`，不会运行动态能力校验。

动态校验不复算候选过滤，不判断 removed 原因，只检查最终 DSL/CardSpec 是否使用了 `effectiveCapabilities` 之外的数据、事件、素材能力。

### 1. JSONL + CardSpec + effective

```bash
python scripts/validate_card.py \
  --dsl out.genui.jsonl \
  --cardspec out.cardspec.json \
  --effective effective.json
```

如果输入是完整 `WidgetArtifact` JSON（包含 `genui`、`cardSpec`、`taskSpec`、`effectiveCapabilities`）：

```bash
python scripts/validate_card.py --artifact artifact.json
```

这是推荐接入方式，因为数据、事件、素材三类能力都有足够上下文。

### 2. 只传 JSONL + effective

```bash
python scripts/validate_card.py \
  --dsl out.genui.jsonl \
  --effective effective.json
```

仍会跑与静态 JSONL 校验相同的协议、组件、表达式、素材基础安全规则，并额外检查：

- DSL 中 `onClick[].call + args` 是否来自 `effectiveCapabilities.event`。
- DSL 中 `Image.src` / `backgroundImage` 是否来自 `effectiveCapabilities.asset` 解析出的资源路径。

只传 JSONL 时缺少 `CardSpec.dataBindings[].writeResultTo`，无法完整判断 `/data/...` 路径是否落在有效数据能力写入路径下；若 DSL 引用了 `/data/...`，推荐使用 `JSONL + CardSpec` 模式。

### 3. 只传 CardSpec + effective

```bash
python scripts/validate_card.py \
  --cardspec out.cardspec.json \
  --effective effective.json
```

仍会跑与静态 CardSpec 校验相同的必填字段、尺寸、`dataBindings` 基础形态、`writeResultTo` 冲突规则，并额外检查：

- `cardSpec.dataBindings[].capabilityId` 是否存在于 `effectiveCapabilities.data`。

由于没有 DSL，这种模式不会检查事件 `onClick` 和素材 `Image.src` / `backgroundImage`。

## effective.json 格式

可以直接传 `effectiveCapabilities`：

```json
{
  "data": ["ViewWeather"],
  "event": [
    {
      "call": "clickToDeeplink",
      "args": {"uri": "weather://home"}
    }
  ],
  "asset": ["asset.calendar_fill"]
}
```

也可以包一层：

```json
{
  "effectiveCapabilities": {
    "data": ["ViewWeather"],
    "event": [],
    "asset": []
  }
}
```

素材可以传 id，也可以传带 src 的对象：

```json
{
  "asset": [
    {
      "id": "asset.calendar_fill",
      "src": "resources/base/media/calendar_fill.svg"
    }
  ]
}
```

如果 effective 中只有素材 id，校验器按以下顺序把 id 解析成 `src`：

1. `artifact.taskSpec.assetCandidates`
2. 显式传入的 `--capabilities-dir/asset_capabilities.json`
3. 未传外部目录时，随 Skill 固化的 capability profile

示例：

```bash
python scripts/validate_card.py \
  --artifact artifact.json \
  --capabilities-dir widget_service/cloud/data/capabilities/app-11.7.5.205_rom-6.0
```

动态模式下，数据绑定、事件与素材解析会优先使用该目录中的三份 manifest。静态模式直接读取随 Skill 固化的 `scripts/rules/capabilities/app-11.7.5.205_rom-6.0/`，不再使用手写 schema 小样本。

如果没有传 `--capabilities-dir`，动态模式默认用 Skill 固化的 capability profile 解析 effective ID，并校验 data `inputSchema`、event `parametersSchema/dynamicArguments` 与 asset `src`。只有清单中确实不存在的外部能力才保持未解析状态。

## 全局参数

- `--format text|json|model`：输出格式，默认 `model`。
- `--stage hard|semantic|quality|all`：校验阶段，默认 `all`。
- `--max-errors N`：最多输出多少条 error，默认 `50`。
- `--fail-on-error`：把退出码从"永远 0"改成"有 error 就退出 1"。默认关闭。
- `--strict`：只有和 `--fail-on-error` 一起使用才有意义，把 warning 也算作 error。
- `--stop-on-stage-error`：hard/semantic 出错后停止后续阶段。
- `--capabilities-dir`：外部能力 manifest 目录，用于解析素材 id、动态数据能力与事件能力。
- `--enable-aesthetic`：显式开启美学质检模块（默认关闭，见下方"美学模块状态"）。

退出码：默认永远 `0`。开 `--fail-on-error` 后：`0` 无 error；`1` 存在 error，或额外指定 `--strict` 且存在 warning。

## Python API

调用方可以直接调用 API，不必起子进程跑 CLI。

### DSL only 快速调用（推荐默认）

```python
import sys
sys.path.insert(0, "scripts")

from validators import validate_dsl

report = validate_dsl(genui_text)  # 直接拿到 render_model 的字符串
print(report)
```

`validate_dsl` 只跑 DSL 相关规则，CardSpec 相关诊断会被自动过滤，返回值直接可以喂给下游模型或写入日志。

需要透传 `effectiveCapabilities`（动态白名单校验）或者调整 `stage` / `max_errors` 等参数时，`options=ValidationOptions(...)` 也可以传给 `validate_dsl`。

### 结构化调用

需要拿到诊断列表、渲染为 JSON、或者带 CardSpec 校验时，使用 `validate_card`：

动态校验完整 artifact：

```python
from pathlib import Path
import sys

sys.path.insert(0, "scripts")

from validators import ValidationOptions, validate_card

reporter = validate_card(
    artifact=artifact_dict,
    options=ValidationOptions(
        capabilities_dir=Path("widget_service/cloud/data/capabilities/app-11.7.5.205_rom-6.0"),
    ),
)

if reporter.error_count:
    print(reporter.render_json())
```

动态校验 JSONL + CardSpec：

```python
reporter = validate_card(
    dsl_text=genui,
    cardspec=card_spec,
    effective_capabilities={
        "data": ["ViewWeather"],
        "event": [],
        "asset": [],
    },
)
```

静态校验：

```python
reporter = validate_card(
    dsl_text=genui,
    cardspec=card_spec,
)
```

## 动态校验边界

动态 effective 校验等价于“最终 DSL/CardSpec 是否使用了 effective 白名单之外的能力”。它不做：

- 不检查候选能力是否合理。
- 不复算 `DeviceCapabilityResolver`。
- 不判断 removed 是否完整、原因是否正确。
- 不判断 effective 本身是否过滤正确。

## 校验阶段与流水线

三阶段固定顺序，由 `--stage` 控制截止点：

| 阶段 | 触发条件 | 参与 validator |
| --- | --- | --- |
| `hard` | 协议/结构错误必须先修 | `ProtocolValidator`、`ComponentValidator`、`DesignContractValidator`、`CardSpecValidator`、`ExpressionValidator`、`AssetValidator` |
| `semantic` | 结构 OK 后跑语义规则 | `BindingValidator`、`CrossValidator`、`EffectiveCapabilityValidator`（仅动态模式） |
| `quality` | 语义 OK 后跑质量规则 | 默认空；仅在 `--enable-aesthetic` 打开时由 `QualityValidator` 承担 |

root 外壳、固定骨架、一级 region/动作/背板上限、主轴预算和关键布局契约始终在 hard 阶段执行。颜色对比、受控色板、2-stop 渐变、字号/ring 与其它审美风险由可选美学模块负责；关闭美学模块时 `quality` 阶段不产生诊断。

默认 `--stage all` 即三阶段全跑；`--stop-on-stage-error` 会在 hard 出错后跳过 semantic、任一阶段累计出 error 后跳过 quality，用于交互式修复减少回合。若 JSONL 出现 `DSL_JSON_PARSE_FAILED`（属于 hard 阶段的致命错），流水线会整体停在解析层不再往后走。

## 目录结构

```text
scripts/
  validate_card.py                  # CLI 入口
  README.md
  rules/
    config/
      protocol.json                 # 协议、组件、CardSpec、列表循环 children、事件 handler 结构规则
      layout.json                   # 固定骨架、布局、字号、间距、ring 与美学阈值
      style.json                    # createSurface 允许样式、组件样式字段与枚举
      asset.json                    # 资源路径禁止模式与素材 manifest 路由
      capabilities.json             # 能力 profile、来源提交与三份 manifest 路由
      expression.json               # 表达式长度、括号深度、禁用变量/操作符/关键字、允许函数
      diagnostics.zh-CN.json        # 错误码 → 中文默认 message/fixHint
    capabilities/
      app-11.7.5.205_rom-6.0/
        data_capabilities.json      # 7 个 data capability
        event_capabilities.json     # 18 个 event capability
        asset_capabilities.json     # 72 个 asset capability
  sync_capability_docs.py           # 从 manifest 重建数据/事件/素材索引
  validators/
    __init__.py                     # 只导出 validate_card / validate_dsl / ValidationOptions
    api.py                          # 顶层：串联 inputs → context → pipeline
    inputs.py                       # dsl/cardspec/artifact/effective 的解析与归一化
    effective_loader.py             # 动态模式：能力目录加载、asset/data 解析
    pipeline.py                     # validator 列表、stage 选择、短路
    rule_registry.py                # 集中加载 rules/ 下配置与能力 manifest
    context.py                      # ValidationContext 数据模型
    source_parser.py                # JSONL/CardSpec/artifact 解析、表达式与列表循环上下文抽取
    diagnostics.py                  # Diagnostic + Reporter，负责聚合、限流、渲染
    base.py                         # BaseValidator + JSON Pointer / 表达式 / 数值工具函数
    protocol_validator.py           # hard 阶段
    component_validator.py          # hard 阶段
    design_contract_validator.py    # hard 阶段：固定骨架与数值布局契约
    cardspec_validator.py           # hard 阶段
    expression_validator.py         # hard 阶段
    asset_validator.py              # hard 阶段
    binding_validator.py            # semantic 阶段
    cross_validator.py              # semantic 阶段
    effective_capability_validator.py # semantic 阶段（动态模式）
    aesthetic/                      # 可选美学子系统（仅 --enable-aesthetic）
      __init__.py                   # 导出 QualityValidator
      validator.py                  # BaseValidator 包装（原 quality_validator.py）
      engine.py                     # 独立美学分析引擎（原 validate_aesthetic.py）
```

## 美学模块状态

美学质检（`validators/aesthetic/`）保留在源码中，但默认不参与流水线：

- 默认 `--stage all` 不再触发它，`validate_card` 不会因它产生 warning/error。
- 加 `--enable-aesthetic` 才在 quality 阶段独立跑并输出 `AESTHETIC_*` 诊断。
- `layout.json` 的固定骨架在 hard 阶段执行；padding、字号、间距、ring、质量阈值及 `style.json` 的受控色板/渐变 pair 还会在 `--enable-aesthetic` 时传入引擎。独立运行 `engine.py` 时使用同值的内置回退。当前规则同时覆盖 2x2 与 2x4。
- 可靠应用/对象主题色可超出默认色板；单色和可证明为同族浅色双 stop 的渐变会标记为 `DESIGN_COMPACT_THEME_*_REVIEW` 信息项，由调用方确认来源。跨色族或不满足弱主题条件的渐变仍按不合规处理。
- 美学模块整体位于 `validators/aesthetic/`：`engine.py` 提供纯分析函数，`validator.py` 包装可选 quality 检查；hard 阶段的 `DesignContractValidator` 复用其中不依赖渲染的固定骨架/布局函数。
- 颜色相关规则（token 回溯、hex 白名单、渐变结构）现在完全由美学模块承担；核心流水线已移除独立的 `ColorValidator`，`rules/config/color.json` 也已删除。

## Validator 与 rules 对应表

流水线通过 `RuleRegistry` 读取 `rules/config/*.json` 与固定 capability bundle；validator 实现确定结构算法，manifest 提供数据、事件和素材能力真相源。下表列出实际读取关系。

### hard 阶段

| Validator | 读取的规则来源 | 主要检查 |
| --- | --- | --- |
| `ProtocolValidator` | `protocol.json` → `version` / `messageOrder` / `messageRequiredFields` / `messageNonEmptyFields` / `catalogIds` / `structureFieldsNoExpression`；`style.json` → `createSurfaceAllowedStyles` | 三行 JSONL 顺序、`version` 固定、必填字段非空、`surfaceId` 三行一致、`catalogId` 合法、`updateDataModel.path` 是结构 Pointer、`createSurface.styles` 只允许外壳形状字段；`createSurface.width/height` 声明后作为 warning 提示删除（渲染实际尺寸由 root 承担） |
| `ComponentValidator` | `protocol.json` → `commonTopLevelFields` / `componentCommonRequiredFields` / `componentNonEmptyRequiredFields` / `componentTopLevelFields` / `componentRequiredFields` / `forbiddenComponentFields` / `templateComponents` / `templateChildren.allowedKeys` / `templateChildren.requiredKeys` / `eventHandlerForbiddenFields` / `allowedComponents`（`RuleRegistry.allowed_components`） | 组件 id 唯一、`root` 存在、组件类型在白名单、顶层字段/必填字段满足配置、`onClick` 数量与禁用键、列表循环 children 结构；root 必须完整声明 `matchParent`、padding12、radius18、clip true 和可证明不透明的有效背景 |
| `DesignContractValidator` | `layout.json` → `safeAreas` / `skeletons` / `regionLimits` / `primaryRegionRatio` / `compactFallback` / 动作尺寸与余量阈值；复用 `aesthetic.engine` 的固定骨架与数值布局函数 | 无需 `--enable-aesthetic` 即检查一级 region、动作/背板上限、root 两轴安全区预算、固定骨架匹配、四动作网格内部几何、关键容器数值宽高、组间/组内距、Text+action 余量、窄焦点显式定位和 2x2 底部动作 |
| `CardSpecValidator` | `protocol.json` → `sizes` 键作为允许 `suggestSize`、`cardSpec.topLevelFields` / `requiredFields` / `staticStringLimits` / `dataBindingRequiredFields` / `writeResultToPrefix` | CardSpec 顶层字段、必填、静态字符串上限、`suggestSize` 合法、`dataBindings` 每项必填、`writeResultTo` 前缀与重叠 |
| `ExpressionValidator` | `expression.json` → `maxLength` / `maxParenDepth` / `bannedVariables` / `bannedOperators` / `bannedKeywords` / `allowedFunctions` | 表达式是否完整包裹、长度、括号深度、禁用变量/操作符/关键字、只允许声明的内置函数；结构字段（id/component/EventHandler.call/as/列表循环 children.path）禁止表达式 |
| `AssetValidator` | `asset.json` → `forbiddenPatterns`；`asset_capabilities.json` → `src` allowlist | 禁止 http/https、data image、base64；静态模式下资源路径必须来自当前素材能力 manifest；动态模式交给 `EffectiveCapabilityValidator` |

### semantic 阶段

| Validator | 读取的规则来源 | 主要检查 |
| --- | --- | --- |
| `BindingValidator` | `data_capabilities.json`、`event_capabilities.json`；动态模式改读 effective manifest | `dataBindings[].capabilityId/arguments/writeResultTo` 是否满足 inputSchema；表达式路径是否可由 outputSchema 推导；`onClick` 是否匹配某个事件的 actionTemplate、dynamicArguments 与 parametersSchema |
| `CrossValidator` | `RuleRegistry.capabilities`（静态能力 schema） | `dataBindings[].writeResultTo` 根结构是否在 `updateDataModel.value` 初始化；capability 是否声明了 `outputSchema`。root 外壳由 ComponentValidator 检查，固定画布/骨架预算由 DesignContractValidator 检查。 |
| `EffectiveCapabilityValidator` | 仅动态模式：`context.effective_capabilities`（`data/event/asset`）+ `context.effective_asset_sources` + `context.effective_data_capabilities`；不读 `rules/` | `dataBindings[].capabilityId` 是否在 effective.data；DSL `/data/...` 是否在 effective 数据能力的 `writeResultTo` 覆盖之下；`onClick` 是否与 effective.event 中的 `{call,args}` 精确匹配；`Image.src` / `backgroundImage` 是否命中 effective.asset 解析出的 src |

### quality 阶段

默认没有任何 validator 参与本阶段。开启 `--enable-aesthetic` 后：

| Validator | 读取的规则来源 | 主要检查 |
| --- | --- | --- |
| `QualityValidator` | `layout.json` 中的美学阈值（对比度、字号/圆角/阴影层级上限等）；委托 `aesthetic/engine.py` | 产出 `AESTHETIC_*` 诊断和 0–100 质量分；颜色对比度、hex 回溯、渐变复杂度等都在此判定 |

### 规则文件到 validator 的反查表

- `rules/config/protocol.json` → `ProtocolValidator`、`ComponentValidator`、`CardSpecValidator`、`CrossValidator`。其中 `forbiddenComponents` 与 `structureFieldsNoExpression` 目前作为规则声明留存，validator 未直接读取（组件白名单 + 各 validator 里对结构字段的表达式禁令已覆盖等价约束）。
- `rules/config/expression.json` → `ExpressionValidator`。
- `rules/config/style.json` → `ProtocolValidator`（`createSurfaceAllowedStyles`）与可选 `QualityValidator` / `aesthetic.engine`（受控色板、渐变 pair、可靠主题 review）。
- `rules/config/capabilities.json` → `RuleRegistry` 的 profile、来源提交和 manifest 路由。
- `rules/config/asset.json` → `AssetValidator` 的禁止模式；allowlist 由 `asset_capabilities.json` 的 `src` 生成。
- `rules/config/layout.json` → hard 阶段 `DesignContractValidator` / `aesthetic.engine`（安全区、固定骨架、区域/动作/背板预算、比例、降级骨架和动作尺寸）以及可选 `QualityValidator` / `aesthetic.engine`（字号、间距、ring、progress 与质量阈值）。
- `rules/config/diagnostics.zh-CN.json` → `Reporter`：为 `add()` 未显式传 `message/fixHint` 的诊断提供默认中文文案。
- `rules/capabilities/.../data_capabilities.json` → `BindingValidator`、`CrossValidator` 的静态数据能力；动态模式下可由 `--capabilities-dir` 覆盖。
- `rules/capabilities/.../event_capabilities.json` → `BindingValidator._check_event_handlers`。
- `rules/capabilities/.../asset_capabilities.json` → `RuleRegistry.asset_allowlist`；`reference/design/asset-library.md` 由 `sync_capability_docs.py` 从同一 manifest 生成。
- 组件目录 / 表达式语法 / CardSpec JSON Schema 参考文档：真相源已迁移到 `protocol.json`、`expression.json`、`protocol.json.cardSpec`；供人阅读的说明由 `reference/protocol/*.md` 承担，`rules/` 下不再冗余保留。
- `rules/config/color.json` 已随 `ColorValidator` 一起删除。
