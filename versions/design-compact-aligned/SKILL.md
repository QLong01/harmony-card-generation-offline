---
name: harmony-card-generation-offline
description: "离线生成、修复、评审或解释 HarmonyOS A2UI Form 服务卡片；输出三行 genui JSONL 与 CardSpec JSON。新卡片的任务收敛、2x2/2x4 固定骨架、信息与动作预算、字体、间距、色板、图表和素材规则与远程 design-compact-dsl Prompt 对齐，同时保留完整 Form DSL、数据绑定和能力契约。"
---

# Harmony 卡片生成（Design Compact 对齐版）

产出同一张卡片的三行 `genui` JSONL 和一个 `cardspec` JSON。协议以 `reference/protocol/`、`reference/capability/` 为准；非协议生成规范以 [`reference/design/design-compact-aligned-spec.md`](reference/design/design-compact-aligned-spec.md) 为唯一依据。

## 必须读取

1. 所有任务先完整读取 `reference/core-rules.md`。
2. 新生成再完整读取 `reference/generation-workflow.md` 与 `reference/design/design-compact-aligned-spec.md`。
3. 写具体 DSL 字段时读 `reference/protocol/component-catalog.md`；需要绑定时读 `reference/protocol/data-binding.md`。
4. 需要动态能力时读 `reference/capability/cardspec.md`，再通过 `reference/capability/data-capability/index.md` 只加载命中的 1–2 个 manifest。
5. 只要图标、图片或背景素材可能承担识别/状态/动作/主媒体职责，就读 `reference/design/asset-library.md`；需要点击时读对应 event capability。

数据、事件与素材能力以 `scripts/rules/config/capabilities.json` 路由的三份原始 manifest 为真相源；生成文档只用于检索，若有冲突以 manifest 为准。

不得把远程极简协议的字段名、压缩组件结构或 TaskSpec 原样输出；必须把其非协议规则映射为本项目的完整 Form 组件、DataModel 与 CardSpec。

## 执行顺序

1. 收敛为一个服务对象和一个主问题；把候选数据、素材、动作分成 `mustKeep / shouldKeep / drop`。
2. 按用户要求锁定尺寸。未指定时默认 `2x2`；明确要求 `2x4` 时保留 `2x4`，不得自动升降尺寸。
3. 选择一个固定骨架：2x2 五选一，2x4 六选一。骨架只约束信息关系和几何，不提供固定文案、示例值或组件模板。
4. 选择一个表面策略与一个色族；最多再用一个真实状态/动作色。
5. 只保留最小充分字段和最少必要素材；每个可见组件职责唯一，主层级最多三层。
6. 先按全画布预算写完整 Form 组件，再接入已声明数据能力、事件能力、绑定和 CardSpec。
7. 对每个 Row/Column 同时核算主轴和交叉轴；受保护文本按保守宽度压力测试。
8. 输出前逐项检查尺寸、骨架、事件显式性、动态字段、颜色家族、素材、协议和能力闭环。

## 生成硬约束摘要

- 逻辑画布：`2x2 = 160×160vp`，`2x4 = 320×160vp`；root `padding: 12`、`borderRadius: 18`、`clip: true`，内部安全区分别为 `136×136vp`、`296×136vp`。
- 间距只用 `2/4/6/8/10/12/14/16vp`，优先 `4/8/12/16`；分组间距不得小于组内间距。
- 字号只用 `10/12/14/16/18/20/32/40fp`，每张卡最多三档；旧的 `30/38fp` 映射为 `32/40fp`。
- 默认胶囊动作高 `36vp`、圆角 `18vp`、文字 `14fp/600`；独立 icon 动作 `30×30vp`，点击目标不得小于 `24vp`。
- ring 直径 `56–72vp`，粗度为直径的 `14%–15%`；线性进度 1–2 行高 `8vp`，3 行高 `4vp`。没有可靠范围或总量时禁用进度。
- 渐变恰好两个同色族 stop；禁止跨色族、三 stop、彩虹、orb、bokeh。默认从 6 组受控色板中整组选择 canvas/surface/accent。
- Image 必须显式 `width/height/objectFit`；SVG 默认可按直接背景和色彩角色染色，PNG 不染色。素材只在承担职责时使用，不为填空使用。
- 2x2 最多 3 个主区域、1 个显式动作、1 个内部内容背板；2x4 最多 4 个主区域，默认最多 2 个动作、1 个主背板加 1 个弱支撑背板。

完整骨架、色值、文字压力测试和事件规则必须读对齐规范，不能只凭摘要生成。

## 输出形态

只输出两个代码块，顺序固定：

```genui
{"version":"v0.9","createSurface":{"surfaceId":"...","catalogId":"ohos.a2ui.extended.catalog.form"}}
{"version":"v0.9","updateComponents":{"surfaceId":"...","root":"...","components":[...]}}
{"version":"v0.9","updateDataModel":{"surfaceId":"...","path":"/","value":{"state":{"ready":true}}}}
```

```cardspec
{
  "title": "状态卡片",
  "description": "状态概览",
  "suggestSize": "2x2"
}
```

- 静态卡片也输出 CardSpec，但不虚构 `dataBindings`。
- 动态 `CardSpec.dataBindings` 必须来自已声明能力；UI 路径由 `writeResultTo + outputSchema` 推导。
- 最终回答只给 DSL/CardSpec，不输出解释、日志、命令、比较过程或中间文件。

## 协议不变量

- root `styles.width/height` 写 `"matchParent"`；`createSurface.width/height` 默认省略。
- 只用允许组件、本地素材和已声明事件；禁用网络图、内联/base64 SVG、emoji、占位媒体、`Button.action` 和非 `onClick` 事件。
- 动态可见值必须绑定到 DataModel 或能力输出；示例初始值只表示预览，不得冒充真实用户数据。
- 可点击 UI 必须有真实 `onClick`；同一动作不得同时绑 root 与按钮。没有动作能力时删除点击外观。
- 动态能力写入子树必须是对应 `outputSchema` 的合法投影；辅助状态放到 `/view` 或 `/state`。

## 失败处理

按此顺序降级：删除 `drop` → 删除装饰性素材 → 删除普通 `shouldKeep` → 删除隐式入口 → 改用同尺寸更简单骨架 → 回退 neutral 色板 → 说明能力边界。用户明确要求的显式动作不得被删；不得靠缩小受保护文本、裁剪、增加自由背板、跨色族配色或自动改尺寸解决失败。
