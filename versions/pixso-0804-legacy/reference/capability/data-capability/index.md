# 数据能力索引

能力源：[`data_capabilities.json`](../../../scripts/rules/capabilities/app-11.7.5.205_rom-6.0/data_capabilities.json)，来源提交 `854956dc6364295ad0cfcb5f683b5f7b4d5bb494`，profile `app-11.7.5.205_rom-6.0`。

先按 query 命中最多 1–2 个必要能力，再读取对应文件。清单外能力不得编造；静态卡片不写 `dataBindings`。

| 用户意图 | 读取文件 | 能力 ID | 推荐 `writeResultTo` |
| --- | --- | --- | --- |
| 天气、空气质量、温湿度、未来预报与天气提醒 | [`weather.md`](weather.md) | `ViewWeather` | `/data/weather` |
| 今日/未来日程、会议、日历提醒与赛事日程 | [`calendar.md`](calendar.md) | `GetCalendarEvents` | `/data/calendar` |
| 指定日期倒数日、纪念日、节日、考试或截止日期 | [`countdown-days.md`](countdown-days.md) | `GetCountdownDays` | `/data/countdown` |
| 指定应用今日使用时长 | [`app-usage.md`](app-usage.md) | `GetAppUsageDuration` | `/data/appUsageStats` |
| 蓝牙耳机连接、电量与左右耳/耳机盒状态 | [`blutoothearphone-status.md`](blutoothearphone-status.md) | `GetEarphoneInfo` | `/data/earphone` |
| 手机电量、充电状态、电池健康、温度、电流与电压 | [`phone-battery.md`](phone-battery.md) | `GetPhoneBatteryInfo` | `/data/phoneBattery` |
| 睡眠、步数、热量、距离、最近运动与心率 | [`healthy-sport.md`](healthy-sport.md) | `GetHealthAndSportSummary` | `/data/healthSport` |

## 共通约束

- CardSpec `arguments` 必须满足原始 `inputSchema`；UI/DataModel 必须满足 `outputSchema`。
- 多个 `writeResultTo` 不得相同、互为父子或彼此覆盖。
- 依赖包不可用时不得假装能力可执行；改用静态降级或说明能力边界。
- 事件参数引用数据时，该字段必须存在于命中 data capability 的 `outputSchema`。
