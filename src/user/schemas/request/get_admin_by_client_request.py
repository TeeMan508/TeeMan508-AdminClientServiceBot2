from pydantic import BaseModel


class GetAdminByClientRequestData(BaseModel):
    tg_id: str
