from pydantic import BaseModel, ConfigDict

from app.schemas.activities import ActivityRead
from app.schemas.buildings import BuildingRead


class OrganizationPhoneRead(BaseModel):
    id: int
    phone: str

    model_config = ConfigDict(from_attributes=True)


class OrganizationBase(BaseModel):
    name: str
    building_id: int


class OrganizationRead(OrganizationBase):
    id: int
    building: BuildingRead
    phones: list[OrganizationPhoneRead] = []
    activities: list[ActivityRead] = []

    model_config = ConfigDict(from_attributes=True)
