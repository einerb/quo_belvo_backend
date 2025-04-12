from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any

def serialize_data(data: Any):
    if isinstance(data, BaseModel):
        return data.model_dump(mode="json")
    elif isinstance(data, list) and all(isinstance(i, BaseModel) for i in data):
        return [item.model_dump(mode="json") for item in data]
    return data

def success_response(data: Any, message: str = "Success", status_code: int = 200):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": serialize_data(data),
        }
    )

def error_response(message: str = "Error", status_code: int = 400):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": None,
        }
    )