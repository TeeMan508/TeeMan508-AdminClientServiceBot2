from pydantic import BaseModel

class IdResponseData(BaseModel):
    tg_id: str