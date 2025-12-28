"""
Shared utilities for the Product Review Engine.
"""

from datetime import datetime
from typing import Any
from pydantic import BaseModel

def model_to_jsonable(obj: Any) -> Any:
    """Convert Pydantic models and other objects to JSON-serializable data.

    Uses Pydantic v2's ``model_dump(mode="json")`` so datetimes and other
    special types become JSON-safe primitives.
    """
    if isinstance(obj, BaseModel):
        # mode="json" ensures datetime and similar types are serialized properly
        return obj.model_dump(mode="json")
    if isinstance(obj, list):
        return [model_to_jsonable(x) for x in obj]
    if isinstance(obj, dict):
        return {k: model_to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj
