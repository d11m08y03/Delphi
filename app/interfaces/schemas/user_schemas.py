from pydantic import BaseModel


class UserDetailsSchema(BaseModel):
    email: str
    first_name: str
    last_name: str
