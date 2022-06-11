from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    access_token: str

    class Config:
        orm_mode = True
