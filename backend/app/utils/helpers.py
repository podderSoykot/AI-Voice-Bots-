"""Utility helper functions."""
from typing import Any, Dict
from datetime import datetime


def format_datetime(dt: datetime) -> str:
    """Format datetime to ISO string."""
    return dt.isoformat() if dt else None


def sanitize_phone_number(phone: str) -> str:
    """Sanitize phone number by removing non-digit characters."""
    return ''.join(filter(str.isdigit, phone))


def validate_phone_number(phone: str) -> bool:
    """Validate phone number format."""
    cleaned = sanitize_phone_number(phone)
    return len(cleaned) >= 10 and len(cleaned) <= 15


def build_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """Build standardized API response."""
    return {
        "success": True,
        "message": message,
        "data": data
    }


def build_error_response(message: str, errors: Dict[str, Any] = None) -> Dict[str, Any]:
    """Build standardized error response."""
    response = {
        "success": False,
        "message": message
    }
    if errors:
        response["errors"] = errors
    return response

