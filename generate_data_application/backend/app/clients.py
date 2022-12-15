"""
Function to define FastAPI routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from schemas import ClientsBase, Clients
from responsesSettings import responsesMessages
import connection, crud_clients
from observability import LOGGER, tracer

traces = tracer.get_tracer(__name__)

LOGGER = LOGGER.getChild(__name__)

router = APIRouter(
    tags=["clients"],
    responses={
        400: responsesMessages['400'],
        403: responsesMessages['403'],
        404: responsesMessages['404'],
        405: responsesMessages['405'],
        422: responsesMessages['422'],
        500: responsesMessages['500']
    }
)

def get_db():
    """
    Database connexion
    """
    db = connection.SessionLocal()
    try:
        LOGGER.debug("Open database connexion")
        yield db
    finally:
        LOGGER.debug("Close database connexion")
        db.close()

@router.post(path="/clients",
    response_model=Clients, 
    status_code=201,
    summary="Client creation"
)
async def post_client(client: ClientsBase, db: Session = Depends(get_db)):
    """
    Create client with all parameters :

    - **firstname**: Firstname of the client
    - **lastname**: Lastname of the client
    """
    with traces.start_as_current_span("Router GET client by ID"):
        LOGGER.info("Start POST Client")
        new_client = crud_clients.create(db=db, client=client)
        return new_client

@router.get(path="/clients",
    response_model=list[Clients],
    status_code=200,
    summary="List clients"
)
async def get_clients(db: Session = Depends(get_db)):
    """
    List all clients
    """
    with traces.start_as_current_span("Router GET clients List"):
        LOGGER.info("Start GET Clients List")
        try:
            list_clients = crud_clients.get_list(db=db)
            return list_clients
        except OperationalError as error:
            LOGGER.error(error)
            return ""

@router.get(path="/clients/{client_id}",
    response_model=Clients,
    status_code=200,
    summary="Details for specific client")
async def get_client(client_id: str, db: Session = Depends(get_db)):
    """
    Details for specific client
    """
    with traces.start_as_current_span("Router GET client by ID"):
        LOGGER.info("Start GET Client by ID")
        client = crud_clients.get_client(db=db, client_id=client_id)
        LOGGER.debug("Return client : %s" % str(client))
        return client

@router.put(path="/clients/{client_id}",
    response_model=Clients,
    status_code=200,
    summary="Modify details for a specific client")
async def put_client(client_id: str, client: ClientsBase, db: Session = Depends(get_db)):
    """
    Modify details for a specific client :

    - **firstname**: Firstname of the client
    - **lastname**: Lastname of the client
    """
    with traces.start_as_current_span("Router Modify clients by ID"):
        LOGGER.info("Start PUT Client by ID")
        try:
            modify_client = crud_clients.put(db=db, client_id=client_id, client=client)
            return modify_client
        except OperationalError as error:
            LOGGER.error(error)
            return ""

@router.delete(path="/clients/{client_id}",
    response_model=None, 
    status_code=204,
    summary="Delete a specific client"
)
async def delete_client(client_id: str, db: Session = Depends(get_db)):
    """
    Delete a specific client
    """
    with traces.start_as_current_span("Router DELETE clients by ID"):
        LOGGER.info("Start DELETE Client by ID")
        delete_client = crud_clients.get_client(db=db, client_id=client_id)
        if delete_client is None:
            raise HTTPException(status_code=405)
        crud_clients.delete(db=db, client_id=client_id)
        return None