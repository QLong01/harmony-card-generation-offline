# 颜色系统

颜色权威来源是 [`design-compact-aligned-spec.md`](design-compact-aligned-spec.md)。

## 选择顺序

1. 默认语义浅色板。
2. 可靠单应用/单对象可用约10%的弱主题色加白色。
3. 天气、睡眠、运动、夜间、音乐等低密度场景可使用同族特殊渐变。
4. 夜间、睡眠、音乐、专注可使用暗色舞台。
5. 只有精确、安静且描述明确为背景的素材才能做背景。
6. 2x4 分栏最多一侧高识别。

## 约束

- 从 neutral、warm coral、sky blue、mint、purple、orange 中整组选择 canvas/surface/accent。
- 一张卡一个主色族，最多一个真实状态/动作色。
- 渐变恰好两个同族 stop，方向服务于布局。
- 禁止第三 stop、跨族、彩虹、径向、orb、bokeh、任意 alpha 派生。
- DSL 只写 `#RRGGBB` 或 `#AARRGGBB`，不写 token 名。

完整色值见 [`color-token-values.md`](color-token-values.md)。
