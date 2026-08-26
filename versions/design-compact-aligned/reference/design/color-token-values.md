# Design Compact 色值速查

最终 DSL 写 hex，不写角色名。

| 色族/角色 | canvas 2-stop | surface | accent |
| --- | --- | --- | --- |
| neutral | `#FFF5F7F9 → #FFFFFFFF` | `#FFFFFFFF` / `#FFF1F3F5` | 语义强调色或深灰 |
| warm coral | `#FFFFE9DE → #FFFFFCF8` | `#FFFFF5EF` | `#FFE56A3A` |
| sky blue | `#FFDCEEFF → #FFF4FAFF` | `#FFEAF4FF` | `#FF1769E0` |
| mint | `#FFE2F6EE → #FFF8FCFA` | `#FFE1F4ED` | `#FF0F8F78` |
| purple | `#FFF2E8FF → #FFFCF9FF` | `#FFF5EEFF` | `#FF8A4DCC` |
| orange | `#FFFFEDD6 → #FFFFFAF2` | `#FFFFF3E5` | `#FFED6F21` |

| 基础/特殊角色 | DSL hex |
| --- | --- |
| 浅色主文字 | `#E5000000` |
| 浅色次文字 | `#99000000` |
| 浅色弱文字 | `#66000000` |
| 高饱和主文字 | `#FFFFFFFF` |
| 高饱和次文字 | `#99FFFFFF` |
| 暗色弱材料 | `#19000000` / `#0C000000` |
| 浅色弱材料 | `#33FFFFFF` / `#19FFFFFF` |
| 晴空蓝渐变 | `#FF0A59F7 → #FF46B1E3` |
| 紫色舞台渐变 | `#FFAC49F5 → #FFC386F0` |
| 正常状态绿 | `#FF64BB5C` |
| 橙色动作 | `#FFF9A01E` |
| 雨天补充 | `#FF46484D` / `#FF467794` |

所有渐变必须正好两个 stop 且同色族。
