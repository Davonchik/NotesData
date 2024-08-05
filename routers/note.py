from sqlmodel import Session, select
from fastapi import Depends, HTTPException, APIRouter, Response, status
from database import get_session
from database.models import *
from typing import List

router = APIRouter()


@router.get("/", response_model=List[NoteRead])
def read_notes(*, session: Session = Depends(get_session)):
    notes = session.exec(select(Note)).all()
    return notes


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_note(*, session: Session = Depends(get_session), note: Note):
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@router.patch("/{note_id}", response_model=NoteRead)
def update_note(*, note_id: int, note: NoteUpdate, session: Session = Depends(get_session)):
    db_note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    note_data = note.model_dump()
    db_note.sqlmodel_update(note_data)
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note


@router.get("/{note_id}", response_model=NoteReadWithCategory)
def read_note(*, note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.delete("/{note_id}", response_model=NoteRead)
def delete_note(*, note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    session.delete(note)
    session.commit()
    return note