# GetEarphoneInfo

能力源：[`data_capabilities.json`](../../../scripts/rules/capabilities/app-11.7.5.205_rom-6.0/data_capabilities.json)，来源提交 `854956dc6364295ad0cfcb5f683b5f7b4d5bb494`，profile `app-11.7.5.205_rom-6.0`。

查询当前手机连接的蓝牙耳机状态，包括耳机名称、主盒与左右耳的当前独立剩余电量百分比，以及它们各自的充电状态。

## 生成规则

- `capabilityId`: `GetEarphoneInfo`
- 推荐 `writeResultTo`: `/data/earphone`
- 必填入参：无
- 依赖包：无
- `arguments` 只能使用下方 `inputSchema.properties`；类型、枚举、范围和必填项必须原样遵守。
- UI 只能访问 `writeResultTo + outputSchema` 可推导路径；初始化数据必须是 outputSchema 的合法投影。
- 顶层输出路径：`/data/earphone/isConnected`, `/data/earphone/earphoneName`, `/data/earphone/batteryLevel`, `/data/earphone/chargingStatusDesc`, `/data/earphone/leftBatteryLevel`, `/data/earphone/leftChargingStatusDesc`, `/data/earphone/rightBatteryLevel`, `/data/earphone/rightChargingStatusDesc`, `/data/earphone/updatedAt`

## 原始能力声明

```json
{
  "id": "GetEarphoneInfo",
  "description": "查询当前手机连接的蓝牙耳机状态，包括耳机名称、主盒与左右耳的当前独立剩余电量百分比，以及它们各自的充电状态。",
  "defaultWriteResultTo": "/data/earphone",
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
    "description": "聚合清洗后的标准化耳机状态数据，适合桌面小部件或快捷控制中心直接绑定显示。",
    "properties": {
      "isConnected": {
        "type": "boolean",
        "description": "当前是否有蓝牙耳机处于连接活跃状态。",
        "sampleValue": true
      },
      "earphoneName": {
        "type": "string",
        "description": "耳机的设备广播名称，如果未连接则返回'未连接耳机'。如: 'FreeBuds Pro 3'。",
        "sampleValue": "示例耳机"
      },
      "batteryLevel": {
        "type": "integer",
        "description": "耳机盒（或整体）的当前电量百分比，取值范围 0-100。",
        "sampleValue": 80
      },
      "chargingStatusDesc": {
        "type": "string",
        "description": "耳机盒（或整体）当前的充电状态中文语义描述，'充电中' 或 '未充电'。",
        "sampleValue": "未充电"
      },
      "leftBatteryLevel": {
        "type": "integer",
        "description": "左耳机的当前电量百分比，取值范围 0-100。若未连接则为 0。",
        "sampleValue": 76
      },
      "leftChargingStatusDesc": {
        "type": "string",
        "description": "左耳机当前的充电状态中文语义描述，'充电中' 或 '未充电'。",
        "sampleValue": "未充电"
      },
      "rightBatteryLevel": {
        "type": "integer",
        "description": "右耳机的当前电量百分比，取值范围 0-100。若未连接则为 0。",
        "sampleValue": 78
      },
      "rightChargingStatusDesc": {
        "type": "string",
        "description": "右耳机当前的充电状态中文语义描述，'充电中' 或 '未充电'。",
        "sampleValue": "未充电"
      },
      "updatedAt": {
        "type": "string",
        "description": "端侧完成多源数据感知和融合的时间戳字符串。如：2026-07-02 20:15",
        "sampleValue": "2026-08-06 09:00"
      }
    }
  },
  "type": "data",
  "dataModelSkeleton": {}
}
```
