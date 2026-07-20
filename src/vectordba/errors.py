from .models import error_response


class QueryBuildError(Exception):
    """Raised when a MongoDB query cannot be generated safely."""

    def __init__(self, reason, status_code=422):
        self.reason = reason
        self.status_code = status_code
        super(QueryBuildError, self).__init__(reason)

    @property
    def response_body(self):
        return error_response(self.reason)