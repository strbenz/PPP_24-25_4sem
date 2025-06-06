from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from .. import schemas, crud, database

router = APIRouter(prefix="/posts", tags=["posts"])

# Теперь используем функцию get_db, а не SessionLocal
get_db = database.get_db

@router.get("/", response_model=list[schemas.PostResponse])
def read_posts(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    if user_id is not None and not crud.get_user(db, user_id):
        raise HTTPException(status_code=404, detail="Пользователь не найден.")
    return crud.get_posts(db, user_id)

@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post_in: schemas.PostCreate, db: Session = Depends(get_db)):
    post = crud.create_post(db, post_in)
    if not post:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")
    return post

@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post_in: schemas.PostUpdate, db: Session = Depends(get_db)):
    updated = crud.update_post(db, post_id, post_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Пост не найден.")
    return updated
