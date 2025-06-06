from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
from typing import Optional

def get_user(db: Session, user_id: int):
    return db.get(models.User, user_id)

def get_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        return None
    return db_user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True

def get_posts(db: Session, user_id: Optional[int] = None):
    query = db.query(models.Post)
    if user_id is not None:
        return query.filter(models.Post.user_id == user_id).all()
    return query.all()

def create_post(db: Session, post: schemas.PostCreate):
    if not get_user(db, post.user_id):
        return None
    db_post = models.Post(text=post.text, user_id=post.user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post: schemas.PostUpdate):
    db_post = db.get(models.Post, post_id)
    if not db_post:
        return None
    db_post.text = post.text
    db.commit()
    db.refresh(db_post)
    return db_post
