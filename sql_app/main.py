from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import engine, SessionLocal
from sql_app.errors import ErrorConnectionServer, get_json_response

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/submitData/', response_model=schemas.PassCreate)
def post_pass(item: schemas.PassCreate, db: Session = Depends(get_db)):
    print(item)
    '''
    :param item: класс схема базовой модели пользователя
    :param db: сессия подключения к БД
    :return: сообщение в формате JSON о результате создания и id объекта
    '''

    try:  # Проверка на подключение к базе
        db.execute('SELECT * FROM users')
    except Exception as error:
        raise ErrorConnectionServer(f'Ошибка соединения: {error}')

    news_user = crud.create_user(db=db, user=item.user)

    new_coords = crud.create_coord(db=db, coords=item.coord)

    item.user = news_user
    item.coord = new_coords

    new_pereval = crud.create_pass(db=db, item=item)

    return get_json_response(200, "Отправлено", new_pereval)


