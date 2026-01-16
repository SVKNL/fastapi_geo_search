from pydantic import BaseModel, ConfigDict


class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float


class BuildingRead(BuildingBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
