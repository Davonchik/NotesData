from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker

db_name = "postgresql://postgres:1111@localhost:5432/postgres"
engine = create_engine(db_name)


def get_session():
    with Session(bind=engine) as session:
        yield session


def create_db():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
