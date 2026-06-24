from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectPlaceCreate(BaseModel):
    external_place_id: int = Field(gt=0)
    notes: str | None = Field(default=None, max_length=2000)


class ProjectPlaceUpdate(BaseModel):
    notes: str | None = Field(default=None, max_length=2000)
    is_visited: bool | None = None


class ProjectPlaceRead(BaseModel):
    id: int
    project_id: int
    external_place_id: int

    title: str
    artist_title: str | None = None
    image_url: str | None = None

    notes: str | None = None
    is_visited: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)



