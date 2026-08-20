from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConstructionSiteBase(BaseModel):
    name: str
    description: str | None = None


class ConstructionSiteCreate(ConstructionSiteBase):
    pass


class ConstructionSiteUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ConstructionSiteResponse(ConstructionSiteBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
