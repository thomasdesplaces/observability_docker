"""
Database models definition
"""

from pydantic import (
    BaseModel,
    Field
)
from observability import LOGGER

LOGGER = LOGGER.getChild(__name__)

class ClientsBase(BaseModel):
    """Base class for clients object"""
    firstname: str = Field(
        description="Firstname of the client",
        max_length=200
    )
    lastname: str = Field(
        description="Lastname of the client",
        max_length=1000
    )
    class Config:
        """For example documentation"""
        schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "Doe"
            }
        }

class ClientCreate(ClientsBase):
    """Class for client creation"""

class Clients(ClientsBase):
    """Full class definition"""
    id: str | None

    class Config:
        """For example documentation"""
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "firstname": "John",
                "lastname": "Doe"
            }
        }
