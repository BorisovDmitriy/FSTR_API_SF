from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import engine, SessionLocal
from sql_app.errors import ErrorConnectionServer, get_json_response
from fastapi.encoders import jsonable_encoder
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/submitData/', response_model=schemas.Pass)
def post_pass(item: schemas.PassCreate, db: Session = Depends(get_db)):
    print(item)
    try:  # Проверка на подключение к базе
        db.execute('SELECT * FROM users')
    except Exception as error:
        raise ErrorConnectionServer(f'Ошибка соединения: {error}')

    news_user = crud.create_user(db=db, user=item.user)

    new_coords = crud.create_coord(db=db, coord=item.coords)

    item.user = news_user
    item.coords = new_coords

    new_pass = crud.create_pass(db=db, item=item)

    crud.search_pass(db=db, new_pass=new_pass, image=item.images)

    return get_json_response(200, "Отправлено", new_pass)


@app.get('/submitData/{id}', response_model=schemas.PassCreate)
def search_pass(id: int, db: Session = Depends(get_db)):
    item = crud.get_pass(db=db, id=id)
    return get_json_response(200, 'Объект получен', jsonable_encoder(item))


@app.get('/submitDate/{email}', response_model=List[schemas.PassBase])
def read_pass(email: str, db: Session = Depends(get_db)):
    pass_all = crud.search_all(db=db, email=email)
    return pass_all


@app.patch("/submitData/{id}", response_model=schemas.PassCreate, response_model_exclude_none=True)
async def patch_submit_data_id(id: int, item: schemas.PassAddedUpdate, db: Session = Depends(get_db)):
    # pending — если модератор взял в работу;
    # accepted — модерация прошла успешно;
    # rejected — модерация прошла, информация не принята.

    statuses = [
        'pending',
        'accepted',
        'rejected',
    ]

    db_pass_info = crud.get_pass(db, id)

    if db_pass_info is None:
        return get_json_response(422, f'Перевал с id {id} отсутствует')

    if db_pass_info['status'] in statuses:
        return get_json_response(422, f'Перевал с id {id} на модерации')

    update_pass = crud.update_pass(id, db, item)
    return get_json_response(200, 'Запись обновлена', update_pass)
