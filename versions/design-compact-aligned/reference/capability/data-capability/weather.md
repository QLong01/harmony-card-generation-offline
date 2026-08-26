# ViewWeather

能力源：[`data_capabilities.json`](../../../scripts/rules/capabilities/app-11.7.5.205_rom-6.0/data_capabilities.json)，来源提交 `854956dc6364295ad0cfcb5f683b5f7b4d5bb494`，profile `app-11.7.5.205_rom-6.0`。

查询指定地区的当前天气与未来数日天气预报。如果不能推断出用户的地区名，则需要追问用户提供。注意，当前不支持查询国外的天气。

## 生成规则

- `capabilityId`: `ViewWeather`
- 推荐 `writeResultTo`: `/data/weather`
- 必填入参：`prefectureName`
- 依赖包：`com.huawei.hmsapp.totemweather`
- `arguments` 只能使用下方 `inputSchema.properties`；类型、枚举、范围和必填项必须原样遵守。
- UI 只能访问 `writeResultTo + outputSchema` 可推导路径；初始化数据必须是 outputSchema 的合法投影。
- 顶层输出路径：`/data/weather/location`, `/data/weather/current`, `/data/weather/daily`, `/data/weather/updatedAt`

## 原始能力声明

```json
{
  "id": "ViewWeather",
  "description": "查询指定地区的当前天气与未来数日天气预报。如果不能推断出用户的地区名，则需要追问用户提供。注意，当前不支持查询国外的天气。",
  "defaultWriteResultTo": "/data/weather",
  "dependencies": {
    "requiredPackages": [
      {
        "packageName": "com.huawei.hmsapp.totemweather"
      }
    ]
  },
  "inputSchema": {
    "type": "object",
    "properties": {
      "districtName": {
        "type": "string",
        "minLength": 1,
        "description": "区县名，如'滨江区'。可选。"
      },
      "prefectureName": {
        "type": "string",
        "minLength": 1,
        "description": "城市名，如'杭州市'。若不能根据用户query或上下文来推断出是哪个城市，则需要向用户发起追问，明确城市名。注意，部分区县对应多个城市，此时也需要让用户明确。"
      },
      "forecastDays": {
        "type": "integer",
        "minimum": 1,
        "maximum": 5,
        "description": "返回预报天数，支持1至5天；可选，不传时默认返回3天。"
      }
    },
    "required": [
      "prefectureName"
    ]
  },
  "outputSchema": {
    "type": "object",
    "description": "适合桌面卡片展示的标准化天气概要。current 是固定对象，daily 是数量由 forecastDays 决定的数组。",
    "properties": {
      "location": {
        "type": "object",
        "description": "实际查询成功的地区。",
        "properties": {
          "cityCode": {
            "type": "string",
            "description": "城市代码，如60814代表青浦区",
            "sampleValue": "60814"
          },
          "districtName": {
            "type": "string",
            "description": "区或县名称",
            "sampleValue": "青浦区"
          },
          "prefectureName": {
            "type": "string",
            "description": "城市名称",
            "sampleValue": "上海市"
          }
        }
      },
      "current": {
        "type": "object",
        "description": "当日天气实况",
        "properties": {
          "temperatureC": {
            "type": "number",
            "description": "当前摄氏温度。",
            "sampleValue": 29
          },
          "temperatureText": {
            "type": "string",
            "description": "适合直接显示的温度文本，例如“29°C”。",
            "sampleValue": "29°C"
          },
          "condition": {
            "type": "string",
            "description": "当前天气现象，例如“阴”“多云”“小雨”。",
            "sampleValue": "多云"
          },
          "feelsLikeC": {
            "type": "number",
            "description": "当前体感摄氏温度。",
            "sampleValue": 31
          },
          "humidityPercent": {
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "description": "当前相对湿度百分比。",
            "sampleValue": 68
          },
          "airQuality": {
            "type": "string",
            "description": "当前空气质量等级，例如“优”“良”。",
            "sampleValue": "良"
          },
          "windDirection": {
            "type": "string",
            "description": "当前风向。",
            "sampleValue": "东南风"
          },
          "windLevel": {
            "type": "integer",
            "minimum": 0,
            "description": "当前风力等级。",
            "sampleValue": 2
          },
          "uvIndex": {
            "type": "string",
            "description": "当前紫外线等级，例如“弱”“中等”“强”。",
            "sampleValue": "中等"
          },
          "coldLevel": {
            "type": "string",
            "description": "感冒指数。",
            "sampleValue": "低"
          },
          "alertLevel": {
            "type": "string",
            "description": "预警信息。",
            "sampleValue": ""
          }
        }
      },
      "daily": {
        "type": "array",
        "description": "从今天开始按日期升序排列的每日预报。",
        "items": {
          "type": "object",
          "properties": {
            "date": {
              "type": "string",
              "description": "预报日期，来源于 day_time。",
              "sampleValue": "2026-08-06"
            },
            "weekday": {
              "type": "string",
              "description": "星期文本，例如“星期日”。",
              "sampleValue": "星期四"
            },
            "condition": {
              "type": "string",
              "description": "白天天气现象，来源于weather_icon。",
              "sampleValue": "多云"
            },
            "temperatureRangeText": {
              "type": "string",
              "description": "适合直接显示的温度范围，例如“24° / 32°”。",
              "sampleValue": "25° / 32°"
            },
            "rainProbabilityPercent": {
              "type": "string",
              "description": "白天降雨概率百分比。如：73%",
              "sampleValue": "20%"
            },
            "airQuality": {
              "type": "string",
              "description": "当天空气质量等级。",
              "sampleValue": "良"
            },
            "uvIndex": {
              "type": "string",
              "description": "当天紫外线等级。",
              "sampleValue": "中等"
            },
            "coldLevel": {
              "type": "string",
              "description": "感冒指数。",
              "sampleValue": "低"
            }
          }
        }
      },
      "updatedAt": {
        "type": "string",
        "description": "端侧完成天气查询和归一化的时间。如：2026-06-14 15:30",
        "sampleValue": "2026-08-06 09:00"
      }
    }
  },
  "type": "data",
  "dataModelSkeleton": {}
}
```
