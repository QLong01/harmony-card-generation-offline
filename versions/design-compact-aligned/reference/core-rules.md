# 核心规则

本文是默认必读的单页质量门。非协议生成裁决只来自 [`design/design-compact-aligned-spec.md`](design/design-compact-aligned-spec.md)。

## P0 阻断

以下任一失败都不要输出：

- 输出不是两个代码块：三行 `genui` JSONL + 一个 `cardspec` JSON。
- 三行 `surfaceId` 不一致，root 引用不存在，root 未写 `width/height: "matchParent"`、`padding: 12`、`borderRadius: 18`、`clip: true` 或明确背景。
- CardSpec 尺寸与 DSL 不一致；用户指定尺寸被擅自改动。协议只允许 `2x2` 与 `2x4`。
- 使用禁用组件、网络图、内联/base64 SVG、emoji、占位媒体、未声明素材或未声明事件。
- 表达式路径不能从 DataModel、`writeResultTo + outputSchema` 或列表当前项推导；能力写入子树不符合 schema。
- 不是一个服务对象/主问题，出现多个主焦点、多个主色族或重复事实。
- 无法明确落入一个固定骨架，或区域/动作/背板数量超出所选尺寸预算。
- Row/Column 任一轴预算不成立，依赖 clip 隐藏溢出，或受保护文本不能完整显示。
- 动态值被写成静态真实状态；副作用动作没有用户明确要求；同一动作重复绑定。

## 协议不变量

- `version: "v0.9"`，`catalogId: "ohos.a2ui.extended.catalog.form"`。
- 只使用 `Text`、`Image`、`Divider`、`Progress`、`Button`、`Checkbox`、`Row`、`Column`、`List`、`Stack`。
- 禁用 `TextInput`、`Toggle`、`Radio`、`CheckboxGroup`、`Select`、`NavContainer`、`Tabs`、`TabContent`、`Web`、`Grid`、`If`、`theme`、`Button.action`、非 `onClick` 事件及未注册上下文变量。
- `children` 只引用组件 ID；List 循环必须使用合法 `{componentId,path}` 结构。新生成的短固定列表优先固定组件/索引，以锁定预算。
- 点击只写 DSL `onClick`；每个 carrier 一个 handler。CardSpec 不写点击。
- Image 只用用户提供或素材库声明路径，显式 `width/height/objectFit`。

## 任务与信息预算

- 写前对数据、素材、事件执行 `mustKeep / shouldKeep / drop`。
- 2x2：一个主信息，最多两个支撑事实；最多 3 个主区域、1 个显式动作、1 个内部背板。
- 2x4：一个主结构，最多四类支撑；最多 4 个主区域，默认最多 2 个动作，最多 1 个主背板 + 1 个弱背板。
- 每个事实只由一个组件主承载；单位换算、别名、父子包含、比例/差值只有提供新判断时才保留。
- 信息不足时增加留白或提高主信息权重，不添加空标签、装饰素材或同义事实。

## 几何与文字

- 2x2 画布 `160×160`，内部安全区 `136×136`；2x4 画布 `320×160`，内部安全区 `296×136`。
- 间距只用 `2/4/6/8/10/12/14/16`，优先 `4/8/12/16`；组间距不小于组内距。
- 字号只用 `10/12/14/16/18/20/32/40`，每张最多三档。
- 受保护文本：显式标题、状态、日期/时间、主指标、价格、数量、联系人、CTA、完整格式化值。不得 ellipsis/clip。
- 每个 Row/Column 同时核算两轴。`spaceBetween/spaceAround/spaceEvenly` 不与 `itemMargin` 并用；Text/Button 行至少留 `4vp` 水平余量。
- 胶囊动作高36、圆角18、文字14/600；独立 icon 动作30；点击目标至少24。
- ring 56–72，stroke 为直径14%–15%；线性进度 1–2 行高8、3行高4，且必须有可靠范围/总量。

## 色彩与素材

- 从 neutral、warm coral、sky blue、mint、purple、orange 选一个完整色族；最多再用一个真实状态/动作色。
- 渐变恰好两个同色族 stop；禁止第三 stop、跨族、彩虹、径向、orb、bokeh。
- 素材只承担对象识别、状态、动作、主媒体或精确背景职责；不用于填空。
- SVG 默认可染色，保留原色/多色/品牌/透明素材除外；PNG 禁止 `fillColor`。

## 数据与事件

- 只有用户明确给出的文案、称呼、地点或目标才能作为静态事实；不得凭常识补写联系人、号码、日程、位置、健康/设备/账户状态。动态状态未返回时使用中性标签或删除状态图标，不写静态结论。
- 示例值只是预览；动态可见值必须绑定能力输出。纯静态/纯事件卡也要初始化最小 `/state/ready`，`updateDataModel.value` 不得为空。
- `updateDataModel.value` 初始化所有 UI 路径。能力写入子树只包含 outputSchema 合法投影；加载态/选择态放 `/view` 或 `/state`。
- 默认最多一个显式事件；第二个需用户明确要求且骨架允许；3–4 个只允许 `wide-four-action-hub`。
- 无事件能力时删除点击外观；安全的同对象详情可绑 root，不能再加重复按钮。

## 降级顺序

删除 `drop` → 删除装饰性素材 → 删除普通 `shouldKeep` → 删除隐式入口 → 同尺寸切换更简单骨架 → neutral 色板 → 说明能力边界。用户明确要求的显式动作不得删除。

生成后先做内部自检；只有用户要求校验文件、修复本地草稿或调试时才运行 `scripts/validate_card.py`。
