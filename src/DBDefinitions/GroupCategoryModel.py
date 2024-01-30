import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship

from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel


class GroupCategoryModel(BaseModel):
    """Urcuje categorii, napr. akademicke typy, vojenske struktury..."""

    __tablename__ = "groupcategories"

    id = UUIDColumn()
    name = Column(String, comment="name of the category")
    name_en = Column(String, comment="english name of the category")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="when record has been created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp")
    createdby = UUIDFKey(nullable=True, comment="who has created this record")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="who has changed this record")#Column(ForeignKey("users.id"), index=True, nullable=True)
    
    rbacobject = UUIDFKey(nullable=True, comment="holds object for role resolution")#Column(ForeignKey("users.id"), index=True, nullable=True)        