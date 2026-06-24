from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.project_place import ProjectPlace
from app.models.travel_project import TravelProject


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, project: TravelProject) -> TravelProject:
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project


    async def get_by_id(self, project_id: int) -> TravelProject | None:
        result = await self.db.execute(
            select(TravelProject).where(TravelProject.id == project_id)
        )
        return result.scalar_one_or_none()


    async def get_by_id_for_user(
        self,
        project_id: int,
        user_id: int,
    ) -> TravelProject | None:
        
        result = await self.db.execute(
            select(TravelProject).where(
                TravelProject.id == project_id,
                TravelProject.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()


    async def get_detail_for_user(
        self,
        project_id: int,
        user_id: int,
    ) -> TravelProject | None:
        
        result = await self.db.execute(
            select(TravelProject)
            .options(selectinload(TravelProject.places))
            .where(
                TravelProject.id == project_id,
                TravelProject.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()


    async def list_by_user(self, user_id: int) -> list[TravelProject]:
        result = await self.db.execute(
            select(TravelProject)
            .where(TravelProject.user_id == user_id)
            .order_by(TravelProject.created_at.desc())
        )
        return list(result.scalars().all())


    async def update(
        self,
        project: TravelProject,
        data: dict[str, Any],
    ) -> TravelProject:
        
        for field, value in data.items():
            setattr(project, field, value)

        await self.db.flush()
        await self.db.refresh(project)

        return project


    async def delete(self, project: TravelProject) -> None:
        await self.db.delete(project)
        await self.db.flush()


    async def has_visited_places(self, project_id: int) -> bool:
        result = await self.db.execute(
            select(ProjectPlace.id)
            .where(
                ProjectPlace.project_id == project_id,
                ProjectPlace.is_visited.is_(True),
            )
            .limit(1)
        )
        return result.scalar_one_or_none() is not None


    async def set_completed(
        self,
        project: TravelProject,
        is_completed: bool,
    ) -> TravelProject:
        
        project.is_completed = is_completed

        await self.db.flush()
        await self.db.refresh(project)

        return project



