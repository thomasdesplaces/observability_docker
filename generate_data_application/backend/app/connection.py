"""
Function to create Database connection
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import settings
from observability import LOGGER

LOGGER = LOGGER.getChild(__name__)

# Database connexion
DATABASE_SETTINGS = settings.DATABASES['local']
SQLALCHEMY_DATABASE_URL = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    DATABASE_SETTINGS.get("username"),
    DATABASE_SETTINGS.get("password"),
    DATABASE_SETTINGS.get("host"),
    DATABASE_SETTINGS.get("port"),
    DATABASE_SETTINGS.get("database")
)

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as error:
    LOGGER.error(error)

LOGGER.debug(engine)
