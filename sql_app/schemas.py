from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Union


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
            "example": {
                "latitude": "45.3842",
                "longitude": "7.1525",
                "height": "1200",
            }
        }


class Coord(CoordBase):
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
            "example": {
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


class ImageBase(BaseModel):
    id: int
    image_url: str
    title: str
    id_pass: int


class ImageCreate(BaseModel):
    image_url: str
    title: str


class Image(ImageCreate):
    id: int
    images: List[ImageCreate]

    class Config:
        orm_mode = True


class PassBase(BaseModel):
    id: int
    beautyTitle: str
    title: str
    other_titles: str
    connect: str
    winter: str
    summer: str
    autumn: str
    spring: str
    user: Optional[UserCreate] = None
    coords: Optional[CoordCreate] = None
    images: Optional[List[ImageBase]]


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
    user: Optional[UserCreate] = None
    coords: Optional[CoordCreate] = None
    images: Optional[List[ImageCreate]]

    class Config:
        schema_extra = {
            "example": {
                "beautyTitle": "пер. ",
                "title": "Пхия",
                "other_titles": "Триев",
                "connect": "",
                "add_time": "2021-09-22 13:18:13",
                "winter": "1B",
                "summer": "1А",
                "autumn": "1А",
                "spring": "1B",
                "user": {
                    "email": "qwer@mail.ru",
                    "phone": "79270123456",
                    "fam": "Пупкин",
                    "name": "Василий",
                    "otc": "Иванович",
                },
                "coords": {
                    "latitude": "45.3842",
                    "longitude": "7.1525",
                    "height": "1200",
                },
                "images":
                    [{"image_url": "",
                      "title": "Седловина"},
                     {"image_url": "",
                      "title": "Подъем"}]
            }
        }


class PassAddedUpdate(BaseModel):
    id: Union[int, None] = None
    beauty_title: Union[str, None] = None
    title: Union[str, None] = None
    other_titles: Union[str, None] = None
    connect: Union[str, None] = None
    winter: Union[str, None] = None
    summer: Union[str, None] = None
    autumn: Union[str, None] = None
    spring: Union[str, None] = None
    coords: Union[CoordCreate, None] = None
    images: Union[List[ImageBase], None] = None

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'beauty_title': 'пер.',
                'title': 'Гроза',
                'other_titles': 'Третьев',
                'connect': ', ',
                'winter': '1Б',
                'summer': '1А',
                'autumn': '1А',
                'spring': '1А',
                'coords': {
                    'latitude': 56.2368,
                    'longitude': 41.683,
                    'height': 120,
                },
                "images":
                    [{"id": 1,
                      "image_url": "media/1",
                      "title": "Спуск",
                      "id_pass": 1},
                     {"id": 2,
                      "image_url": "media/1",
                      "title": "Равнина",
                      "id_pass": 1}]
            }
        }


class Pass(PassCreate):
    id: int
    status: str
    user: int
    coord: int

    class Config:
        orm_mode = True
