from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project_place import ProjectPlace


class ProjectPlaceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, place: ProjectPlace) -> ProjectPlace:
        self.db.add(place)
        await self.db.flush()
        await self.db.refresh(place)
        return place

    async def get_by_id(self, place_id: int) -> ProjectPlace | None:
        result = await self.db.execute(
            select(ProjectPlace)
            .where(ProjectPlace.id == place_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id_for_project(
        self,
        place_id: int,
        project_id: int,
    ) -> ProjectPlace | None:

        result = await self.db.execute(
            select(ProjectPlace).where(
                ProjectPlace.id == place_id,
                ProjectPlace.project_id == project_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_project(self, project_id: int) -> list[ProjectPlace]:
        result = await self.db.execute(
            select(ProjectPlace)
            .where(ProjectPlace.project_id == project_id)
            .order_by(ProjectPlace.created_at.desc())
        )
        return list(result.scalars().all())

    async def count_by_project(self, project_id: int) -> int:
        result = await self.db.execute(
            select(func.count(ProjectPlace.id))
            .where(ProjectPlace.project_id == project_id)
        )
        return result.scalar_one()

    async def exists_by_external_id(
        self,
        project_id: int,
        external_place_id: int,
    ) -> bool:

        result = await self.db.execute(
            select(ProjectPlace.id)
            .where(
                ProjectPlace.project_id == project_id,
                ProjectPlace.external_place_id == external_place_id,
            )
            .limit(1)
        )
        return result.scalar_one_or_none() is not None

    async def update(
        self,
        place: ProjectPlace,
        data: dict[str, Any],
    ) -> ProjectPlace:

        for field, value in data.items():
            setattr(place, field, value)

        await self.db.flush()
        await self.db.refresh(place)

        return place

    async def all_places_visited(self, project_id: int) -> bool:
        total_result = await self.db.execute(
            select(func.count(ProjectPlace.id))
            .where(ProjectPlace.project_id == project_id)
        )
        total_places = total_result.scalar_one()

        if total_places == 0:
            return False

        unvisited_result = await self.db.execute(
            select(ProjectPlace.id)
            .where(
                ProjectPlace.project_id == project_id,
                ProjectPlace.is_visited.is_(False),
            )
            .limit(1)
        )

        return unvisited_result.scalar_one_or_none() is None
