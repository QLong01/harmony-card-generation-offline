# GetHealthAndSportSummary

能力源：[`data_capabilities.json`](../../../scripts/rules/capabilities/app-11.7.5.205_rom-6.0/data_capabilities.json)，来源提交 `854956dc6364295ad0cfcb5f683b5f7b4d5bb494`，profile `app-11.7.5.205_rom-6.0`。

一键合并查询用户指定时间段内的大健康、日常大盘活动与单次专业运动训练指标。包含极其精细的夜间科学睡眠分析、当日全天步数/热量/距离总合大盘，以及最近一次专业运动训练的起止时间、计划与详尽的心率区间剖析。

## 生成规则

- `capabilityId`: `GetHealthAndSportSummary`
- 推荐 `writeResultTo`: `/data/healthSport`
- 必填入参：无
- 依赖包：`com.huawei.hmos.health`
- `arguments` 只能使用下方 `inputSchema.properties`；类型、枚举、范围和必填项必须原样遵守。
- UI 只能访问 `writeResultTo + outputSchema` 可推导路径；初始化数据必须是 outputSchema 的合法投影。
- 顶层输出路径：`/data/healthSport/targetDateText`, `/data/healthSport/sleepScore`, `/data/healthSport/sleepStatus`, `/data/healthSport/sleepTypeDesc`, `/data/healthSport/nightSleepDurationText`, `/data/healthSport/deepSleepDurationText`, `/data/healthSport/totalNapDurationText`, `/data/healthSport/fallAsleepTimeText`, `/data/healthSport/wakeupTimeText`, `/data/healthSport/dailySteps`, `/data/healthSport/dailyTotalCaloriesText`, `/data/healthSport/dailyDistanceText`, `/data/healthSport/exerciseTypeName`, `/data/healthSport/exerciseStartTimeText`, `/data/healthSport/exerciseEndTimeText`, `/data/healthSport/exerciseDurationText`, `/data/healthSport/exerciseCalorieText`, `/data/healthSport/exerciseHeartRateAvg`, `/data/healthSport/exerciseHeartRateMax`, `/data/healthSport/exerciseHeartRateMin`, `/data/healthSport/updatedAt`

## 原始能力声明

```json
{
  "id": "GetHealthAndSportSummary",
  "description": "一键合并查询用户指定时间段内的大健康、日常大盘活动与单次专业运动训练指标。包含极其精细的夜间科学睡眠分析、当日全天步数/热量/距离总合大盘，以及最近一次专业运动训练的起止时间、计划与详尽的心率区间剖析。",
  "defaultWriteResultTo": "/data/healthSport",
  "dependencies": {
    "requiredPackages": [
      {
        "packageName": "com.huawei.hmos.health"
      }
    ]
  },
  "inputSchema": {
    "type": "object",
    "properties": {
      "targetDayOffset": {
        "type": "integer",
        "description": "需要查询的目标日期相对今天的偏移天数。0 代表查询今天，-1 代表查询昨天，-2 代表前天，以此类推。支持最大历史跨度为过去30天（-30）。若不传，端侧默认查询今天（0）的大盘数据。"
      }
    },
    "required": []
  },
  "outputSchema": {
    "type": "object",
    "description": "完全对齐 SleepPrunedData 数据契约的融合规整规整化健康与运动大盘字典。所有时长、热量、距离及时间表达均已在端侧完成格式化转换，适合UI卡片直接渲染或大模型播报。",
    "properties": {
      "targetDateText": {
        "type": "string",
        "description": "该组健康与运动数据所归属的确切日期文本，格式为 YYYY-MM-DD，例如 '2026-07-06'。用于明确展示当前查阅的是哪一天的数据。",
        "sampleValue": "2026-08-06"
      },
      "sleepScore": {
        "type": "integer",
        "description": "睡眠综合得分，取值范围 0-100。",
        "sampleValue": 82
      },
      "sleepStatus": {
        "type": "string",
        "description": "基于得分智能生成的睡眠状态语义判定，包括：'优秀'、'良好'、'一般'、'较差'。",
        "sampleValue": "良好"
      },
      "sleepTypeDesc": {
        "type": "string",
        "description": "睡眠记录方式或类型的描述，例如“科学睡眠”、“普通睡眠”、“手动输入睡眠”、“手机记录睡眠”。",
        "sampleValue": "科学睡眠"
      },
      "nightSleepDurationText": {
        "type": "string",
        "description": "夜间正式睡眠的总时长文本，例如“7小时1分”。",
        "sampleValue": "7小时1分"
      },
      "deepSleepDurationText": {
        "type": "string",
        "description": "夜间正式睡眠中的深睡总时长文本，例如“2小时15分”。",
        "sampleValue": "2小时15分"
      },
      "totalNapDurationText": {
        "type": "string",
        "description": "白天零星小睡（午休）的累计总时长文本，例如“45分”或“0分”。",
        "sampleValue": "0分"
      },
      "fallAsleepTimeText": {
        "type": "string",
        "description": "格式化后的确切入睡时刻短文本（HH:mm），例如“23:15”。",
        "sampleValue": "23:15"
      },
      "wakeupTimeText": {
        "type": "string",
        "description": "格式化后的确切醒来时刻短文本（HH:mm），例如“07:30”。",
        "sampleValue": "07:30"
      },
      "dailySteps": {
        "type": "integer",
        "description": "与最新睡眠同属一天的日常全天累计活动总步数，例如 1070。",
        "sampleValue": 6200
      },
      "dailyTotalCaloriesText": {
        "type": "string",
        "description": "与最新睡眠同属一天的日常活动及总消耗热量文本（已完成千分位归一化换算），例如“998 千卡”。",
        "sampleValue": "420 千卡"
      },
      "dailyDistanceText": {
        "type": "string",
        "description": "与最新睡眠同属一天的日常活动总距离文本。端侧已根据数值大小自动变换米或公里后缀，例如“5.42 公里”或“755 米”。",
        "sampleValue": "4.60 公里"
      },
      "exerciseTypeName": {
        "type": "string",
        "description": "最近一次发生的单次专业运动训练类型的中文映射名称，如“羽毛球”、“自由训练”、“户外跑步”。若无记录则返回“暂无运动”。",
        "sampleValue": "户外跑步"
      },
      "exerciseStartTimeText": {
        "type": "string",
        "description": "专业运动开始的确切时刻文本（HH:mm），例如“18:30”。",
        "sampleValue": "18:30"
      },
      "exerciseEndTimeText": {
        "type": "string",
        "description": "专业运动结束的确切时刻文本（HH:mm），例如“19:50”。",
        "sampleValue": "19:10"
      },
      "exerciseDurationText": {
        "type": "string",
        "description": "该单次专业运动的实际持续时长文本，例如“1小时40分”。",
        "sampleValue": "40分"
      },
      "exerciseCalorieText": {
        "type": "string",
        "description": "该单次专业运动所产生的净热量消耗文本（已转换千卡），例如“98 千卡”。",
        "sampleValue": "260 千卡"
      },
      "exerciseHeartRateAvg": {
        "type": "integer",
        "description": "专业运动期间的平均心率（次/分钟）。",
        "sampleValue": 135
      },
      "exerciseHeartRateMax": {
        "type": "integer",
        "description": "专业运动期间录得的最大极限心率（次/分钟）。",
        "sampleValue": 168
      },
      "exerciseHeartRateMin": {
        "type": "integer",
        "description": "专业运动期间录得的最低心率（次/分钟）。",
        "sampleValue": 96
      },
      "updatedAt": {
        "type": "string",
        "description": "端侧完成多实体规整转换的系统格式化时间戳字符串，如 '2026-07-03 14:57'。",
        "sampleValue": "2026-08-06 09:00"
      }
    }
  },
  "type": "data",
  "dataModelSkeleton": {}
}
```
