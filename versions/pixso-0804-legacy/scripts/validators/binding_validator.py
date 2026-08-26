from __future__ import annotations

from typing import Any

from .base import BaseValidator, expression_references, is_json_pointer, read_pointer, schema_path_exists
from .capability_schema import contains_binding, schema_errors


class BindingValidator(BaseValidator):
    stage = "semantic"
    name = "binding"

    def validate(self, context, rules, reporter) -> None:
        self._check_capability_arguments(context, rules, reporter)
        self._check_template_paths(context, rules, reporter)
        self._check_expression_paths(context, rules, reporter)
        if not getattr(context, "use_effective_capabilities", False):
            self._check_event_handlers(context, rules, reporter)

    def _check_capability_arguments(self, context, rules, reporter) -> None:
        bindings = context.cardspec.get("dataBindings")
        if not isinstance(bindings, list):
            return
        for index, binding in enumerate(bindings):
            if not isinstance(binding, dict):
                continue
            pointer = f"/dataBindings/{index}"
            capability_id = binding.get("capabilityId")
            capability = self._capability_for_binding(binding, context, rules)
            if capability is None:
                if getattr(context, "use_effective_capabilities", False):
                    # EffectiveCapabilityValidator owns membership diagnostics.
                    # A bare id without a resolved manifest has no schema to check.
                    continue
                reporter.add(
                    "error",
                    "CARD_CAPABILITY_UNKNOWN",
                    "semantic",
                    "cardspec",
                    json_pointer=f"{pointer}/capabilityId",
                    actual=capability_id,
                    expected=sorted(rules.capabilities.keys()),
                    message="capabilityId 必须来自已声明 data capability。",
                )
                continue
            arguments = binding.get("arguments")
            input_schema = capability.get("inputSchema", {})
            properties = input_schema.get("properties", {})
            required = set(input_schema.get("required", []))
            if not isinstance(arguments, dict):
                reporter.add("error", "CARD_ARGUMENT_UNKNOWN", "semantic", "cardspec", json_pointer=f"{pointer}/arguments", actual=arguments, message="arguments 必须是 object。")
                continue
            extra = sorted(set(arguments.keys()) - set(properties.keys()))
            missing = sorted(required - set(arguments.keys()))
            if extra:
                reporter.add("error", "CARD_ARGUMENT_UNKNOWN", "semantic", "cardspec", json_pointer=f"{pointer}/arguments", actual=extra, expected=sorted(properties.keys()), message="arguments 包含 capability 未声明的字段。")
            if missing:
                reporter.add("error", "CARD_ARGUMENT_UNKNOWN", "semantic", "cardspec", json_pointer=f"{pointer}/arguments", actual=arguments, expected=missing, message="arguments 缺少 capability 必填字段。")
            if self._contains_binding(arguments):
                reporter.add("error", "CARD_ARGUMENT_UNKNOWN", "semantic", "cardspec", json_pointer=f"{pointer}/arguments", actual=arguments, message="arguments 是端侧能力静态入参，不能写 DSL 表达式或绑定对象。")
            schema_errors = self._schema_errors(arguments, input_schema)
            if schema_errors:
                reporter.add(
                    "error",
                    "CARD_ARGUMENT_SCHEMA_INVALID",
                    "semantic",
                    "cardspec",
                    json_pointer=f"{pointer}/arguments",
                    actual={"arguments": arguments, "errors": schema_errors[:20]},
                    expected=input_schema,
                    message="arguments 的类型、枚举或数值范围不符合 data capability inputSchema。",
                )
            preferred = capability.get("preferredWriteResultTo") or capability.get(
                "defaultWriteResultTo"
            )
            if preferred and binding.get("writeResultTo") != preferred:
                reporter.add("warning", "CARD_WRITE_RESULT_PATH_INVALID", "semantic", "cardspec", json_pointer=f"{pointer}/writeResultTo", actual=binding.get("writeResultTo"), expected=preferred, message="该 capability 建议写入约定的 DataModel 根路径。")

    def _contains_binding(self, value: Any) -> bool:
        return contains_binding(value)

    def _check_template_paths(self, context, rules, reporter) -> None:
        for component in context.components:
            children = component.get("children")
            if not isinstance(children, dict):
                continue
            path = children.get("path")
            if not is_json_pointer(path):
                continue
            if self._path_is_array(path, context, rules):
                continue
            reporter.add(
                "error",
                "BINDING_TEMPLATE_PATH_NOT_ARRAY",
                "semantic",
                "genui",
                line=2,
                json_pointer=f"/updateComponents/componentsById/{component.get('id')}/children/path",
                actual=path,
                message="模板 children.path 必须指向数组。",
                fix_hint="确认 updateDataModel.value 中该路径初始化为 []，或 CardSpec outputSchema 中该路径是 array。",
            )

    def _check_expression_paths(self, context, rules, reporter) -> None:
        for file_kind, pointer, value, component_id in context.expression_locations:
            if file_kind != "genui":
                continue
            template_context = context.template_context_by_component.get(component_id or "")
            for ref in expression_references(value):
                if ref.startswith("/"):
                    if self._absolute_path_exists(ref, context, rules):
                        continue
                    reporter.add(
                        "error",
                        "BINDING_PATH_NOT_FOUND",
                        "semantic",
                        "genui",
                        line=2,
                        json_pointer=pointer,
                        actual=ref,
                        message="表达式引用的 DataModel 路径无法从 updateDataModel 或 CardSpec outputSchema 推导。",
                        fix_hint="初始化该路径，或改为 writeResultTo + outputSchema 中存在的字段。",
                    )
                else:
                    if template_context and self._relative_path_exists(ref, template_context["path"], context, rules):
                        continue
                    if template_context:
                        reporter.add(
                            "warning",
                            "BINDING_PATH_NOT_FOUND",
                            "semantic",
                            "genui",
                            line=2,
                            json_pointer=pointer,
                            actual=ref,
                            message="模板相对字段未能从样例数据或 outputSchema 明确推导。",
                            fix_hint="确认模板数组项中存在该字段，或改用已声明字段。",
                        )
                    else:
                        reporter.add(
                            "error",
                            "BINDING_PATH_NOT_FOUND",
                            "semantic",
                            "genui",
                            line=2,
                            json_pointer=pointer,
                            actual=ref,
                            message="相对表达式只能用于模板项子树内。",
                        )

    def _check_event_handlers(self, context, rules, reporter) -> None:
        self._check_manifest_event_handlers(context, rules, reporter)

    def _check_manifest_event_handlers(self, context, rules, reporter) -> None:
        capabilities = rules.event_capabilities
        calls = sorted(
            {
                item.get("actionTemplate", {}).get("call")
                for item in capabilities
                if isinstance(item.get("actionTemplate"), dict)
                and isinstance(item.get("actionTemplate", {}).get("call"), str)
            }
        )
        for component in context.components:
            handlers = component.get("onClick")
            if handlers is None or not isinstance(handlers, list):
                continue
            for index, handler in enumerate(handlers):
                if not isinstance(handler, dict):
                    continue
                pointer = f"/updateComponents/componentsById/{component.get('id')}/onClick/{index}"
                call = handler.get("call")
                args = handler.get("args", {})
                candidates = [
                    item
                    for item in capabilities
                    if isinstance(item.get("actionTemplate"), dict)
                    and item["actionTemplate"].get("call") == call
                ]
                if not candidates:
                    reporter.add(
                        "error",
                        "EVENT_CAPABILITY_UNKNOWN",
                        "semantic",
                        "genui",
                        line=2,
                        json_pointer=f"{pointer}/call",
                        actual=call,
                        expected=calls,
                        message="onClick.call 必须来自当前事件能力清单。",
                    )
                    continue
                if not isinstance(args, dict):
                    reporter.add(
                        "error",
                        "EVENT_ARGUMENT_INVALID",
                        "semantic",
                        "genui",
                        line=2,
                        json_pointer=f"{pointer}/args",
                        actual=args,
                        message="EventHandler.args 必须是 object。",
                    )
                    continue
                matching_ids: list[str] = []
                candidate_errors: dict[str, list[str]] = {}
                for candidate in candidates:
                    dynamic_paths = {
                        item.get("path")
                        for item in candidate.get("dynamicArguments", [])
                        if isinstance(item, dict) and isinstance(item.get("path"), str)
                    }
                    errors = self._schema_errors(
                        args,
                        candidate.get("parametersSchema", {}),
                        dynamic_paths=dynamic_paths,
                    )
                    candidate_id = str(candidate.get("id", "<unknown>"))
                    if errors:
                        candidate_errors[candidate_id] = errors[:10]
                    else:
                        matching_ids.append(candidate_id)
                if matching_ids:
                    continue
                reporter.add(
                    "error",
                    "EVENT_ARGUMENT_INVALID",
                    "semantic",
                    "genui",
                    line=2,
                    json_pointer=f"{pointer}/args",
                    actual={"call": call, "args": args, "mismatches": candidate_errors},
                    expected={"eventCapabilityIds": [str(item.get("id")) for item in candidates]},
                    message="onClick 与当前事件能力的 actionTemplate/parametersSchema 均不匹配。",
                )

    def _schema_errors(
        self,
        value: Any,
        schema: Any,
        path: str = "",
        *,
        dynamic_paths: set[str] | None = None,
    ) -> list[str]:
        return schema_errors(value, schema, path, dynamic_paths=dynamic_paths)

    def _absolute_path_exists(self, pointer: str, context, rules) -> bool:
        ok, _ = read_pointer(context.data_model, pointer)
        if ok:
            return True
        for binding in context.cardspec.get("dataBindings", []) if isinstance(context.cardspec.get("dataBindings"), list) else []:
            if not isinstance(binding, dict):
                continue
            root = binding.get("writeResultTo")
            capability = self._capability_for_binding(binding, context, rules)
            if not is_json_pointer(root) or capability is None:
                if getattr(context, "use_effective_capabilities", False) and self._path_under_root(pointer, root):
                    return True
                continue
            root = root.rstrip("/")
            if pointer == root or pointer.startswith(root + "/"):
                relative = "/" + pointer[len(root):].strip("/")
                if relative == "/":
                    return True
                if schema_path_exists(capability.get("outputSchema", {}), relative):
                    return True
        return False

    def _relative_path_exists(self, ref: str, template_path: str, context, rules) -> bool:
        ok, array_value = read_pointer(context.data_model, template_path)
        if ok and isinstance(array_value, list):
            if not array_value:
                return True
            first = array_value[0]
            return read_pointer(first, "/" + ref)[0] if isinstance(first, dict) else False
        for binding in context.cardspec.get("dataBindings", []) if isinstance(context.cardspec.get("dataBindings"), list) else []:
            root = binding.get("writeResultTo")
            capability = self._capability_for_binding(binding, context, rules)
            if not is_json_pointer(root) or capability is None:
                if getattr(context, "use_effective_capabilities", False) and self._path_under_root(template_path, root):
                    return True
                continue
            root = root.rstrip("/")
            if template_path == root or template_path.startswith(root + "/"):
                relative = "/" + template_path[len(root):].strip("/")
                item_relative = relative + "/0/" + ref
                if schema_path_exists(capability.get("outputSchema", {}), item_relative):
                    return True
        return False

    def _path_is_array(self, pointer: str, context, rules) -> bool:
        ok, value = read_pointer(context.data_model, pointer)
        if ok:
            return isinstance(value, list)
        for binding in context.cardspec.get("dataBindings", []) if isinstance(context.cardspec.get("dataBindings"), list) else []:
            root = binding.get("writeResultTo")
            capability = self._capability_for_binding(binding, context, rules)
            if not is_json_pointer(root) or capability is None:
                if getattr(context, "use_effective_capabilities", False) and self._path_under_root(pointer, root):
                    return True
                continue
            root = root.rstrip("/")
            if pointer == root or pointer.startswith(root + "/"):
                relative = "/" + pointer[len(root):].strip("/")
                schema = capability.get("outputSchema", {})
                return self._schema_type(schema, relative) == "array"
        return False

    def _capability_for_binding(self, binding: dict[str, Any], context, rules) -> dict[str, Any] | None:
        capability_id = binding.get("capabilityId")
        if getattr(context, "use_effective_capabilities", False):
            capability = context.effective_data_capabilities.get(capability_id)
            return capability if isinstance(capability, dict) else None
        capability = rules.capabilities.get(capability_id)
        return capability if isinstance(capability, dict) else None

    def _path_under_root(self, pointer: str, root: Any) -> bool:
        if not is_json_pointer(pointer) or not is_json_pointer(root):
            return False
        root = str(root).rstrip("/")
        return pointer == root or pointer.startswith(root + "/")

    def _schema_type(self, schema: dict[str, Any], pointer: str) -> str | None:
        current = schema
        if pointer == "/":
            return current.get("type")
        for raw_part in pointer.strip("/").split("/"):
            if current.get("type") == "array":
                current = current.get("items", {})
                if raw_part.isdigit():
                    continue
            properties = current.get("properties", {})
            if raw_part not in properties:
                return None
            current = properties[raw_part]
        return current.get("type")
