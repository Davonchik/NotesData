from sqlmodel import Session, select
from fastapi import Depends, HTTPException, APIRouter, Response, status
from database import get_session
from database.models import *
from typing import List


router = APIRouter()


@router.get("/", response_model=List[CategoryRead])
def read_categories(*, session: Session = Depends(get_session)):
    categories = session.exec(select(Category)).all()
    return categories


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(*, session: Session = Depends(get_session), category: Category):
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.patch("/{category_id}", response_model=CategoryRead)
def update_note(*, category_id: int, category: CategoryUpdate, session: Session = Depends(get_session)):
    db_category = session.get(Note, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    category_data = category.model_dump()
    db_category.sqlmodel_update(category_data)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.delete("/{category_id}", response_model=CategoryRead)
def delete_category(*, category_id: int, session: Session = Depends(get_session)):
    category = session.get(Note, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    session.delete(category)
    session.commit()
    return category
