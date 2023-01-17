from enum import Enum


class ErrorTypes(str, Enum):
    """
    Custom error types for exception handling
    """

    # APP errors
    UNKNOWN = "unknown"

    # API errors
    UNAUTHORIZED = "unauthorized"
    BAD_REQUEST = "bad_request"

    # Forex errors
    CONVERTER_ERROR = "converter_error"

