# 参考文档路由

本项目按三层裁决：

1. `reference/protocol/`：完整 Form JSONL 组件、绑定与事件结构。
2. `reference/capability/`：CardSpec、数据能力和事件能力。
3. `reference/design/design-compact-aligned-spec.md`：任务选择、固定骨架、布局、视觉、素材和动作预算。

远程 Prompt 的极简协议、TaskSpec 和 few-shot 不进入输出；它们的非协议规则已映射到本项目文档。

## 常用入口

- `core-rules.md`：默认必读质量门。
- `generation-workflow.md`：自然语言到完整 Form DSL 的固定生成顺序。
- `design/design-compact-aligned-spec.md`：唯一非协议生成规范。
- `design/layout-system.md`：固定骨架到完整 Form DSL 的映射摘要。
- `design/color-token-system.md` / `color-token-values.md`：受控色族与 hex。
- `design/asset-library.md`：本地素材路径与职责。
- `protocol/component-catalog.md`：组件字段。
- `protocol/data-binding.md`：表达式与路径绑定。
- `capability/cardspec.md`：CardSpec 契约。
- `capability/data-capability/index.md`：按场景加载 capability manifest。

## 读取策略

- 新生成：core → workflow → aligned spec → 必要协议/能力/素材文档。
- 修复/评审：core → 与失败直接相关的协议、能力或设计文档。
- 不预加载全部 manifest，不复制历史样例作为模板。

2x2 与 2x4 都允许新生成。用户指定尺寸时保持一致；未指定默认 2x2，并从该尺寸的固定骨架中选一个。
