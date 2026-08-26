from __future__ import annotations

from .aesthetic.engine import (
    evaluate_fixed_skeleton,
    evaluate_layout_contracts,
    prepare_context,
)
from .base import BaseValidator


class DesignContractValidator(BaseValidator):
    """Enforce deterministic Design Compact layout contracts in hard stage."""

    stage = "hard"
    name = "design_contract"

    def validate(self, context, rules, reporter) -> None:
        if not context.dsl_messages:
            return
        aesthetic_context, _ = prepare_context(context.dsl_text)
        if aesthetic_context is None:
            # Protocol/Component validators own malformed-graph diagnostics.
            return
        size = (
            context.cardspec.get("suggestSize")
            if isinstance(context.cardspec, dict)
            else None
        )
        layout_rules = getattr(rules, "layout", {}) or {}
        diagnostics = evaluate_fixed_skeleton(
            aesthetic_context,
            suggest_size=size,
            layout_rules=layout_rules,
        )
        diagnostics.extend(
            evaluate_layout_contracts(
                aesthetic_context, suggest_size=size, layout_rules=layout_rules
            )
        )
        for item in diagnostics:
            code = item.get("code", "DESIGN_COMPACT_CONTRACT_INVALID")
            severity = (
                "warning"
                if code == "DESIGN_COMPACT_PRIMARY_REGION_RATIO"
                else "error"
            )
            reporter.add(
                severity,
                code,
                "hard",
                "genui",
                line=2,
                json_pointer=item.get("jsonPointer", ""),
                actual=item.get("actual"),
                expected=item.get("expected"),
                message=item.get("message", ""),
                fix_hint=item.get("fixHint", ""),
            )
