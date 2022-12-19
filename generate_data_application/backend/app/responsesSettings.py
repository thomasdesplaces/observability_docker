"""
Response message definition
"""

responsesMessages = {
    '400': {
        "description": "Bad request",
        "content": {
            "application/json": {
                "example": {
                    "code": "400.01",
                    "message": "Bad request"
                }
            }
        }
    },
    '403': {
        "description": "Not authorize",
        "content": {
            "application/json": {
                "example": {
                    "code": "403.01",
                    "message": "Not authorize"
                }
            }
        }
    },
    '404': {
        "description": "Not found",
        "content": {
            "application/json": {
                "example": {
                    "code": "404.01",
                    "message": "Not found"
                }
            }
        }
    },
    '405': {
        "description": "Method not allowed",
        "content": {
            "application/json": {
                "example": {
                    "code": "405.01",
                    "message": "Method not allowed"
                }
            }
        }
    },
    '422': {
        "description": "Error in the attributs",
        "content": {
            "application/json": {
                "example": {
                    "code": "422.01",
                    "message": "Error in the attributs"
                }
            }
        }
    },
    '500': {
        "description": "Internal error",
        "content": {
            "application/json": {
                "example": {
                    "code": "500.01",
                    "message": "Internal error"
                }
            }
        }
    }
}
