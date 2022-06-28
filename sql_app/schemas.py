from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Union, Optional


class CoordBase(BaseModel):
    latitude: float
    longitude: float
    height: int


class CoordCreate(CoordBase):
    latitude: float
    longitude: float
    height: int

    class Config:
        schema_extra = {
            'example': {
                "latitude": "45.3842",
                "longitude": "7.1525",
                "height": "1200",
            }
        }


class Coord(CoordCreate):
    id: int
    pass_id: int
    pass_add: 'Pass'

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    email: str
    fam: str
    name: str
    otc: str
    phone: str

    class Config:
        schema_extra = {
            'example': {
                "email": "qwerty@mail.ru",
                "fam": "Пупкин",
                "name": "Василий",
                "otc": "Иванович",
                "phone": "79270123456",
            }
        }


class User(UserBase):
    id: int
    pass_id: int
    pass_add: 'Pass'

    class Config:
        orm_mode = True


# class PassBase(BaseModel):
#     id: int
#     beautyTitle: str
#     title: str
#     other_titles: str
#     connect: str
#     winter: str
#     summer: str
#     autumn: str
#     spring: str
#     user: Optional[UserCreate]
#     coord: Optional[CoordCreate]
#     # images: Optional[List[ImageBase]]


class PassCreate(BaseModel):
    beautyTitle: str
    title: str
    other_titles: str
    connect: str
    add_time: datetime
    winter: str
    summer: str
    autumn: str
    spring: str
    user: Optional[UserCreate]
    coord: Optional[CoordCreate]
    # images: Optional[List[ImageCreate]]

    class Config:
        schema_extra = {
            'example': {
                "beautyTitle": "пер. ",
                "title": "Пхия",
                "other_titles": "Триев",
                "connect": "",
                "add_time": "2021-09-22 13:18:13",
                "winter": "",
                "summer": "1А",
                "autumn": "1А",
                "spring": "",
                "user": {
                    "email": "qwer@mail.ru",
                    "phone": "79270123456",
                    "fam": "Пупкин",
                    "name": "Василий",
                    "otc": "Иванович"
                },
                "coords": {
                    "latitude": "45.3842",
                    "longitude": "7.1525",
                    "height": "1200",
                },
                # "images":
                #     [{"image_url": "",
                #       "title": "Седловина"},
                #      {"image_url": "",
                #       "title": "Подъем"}]
            }
        }


class Pass(PassCreate):
    id: int
    status: str
    user: int
    coord: int

    class Config:
        orm_mode = True
