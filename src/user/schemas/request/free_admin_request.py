from pydantic import BaseModel


class FreeAdminRequestData(BaseModel):
    tg_id: str