from sqlalchemy.orm import Session
from sql_app import models, schemas
import datetime
from fastapi.encoders import jsonable_encoder


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = get_user_by_email(db, email=user.email)
    if db_user is None:
        db_users = models.User(**user.dict())
        db.add(db_users)
        db.commit()
        db.refresh(db_users)
        return db_users.id
    else:
        db_users = db_user
        return db_users.id


def create_coord(db: Session, coord: schemas.CoordCreate) -> int:
    db_coord = models.Coord(**coord.dict())
    db.add(db_coord)
    db.commit()
    db.refresh(db_coord)
    return db_coord.id


def create_pass(db: Session, item: schemas.PassCreate) -> object:
    db_pass = models.Pass(
        beautyTitle=item.beautyTitle,
        title=item.title,
        other_titles=item.other_titles,
        connect=item.connect,
        add_time=item.add_time,
        user=item.user,
        coords=item.coords,
        winter=item.winter,
        summer=item.summer,
        autumn=item.autumn,
        spring=item.spring,
    )

    db_pass.status = 'new'
    db_pass.date_added = datetime.datetime.now()

    db.add(db_pass)
    db.commit()
    db.refresh(db_pass)

    return db_pass.id


def search_pass(db: Session, new_pass: int, image: schemas.ImageCreate):
    for i in image:
        db_image = models.Image(**i.dict())

        db_image.id_pass = new_pass

        db.add(db_image)

    db.commit()


def get_pass(db: Session, id: int) -> dict:
    c_pass = db.query(models.Pass).filter(models.Pass.id == id).first()
    user = db.query(models.User).filter(models.User.id == c_pass.user).first()
    coords = db.query(models.Coord).filter(models.Coord.id == c_pass.coords).first()
    image = db.query(models.Image).filter(models.Image.id_pass == id).all()

    json_user = jsonable_encoder(user)
    json_coords = jsonable_encoder(coords)
    json_images = jsonable_encoder(image)
    dict_pass = jsonable_encoder(c_pass)

    dict_pass['user'] = json_user
    dict_pass['coords'] = json_coords
    dict_pass['images'] = json_images

    return dict_pass
