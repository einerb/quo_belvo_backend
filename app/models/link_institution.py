from sqlalchemy import Column, String, Date

from app.db.base import BaseModel

class LinkInstitution(BaseModel):
    __tablename__ = "link_institutions"

    name = Column(String, unique=True, index=True)
    link_id = Column(String)
    date_expiration = Column(Date, nullable=False)