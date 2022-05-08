from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Dict, List, Optional


from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db
from ..utils import verify_answers

router = APIRouter(
    prefix="/quiz",
    tags=['Take a Quiz']
)

#get quiz scores
@router.get("/scores", response_model=List[schemas.Score])
def get_score(db: Session = Depends(get_db), current_user: Dict = Depends(oauth2.get_current_user),
        limit: int = 10, skip: int = 0, search: Optional[str] = ""):
 
    score = db.query(models.Score).filter(models.Score.user == current_user.id).first()
    
    if score == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Oups! it seems like {current_user.names} have not attempted any quiz")
    

    scores = db.query(models.Quiz, models.Score).join(
        models.Score, models.Score.quiz == models.Quiz.id, isouter=True).group_by(models.Quiz.id).filter(
             models.Quiz.title.contains(search), models.Score.user == current_user.id).limit(limit).offset(skip).all()

    return scores

#Get to a quiz by id:
@router.get("/{id}", response_model=schemas.QuizOut)
def get_quiz(id: int, db : Session = Depends(get_db,), current_user :int = Depends(oauth2.get_current_user)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()

    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"quiz with id: {id} was not found")

    question_list = db.query(models.Question).filter(models.Question.quiz == id).all()


    return {**quiz.dict(), "questions" : question_list}


#attempt a quiz:
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.QuizAnswersStudent)
def create_quiz(responses: schemas.Answering, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    for answer_given in responses.answers:
        answers_given = models.Answer(**answer_given.dict())
        db.add(answers_given)
        db.commit()
        db.refresh(answers_given)
    
    #the marking logic 
    verify_answers(responses.answers, models.Answer, db)

    #returning the collected quiz with answers to the student
    answers = db.quey(models.Question, models.Answer).join(models.Answer, models.Answer.question_id == models.Question.id,
         isouter=True).group_by(models.Question.id).filter(models.Question.quiz == responses.quiz_id).all()
    
    return answers




