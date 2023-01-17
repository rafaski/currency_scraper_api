from enum import Enum


class ErrorTypes(str, Enum):
    """
    Custom error types for exception handling
    """

    # APP errors
    UNKNOWN = "unknown"

    # API errors
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    BAD_REQUEST = "bad_request"

    # Forex errors
    FOREX_ERROR = "forex_error"

