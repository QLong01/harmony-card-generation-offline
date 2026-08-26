---
name: harmony-card-generation-offline
description: "离线生成、修复、评审或解释 HarmonyOS A2UI Form 服务卡片；输出三行 genui JSONL 与 cardspec JSON。新卡片视觉严格遵循 Pixso 0804 的 2×2 布局、字体、间距、图表、背景和 icon 规范，并按 Form DSL 协议处理绑定、事件与能力契约。"
---

# Harmony 卡片生成（Pixso 0804 离线版）

产出同一张卡片的三行 `genui` JSONL 和一个 `cardspec` JSON。协议以本 skill 的 `reference/protocol/`、`reference/capability/` 为准；视觉唯一依据是 [`reference/design/pixso-0804-spec.md`](reference/design/pixso-0804-spec.md)。

## 必须读取

1. 所有任务先读 `reference/core-rules.md`。
2. 新生成先完整读 `reference/generation-workflow.md` 和 `reference/design/pixso-0804-spec.md`。
3. 需要具体 DSL 字段时读 `reference/protocol/component-catalog.md`；需要绑定时读 `reference/protocol/data-binding.md`。
4. 需要动态能力时读 `reference/capability/cardspec.md`，再通过 `reference/capability/data-capability/index.md` 只加载命中的 1–2 个 manifest。
5. 需要素材时读 `reference/design/asset-library.md`；需要点击时读对应 event capability。

不得用旧样例、记忆、包外 UX 文档或自由设计启发补充 Pixso 未给出的视觉规则。

## 执行顺序

1. 收敛为一个主问题，标记 `mustKeep`、可删除描述、必要动作和来源应用。
2. 新生成锁定 `2x2 = 160vp × 160vp`。Pixso 0804 没有 2×4 视觉几何；用户要求新生成 2×4 时说明边界或收敛为 2×2，不把 2×2 外推。
3. 从 Pixso 指定背景中选择一个：专注、日程、防沉迷、耳机、低电、清理、晴天关怀、雨天打车、赛事倒计时、睡眠监督、应用背景或通用背景。
4. 用固定三段骨架：必选标题区、可选内容区、可选按钮区。root `padding: 8`；内容距标题和按钮都至少 `8vp`。
5. 只选择一个主要内容原子：常规文字、大数值、单选列表视觉、环形图、线性进度条或图片。
6. 按 `component-catalog.md` 写组件；协议不支持 Pixso 的 Radio 时，用圆形 Checkbox 或 Image + Text 复现，不输出禁用组件。
7. 动态字段和 CardSpec 只来自已声明 capability；动作能力不明时删除点击和按钮。
8. 输出前逐项对照 Pixso：字号、最大行数、间距、按钮/icon/ring/进度尺寸、背景、前景和 icon 颜色；再检查协议、绑定、事件和 CardSpec 闭环。

## Pixso 硬约束摘要

- root `padding: 8`；结构间距只用 `0/2/4/8/12/16vp`。
- 标题 12fp；可选右上 icon `20×20vp`、圆角4、间隔4；有 icon 时文字区最大112vp。
- 胶囊按钮高36，文字14（最低12），可选 icon20；纯 icon 按钮30，中心 icon16。
- 字号只用 `10/12/14/16/20/30/38fp`，禁用旧版18/32/40fp。
- ring 默认52、最小44、粗6、中心 icon24；进度1–2条粗8，3条粗4。
- 浅色层级为黑90/60/40/10；浅色背景是白底加指定场景色10%到透明白；特殊全幅渐变只允许 Pixso 列出的四组2-stop色值。
- 不创建场景拓展色，不使用第三 stop、径向渐变、orb、bokeh、玻璃拟态、自由比例带、dashboard 或装饰性卡片套卡片。

完整规则必须读 `reference/design/pixso-0804-spec.md`，不能只凭本摘要生成。

## 输出形态

只输出两个代码块，顺序固定：

```genui
{"version":"v0.9","createSurface":{"surfaceId":"...","catalogId":"ohos.a2ui.extended.catalog.form"}}
{"version":"v0.9","updateComponents":{"surfaceId":"...","root":"...","components":[...]}}
{"version":"v0.9","updateDataModel":{"surfaceId":"...","path":"/","value":{}}}
```

```cardspec
{
  "title": "状态卡片",
  "description": "状态概览",
  "suggestSize": "2x2"
}
```

- 静态卡片也输出 `cardspec`，但不虚构 `dataBindings`。
- 动态 `cardspec.dataBindings` 必须来自已声明能力，UI 路径可由 `writeResultTo + outputSchema` 推导。
- 模式 1/2 的最终回答只给 DSL/CardSpec，不输出解释、日志、命令、比较过程或中间文件。

## 协议不变量

- root `styles.width/height` 写 `"matchParent"`；`createSurface.width/height` 默认省略。
- root 继续使用当前 Form 约束的 `borderRadius: 18`、`clip: true`；该值是协议兼容要求，不用于推导 Pixso 内部圆角。
- 新生成使用稳定语义 ID；删除组件时同步清理 `children` 和 DataModel 冗余字段。
- 只用允许组件、本地素材和已声明事件；禁用网络图、内联/base64 SVG、emoji、占位媒体、`Button.action` 和非 `onClick` 事件。
- 可点击 UI 必须有真实 `onClick`；无动作能力时不要保留按钮外观。

## 失败处理

按此顺序降级：删除描述/辅助信息 → 使用 Pixso 同原子的小字号档 → 删除非必要 icon/图片 → 回退通用背景 → 收敛为更简单的 Pixso 内容分支 → 说明能力边界。不得以自定义颜色、间距、字号、2×4 外推或自由构图解决失败。
