from fastapi import FastAPI, Depends
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

    return get_json_response(200, "Отправлено", new_pass)
