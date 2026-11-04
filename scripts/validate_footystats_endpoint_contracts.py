#!/usr/bin/env python3
"""Strict offline validators for documented FootyStats endpoint response contracts."""
from __future__ import annotations
import math
from typing import Any

PAGED_ENDPOINTS = {"league-matches", "league-teams"}
SINGLE_ENDPOINT_SHAPES = {
    "league-tables": (dict,),
    "league-season": (dict, list),
    "match": (dict,),
}

def _positive_int(value: Any, field: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be an integer")
    try:
        number = int(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{field} must be an integer") from exc
    if str(value).strip() not in {str(number), f"{number}.0"} or number < 1:
        raise ValueError(f"{field} must be a positive integer")
    return number

def validate_paged_response(endpoint: str, payload: dict[str, Any], requested_page: int) -> dict[str, Any]:
    """Require explicit page/total metadata and an exact expected row count."""
    if endpoint not in PAGED_ENDPOINTS:
        raise ValueError(f"unsupported paged endpoint: {endpoint}")
    page = _positive_int(requested_page, "requested_page")
    if not isinstance(payload, dict) or payload.get("success") is not True:
        raise ValueError(f"{endpoint} response must have success=true")
    data = payload.get("data")
    if not isinstance(data, list):
        raise ValueError(f"{endpoint} data must be a list")
    pager = payload.get("pager")
    if not isinstance(pager, dict):
        raise ValueError(f"{endpoint} pager metadata is required for completeness")
    current_raw = pager.get("current_page", pager.get("page"))
    per_page_raw = pager.get("results_per_page", pager.get("per_page"))
    total_raw = pager.get("total_results")
    current = _positive_int(current_raw, "pager.current_page/page")
    per_page = _positive_int(per_page_raw, "pager.results_per_page/per_page")
    if isinstance(total_raw, bool):
        raise ValueError("pager.total_results must be a non-negative integer")
    try:
        total = int(total_raw)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("pager.total_results must be a non-negative integer") from exc
    if str(total_raw).strip() not in {str(total), f"{total}.0"} or total < 0:
        raise ValueError("pager.total_results must be a non-negative integer")
    if current != page:
        raise ValueError(f"requested page {page} does not match provider page {current}")
    expected_pages = max(1, math.ceil(total / per_page))
    max_page_raw = pager.get("max_page")
    if max_page_raw not in (None, ""):
        max_page = _positive_int(max_page_raw, "pager.max_page")
        if max_page != expected_pages:
            raise ValueError(f"pager.max_page={max_page} conflicts with total_results/per_page={expected_pages}")
    if current > expected_pages:
        raise ValueError(f"provider page {current} exceeds expected page count {expected_pages}")
    expected_count = max(0, min(per_page, total - ((current - 1) * per_page)))
    if len(data) != expected_count:
        raise ValueError(
            f"{endpoint} page {current} returned {len(data)} rows; expected {expected_count} "
            f"from total_results={total} and per_page={per_page}"
        )
    return {
        "endpoint": endpoint,
        "requested_page": page,
        "provider_page": current,
        "per_page": per_page,
        "total_results": total,
        "expected_page_count": expected_pages,
        "returned_rows": len(data),
        "page_complete": True,
        "has_more": current < expected_pages,
        "next_page": current + 1 if current < expected_pages else None,
        "pagination_status": "PAGE_COUNT_AND_ROW_COUNT_VERIFIED",
    }

def validate_single_response(endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
    if endpoint not in SINGLE_ENDPOINT_SHAPES:
        raise ValueError(f"unsupported single-response endpoint: {endpoint}")
    if not isinstance(payload, dict) or payload.get("success") is not True:
        raise ValueError(f"{endpoint} response must have success=true")
    data = payload.get("data")
    if not isinstance(data, SINGLE_ENDPOINT_SHAPES[endpoint]):
        allowed = ", ".join(shape.__name__ for shape in SINGLE_ENDPOINT_SHAPES[endpoint])
        raise ValueError(f"{endpoint} data must have documented shape: {allowed}")
    return {
        "endpoint": endpoint,
        "data_shape": "dict" if isinstance(data, dict) else "list",
        "response_status": "SUCCESS_SHAPE_VERIFIED",
        "pagination_status": "NOT_PAGINATED_BY_DOCUMENTED_CONTRACT",
    }
