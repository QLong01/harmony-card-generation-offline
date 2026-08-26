# 点击事件能力

能力源：[`event_capabilities.json`](../../../scripts/rules/capabilities/app-11.7.5.205_rom-6.0/event_capabilities.json)，来源提交 `854956dc6364295ad0cfcb5f683b5f7b4d5bb494`，profile `app-11.7.5.205_rom-6.0`。

只使用下表声明的事件。DSL `onClick` 仍写单元素 EventHandler 数组；复制命中能力的 `actionTemplate.call/args`，只替换 `dynamicArguments` 指定路径，并让最终值满足 `parametersSchema`。

| 能力 ID | call | targetScene | 动态参数路径 | 依赖包 | 用途 |
| --- | --- | --- | --- | --- | --- |
| `event.call.phone` | `clickToApi` | `CallPhone` | /params/relationship, /params/phoneNumber | — | 点击跳转至指定号码的拨号界面，给某个亲人打电话 |
| `event.clean.memory` | `clickToApi` | `CleanRAMMemory` | — | — | 点击清理手机运行时内存，释放系统资源 |
| `event.open.settings.dnd` | `clickToDeeplink` | `Settings` | — | — | 打开系统设置中的情景模式，用户可以打开免打扰或专注模式 |
| `event.open.settings.bluetooth` | `clickToDeeplink` | `Settings` | — | — | 打开系统设置中的蓝牙设置页 |
| `event.open.settings.battery` | `clickToDeeplink` | `Settings` | — | — | 打开系统设置中的电池页 |
| `event.open.settings.batteryHealth` | `clickToDeeplink` | `Settings` | — | — | 打开系统设置中的电池健康页 |
| `event.open.settings.parentControl` | `clickToDeeplink` | `Settings` | — | — | 打开系统设置中的健康使用App页面，为了设置应用使用时长 |
| `event.open.settings.storage` | `clickToDeeplink` | `Settings` | — | — | 打开系统设置中的存储空间页 |
| `event.open.weather` | `clickToDeeplink` | `Weather_CityCode` | /uri | com.huawei.hmsapp.totemweather | 打开手机天气应用某城市页，uri为固定值勿更改。cityCode来自于数据能力中ViewWeather出参cityCode字段，进行动态拼接，表示跳转到指定城市天气页。 |
| `event.open.clock.alarm` | `clickToDeeplink` | `Clock` | — | — | 打开闹钟应用首页 |
| `event.open.music.daily` | `clickToDeeplink` | `Music` | — | — | 打开音乐app的每日30首歌单，uri为固定值勿更改 |
| `event.open.music.favorite` | `clickToDeeplink` | `Music` | — | — | 打开音乐app的收藏歌单/心动歌单，uri为固定值勿更改 |
| `event.open.health.sport` | `clickToDeeplink` | `Health` | — | com.huawei.hmos.health | 打开运动健康应用的锻炼Tab页 |
| `event.open.health.sleep` | `clickToDeeplink` | `Health` | — | com.huawei.hmos.health | 打开运动健康应用的睡眠详情页 |
| `event.enter.meeting` | `clickToDeeplink` | `EnterMeeting` | /uri | — | 点击一键加入下一个日程对应的Welink会议。uri取自数据能力GetCalendarEvents返回结果中event的oneClickServiceLink字段。注意：模板中events/i的i需替换为当前事件的实际索引，如events/0、events/1等。 |
| `event.viewCalendarEvent` | `clickToIntent` | `ViewCalendarEvent` | /params/entityId | — | 点击日程卡片 or 日程按钮，跳转到日程 App 查看该日程的详情 |
| `event.startNavigate` | `clickToIntent` | `StartNavigate` | /params/dstLocation/location | — | 点击导航按钮，跳转到地图应用进行导航。大模型需根据用户说的目的地选择location的值，只支持回家和去公司的导航 |
| `event.setPowerSavingMode` | `clickToIntent` | `SetSettingSwitch` | /params/switchFlag | — | 点击一键开启/关闭省电模式。大模型根据用户表达确定是开启还是关闭，然后传对应的switchFlag值 |

## 约束

- 未命中能力时删除点击与动作外观，不编造 call、intentName、URI、bundleName 或 params。
- `actionTemplate` 中未列为动态参数的常量不得改写；动态表达式必须能从 DataModel 推导。
- 依赖包不可用时不得选择该事件；同一交互只绑定一个 onClick。
- 完整 actionTemplate、dynamicArguments 和 parametersSchema 以原始 manifest 为准。
