from fastapi import HTTPException, status


class FieldSetNotFound(HTTPException):
    def __init__(self, field_set_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Field set not {field_set_id} found",
        )


class FieldSetNotCreated(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Field set not created"
        )
