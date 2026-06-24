class AppError(Exception):
    message = "Application error"

    def __init__(self, message: str | None = None):
        self.message = message or self.message
        super().__init__(self.message)


class UserAlreadyExistsError(AppError):
    message = "User with this email already exists"


class InvalidCredentialsError(AppError):
    message = "Invalid email or password"


class ProjectNotFoundError(AppError):
    message = "Project not found"


class ProjectDeleteForbiddenError(AppError):
    message = "Project cannot be deleted because it has visited places"


class DuplicatePlaceError(AppError):
    message = "This place already exists in the project"


class ProjectPlacesLimitError(AppError):
    message = "Project cannot have more than 10 places"


class ExternalPlaceNotFoundError(AppError):
    message = "Place not found in external API"


class InvalidProjectPlacesError(AppError):
    message = "Duplicate places are not allowed"


class PlaceNotFoundError(AppError):
    message = "Place not found"
