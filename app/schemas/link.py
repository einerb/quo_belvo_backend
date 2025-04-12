from pydantic import BaseModel
from typing import Dict, Optional

class CreateLinkDTO(BaseModel):
    institution: str
    credentials: Dict[str, str]
    access_mode: Optional[str] = "single"
    type: Optional[str] = "sandbox"
    save_data: bool = True

class LinkDTO(BaseModel):
    link: str
