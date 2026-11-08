from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    id: int
    actor_id: int | None
    action: str
    entity_type: str
    entity_id: int | None
    details: dict | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
