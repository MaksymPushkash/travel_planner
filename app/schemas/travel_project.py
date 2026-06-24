from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.project_place import ProjectPlaceCreate, ProjectPlaceRead


class TravelProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    start_date: date | None = None

    places: list[ProjectPlaceCreate] = Field(
        default_factory=list,
        max_length=10,
    )


class TravelProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    start_date: date | None = None


class TravelProjectRead(BaseModel):
    id: int
    user_id: int

    name: str
    description: str | None = None
    start_date: date | None = None
    is_completed: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TravelProjectDetail(TravelProjectRead):
    places: list[ProjectPlaceRead] = Field(default_factory=list)



