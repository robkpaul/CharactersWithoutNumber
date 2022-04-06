from pydantic import BaseModel

class CharacterBase(BaseModel):
    id: int
    charsheet: dict

class CharacterCreate(CharacterBase):
    pass

class Character(CharacterBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    characters: list[Character] = []

    class Config:
        orm_mode = True