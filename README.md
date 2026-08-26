# Harmony Card Generation Offline — Version Archive

本仓库只保存 `harmony-card-generation-offline` Skill 的两个固定版本。仓库根目录是版本索引，不再维护一份重复的 Skill 副本。

| 版本目录 | 视觉/生成基线 | 说明 | 入口 |
| --- | --- | --- | --- |
| `pixso-0804-legacy` | `d118b5f` | 初始 offline 版本，采用原 Pixso 0804 / 2x2 规则 | [`versions/pixso-0804-legacy/SKILL.md`](versions/pixso-0804-legacy/SKILL.md) |
| `design-compact-aligned` | `0a9f8d2` | 对齐远程 Design Compact Prompt，支持 2x2/2x4 | [`versions/design-compact-aligned/SKILL.md`](versions/design-compact-aligned/SKILL.md) |

每个版本目录保留对应提交的视觉与生成逻辑，并共同同步 `app-11.7.5.205_rom-6.0` 能力包（来源提交 `854956d`）：7 个数据能力、18 个事件能力、72 个素材能力。需要使用哪个版本，就复制或安装对应的整个目录。

更多信息见 [`versions/README.md`](versions/README.md)。
