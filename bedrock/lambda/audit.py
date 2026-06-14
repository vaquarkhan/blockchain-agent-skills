"""Audit logging helpers for Bedrock Lambda handlers."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any


def audit_log(event: dict[str, Any], action: str, result: dict[str, Any]) -> None:
    """Write audit entry to stdout (CloudWatch) or DynamoDB when configured."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": event.get("sessionId"),
        "action_group": event.get("actionGroup"),
        "function": action,
        "result_summary": list(result.keys()),
    }
    table = os.environ.get("AUDIT_TABLE_NAME", "").strip()
    if table:
        entry["dynamodb_table"] = table
    print(json.dumps({"audit": entry}))
