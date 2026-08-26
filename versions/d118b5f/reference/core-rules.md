# 核心规则

本文是默认必读的单页质量门。先看 P0 阻断项，再按 L0 协议、L1 数值布局、L2 内容视觉展开检查。视觉裁决只来自 `design/pixso-0804-spec.md`。

## 单文件兜底

- `support.*` 是支撑组；`metric/tile/status/badge` 是并列小事实角色，不按支撑条数折算。
- `不可截断文本`：CTA、主指标、倒计时、关键时间/日期、关键状态、价格/数量和必须识别的用户字段，必须完整显示。标题、正文和辅助信息按 Pixso 规定的最大行数与省略号处理。

## P0 先决阻断

以下任一组失败都不要输出：

- 输出契约：必须是两个代码块，`genui` 为三行 JSONL，`cardspec` 为 JSON；`version`、`catalogId`、CardSpec 尺寸、root `matchParent` 写法、实际布局预算和 root 圆角一致。root `styles.width/height` 必须写 `"matchParent"`；`createSurface.width/height` 默认省略，若声明只能写 `"matchParent"`。
- Surface/root：`createSurface` 只声明 `surfaceId`、`catalogId`，默认不写 `width/height/styles`；宿主明确要求外层形状/裁切时才写 `createSurface.styles`，且仅限 `borderRadius`、`clip`；`updateComponents.root` 引用已存在组件；root 承载 `width`、`height`、`padding`、`borderRadius`、`clip` 和至少一种明确的表面背景（优先 `backgroundColor` 或 `linearGradient`，也可由 root 下的真实背景组件承载），否则可能渲染默认白底。
- 消息闭环：三行 JSONL 的 `surfaceId` 必须一致；新卡片默认 `updateDataModel.path: "/"`，`value` 初始化所有 UI 表达式引用的根结构和必要状态。动态数据能力路径允许使用示例初始值，但该子树必须是对应 `outputSchema` 的合法投影。
- 协议范围：只使用 Form 允许组件；`children` 只引用组件 id；列表循环必须有 `{ "componentId": "...", "path": "..." }`，可选 `itemVar/indexVar`；不用禁用组件、网络图、内联/base64 SVG data URI、emoji、未声明资源或未声明事件能力。
- 绑定/DataModel：动态展示值、样式动态值和事件参数使用静态值、完整 `{{ ... }}` Expression、合法 PathBinding 或宿主明确注册的 FunctionCall；所有可见表达式引用都能在 `updateDataModel.value`、`writeResultTo + outputSchema` 或列表循环当前项中推导；数据能力运行时字段至少初始化到可推导根结构。若在 `writeResultTo` 对应动态子树中写入示例初始值，每个字段、层级、类型、枚举、范围和数组项结构都必须符合对应 `outputSchema`，不得在该子树中添加展示辅助字段。`updateDataModel.path`、`writeResultTo`、列表循环 `children.path` 仍是协议结构 JSON Pointer。
- 布局可渲染：Row/Column 宽高预算成立且包含子项 `margin`；关键父容器和关键子项不依赖默认伸缩；Row 内 `Text + Button` 并排时，父 Row、Text、Button 都有明确宽高预算。
- Pixso 闭环：新生成只做 2×2；root `padding: 8`，标题/内容/按钮、字体、间距、图表、背景和 icon 都能在 `design/pixso-0804-spec.md` 中找到对应分支。出现未定义视觉或把 2×2 外推成 2×4 时阻断。

## L0 协议

- `genui` 必须是三行 JSONL：`createSurface`、`updateComponents`、`updateDataModel`。
- 使用 `version: "v0.9"` 和 `catalogId: "ohos.a2ui.extended.catalog.form"`。
- CardSpec 必须包含静态短 `title`、静态短 `description` 和 `suggestSize`；`title/description` 不写表达式、绑定或 DataModel 路径。
- 协议尺寸只允许 `2x2` 或 `2x4`，且 CardSpec 与 DSL 一致。逻辑画布和协议校验预算固定为：
  - `2x2`: 实际预算 `160vp x 160vp`、root `borderRadius: 18`、`clip: true`。
  - `2x4`: 实际预算 `320vp x 160vp`、root `borderRadius: 18`、`clip: true`。
- Pixso 0804 只定义 2×2 视觉；2×4 只用于协议修复/解释，不得用于新生成并声称 Pixso 合规。
- `updateComponents.root` 必须引用一个已存在组件；root 组件是卡片 shell 和组件树入口。
- root 组件必须写 `width`、`height`、`padding`、`borderRadius`、`clip` 和表面样式；root `width/height` 写 `"matchParent"`，`borderRadius` 无论 `2x2` 还是 `2x4` 都固定为 `18`，实际内部预算按目标尺寸计算。该固定值不限制内部组件圆角。`createSurface` 默认省略 `width/height/styles`；只有宿主明确要求外层形状/裁切时才写 `createSurface.styles` 作为可选辅助；`backgroundColor`、`linearGradient`、`backgroundImage` 等背景字段必须写在 `root.styles` 或 root 下的真实背景组件，不写进 `createSurface.styles`，因为 root 默认不透明白底会遮挡 surface 层背景。
- 只使用 `Text`、`Image`、`Divider`、`Progress`、`Button`、`Checkbox`、`Row`、`Column`、`List`、`Stack`。
- 禁用 `TextInput`、`Toggle`、`Radio`、`CheckboxGroup`、`Select`、`NavContainer`、`Tabs`、`TabContent`、`Web`、`Grid`、`If`、`theme`、`Button.action`、非 `onClick` 事件、预定义扩展函数、`$__widthBreakpoint`、`$__colorMode`、`$context`。
- `children` 只能是组件 ID 数组；列表循环只允许 `{ "componentId": "...", "path": "..." }` 加可选 `itemVar/indexVar`。
- 动态值优先用完整 `{{ ... }}` 表达式；简单直取可用 `{"path":"/..."}` PathBinding，宿主明确注册时才用 FunctionCall；复杂格式化可先写入 `updateDataModel` 预计算字段，再用表达式读取。
- 点击只写 DSL `onClick`，且 `call` 必须来自已声明 event capability；CardSpec 不写点击行为。
- 每个 `onClick` 只写 1 个 handler；不写 `condition/as/$context`。
- `Image.src` / `backgroundImage` 只使用用户提供或素材库声明的本地/资源路径；资源路径 SVG 受支持；禁用网络 URL、内联/base64 SVG data URI、emoji 和占位图。

## L1 数值布局

- 新生成 2×2 的安全区固定为 root `padding: 8`，内容区 `144vp x 144vp`。不得保留旧版 `padding: 12`。
- 所有组件必须使用数值宽高或可静态推导的约束，不能把内部布局改成默认伸缩或填满父容器。
- 新生成默认 2×2。用户要求新生成 2×4 时说明 Pixso 0804 没有相应几何或收敛成 2×2；不得自由升级。
- 使用必选标题区、可选内容区、可选按钮区；内容距标题和按钮都至少 8vp。
- 间距只用 `0/2/4/8/12/16`；结构优先 `4/8`。
- 字号只用 `10/12/14/16/20/30/38`；标题区12，CTA14，核心单数值38（不足降30），双数值30。
- 文本估算：中文约 `fontSize`，英文/数字约 `0.6 * fontSize`，垂直高度按 `fontSize + 2-4` 预留。
- CTA、主指标、倒计时、关键时间/日期、关键状态、价格/数量和必须识别的用户字段不得截断；标题、正文、辅助信息必须显式使用 Pixso 对应原子的最大行数，允许 `ellipsis`，不用 `clip` 掩盖溢出。
- 每个 Row/Column 必须预算成立：子项宽高 + 子项 margin + 父容器 padding + itemMargin 不得超过父容器。
- Row/Column 不得依赖默认伸缩完成关键布局；父容器、按钮、图标、进度图形和受保护文本必须能推导出明确宽高。
- Row 内 `Text + Button` 并排时，父 Row 必须有明确 `width`/`height`，Button 必须显式 `width`/`height`，Text 必须显式 `width` 或有明确剩余宽度。
- 并排布局自检公式：`sum(子项 width + 子项左右 margin) + itemMargin * 间隔数 + 父容器左右 padding <= 父容器 width`；纵向同理检查 `height + 上下 margin + 上下 padding`。
- 可点击按钮视觉只用 Pixso 两档：胶囊高36vp，或纯 icon 背景30×30vp；CTA 宽度包含文字估算和左右8vp内容 padding。
- 按钮区贴卡片底部；胶囊按钮距卡片左右边至少12vp，按钮区与内容区至少8vp。
- 紧凑 Row 中 `Button` 与小号文本并排时，不要只依赖 `alignItems: "center"`；优先用按钮槽位、明确高度或非对称 padding 校正。若 Button 高度已等于父 Row 高度，不要再加 `margin.top/bottom`。
- Stack 只用于背景、进度或明确叠加；不得覆盖受保护文本、CTA 或主数值。

## L2 内容与视觉

- 先确定一个服务对象或主问题；`2x2` 默认展示不超过 4 个可见字段，按 `object`、`primary`、`support`、`metric/tile/status/badge`、`action`、`asset` 角色取舍。`metric/tile/status/badge` 是结构化并列角色，不按 `support.*` 条数折算；未入选字段留给详情页。
- 可见组件的信息职责必须互斥：对象、状态、设定值、实际值、差值、比例/进度、趋势、时间点/段、位置、金额、数量、动作入口等，每个事实只由一个组件主承载。
- 写前把文案和数值归入“事实等价类”：单位换算、别名/简称、同义标签、短标签扩写、父子包含、聚合/拆分、差值/比例/状态等，只要回答同一事实或判断，就算重复。
- 派生事实只有承担新判断时才展示；进度条只作可视化承载，旁边文案不要复述两端值，除非该值是唯一主事实。
- 信息不足时调整比例、层级和留白，不加空标签、同义指标或装饰填空。
- 背景只能从 Pixso 的浅色场景、四个特殊全幅渐变、应用背景或通用背景中选一个；找不到精确场景时回到通用背景。
- 禁止场景拓展色、第三个渐变 stop、径向渐变、手调 alpha、orb、bokeh 或把相近场景拼色。
- 浅色前景固定黑90/60/40/10层级；特殊全幅渐变用白/白60；按钮和 icon 严格按同一 Pixso 分支配对。

## 人工阻断补充

以下项通常需要输出前复核；任一失败都先收敛内容、删除弱信息或回退到更简单布局，不交付：

- 生成时照搬 skill 包外历史样例、示例文案、示例 DataModel 或示例素材组合。
- 用同义标签、单位换算、父子包含、派生比例/差值填充空间，导致多个组件重复回答同一事实。
- 没有单一服务对象或主问题，出现多个互相竞争的主显示组、多个主色族、多个主动作，或动作抢走主信息焦点。
- 动作能力不明却保留可点击视觉；应删除 `onClick` 并把动作区降级为非误导支撑信息。
- 颜色无法定位到 `design/pixso-0804-spec.md` 的明确分支，或 DSL 输出 token 名而不是 hex。
- 状态色服务装饰而非真实状态；出现 Pixso 未列出的渐变、拓展色或 alpha。
- 用阴影、额外背板、装饰图形、自由比例或卡片套卡片填充空白。
- 文本、按钮、背板虽然通过宽高估算，但视觉上贴顶、悬浮、基线不齐或靠近圆角裁剪风险区。
- 修复已有 DSL 时仍保留未注册 FunctionCall、已裁剪组件字段，或没有把无法确认的函数绑定改写为完整表达式/预计算字段。

## 生成后校验

先做输出前自检，不要为了校验新建、输出或保留草稿文件。先查协议、绑定、布局、颜色、事件和尺寸，再查信息职责、事实等价类、派生判断和组件删除后的引用完整性。仅在用户要求校验既有文件、修复本地草稿或调试脚本时运行 `scripts/validate_card.py`。
