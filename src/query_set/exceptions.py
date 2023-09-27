from fastapi import HTTPException, status


class QuerySetNotFound(HTTPException):
    def __init__(self, query_set_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Query set not {query_set_id} found",
        )


class QuerySetNotCreated(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Query set not created"
        )
