from pydantic import BaseModel

class SetClientToAdminRequestData(BaseModel):
    tg_id: str