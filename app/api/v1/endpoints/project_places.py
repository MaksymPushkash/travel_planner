from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.project_place import (
    ProjectPlaceCreate,
    ProjectPlaceRead,
    ProjectPlaceUpdate,
)
from app.services.project_place_service import ProjectPlaceService

router = APIRouter()


@router.post(
    "/{project_id}/places",
    response_model=ProjectPlaceRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_place(
    project_id: int,
    data: ProjectPlaceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await ProjectPlaceService(db).add_place(
        project_id=project_id,
        user_id=current_user.id,
        data=data,
    )


@router.get("/{project_id}/places", response_model=list[ProjectPlaceRead])
async def list_places(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await ProjectPlaceService(db).list_places(
        project_id=project_id,
        user_id=current_user.id,
    )


@router.get("/{project_id}/places/{place_id}", response_model=ProjectPlaceRead)
async def get_place(
    project_id: int,
    place_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await ProjectPlaceService(db).get_place(
        project_id=project_id,
        place_id=place_id,
        user_id=current_user.id,
    )


@router.patch("/{project_id}/places/{place_id}", response_model=ProjectPlaceRead)
async def update_place(
    project_id: int,
    place_id: int,
    data: ProjectPlaceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await ProjectPlaceService(db).update_place(
        project_id=project_id,
        place_id=place_id,
        user_id=current_user.id,
        data=data,
    )



