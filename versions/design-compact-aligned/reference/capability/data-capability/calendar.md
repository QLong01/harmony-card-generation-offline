# GetCalendarEvents

能力源：[`data_capabilities.json`](../../../scripts/rules/capabilities/app-11.7.5.205_rom-6.0/data_capabilities.json)，来源提交 `854956dc6364295ad0cfcb5f683b5f7b4d5bb494`，profile `app-11.7.5.205_rom-6.0`。

查询用户系统日历中的日程安排。可返回高度精简的结构化用户日程信息，包含日程倒计时计算、日程开始/截止时间等，并支持一键拉起第三方应用（如视频会议、赛事直播）的跳转链接。返回的日程均为由近到远顺序返回，暂不支持按特定条件过滤(比如按天)。

## 生成规则

- `capabilityId`: `GetCalendarEvents`
- 推荐 `writeResultTo`: `/data/calendar`
- 必填入参：无
- 依赖包：`com.huawei.hmos.calendar`
- `arguments` 只能使用下方 `inputSchema.properties`；类型、枚举、范围和必填项必须原样遵守。
- UI 只能访问 `writeResultTo + outputSchema` 可推导路径；初始化数据必须是 outputSchema 的合法投影。
- 顶层输出路径：`/data/calendar/eventCount`, `/data/calendar/events`, `/data/calendar/updatedAt`

## 原始能力声明

```json
{
  "id": "GetCalendarEvents",
  "description": "查询用户系统日历中的日程安排。可返回高度精简的结构化用户日程信息，包含日程倒计时计算、日程开始/截止时间等，并支持一键拉起第三方应用（如视频会议、赛事直播）的跳转链接。返回的日程均为由近到远顺序返回，暂不支持按特定条件过滤(比如按天)。",
  "defaultWriteResultTo": "/data/calendar",
  "dependencies": {
    "requiredPackages": [
      {
        "packageName": "com.huawei.hmos.calendar"
      }
    ]
  },
  "inputSchema": {
    "type": "object",
    "properties": {
      "futureDays": {
        "type": "integer",
        "description": "需要查询的未来时间窗口天数。例如用户想看'这周'或'未来7天'的日程则传 7。若不传，端侧默认查询未来7天。"
      }
    },
    "required": []
  },
  "outputSchema": {
    "type": "object",
    "description": "经过端侧高级清洗后的系统日程概要，包含命中该时间段的日程总数以及按时间升序排列的具体日程明细列表。",
    "properties": {
      "eventCount": {
        "type": "integer",
        "description": "查询到的日程记录总数量。",
        "sampleValue": 1
      },
      "events": {
        "type": "array",
        "description": "高密度结构化日程信息实体列表，已按开始时间由早到晚进行升序排列。",
        "items": {
          "type": "object",
          "properties": {
            "entityName": {
              "type": "string",
              "description": "固定为 'CalendarEvent'，用于系统底层实体识别。",
              "sampleValue": "CalendarEvent"
            },
            "entityId": {
              "type": "string",
              "description": "系统日程的全局唯一实体ID。",
              "sampleValue": "example-event-001"
            },
            "senderName": {
              "type": "string",
              "description": "日程数据标识符或发起方标识（如邀请人），若无则为空字符串。",
              "sampleValue": ""
            },
            "title": {
              "type": "string",
              "description": "日程标题，例如“咪咕视频《西班牙 VS 奥地利》”或航班、车次信息。",
              "sampleValue": "项目例会"
            },
            "eventLocation": {
              "type": "string",
              "description": "日程的具体地点描述，若未填写则为空字符串。",
              "sampleValue": "会议室"
            },
            "description": {
              "type": "string",
              "description": "日程的备注、摘要或补充叙述文本。",
              "sampleValue": "周例会"
            },
            "dtStart": {
              "type": "string",
              "description": "格式化后的日程开始时间短文本，如 '03:00'，若为全天日程可能为特殊标记。",
              "sampleValue": "14:00"
            },
            "dtEnd": {
              "type": "string",
              "description": "格式化后的日程结束时间短文本，如 '05:00'。",
              "sampleValue": "15:00"
            },
            "timeZone": {
              "type": "string",
              "description": "日程所处的时区标识，例如 'Asia/Shanghai'。",
              "sampleValue": "Asia/Shanghai"
            },
            "importantEventType": {
              "type": "integer",
              "description": "日程事件的重要程度或分类枚举值（Type）。",
              "sampleValue": 0
            },
            "remindTime": {
              "type": "array",
              "description": "预设的提前提醒时间跨度数组（字符串化），例如 ['15'] 代表提前15分钟提醒。",
              "items": {
                "type": "string",
                "description": "提前提醒分钟数（字符串形式）。",
                "sampleValue": "15"
              }
            },
            "oneClickServiceType": {
              "type": "string",
              "enum": [
                "Meeting",
                "Watching",
                "Repayment",
                "Live",
                "Shopping",
                "Trip",
                "Class",
                "SportsEvents",
                "SportsExercise",
                ""
              ],
              "description": "绑定的轻服务类型名称。大模型生成一键服务按钮时，应按照端侧能力声明的枚举选择文案。",
              "sampleValue": "Meeting"
            },
            "oneClickServiceLink": {
              "type": "string",
              "description": "一键直达的 URI 深度跳转链接，UI 卡片可直接通过此链接拉起第三方 App 落地页。",
              "sampleValue": ""
            },
            "isServiceValid": {
              "type": "integer",
              "description": "跳转服务连接是否有效。1代表存在有效跳转链接，0代表没有。",
              "sampleValue": 0
            },
            "startDate": {
              "type": "string",
              "description": "日程开始日期格式化文本，例如 '07-03'。",
              "sampleValue": "08-06"
            },
            "countdownDays": {
              "type": "integer",
              "description": "纯数字的倒数日天数。0代表今天发生（或已发生），正整数代表距离日程开始还有多少天。",
              "sampleValue": 0
            },
            "isAllDay": {
              "type": "boolean",
              "description": "标识该日程是否为全天日程。",
              "sampleValue": false
            }
          }
        }
      },
      "updatedAt": {
        "type": "string",
        "description": "端侧完成数据组装的时间戳字符串，格式如 '2026-07-03 15:30'。",
        "sampleValue": "2026-08-06 09:00"
      }
    }
  },
  "type": "data",
  "dataModelSkeleton": {}
}
```
