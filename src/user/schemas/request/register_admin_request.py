from pydantic import BaseModel


class RegisterAdminRequestData(BaseModel):
    tg_id: str