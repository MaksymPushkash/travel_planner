from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.art_institute_client import ArtInstituteClient
from app.core.exceptions import (
    DuplicatePlaceError,
    ExternalPlaceNotFoundError,
    PlaceNotFoundError,
    ProjectNotFoundError,
    ProjectPlacesLimitError,
)
from app.models.project_place import ProjectPlace
from app.repositories.project_place_repo import ProjectPlaceRepository
from app.repositories.project_repo import ProjectRepository
from app.schemas.project_place import ProjectPlaceCreate, ProjectPlaceUpdate

MAX_PLACES_PER_PROJECT = 10


class ProjectPlaceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.projects = ProjectRepository(db)
        self.places = ProjectPlaceRepository(db)
        self.art_client = ArtInstituteClient()

    async def add_place(
        self,
        project_id: int,
        user_id: int,
        data: ProjectPlaceCreate,
    ) -> ProjectPlace:
        
        project = await self.projects.get_by_id_for_user(
            project_id=project_id,
            user_id=user_id,
        )

        if project is None:
            raise ProjectNotFoundError()

        places_count = await self.places.count_by_project(project_id)

        if places_count >= MAX_PLACES_PER_PROJECT:
            raise ProjectPlacesLimitError()

        already_exists = await self.places.exists_by_external_id(
            project_id=project_id,
            external_place_id=data.external_place_id,
        )

        if already_exists:
            raise DuplicatePlaceError()

        artwork = await self.art_client.get_artwork_by_id(data.external_place_id)

        if artwork is None:
            raise ExternalPlaceNotFoundError()

        place = ProjectPlace(
            project_id=project_id,
            external_place_id=artwork["external_place_id"],
            title=artwork["title"],
            artist_title=artwork.get("artist_title"),
            image_url=artwork.get("image_url"),
            notes=data.notes,
        )

        place = await self.places.create(place)

        await self.db.commit()
        await self.db.refresh(place)

        return place


    async def list_places(
        self,
        project_id: int,
        user_id: int,
    ) -> list[ProjectPlace]:
        
        project = await self.projects.get_by_id_for_user(
            project_id=project_id,
            user_id=user_id,
        )

        if project is None:
            raise ProjectNotFoundError()

        return await self.places.list_by_project(project_id)


    async def get_place(
        self,
        project_id: int,
        place_id: int,
        user_id: int,
    ) -> ProjectPlace:
        
        project = await self.projects.get_by_id_for_user(
            project_id=project_id,
            user_id=user_id,
        )

        if project is None:
            raise ProjectNotFoundError()

        place = await self.places.get_by_id_for_project(
            place_id=place_id,
            project_id=project_id,
        )

        if place is None:
            raise PlaceNotFoundError("Place not found")

        return place


    async def update_place(
        self,
        project_id: int,
        place_id: int,
        user_id: int,
        data: ProjectPlaceUpdate,
    ) -> ProjectPlace:
        
        project = await self.projects.get_by_id_for_user(
            project_id=project_id,
            user_id=user_id,
        )

        if project is None:
            raise ProjectNotFoundError()

        place = await self.places.get_by_id_for_project(
            place_id=place_id,
            project_id=project_id,
        )

        if place is None:
            raise PlaceNotFoundError("Place not found")

        update_data = data.model_dump(exclude_unset=True)

        place = await self.places.update(place, update_data)

        all_visited = await self.places.all_places_visited(project_id)

        await self.projects.set_completed(
            project=project,
            is_completed=all_visited,
        )

        await self.db.commit()
        await self.db.refresh(place)

        return place



