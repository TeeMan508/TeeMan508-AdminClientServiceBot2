from pydantic import BaseModel

class RegisterClientRequestData(BaseModel):
    tg_id: str
    complaint: str