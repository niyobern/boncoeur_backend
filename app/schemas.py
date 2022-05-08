from pydantic import BaseModel, EmailStr
from fastapi import UploadFile
from datetime import datetime
from typing import List, Optional

from pydantic.types import conint


class LessonBase(BaseModel):
    title: str
    content: str
    published: bool = True


class LessonCreate(LessonBase):
    files: List[UploadFile] | None = None
    video_url: str | None = None
    lesson_banner: UploadFile | None = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Lesson(LessonBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    lesson_banner: str | None = None
    video_url: str | None = None


    class Config:
        orm_mode = True


class File(BaseModel):
    file_url: str
    file_type: str

class LessonOut(BaseModel):
    Lesson: Lesson
    File: File
    votes: int


    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    names: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    lesson_id: int
    dir: conint(le=1)

class Question(BaseModel):
    question: str
    type: str
    options: List[str] | None = None

    class Config:
        orm_mode = True

class QuestionCreate(Question):
    answer: str
    
class QuizCreate(BaseModel):
    title: str
    description: str
    deadline: datetime
    questions: List[QuestionCreate]    

class QuizOut(BaseModel):
    title: str
    description: str
    deadline: datetime
    created_by: str

    class Config:
        orm_mode = True

class QuizList(BaseModel):
    Quiz: QuizOut
    number_of_questions: int

class Answer(BaseModel):
    question_id: int
    answer: str

    class Config:
        orm_mode = True

class Answering(BaseModel):
    quiz_id: int
    answers : List[Answer]
    
class AnswerOut(BaseModel):
    question: str
    answer: str

    class Config:
        orm_mode = True

class AnswerOutStudent(AnswerOut):
    passed: bool


class QuizAnswers(BaseModel):
    Quiz: QuizOut
    answers: AnswerOut
 
    class Config:
        orm_mode = True

class QuizAnswersStudent(BaseModel):
    Quiz: QuizOut
    answers: List[AnswerOutStudent]
 
    class Config:
        orm_mode = True

class Score(BaseModel):
    pass

    class Config:
        orm_mode = True