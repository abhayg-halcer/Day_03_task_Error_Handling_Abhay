"""Custom exceptions for the data toolkit."""


class DataToolkitError(Exception):
    """Base exception for application errors."""


class FileAccessError(DataToolkitError):
    """Raised when a CSV file cannot be accessed."""


class FileFormatError(DataToolkitError):
    """Raised when a CSV file is malformed."""


class SchemaValidationError(DataToolkitError):
    """Raised when required CSV columns are missing."""


class DataValidationError(DataToolkitError):
    """Raised when a record contains invalid values."""
