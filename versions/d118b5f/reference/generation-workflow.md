# 新卡片生成流程（Pixso 0804）

本流程生成协议合法且视觉严格符合 Pixso 0804 的 2×2 Form 卡片。先读 [`design/pixso-0804-spec.md`](design/pixso-0804-spec.md)；不要使用旧版 composition pattern、surface strategy、scene vector、比例带、场景拓展色或自由表面技法。

## 1. 收敛需求

先写内部规划，不输出：

```text
primaryQuestion: 卡片在 1–2 秒内必须回答的问题
mustKeep: 没有就无法回答的问题字段
optional: 空间允许才保留的描述/辅助字段
action: 是否有已声明且必要的 onClick
sourceApp: 单一应用 | 多来源 | 未知
pixsoScene: focus | schedule | antiAddiction | earphone | lowPower | cleanup | sunnyCare | rainyTaxi | eventCountdown | sleep | app | general
contentAtom: regularText | largeNumber | radioList | ring | progress | image
contentLayout: singleText | singleImage | imageText | imageTwoTexts | twoTexts
```

- 只保留一个 `primaryQuestion`。
- `mustKeep` 中的 CTA、主值、关键时间/状态必须完整显示；标题、正文和辅助信息按 Pixso 最大行数省略。`optional` 不得挤压标题、主值、按钮或必要状态。
- 相同事实只保留一个主承载组件；单位换算、同义标签、差值/比例只有提供新判断时才保留。
- 动作能力不明时删除点击和按钮，不生成假 CTA。

## 2. 锁定尺寸

- Pixso 0804 的视觉规范只覆盖 `2x2 = 160vp × 160vp`，新生成默认并优先使用 2×2。
- 用户未指定尺寸时只生成 2×2。
- 用户明确要 2×4 时，不外推 2×2 视觉：说明当前 Pixso 缺少 2×4 规范，并询问是否收敛为 2×2；只有修复既有 2×4 协议时才继续处理协议问题，不能声称视觉合规。

## 3. 选择 Pixso 背景分支

严格按 [`design/pixso-0804-spec.md`](design/pixso-0804-spec.md) 的背景映射选择：

- 精确命中专注、日程、防沉迷、耳机、低电、清理时用对应浅色分支。
- 精确命中晴天关怀、雨天打车、赛事倒计时、睡眠监督时用对应特殊渐变。
- 明确来自一个原生/第三方应用时用应用主色10%叠层，保留应用 icon 原色。
- 其他需求统一用通用背景；不要做“相似场景配色”推断。

## 4. 建立三段骨架

1. root：`padding: 8`，白底/指定渐变，协议圆角和 clip。
2. 标题区必选：12fp；满足单一应用来源条件时才放右上 20vp icon。
3. 内容区可选：与标题至少 8vp，选择一个 Pixso 内容布局和一个主要原子。
4. 按钮区可选：与内容至少 8vp，贴底；胶囊 36vp 或纯 icon 30vp。

不要同时选择多个主要原子，不生成第二主任务、dashboard、按钮网格或卡片套卡片。

## 5. 选择内容原子

- 常规标题/正文/辅助文字：按 14→12fp 和最大行数规则。
- 核心单数值：38fp，宽度不足降 30fp；双数值固定 30fp；单位12fp。
- 单选列表视觉：用协议允许的圆形 Checkbox 复现，选项背板间隔4vp。
- 占比：ring 默认52、最小44、粗6；中心 icon24或数字16→14→12。
- 进度：1–2条粗8、间隔8；3条粗4、间隔4。
- 图片：按有/无按钮的 Pixso 图文分支放置；2:1 宽图切换上下布局。

## 6. 绑定与能力

需要动态数据时：

1. 读 `capability/cardspec.md`。
2. 读 `capability/data-capability/index.md`，只加载命中的 1–2 个 manifest。
3. `capabilityId`、`arguments`、`writeResultTo`、DataModel 类型和 UI 路径必须由 manifest 推导。
4. UI 字段必须属于 `mustKeep` 或入选的 `optional`；不为填满画面引入额外能力字段。

## 7. 写 DSL

- 三行 JSONL 顺序固定：`createSurface`、`updateComponents`、`updateDataModel`。
- 组件字段只用 `protocol/component-catalog.md`；绑定只用 `protocol/data-binding.md`。
- 先写 root/背景，再写标题、内容、按钮；每个固定元素写可静态推导的宽高和间距。
- DSL 颜色写 hex；颜色表见 `design/color-token-values.md`。
- Image 只用素材库声明路径，显式 `width/height/objectFit`；品牌/应用 icon 不染色。

## 8. 交付门禁

- 视觉来源：每个布局、字号、间距、图表、背景、前景、按钮和 icon 决策都能在 Pixso 0804 文件中定位。
- 尺寸：新生成是 2×2，root padding8；不存在未经授权的 2×4 外推。
- 标题/内容/按钮：分支正确，两个 8vp 间隔成立，按钮贴底。
- 原子：字号、最大行数、ring/进度尺寸精确；无旧版18/32/40fp或自由环尺寸。
- 色彩：只用一个明确背景分支；无拓展色、第三 stop 或手调 alpha。
- 协议：三行消息、root、组件字段、绑定、事件和 CardSpec 全部闭环。

任一项失败就删减 optional、回退通用背景或说明能力边界；不得新增 Pixso 未定义的视觉方案。
