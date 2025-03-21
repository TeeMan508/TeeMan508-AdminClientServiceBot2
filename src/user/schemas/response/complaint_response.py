from pydantic import BaseModel

class ComplaintResponse(BaseModel):
    complaint: str