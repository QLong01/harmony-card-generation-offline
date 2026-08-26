# GetCountdownDays

能力源：[`data_capabilities.json`](../../../scripts/rules/capabilities/app-11.7.5.205_rom-6.0/data_capabilities.json)，来源提交 `854956dc6364295ad0cfcb5f683b5f7b4d5bb494`，profile `app-11.7.5.205_rom-6.0`。

计算指定的日历日期距离今天还有多少天；目标日期由模型提取，实际天数差值由端侧计算。

## 生成规则

- `capabilityId`: `GetCountdownDays`
- 推荐 `writeResultTo`: `/data/countdown`
- 必填入参：`targetDate`
- 依赖包：无
- `arguments` 只能使用下方 `inputSchema.properties`；类型、枚举、范围和必填项必须原样遵守。
- UI 只能访问 `writeResultTo + outputSchema` 可推导路径；初始化数据必须是 outputSchema 的合法投影。
- 顶层输出路径：`/data/countdown/countdownDays`

## 原始能力声明

```json
{
  "id": "GetCountdownDays",
  "description": "计算指定的日历日期距离今天还有多少天；目标日期由模型提取，实际天数差值由端侧计算。",
  "defaultWriteResultTo": "/data/countdown",
  "dependencies": {
    "requiredPackages": []
  },
  "inputSchema": {
    "type": "object",
    "description": "计算倒数日需要的入参。",
    "properties": {
      "targetDate": {
        "type": "string",
        "description": "目标日期，必须是 YYYY-MM-DD 格式。"
      }
    },
    "required": [
      "targetDate"
    ]
  },
  "outputSchema": {
    "type": "object",
    "description": "计算得出的倒数日天数结果实体。",
    "properties": {
      "countdownDays": {
        "type": "integer",
        "description": "距离目标日期的自然日天数；正数表示未来，0 表示今天，负数表示已经过去。",
        "sampleValue": 30
      }
    }
  },
  "type": "data",
  "dataModelSkeleton": {}
}
```
