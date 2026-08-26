# GetAppUsageDuration

能力源：[`data_capabilities.json`](../../../scripts/rules/capabilities/app-11.7.5.205_rom-6.0/data_capabilities.json)，来源提交 `854956dc6364295ad0cfcb5f683b5f7b4d5bb494`，profile `app-11.7.5.205_rom-6.0`。

获取指定应用的使用时长数据

## 生成规则

- `capabilityId`: `GetAppUsageDuration`
- 推荐 `writeResultTo`: `/data/appUsageStats`
- 必填入参：`appBundleName`
- 依赖包：无
- `arguments` 只能使用下方 `inputSchema.properties`；类型、枚举、范围和必填项必须原样遵守。
- UI 只能访问 `writeResultTo + outputSchema` 可推导路径；初始化数据必须是 outputSchema 的合法投影。
- 顶层输出路径：`/data/appUsageStats/appUsage`, `/data/appUsageStats/updatedAt`

## 原始能力声明

```json
{
  "id": "GetAppUsageDuration",
  "enabled": false,
  "description": "获取指定应用的使用时长数据",
  "defaultWriteResultTo": "/data/appUsageStats",
  "dependencies": {
    "requiredPackages": []
  },
  "inputSchema": {
    "type": "object",
    "description": "查询应用使用时长的输入参数",
    "properties": {
      "appBundleName": {
        "type": "string",
        "description": "目标应用的包名，例如：com.ss.hm.ugc.aweme"
      }
    },
    "required": [
      "appBundleName"
    ]
  },
  "outputSchema": {
    "type": "object",
    "description": "适合桌面卡片展示的应用时长概要。",
    "properties": {
      "appUsage": {
        "type": "object",
        "description": "应用具体的使用时长详情",
        "properties": {
          "appName": {
            "type": "string",
            "description": "应用名称文本，例如：“抖音”",
            "sampleValue": "示例应用"
          },
          "durationText": {
            "type": "string",
            "description": "应用今日运行总时间文本（自带单位），例如：“25 秒”或“1 分钟 21 秒”",
            "sampleValue": "25 分钟"
          }
        }
      },
      "updatedAt": {
        "type": "string",
        "description": "端侧完成数据查询和归一化的时间，格式如：2026-07-14 10:16。",
        "sampleValue": "2026-08-06 09:00"
      }
    }
  },
  "type": "data",
  "dataModelSkeleton": {}
}
```
