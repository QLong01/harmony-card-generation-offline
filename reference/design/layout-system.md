# 布局系统

权威来源是 [`design-compact-aligned-spec.md`](design-compact-aligned-spec.md)。本文只说明完整 Form DSL 的落地要点。

## 画布

- 2x2：160×160，root padding12，内部 136×136。
- 2x4：320×160，root padding12，内部 296×136。
- root `borderRadius: 18`、`clip: true`、显式背景。

## 骨架路由

2x2：`compact-metric-action`、`compact-event-action`、`compact-date-next`、`compact-dual-fact`、`compact-dual-item-summary`。

2x4：`wide-hero-context`、`wide-timeseries-strip`、`wide-agenda-stack`、`wide-metric-detail-action`、`wide-dual-domain`、`wide-four-action-hub`。

精确预算见主规范。骨架只约束区域关系，不是预制 JSON 模板。

## DSL 预算规则

- 间距只用 `2/4/6/8/10/12/14/16`；组间距不小于组内距。
- 内部板圆角8–12，主要支撑板12–16，胶囊半高圆角。
- 每个 Row/Column 两轴都必须闭合；Text/Button 行留至少4vp水平余量。
- `spaceBetween/spaceAround/spaceEvenly` 不与 `itemMargin` 同时使用。
- 新生成的短列表优先固定组件/索引，避免运行时项数破坏固定画布；合法动态 List 仅用于修复或已知严格上限场景。
- Stack 只用于背景、进度或必要叠加，不覆盖受保护文本和动作。

## 文本与图形

- 字号：10/12/14/16/18/20/32/40；每卡最多三档。
- 胶囊动作36高、18圆角、14/600；独立 icon 动作30，中心16–20。
- 常规 icon16–24；header20；hero 2x2为40–56、2x4为48–72。
- ring 56–72，stroke为直径14%–15%；线性进度1–2行高8、3行高4。
- Image 显式 width/height/objectFit。

## 阻断项

- root 不是 padding12，或尺寸/安全区与 CardSpec 不一致。
- 无法命名固定骨架，或区域/动作/背板超预算。
- 受保护文本裁剪，或两轴预算不成立。
- 自由 dashboard、多层卡片套卡片、任意按钮网格、装饰性空白填充。
