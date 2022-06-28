from sqlalchemy.orm import Session
from sql_app import models, schemas
import datetime


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    print(user)

    db_user = get_user_by_email(db, email=user.email)
    if db_user is None:
        db_users = models.User(**user.dict())
        db.add(db_users)
        db.commit()
        db.refresh(db_users)
        return db_users
    else:
        db_users = db_user
        return db_users


def create_coord(db: Session, coords: schemas.CoordCreate):
    db_coord = models.Coord(**coords.dict())

    db.add(db_coord)
    db.commit()
    db.refresh(db_coord)

    return db_coord.id


def create_pass(db: Session, item: schemas.PassCreate):
    """
    Запрос на создание перевала
    :param db: сессия подключения
    :param item: схема
    :return:
    """

    db_pass = models.Pass(
        beautyTitle=item.beautyTitle,
        title=item.title,
        other_titles=item.other_titles,
        connect=item.connect,
        add_time=item.add_time,
        winter=item.winter,
        summer=item.summer,
        autumn=item.autumn,
        spring=item.spring,
        user=item.user,
        coord=item.coord,
    )

    db_pass.status = 'new'
    db_pass.date_added = datetime.datetime.now()

    db.add(db_pass)
    db.commit()
    db.refresh(db_pass)

    return db_pass.id
