"""
Function to interact with database for each object
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import uuid
import schemas, models
from observability import LOGGER, tracer

traces = tracer.get_tracer(__name__)
LOGGER = LOGGER.getChild(__name__)

def get_client(db: Session, client_id: str):
    """Get all details about a specific client"""
    with traces.start_as_current_span("CRUD GET Client by ID"):
        LOGGER.info("Start GET Client by ID Query DB")
        try:
            client = db.query(models.ClientsClass).filter(models.ClientsClass.id == client_id).first()
        except Exception as error:
            LOGGER.error(error)
            raise HTTPException(status_code=500)
        if client is None:
            raise HTTPException(status_code=404)
        return client

def get_list(db: Session):
    """Get all clients"""
    with traces.start_as_current_span("CRUD GET Clients List"):
        LOGGER.info("Start GET Clients List Query DB")
        try:
            clients = db.query(models.ClientsClass).all()
        except Exception as error:
            LOGGER.error(error)
            raise HTTPException(status_code=500)
        if clients is None:
            raise HTTPException(status_code=404)
        return clients

def create(db: Session, client: schemas.ClientCreate):
    """Create client"""
    with traces.start_as_current_span("CRUD POST Client"):
        LOGGER.info("Start POST Client Query DB")
        new_client = models.ClientsClass(
            id=str(uuid.uuid4()),
            firstname=client.firstname,
            lastname=client.lastname
        )
        try:
            db.add(new_client)
            db.commit()
            db.refresh(new_client)
        except IntegrityError as error:
            LOGGER.error(str(error.orig))
            raise HTTPException(
                status_code=400, detail={
                "code":"400.01",
                "message": str(error.orig)
                }
            )
        return new_client

def put(db: Session, client_id: str, client: schemas.Clients):
    """Modify a specific client"""
    with traces.start_as_current_span("CRUD PUT Client by ID"):
        LOGGER.info("Start PUT Client by ID Query DB")
        modify_client = models.ClientsClass(
            id=client.id,
            firstname=client.firstname,
            lastname=client.lastname
        )
        try:
            db.query(models.ClientsClass).filter(models.ClientsClass.id == modify_client.id).update(values={
                models.ClientsClass.firstname: client.firstname,
                models.ClientsClass.lastname: client.lastname
            }, synchronize_session=False)
            db.commit()
        except Exception as error:
            LOGGER.debug(error)
            return error
        return modify_client

def delete(db: Session, client_id: str):
    """Delete a specific client"""
    with traces.start_as_current_span("CRUD DELETE Client by ID"):
        LOGGER.info("Start DELETE Client by ID Query DB")
        try:
            delete_client = db.query(models.ClientsClass).filter(models.ClientsClass.id == client_id).first()
            db.query(models.ClientsClass).filter(models.ClientsClass.id == client_id).delete()
            db.commit()
        except Exception as error:
            LOGGER.error(error)
            raise HTTPException(status_code=500)
        if delete_client is None:
            raise HTTPException(status_code=404)
        return None