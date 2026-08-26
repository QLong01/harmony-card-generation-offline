# 系统内存能力

```json
{
  "id": "GetSystemMemInfo",
  "inputSchema": {
    "type": "object",
    "properties": {},
    "required": [],
    "additionalProperties": false
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "totalMemText": {"type": "string"},
      "freeMemText": {"type": "string"},
      "availableMemText": {"type": "string"},
      "usagePercent": {"type": "number"}
    }
  }
}
```

## 使用规则

- 适用于系统总内存、空闲/可用内存和内存占用比例。
- CardSpec 使用 `capabilityId: "GetSystemMemInfo"`，`arguments: {}`，推荐 `writeResultTo: "/data/systemMem"`。
- UI 路径只使用 `/data/systemMem/totalMemText`、`freeMemText`、`availableMemText`、`usagePercent`。
- 2x2 只选择一个主问题：占用比例或清理状态。占用比例可用 56–72vp 环形图，stroke 为直径 14%–15%；不要同时展示全部字段。
- 初始 DataModel 可以使用合法示例值，但字段名和类型必须严格符合上方 `outputSchema`。
