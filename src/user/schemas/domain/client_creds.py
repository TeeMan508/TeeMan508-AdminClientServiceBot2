from pydantic import BaseModel

class ClientCredentials(BaseModel):
    tg_id: str
    complaint: str