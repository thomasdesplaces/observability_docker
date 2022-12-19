"""
OpenAPI description for FastAPI documentation
"""

# https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api
API_DESCRIPTION = {
    "title": "Clients API",
    "version": "0.0.1"
}

# https://fastapi.tiangolo.com/tutorial/metadata/#create-metadata-for-tags
TAGS = [
    {
        "name": "clients",
        "description": "Clients object operations"
    }
]
