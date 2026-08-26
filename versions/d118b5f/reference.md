# Harmony 卡片参考索引

默认读取 `SKILL.md` 和 `reference/core-rules.md`。新生成必须再完整读取 `reference/generation-workflow.md` 与 `reference/design/pixso-0804-spec.md`。

## 权威顺序

1. 用户的功能需求与明确内容。
2. Form 协议、组件字段、绑定、事件与 CardSpec 合法性。
3. Pixso 0804 视觉规范。
4. 信息去重和能力边界。

协议不支持 Pixso 中的组件时，用允许组件复现相同视觉；不得输出禁用字段。Pixso 未定义的视觉不得从旧样例、记忆、网页或“设计经验”补齐。

## 文件职责

- `core-rules.md`：默认 P0/L0/L1/L2 门禁。
- `generation-workflow.md`：从自然语言到 Pixso 2×2 的固定生成顺序。
- `design/pixso-0804-spec.md`：布局、字号、间距、图表、背景、前景与 icon 的唯一视觉依据。
- `design/layout-system.md`：Pixso 几何到 Form DSL 的映射摘要。
- `design/color-token-system.md`：Pixso 背景分支选择与 DSL 颜色编码。
- `design/color-token-values.md`：Pixso 使用色值速查。
- `design/design-heuristics.md`：仅做 Pixso 一致性复核，不提供自由启发式。
- `design/asset-library.md`：本地资源 allowlist 与语义说明。
- `protocol/protocol.md`：三行 JSONL、surface/root、事件和禁用能力。
- `protocol/component-catalog.md`：允许组件、顶层字段、styles 和枚举的权威来源。
- `protocol/data-binding.md`：DataModel、Expression、PathBinding、循环项和事件参数。
- `capability/cardspec.md`：CardSpec 与 data capability 契约。
- `capability/data-capability/index.md`：能力路由；只打开命中的 manifest。
- `capability/event-capability/click-event.md`：点击事件语法和参数。

## 任务路由

- 新生成：`core-rules.md` → `generation-workflow.md` → `design/pixso-0804-spec.md` → 命中的协议/能力/素材文件。
- 修复/评审：先读 `core-rules.md`，按失败类型读协议或 Pixso 文件；不要为修复视觉引入新视觉规则。
- 动态数据：`capability/cardspec.md` → `data-capability/index.md` → 仅命中的 1–2 个 manifest。
- 白屏/JSONL/root：`protocol/protocol.md`，再查 `component-catalog.md`。
- 表达式/路径/循环：`protocol/data-binding.md`。
- 布局/字号/按钮/icon/ring/进度：先读 `design/pixso-0804-spec.md`，实现细节再读 `design/layout-system.md`。
- 背景/前景/渐变/icon 颜色：先读 `design/pixso-0804-spec.md`，编码再读 `design/color-token-system.md` 与值表。
- 素材：`design/asset-library.md`；只使用明确匹配资源。

## 2×4 边界

协议允许 2×4，但 Pixso 0804 画布只定义 2×2。新生成不得外推 2×4 视觉；用户要求时说明缺少规范或收敛成 2×2。修复既有 2×4 可以处理协议、绑定和明显渲染错误，但不能声称通过 Pixso 视觉验收。
