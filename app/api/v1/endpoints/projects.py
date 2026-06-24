from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.travel_project import (
    TravelProjectCreate,
    TravelProjectDetail,
    TravelProjectRead,
    TravelProjectUpdate,
)
from app.services.project_service import ProjectService

router = APIRouter()


@router.post(
    "",
    response_model=TravelProjectDetail,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    data: TravelProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await ProjectService(db).create_project(
        data=data,
        user_id=current_user.id,
    )


@router.get("", response_model=list[TravelProjectRead])
async def list_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await ProjectService(db).list_projects(user_id=current_user.id)


@router.get("/{project_id}", response_model=TravelProjectDetail)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await ProjectService(db).get_project(
        project_id=project_id,
        user_id=current_user.id,
    )


@router.patch("/{project_id}", response_model=TravelProjectRead)
async def update_project(
    project_id: int,
    data: TravelProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await ProjectService(db).update_project(
        project_id=project_id,
        user_id=current_user.id,
        data=data,
    )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await ProjectService(db).delete_project(
        project_id=project_id,
        user_id=current_user.id,
    )
