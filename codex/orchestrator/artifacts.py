from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from typing import Any


def artifact_to_dict(obj: Any) -> dict[str, Any]:
    if not is_dataclass(obj):
        raise TypeError("artifact must be a dataclass instance")
    return asdict(obj)


def artifact_to_json(obj: Any) -> str:
    return json.dumps(artifact_to_dict(obj), ensure_ascii=False, indent=2)
