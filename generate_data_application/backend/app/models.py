"""
Models definition
"""

from sqlalchemy import (
    Column,
    String
)
from connection import Base
from observability import LOGGER

LOGGER = LOGGER.getChild(__name__)

class ClientsClass(Base):
    """Clients object class"""
    __tablename__ = "clients"

    id = Column(String, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
