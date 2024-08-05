from fastapi import FastAPI
from routers import note
from database import create_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(note.router, tags=["Notes"], prefix="/api/notes")
# app.include_router(category.router, tags=["Categories"], prefix="/api/categories")


@app.get("/api/health_checker")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
def on_startup():
    create_db()