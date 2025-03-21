from pydantic import BaseModel


class GetClientRequestData(BaseModel):
    tg_id: str