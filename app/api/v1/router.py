from fastapi import APIRouter

from app.api.v1.endpoints import auth, project_places, projects

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)

api_router.include_router(
    projects.router,
    prefix="/projects",
    tags=["projects"],
)

api_router.include_router(
    project_places.router,
    prefix="/projects",
    tags=["project places"],
)
