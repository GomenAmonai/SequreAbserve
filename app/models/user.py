from pydantic import BaseModel, Field
from uuid import UUID

class UserOut(BaseModel):
    id: UUID
    wg_public: str
    wg_private: str
    ss_password: str
    active: bool = Field(default=False)