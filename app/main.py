from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import lesson, user, auth, vote, quiz_student, quiz_teachers, teachers_auth 


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lesson.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(quiz_student.router)
app.include_router(quiz_teachers.router)
app.include_router(teachers_auth.router)

@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}
