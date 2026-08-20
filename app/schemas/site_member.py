from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.site_member import SiteMemberRole


class SiteMemberCreate(BaseModel):
    user_id: int
    role: SiteMemberRole = SiteMemberRole.MEMBER


class SiteMemberResponse(BaseModel):
    site_id: int
    user_id: int
    role: SiteMemberRole
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)
