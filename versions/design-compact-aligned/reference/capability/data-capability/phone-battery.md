# GetPhoneBatteryInfo

能力源：[`data_capabilities.json`](../../../scripts/rules/capabilities/app-11.7.5.205_rom-6.0/data_capabilities.json)，来源提交 `854956dc6364295ad0cfcb5f683b5f7b4d5bb494`，profile `app-11.7.5.205_rom-6.0`。

获取手机本机的全量电池状态快照，返回经过端侧语义化和字符化转换的电池状态。

## 生成规则

- `capabilityId`: `GetPhoneBatteryInfo`
- 推荐 `writeResultTo`: `/data/phoneBattery`
- 必填入参：无
- 依赖包：无
- `arguments` 只能使用下方 `inputSchema.properties`；类型、枚举、范围和必填项必须原样遵守。
- UI 只能访问 `writeResultTo + outputSchema` 可推导路径；初始化数据必须是 outputSchema 的合法投影。
- 顶层输出路径：`/data/phoneBattery/batterySOC`, `/data/phoneBattery/batterySOCText`, `/data/phoneBattery/chargingStatusDesc`, `/data/phoneBattery/batteryCapacityLevelDesc`, `/data/phoneBattery/healthStatusDesc`, `/data/phoneBattery/pluggedTypeDesc`, `/data/phoneBattery/batteryTemperatureText`, `/data/phoneBattery/nowCurrentText`, `/data/phoneBattery/voltageText`, `/data/phoneBattery/isBatteryPresentText`, `/data/phoneBattery/updatedAt`

## 原始能力声明

```json
{
  "id": "GetPhoneBatteryInfo",
  "description": "获取手机本机的全量电池状态快照，返回经过端侧语义化和字符化转换的电池状态。",
  "defaultWriteResultTo": "/data/phoneBattery",
  "dependencies": {
    "requiredPackages": []
  },
  "inputSchema": {
    "type": "object",
    "properties": {},
    "required": []
  },
  "outputSchema": {
    "type": "object",
    "description": "经过中文语义化清洗后的手机本机电池物理状态。",
    "properties": {
      "batterySOC": {
        "type": "integer",
        "description": "当前手机设备剩余电池电量百分比纯数字，取值范围为 0 到 100。",
        "sampleValue": 68
      },
      "batterySOCText": {
        "type": "string",
        "description": "当前手机设备剩余电池电量百分比格式化文本。",
        "sampleValue": "68%"
      },
      "chargingStatusDesc": {
        "type": "string",
        "description": "当前设备电池的充电状态文本描述。",
        "sampleValue": "未充电"
      },
      "batteryCapacityLevelDesc": {
        "type": "string",
        "description": "设备电池电量等级的语义化文本描述。",
        "sampleValue": "正常电量"
      },
      "healthStatusDesc": {
        "type": "string",
        "description": "当前设备电池的物理健康状态文本描述。",
        "sampleValue": "正常"
      },
      "pluggedTypeDesc": {
        "type": "string",
        "description": "当前设备连接的充电器类型文本描述。",
        "sampleValue": "未连接充电器"
      },
      "batteryTemperatureText": {
        "type": "string",
        "description": "当前设备电池的实时温度文本，带有摄氏度单位。",
        "sampleValue": "29.0 ℃"
      },
      "nowCurrentText": {
        "type": "string",
        "description": "当前设备电池的实时电流文本，带有毫安单位。",
        "sampleValue": "-151 mA"
      },
      "voltageText": {
        "type": "string",
        "description": "当前设备电池的实时电压文本，带有伏特单位。",
        "sampleValue": "4 V"
      },
      "isBatteryPresentText": {
        "type": "string",
        "description": "当前设备物理电池是否在位或受支持的状态描述。",
        "sampleValue": "在位"
      },
      "updatedAt": {
        "type": "string",
        "description": "端侧完成全量电量状态字符化转换的系统时间文本。",
        "sampleValue": "2026-08-06 09:00"
      }
    }
  },
  "type": "data",
  "dataModelSkeleton": {}
}
```
