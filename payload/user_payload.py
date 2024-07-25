from typing import Optional, List

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    owner_id: int


class UserResponse(BaseModel):
    id: int
    username: str
    disabled: bool

    class Config:
        from_attributes = True


class UsersNameResponse(BaseModel):
    username: str

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int

    class Config:
        from_attributes = True


class ProjectRequest(BaseModel):
    name: str


class TeamRequest(BaseModel):
    name: str
    project_ids: Optional[List[int]] = []


class PassportRequest(BaseModel):
    passport_number: str
    person_id: int
