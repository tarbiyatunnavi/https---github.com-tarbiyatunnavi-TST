from pydantic import BaseModel, Field
class UserSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "Tarbiyatunnavi",
                "password": "tst1234"
            }
        }

class UserLoginSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "Tarbiyatun Nafiah",
                "password": "tst1234"
            }
        }