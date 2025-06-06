from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter(prefix="/users", tags=["users"])

# Раньше было: get_db = database.SessionLocal
# Теперь используем функцию-генератор get_db
get_db = database.get_db

@router.get("/", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.create_user(db, user_in)
    if not user:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует.")
    return user

@router.get("/{user_id}/posts", response_model=list[schemas.PostResponse])
def read_user_posts(user_id: int, db: Session = Depends(get_db)):
    if not crud.get_user(db, user_id):
        raise HTTPException(status_code=404, detail="Пользователь не найден.")
    return crud.get_posts(db, user_id)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")
    return {}
