from fastapi import HTTPException
from fastapi.responses import JSONResponse

class CustomHTTPException(HTTPException):
    def __init__(self, message: str = "Error", status_code: int = 400):
        super().__init__(status_code=status_code, detail=message)

    def to_response(self):
        return JSONResponse(
            status_code=self.status_code,
            content={
                "success": False,
                "message": self.detail,
                "data": None,
            }
        )
