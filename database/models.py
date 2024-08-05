from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, Session


class CategoryBase(SQLModel):
    name: str = Field(index=True)
    description: str


class Category(CategoryBase, table=True):
    __tablename__ = "categories"
    id: Optional[int] = Field(default=None, primary_key=True)
    notes: List["Note"] = Relationship(back_populates="category")


class CategoryRead(CategoryBase):
    id: int


class NoteBase(SQLModel):
    title: str
    content: str
    priority: str
    published: bool
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id")


class Note(NoteBase, table=True):
    __tablename__ = "notes"
    id: Optional[int] = Field(default=None, primary_key=True)
    category: Optional[Category] = Relationship(back_populates="notes")


class NoteRead(NoteBase):
    id: int


class NoteReadWithCategory(NoteRead):
    category: Optional["CategoryRead"] = None


class NoteUpdate(SQLModel):
    title: str
    content: str
    priority: str
    published: bool
    category_id: Optional[int] = Field(default=None, foreign_key="notes.id")


class CategoryUpdate(SQLModel):
    name: str
    description: str
    priority: str
    published: bool
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id")
