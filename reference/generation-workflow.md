# 新卡片生成流程

本流程将远程 Design Compact 规则映射为完整 Form JSONL + CardSpec。先完整读取 [`design/design-compact-aligned-spec.md`](design/design-compact-aligned-spec.md)。

## 1. 建立内部规划

```text
primaryObject: 单一服务对象
primaryQuestion: 1–2 秒内必须回答的问题
size: 2x2 | 2x4
mustKeep: 必要数据/素材/事件
shouldKeep: 空间允许才保留
drop: 重复、低价值或越界候选
skeleton: 一个固定骨架名
eventClass: explicit | implicit | sideEffect | none
surfaceStrategy: semanticLight | weakTheme | specialGradient | darkStage | backgroundAsset | wideSplit
palette: neutral | warmCoral | skyBlue | mint | purple | orange
```

用户指定尺寸时原样保留；未指定默认 2x2。用户视觉偏好只能在协议、骨架、可读性和受控色板范围内实现。

## 2. 选骨架

2x2 从以下五个中选一个：

- `compact-metric-action`
- `compact-event-action`
- `compact-date-next`
- `compact-dual-fact`
- `compact-dual-item-summary`

2x4 从以下六个中选一个：

- `wide-hero-context`
- `wide-timeseries-strip`
- `wide-agenda-stack`
- `wide-metric-detail-action`
- `wide-dual-domain`
- `wide-four-action-hub`

骨架仅约束关系和几何；不复制远程示例或历史 DSL 的文案、数据、组件树和素材组合。

## 3. 收敛事件

- 用户明确要求的打开/导航/拨号/清理/播放等标记为 `explicit`。
- 安全、无副作用、同对象详情入口可标记为 `implicit` 并绑定 root。
- 会改变状态或产生外部影响的动作标记为 `sideEffect`；没有明确授权就删除。
- 默认最多一个显式动作；只有骨架明确允许且用户确实需要时再增加。

## 4. 选数据与能力

1. 读 `capability/cardspec.md`。
2. 通过 `capability/data-capability/index.md` 选择最多 1–2 个 manifest。
3. 只取回答主问题的最小字段；UI 路径由 `writeResultTo + outputSchema` 推导。
4. 初始化值必须 schema-valid，且只是预览；辅助状态放 `/view` 或 `/state`。纯静态/纯事件卡也写最小 `state.ready`，不能输出空 DataModel。

## 5. 选表面与素材

- 从六个受控色族中整组选择 canvas/surface/accent；最多一个额外状态/动作色。
- 只在特殊低密度场景使用高识别渐变或暗色舞台。
- 读取 `design/asset-library.md`，选择完成识别/状态/动作所需的最少素材。
- 不用图片填空；PNG 不染色；SVG 根据直接背景与角色染色，描述要求保留原色时不染色。

## 6. 写完整 DSL

1. 三行顺序固定：createSurface、updateComponents、updateDataModel。
2. root 写 `matchParent`、padding12、radius18、clip 和背景。
3. 按骨架先锁主区域宽高/间距，再写内部组件。
4. 对每个 Row/Column 计算两轴和 4vp 安全余量。
5. 受保护文本按 1.2× 宽度压力测试；失败时删 shouldKeep 或换更简单骨架。
6. 动态值绑定 DataModel；点击只使用已声明事件能力。
7. 写 CardSpec，并确认尺寸、能力路径与 DSL 一致。

## 7. 交付门禁

- 一个主问题、一个焦点、一个主色族。
- 骨架名与实际结构一致，区域/动作/背板未超预算。
- root 和内部画布闭合；无依赖裁切的布局。
- 字体、按钮、图标、进度、间距、圆角、渐变都在受控范围。
- 素材语义匹配、路径存在、染色正确。
- 动态字段、事件、DataModel、capability 与 CardSpec 闭环；用户明确要求的显式动作未在降级中丢失。
- 最终只输出两个代码块，不输出内部规划。
