from pydantic import BaseModel, Field
from typing import Optional

class NodeIn(BaseModel):
    ip: str
    country: Optional[str] = None
    wg_port: int = Field(gt=0, lt=65536)
    ss_port: int
    vless_port: int

class NodeOut(NodeIn):
    id: str
    load: int = 0