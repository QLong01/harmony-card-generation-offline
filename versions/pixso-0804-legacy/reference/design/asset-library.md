# 素材能力索引

能力源：[`asset_capabilities.json`](../../scripts/rules/capabilities/app-11.7.5.205_rom-6.0/asset_capabilities.json)，来源提交 `854956dc6364295ad0cfcb5f683b5f7b4d5bb494`，profile `app-11.7.5.205_rom-6.0`。

## 选择规则

- 只使用下表/原始 manifest 中存在的 `id` 与 `src`，不得猜测文件名或替换目录。
- 按 description、sceneTags 和实际内容职责选择最少必要素材；没有语义职责时不为填空使用素材。
- 数量、尺寸、布局、染色和背景策略服从当前版本的视觉规范 `pixso-0804-spec.md`。
- SVG 只有在描述与素材结构允许时染色；PNG、品牌、多色、渐变或要求保留原色的素材不染色。
- `Image` 必须显式声明 width、height、objectFit；依赖版本不满足 `minXiaoyiVersion` 时不得使用。

## 素材清单

| 能力 ID | src | sceneTags | description | 最低小艺版本 |
| --- | --- | --- | --- | --- |
| `asset.air_fill` | `resources/base/media/air_fill.svg` | air, home | 样式：默认黑色的单色实心空调室内机图标，正面矩形机身，顶部有三个圆点，底部为横向出风口；适用：空调设备、空调关闭或普通状态、智能家居空气设备。 | `1.0.0` |
| `asset.air_open_fill` | `resources/base/media/air_open_fill.svg` | air, home | 样式：默认黑色的单色实心空调室内机图标，正面矩形机身，底部有三条向下气流线；适用：空调开启、送风、新风或空气循环运行状态。 | `1.0.0` |
| `asset.airplane_departure` | `resources/base/media/airplane_departure.svg` | travel, flight | 样式：飞机起飞图标，默认黑色，图形为飞机从跑道起飞的侧视图；适用：出行计划、航班出发信息、旅行日程。 | `1.0.0` |
| `asset.airplane_fill_1` | `resources/base/media/airplane_fill_1.svg` | travel, flight | 样式：默认黑色的单色实心飞机俯视图，机头朝右上方倾斜；适用：航空旅行、航班概览、飞行状态。 | `1.0.0` |
| `asset.alarm_fill_1` | `resources/base/media/alarm_fill_1.svg` | alarm, reminder | 样式：闹钟实心图标，黑白双色，图形为带铃铛的圆形表盘，建议保留原色；适用：闹钟设置、定时提醒、日程提醒。 | `1.0.0` |
| `asset.backward_fill` | `resources/base/media/backward_fill.svg` | media, control | 样式：快退/后退实心图标，默认黑色，图形为两个向左的三角箭头；适用：音乐播放器快退控制、视频回退。 | `1.0.0` |
| `asset.battery_leaf_fill` | `resources/base/media/battery_leaf_fill.svg` | battery, power | 样式：默认黑色的单色实心横向电池图标，电池内部为叶片留白；适用：省电模式、节能电池、绿色用电状态。 | `1.0.0` |
| `asset.bell_fill` | `resources/base/media/bell_fill.svg` | notification, alarm | 样式：铃铛实心图标，默认黑色，图形为经典吊铃造型；适用：通知提醒、消息提示、闹铃开启状态。 | `1.0.0` |
| `asset.bell_slash_fill` | `resources/base/media/bell_slash_fill.svg` | notification, silent | 样式：铃铛加斜杠实心图标，黑白双色，图形为铃铛上叠加删除线，建议保留原色；适用：静音模式、关闭通知、勿扰设置。 | `1.0.0` |
| `asset.bolt_fill` | `resources/base/media/bolt_fill.svg` | battery, power | 样式：默认黑色的单色实心竖向闪电图标；适用：正在充电、快充、电能或闪电状态。 | `1.0.0` |
| `asset.bus_fill` | `resources/base/media/bus_fill.svg` | traffic, bus | 样式：公交车实心图标，默认黑色，图形为正面视角公共汽车轮廓；适用：公共交通出行、路线导航、公交到站提醒。 | `1.0.0` |
| `asset.calendar_fill` | `resources/base/media/calendar_fill.svg` | calendar, schedule | 样式：日历实心图标，默认黑色，图形为带格线的日历本造型；适用：日程管理、日历事件查看、当日安排。 | `1.0.0` |
| `asset.checkmark_calendar_fill` | `resources/base/media/checkmark_calendar_fill.svg` | calendar, task | 样式：带对勾的日历实心图标，黑白双色，图形为日历上叠加对勾，建议保留原色；适用：已完成日程、日程确认、任务打卡。 | `1.0.0` |
| `asset.clean_fill` | `resources/base/media/clean_fill.svg` | clean, maintenance | 样式：默认黑色的单色实心扫帚图标，竖向手柄，下方为三束刷毛；适用：清扫、垃圾清理、系统清理或家居清洁动作。 | `1.0.0` |
| `asset.clock` | `resources/base/media/clock.svg` | time, clock | 样式：时钟线框图标，默认黑色，图形为圆形表盘加指针的线性轮廓；适用：时间显示、定时功能、倒计时。 | `1.0.0` |
| `asset.clock_fill` | `resources/base/media/clock_fill.svg` | time, clock | 样式：时钟实心图标，黑白双色，图形为圆形实心表盘加白色指针，建议保留原色；适用：时间显示、闹钟设置、定时器。 | `1.0.0` |
| `asset.cold` | `resources/base/media/cold.svg` | health, protection | 样式：默认黑色的单色线框圆形人脸，口鼻处佩戴口罩；适用：佩戴口罩、防护、呼吸道健康或传染风险提示。 | `1.0.0` |
| `asset.drop_1` | `resources/base/media/drop_1.svg` | weather, water | 样式：水滴图标，默认黑色，图形为圆润水滴轮廓；适用：湿度数据展示、饮水提醒、天气降雨信息。 | `1.0.0` |
| `asset.earphone_case_16644` | `resources/base/media/earphone_case_16644.svg` | device, audio | 样式：耳机收纳盒实心图标，默认黑色，图形为无线耳机充电盒造型；适用：蓝牙耳机设备连接、音频设备管理。 | `1.0.0` |
| `asset.externaldrive_fill` | `resources/base/media/externaldrive_fill.svg` | storage, device | 样式：外置存储设备实心图标，默认黑色，图形为矩形硬盘盒造型；适用：本地存储管理、数据备份、文件传输。 | `1.0.0` |
| `asset.face` | `resources/base/media/face.svg` | person, emotion | 样式：默认黑色的单色线框圆形笑脸，带眼睛、鼻子和微笑嘴形；适用：愉悦状态、用户形象占位、满意度或友好提示。 | `1.0.0` |
| `asset.fast_forward` | `resources/base/media/fast_forward.svg` | media, control | 样式：快进图标，默认黑色，图形为两个向右的三角箭头；适用：音乐播放器快进控制、视频快进。 | `1.0.0` |
| `asset.figure_pool_swim` | `resources/base/media/figure_pool_swim.svg` | health, sport | 样式：游泳人物图标，默认黑色，图形为人体游泳动作侧视轮廓；适用：运动记录、游泳锻炼追踪、健康运动卡片。 | `1.0.0` |
| `asset.figure_run` | `resources/base/media/figure_run.svg` | health, sport | 样式：跑步人物图标，默认黑色，图形为人体奔跑动作侧视轮廓；适用：运动记录、跑步锻炼追踪、步数统计。 | `1.0.0` |
| `asset.flame_fill` | `resources/base/media/flame_fill.svg` | health, heat | 样式：默认黑色的单色实心火焰图标；适用：运动热量消耗、燃烧、火焰或加热状态。 | `1.0.0` |
| `asset.heart_fill` | `resources/base/media/heart_fill.svg` | health, heart | 样式：默认黑色的单色实心爱心图标；适用：喜欢、收藏、关爱、心脏健康或心率栏目入口。 | `1.0.0` |
| `asset.heat_generation` | `resources/base/media/heat_generation.svg` | temperature, heat | 样式：默认黑色的单色线框温度计，底部为圆形感温泡，内部带弧形刻度；适用：温度、升温、制热或体感温度。 | `1.0.0` |
| `asset.house_fill` | `resources/base/media/house_fill.svg` | home | 样式：房屋实心图标，黑白双色，图形为三角屋顶加矩形门洞的家形造型，建议保留原色；适用：首页导航、智能家居入口、回家提醒。 | `1.0.0` |
| `asset.hourglass_fill` | `resources/base/media/hourglass_fill.svg` | — | 样式：沙漏和齿轮组合图标，图形为沙漏线性右下角齿轮组合的造型，建议保留原色；适用：应用时长。 | `1.0.0` |
| `asset.id_fill` | `resources/base/media/id_fill.svg` | identity | 样式：默认黑色的单色圆角矩形徽标，内部以留白显示大写 ID；适用：会议 ID、身份编号、证件编号或标识码。 | `1.0.0` |
| `asset.kidswatch_fill` | `resources/base/media/kidswatch_fill.svg` | device, watch | 样式：默认黑色的单色实心智能手表正视图，矩形圆角表盘和上下表带；适用：儿童手表、可穿戴设备、手表连接或设备管理。 | `1.0.0` |
| `asset.l_circle_fill` | `resources/base/media/l_circle_fill.svg` | audio, left | 样式：黑色实心圆形徽标，内部以留白显示大写 L，建议保留原色；适用：左耳、左声道、左侧设备或 L 标记。 | `1.0.0` |
| `asset.lamp_ceiling` | `resources/base/media/lamp_ceiling.svg` | home, light | 样式：吸顶灯图标（关灯状态），默认黑色，图形为圆形灯盘加固定架造型；适用：智能照明控制、灯光管理、家居灯光。 | `1.0.0` |
| `asset.lamp_ceiling_light` | `resources/base/media/lamp_ceiling_light.svg` | home, light | 样式：吸顶灯亮起图标（开灯状态），默认黑色，图形为圆形灯盘加射线光芒造型；适用：灯光开启状态展示、智能照明控制。 | `1.0.0` |
| `asset.local_fill` | `resources/base/media/local_fill.svg` | location | 样式：默认黑色的单色实心地图定位针，中央为圆形留白；适用：当前位置、地点、地图标记、位置服务。 | `1.0.0` |
| `asset.location_north_up_right_fill` | `resources/base/media/location_north_up_right_fill.svg` | location, navigation | 样式：方向导航实心图标，默认黑色，图形为指向右上方的导航箭头；适用：地图导航、方向指引、路线规划。 | `1.0.0` |
| `asset.moon_circle_fill` | `resources/base/media/moon_circle_fill.svg` | sleep, night | 样式：月亮圆形实心图标，黑白双色，图形为圆形背景内白色月牙，建议保留原色；适用：夜间模式、睡眠追踪、勿扰模式。 | `1.0.0` |
| `asset.moon_z_fill_1` | `resources/base/media/moon_z_fill_1.svg` | sleep, night | 样式：月亮加Z睡眠实心图标，默认黑色，图形为月牙旁附带字母Z表示入睡；适用：睡眠模式开启、休息提醒、晚安场景。 | `1.0.0` |
| `asset.music_fill` | `resources/base/media/music_fill.svg` | music, media | 样式：音乐音符实心图标，默认黑色，图形为双音符连接造型；适用：音乐播放卡片、音频功能入口、歌单展示。 | `1.0.0` |
| `asset.pause_fill` | `resources/base/media/pause_fill.svg` | media, control | 样式：暂停实心图标，默认黑色，图形为两条竖向平行矩形；适用：音乐/视频播放暂停控制。 | `1.0.0` |
| `asset.person_3_fill` | `resources/base/media/person_3_fill.svg` | person, group | 样式：三人组实心图标，默认黑色，图形为三个人形轮廓并排排列；适用：群组联系人、团队成员展示、家庭成员列表。 | `1.0.0` |
| `asset.phone_fill` | `resources/base/media/phone_fill.svg` | phone, call | 样式：电话实心图标，默认黑色，图形为经典听筒造型；适用：拨打电话、通话功能入口。 | `1.0.0` |
| `asset.play_fill` | `resources/base/media/play_fill.svg` | media, control | 样式：播放实心图标，默认黑色，图形为向右的实心三角形；适用：音乐/视频播放控制、媒体播放器。 | `1.0.0` |
| `asset.qrcode` | `resources/base/media/qrcode.svg` | qrcode, share | 样式：默认黑色的单色线面结合二维码符号，包含三个定位方块和右下点阵；适用：扫码入口、二维码功能、设备配对或分享入口。 | `1.0.0` |
| `asset.r_circle_fill` | `resources/base/media/r_circle_fill.svg` | audio, right | 样式：黑色实心圆形徽标，内部以留白显示大写 R，建议保留原色；适用：右耳、右声道、右侧设备或 R 标记。 | `1.0.0` |
| `asset.stopwatch_fill` | `resources/base/media/stopwatch_fill.svg` | time, sport | 样式：秒表实心图标，黑白双色，图形为带按钮的圆形秒表造型，建议保留原色；适用：计时功能、运动计时、倒计时。 | `1.0.0` |
| `asset.sun_max` | `resources/base/media/sun_max.svg` | weather, sun | 样式：默认黑色的单色线框太阳，中央大圆环，周围为八条较长放射线；适用：高亮度、强光、晴天或亮度增大。 | `1.0.0` |
| `asset.sun_min` | `resources/base/media/sun_min.svg` | weather, sun | 样式：默认黑色的单色线框太阳，中央圆环，周围为八个较短圆点式光芒；适用：低亮度、柔和阳光、亮度减小。 | `1.0.0` |
| `asset.tram_fill` | `resources/base/media/tram_fill.svg` | traffic, tram | 样式：默认黑色的单色实心有轨电车正视图，顶部带受电弓，底部带车轮；适用：有轨电车、轻轨、轨道交通站点或线路。 | `1.0.0` |
| `asset.typhoon_fill` | `resources/base/media/typhoon_fill.svg` | — | 样式：台风黑色图标，图形为台风漩涡造型；适用：台风预警、台风路径。 | `1.0.0` |
| `asset.z_alarm_fill` | `resources/base/media/z_alarm_fill.svg` | alarm, sleep | 样式：带Z的闹钟贪睡实心图标，默认黑色，图形为闹钟旁附带字母Z表示贪睡；适用：闹钟贪睡功能、延迟提醒、睡眠场景。 | `1.0.0` |
| `asset.icon_id` | `resources/base/media/icon_id.svg` | — | 样式：米灰色半透明圆角矩形徽标，内部以浅色显示大写 ID，原始尺寸为 12×12，保留原色与透明度；适用：会议 ID、身份编号或日程中的标识码。 | `1.0.0` |
| `asset.icon_meeting` | `resources/base/media/icon_meeting.svg` | — | 样式：纯白色单色线面结合的会议演示板图标，画板内有两条横线，原始尺寸为 14×14；适用：会议、汇报、演示、议程。 | `1.0.0` |
| `asset.icon_watermark` | `resources/base/media/icon_watermark.svg` | — | 样式：米灰色低透明度的大型日历轮廓装饰，画布和图形尺寸关系特殊，保留原色与透明层级；适用：日程卡片的弱化背景水印或装饰锚点。 | `1.0.0` |
| `asset.icon_allergy` | `resources/base/media/icon_allergy.svg` | — | 样式：默认黑色的单色侧面人头轮廓，面部周围分布颗粒点，表现过敏原或空气刺激；适用：过敏、花粉、空气刺激、呼吸道敏感提示。 | `1.0.0` |
| `asset.icon_high_temperature` | `resources/base/media/icon_high_temperature.svg` | — | 样式：默认黑色的单色线框温度计，内部温度柱较高，源文件语义指向体温；适用：体温偏高、发热、人体温度提醒。 | `1.0.0` |
| `asset.icon_tiktok` | `resources/base/media/icon_tiktok.png` | — | 样式：黑色圆形底上的抖音品牌音符，包含青色、红色和白色叠色，64×64 PNG，PNG 位图需保留品牌原色；适用：抖音应用、抖音使用时长或防沉迷统计。 | `1.0.0` |
| `asset.icon_timing` | `resources/base/media/icon_timing.svg` | — | 样式：白色实心秒表配黑色指针，顶部有按钮，属于高对比双色图标，建议保留原色；适用：计时、使用时长、倒计时或时限。 | `1.0.0` |
| `asset.icon_earphone` | `resources/base/media/icon_earphone.svg` | — | 样式：黑色实心左右分体式开放耳机，局部有白色高光与分隔，建议保留原色；适用：无线耳机本体、耳机连接、左右耳设备状态。 | `1.0.0` |
| `asset.icon_phone` | `resources/base/media/icon_phone.svg` | — | 样式：默认黑色的单色线框竖向智能手机，内部有屏幕轮廓；适用：手机设备、手机状态、专注模式中的手机对象。 | `1.0.0` |
| `asset.icon_car` | `resources/base/media/icon_car.svg` | — | 样式：默认黑色的单色汽车正视图，带前窗、车灯和车轮；适用：汽车、打车、驾车出行或车辆状态。 | `1.0.0` |
| `asset.icon_focus` | `resources/base/media/icon_focus.svg` | — | 样式：默认黑色的单色实心月牙图标，无圆形底和睡眠字样；适用：专注模式、勿扰模式、夜间状态。 | `1.0.0` |
| `asset.icon_schedule` | `resources/base/media/icon_schedule.svg` | — | 样式：纯白色单色实心日历图标，顶部双装订环，内部为六个日期点；适用：日程、日期、日历入口或当日安排。 | `1.0.0` |
| `asset.icon_save_power` | `resources/base/media/icon_save_power.svg` | — | 样式：默认黑色的单色实心横向电池图标，内部为叶片造型；适用：省电模式、节能设置、绿色电池状态。 | `1.0.0` |
| `asset.icon_run` | `resources/base/media/icon_run.svg` | — | 样式：纯白色单色奔跑人物侧视图，浅色背景需染色；适用：跑步、运动锻炼、活动日程。 | `1.0.0` |
| `asset.icon_left` | `resources/base/media/icon_left.svg` | — | 样式：黑色实心圆形徽标，内部以白色显示大写 L，源文件语义为左耳机，建议保留原色；适用：左耳、左声道、左侧耳机电量。 | `1.0.0` |
| `asset.icon_music` | `resources/base/media/icon_music.svg` | — | 样式：黑色实心双音符图标，内部使用白色分隔形成音符结构，建议保留原色；适用：音乐、歌曲、歌单或音频内容。 | `1.0.0` |
| `asset.icon_right` | `resources/base/media/icon_right.svg` | — | 样式：黑色实心圆形徽标，内部以白色显示大写 R，源文件语义为右耳机，建议保留原色；适用：右耳、右声道、右侧耳机电量。 | `1.0.0` |
| `asset.icon_weather_temperature1` | `resources/base/media/icon_weather_temperature1.svg` | — | 样式：淡黄色外壳与粉红色温度柱组成的彩色温度计，右侧带刻度，建议保留原色；适用：当前气温、最高最低温、体感温度或天气温度概览 | `1.0.0` |
| `asset.icon_weather_thermometer_medium` | `resources/base/media/icon_weather_thermometer_medium.svg` | — | 样式：黑色的单色温度计图标，内部温度柱处于中档，管身右侧带三组刻度；适用：中等温度、舒适温度区间、当前气温或温度等级。 | `1.0.0` |
| `asset.icon_weather_thermometer` | `resources/base/media/icon_weather_thermometer.svg` | — | 样式：黑色的单色温度计图标，底部为实心感温泡，管身内侧带三段刻度；适用：天气温度、温度指标、温差变化或冷热趋势。 | `1.0.0` |
| `asset.icon_weather_wind` | `resources/base/media/icon_weather_wind.svg` | — | 样式：黑色的单色线面结合风力图标，主体为水滴状轮廓并带两组横向波浪气流；适用：风速、风向、风力等级或大风提醒。 | `1.0.0` |
