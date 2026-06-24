from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    DuplicatePlaceError,
    ExternalPlaceNotFoundError,
    InvalidCredentialsError,
    InvalidProjectPlacesError,
    PlaceNotFoundError,
    ProjectDeleteForbiddenError,
    ProjectNotFoundError,
    ProjectPlacesLimitError,
    UserAlreadyExistsError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserAlreadyExistsError)
    async def user_already_exists_handler(
        request: Request,
        exc: UserAlreadyExistsError,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": exc.message},
        )


    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_handler(
        request: Request,
        exc: InvalidCredentialsError,
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.message},
        )


    @app.exception_handler(ProjectNotFoundError)
    async def project_not_found_handler(
        request: Request,
        exc: ProjectNotFoundError,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message},
        )


    @app.exception_handler(PlaceNotFoundError)
    async def place_not_found_handler(
        request: Request,
        exc: PlaceNotFoundError,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message},
        )


    @app.exception_handler(ExternalPlaceNotFoundError)
    async def external_place_not_found_handler(
        request: Request,
        exc: ExternalPlaceNotFoundError,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message},
        )


    @app.exception_handler(DuplicatePlaceError)
    async def duplicate_place_handler(
        request: Request,
        exc: DuplicatePlaceError,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": exc.message},
        )


    @app.exception_handler(ProjectPlacesLimitError)
    async def project_places_limit_handler(
        request: Request,
        exc: ProjectPlacesLimitError,
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )


    @app.exception_handler(ProjectDeleteForbiddenError)
    async def project_delete_forbidden_handler(
        request: Request,
        exc: ProjectDeleteForbiddenError,
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )


    @app.exception_handler(InvalidProjectPlacesError)
    async def invalid_project_places_handler(
        request: Request,
        exc: InvalidProjectPlacesError,
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )



