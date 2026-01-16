from pydantic import BaseModel, ConfigDict


class ActivityBase(BaseModel):
    name: str
    parent_id: int | None = None
    depth: int


class ActivityRead(ActivityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
