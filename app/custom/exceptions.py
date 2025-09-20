"""custom exceptions for the application."""


class AppExceptionError(Exception):
    """Base exception with adapter support."""

    default_message: str = "An application error occurred."
    status_code: int = 500

    def __init__(
        self,
        message: str | None = None,
        name: str = "TRIMMER",
        context: dict | None = None,
        cause: Exception | None = None,
    ):
        self.message = message or self.default_message
        self.name = name
        self.context = context or {}
        self.__cause__ = cause
        super().__init__(self.message)


class MemberGenericError(AppExceptionError):
    """Base exception for member-related errors."""

    default_message: str = "A member error occurred."
    status_code: int = 400


class MemberAlreadyExistsError(MemberGenericError):
    """Exception raised when a member already exists."""

    default_message: str = "Member already exists."
    status_code: int = 400


class MemberNotFoundError(MemberGenericError):
    """Exception raised when a member is not found."""

    default_message: str = "Member not found."
    status_code: int = 404
