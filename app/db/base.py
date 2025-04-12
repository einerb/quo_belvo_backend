import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncAttrs

Base = declarative_base()

class BaseModel(AsyncAttrs, Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self):
        """Representación para debugging"""
        cols = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        return f"<{self.__class__.__name__}({cols})>"

    def to_dict(self):
        """Convierte modelo a diccionario"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}