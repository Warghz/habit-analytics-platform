
class AppException(Exception):
    """Base app exception"""
    detail: str = "Application error"


class HabitNotFoundError(AppException):
    pass


class HabitAlreadyExistsError(AppException):
    pass


class ForbiddenError(AppException):
    pass