from fastapi import HTTPException, status


class ReportNotFound(HTTPException):
    def __init__(self, report_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report not {report_id} found",
        )


class ReportNotCreated(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Report not created"
        )
