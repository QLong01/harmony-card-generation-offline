# Version snapshots

本目录保存两个可独立安装的 Skill 版本。它们分别保留历史提交的视觉/生成基线，同时共同同步 CreateMyCard `app-11.7.5.205_rom-6.0` 的数据、事件和素材能力。

| 目录 | 视觉/生成基线 | 日期 | 说明 |
| --- | --- | --- | --- |
| [`pixso-0804-legacy/`](pixso-0804-legacy/) | `d118b5f` | 2026-08-25 | 初始 offline skill，采用原 Pixso 0804 / 2x2 规则 |
| [`design-compact-aligned/`](design-compact-aligned/) | `0a9f8d2` | 2026-08-26 | 对齐远程 Design Compact Prompt 的 2x2/2x4 版本 |

仓库根目录只作为版本索引，不再保存重复的当前副本。使用时直接选择对应目录中的 `SKILL.md` 及其同级文件。

## 共同能力基线

- Profile：`app-11.7.5.205_rom-6.0`
- 能力来源提交：`854956dc6364295ad0cfcb5f683b5f7b4d5bb494`
- 同步内容：7 个 data、18 个 event、72 个 asset capability
- 该提交是同步时远程 `dev` 的头；三份本地 manifest 与远程对应文件的 Git blob 完全一致。
