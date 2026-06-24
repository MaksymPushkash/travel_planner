from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.art_institute_client import ArtInstituteClient
from app.core.exceptions import (
    ExternalPlaceNotFoundError,
    InvalidProjectPlacesError,
    ProjectDeleteForbiddenError,
    ProjectNotFoundError,
)
from app.models.project_place import ProjectPlace
from app.models.travel_project import TravelProject
from app.repositories.project_place_repo import ProjectPlaceRepository
from app.repositories.project_repo import ProjectRepository
from app.schemas.travel_project import TravelProjectCreate, TravelProjectUpdate


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.projects = ProjectRepository(db)
        self.places = ProjectPlaceRepository(db)
        self.art_client = ArtInstituteClient()

    async def create_project(
        self,
        data: TravelProjectCreate,
        user_id: int,
    ) -> TravelProject:
        
        external_ids = [place.external_place_id for place in data.places]

        if len(external_ids) != len(set(external_ids)):
            raise InvalidProjectPlacesError()

        artworks = []

        for place_data in data.places:
            artwork = await self.art_client.get_artwork_by_id(
                place_data.external_place_id
            )

            if artwork is None:
                raise ExternalPlaceNotFoundError(
                    f"Place {place_data.external_place_id} not found in external API"
                )

            artworks.append((place_data, artwork))

        project = TravelProject(
            user_id=user_id,
            name=data.name,
            description=data.description,
            start_date=data.start_date,
        )

        project = await self.projects.create(project)

        for place_data, artwork in artworks:
            place = ProjectPlace(
                project_id=project.id,
                external_place_id=artwork["external_place_id"],
                title=artwork["title"],
                artist_title=artwork.get("artist_title"),
                image_url=artwork.get("image_url"),
                notes=place_data.notes,
            )

            await self.places.create(place)

        await self.db.commit()

        return await self.get_project(project.id, user_id)


    async def list_projects(self, user_id: int) -> list[TravelProject]:
        return await self.projects.list_by_user(user_id)


    async def get_project(
        self,
        project_id: int,
        user_id: int,
    ) -> TravelProject:
        
        project = await self.projects.get_detail_for_user(
            project_id=project_id,
            user_id=user_id,
        )

        if project is None:
            raise ProjectNotFoundError()

        return project


    async def update_project(
        self,
        project_id: int,
        user_id: int,
        data: TravelProjectUpdate,
    ) -> TravelProject:
        
        project = await self.projects.get_by_id_for_user(
            project_id=project_id,
            user_id=user_id,
        )

        if project is None:
            raise ProjectNotFoundError()

        update_data = data.model_dump(exclude_unset=True)

        project = await self.projects.update(project, update_data)

        await self.db.commit()
        await self.db.refresh(project)

        return project


    async def delete_project(
        self,
        project_id: int,
        user_id: int,
    ) -> None:
        
        project = await self.projects.get_by_id_for_user(
            project_id=project_id,
            user_id=user_id,
        )

        if project is None:
            raise ProjectNotFoundError()

        has_visited_places = await self.projects.has_visited_places(project.id)

        if has_visited_places:
            raise ProjectDeleteForbiddenError()

        await self.projects.delete(project)
        await self.db.commit()




