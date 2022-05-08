from tkinter import CASCADE
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .config import default_lesson_banner

from .database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    has_files = Column(Boolean, nullable=False, server_default='FALSE')
    lesson_banner = Column(String, nullable=False, server_default=default_lesson_banner)
    video_url = Column(String)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    is_super_user = Column(Boolean, nullable=False, server_default='FALSE')
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    names = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    lesson_id = Column(Integer, ForeignKey(
        "lessons.id", ondelete="CASCADE"), primary_key=True)

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, nullable=False)
    file_url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), primary_key=True)  

class Quiz(Base):
    __tablename__ = "quizes"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    deadline = Column(TIMESTAMP(timezone=True))
    created_by = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, nullable=False)
    question = Column(String, nullable=False)
    options = Column(ARRAY(String))
    type = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    quiz = Column(Integer, ForeignKey(
        "quizes.id", ondelete="CASCADE"), nullable=False)

    
class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, nullable=False)
    answer = Column(String)
    passed = Column(Boolean, nullable=False, server_default='FALSE')
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, nullable=False)
    quiz = Column(Integer, ForeignKey("quizes.id", name="quiz_score_fkey", ondelete=CASCADE))
    max_score = Column(Integer, nullable=False)
    user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    score = Column(Integer, nullable=False)
