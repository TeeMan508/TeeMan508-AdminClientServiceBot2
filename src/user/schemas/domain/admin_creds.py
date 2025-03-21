from pydantic import BaseModel

class AdminCredentials(BaseModel):
    tg_id: str