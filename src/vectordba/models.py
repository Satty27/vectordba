from copy import deepcopy

ALL_OPERATIONS = (
    "aggregate",
    "find",
    "countDocuments",
    "updateOne",
    "updateMany",
    "error",
)

DEFAULT_QUERY_RESPONSE = {
    "operation": "error",
    "collection": None,
    "query": {},
    "pipeline": [],
    "document": {},
    "documents": [],
    "update": {},
    "options": {},
    "projection": {},
    "sort": {},
    "limit": None,
    "requires_confirmation": False,
    "reason": "",
}


def default_query_response():
    """Return a fresh response object using the required output structure."""

    return deepcopy(DEFAULT_QUERY_RESPONSE)


def error_response(reason):
    """Return the required error response structure."""

    response = default_query_response()
    response["operation"] = "error"
    response["collection"] = None
    response["reason"] = reason
    return response
