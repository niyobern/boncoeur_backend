from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Dict, List, Optional


from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/teacher/quizes",
    tags=['Quizes']
)

@router.get("/", response_model=List[schemas.QuizAnswers])
def get_quiz(id: int, db : Session = Depends(get_db,), current_user :int = Depends(oauth2.get_current_user), 
        limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    if not current_user.is_super_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to view this page")    

    quizes = db.query(models.Quiz, func.count(models.Question.quiz).label("number_of_questions")).join(
        models.Question, models.Question.quiz == models.Quiz.id, isouter=True).group_by(models.Lesson.id).filter(
             models.Quiz.title.contains(search)).limit(limit).offset(skip).all()


    return quizes

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.QuizOut)
def create_quiz(quiz: schemas.QuizCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    if not current_user.is_super_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    new_quiz = models.Quiz(created_by=current_user.id, title=quiz.title, description=quiz.description)
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    
    saved_questions = [] #an empty list for questions that have already been added to the database
    for question in quiz.questions:
        new_question = models.Question(quiz=new_quiz.id, **question.dict())
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
        #save the added questions to a list
        saved_questions.append(new_question)

    return saved_questions  
    
#get all scores for teachers
@router.get("/scores", response_model=List[schemas.Score])
def get_score(db: Session = Depends(get_db), current_user: Dict = Depends(oauth2.get_current_user),
        limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    if not current_user.is_super_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to view this page")       

    scores = db.query(models.Quiz, models.Score, models.User).join(models.Score, models.Score.quiz == models.Quiz.id, 
        isouter=True).join(models.User, models.User.id == models.Score.user).group_by(models.Quiz.id).filter(
             models.Quiz.title.contains(search)).limit(limit).offset(skip).all()

    return scores
       


@router.get("/{id}", response_model=schemas.QuizAnswers)
def get_quiz(id: int, db : Session = Depends(get_db,), current_user :int = Depends(oauth2.get_current_user)):

    if not current_user.is_super_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()

    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"quiz with id: {id} was not found")

    question_list = db.query(models.Question).filter(models.Question.quiz == id).all()

    #I bernard commented out the folowing lines of code because I can't gurante their credibility
    #quiz_with_questions = db.query(models.Quiz, models.Question).join(models.Question, models.Question.quiz == models.Quiz.id, 
        #isouter=True).group_by(models.Quiz.id).filter(models.Quiz.id == id).all()

    return {**quiz.dict(), "questions" : question_list}



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(
    #     """DELETE FROM lessons WHERE id = %s returning *""", (str(id),))
    # deleted_lesson = cursor.fetchone()
    # conn.commit()

    if not current_user.is_super_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    quiz_query = db.query(models.Quiz).filter(models.Quiz.id == id)

    quiz = quiz_query.first()

    if quiz == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"quiz with id: {id} does not exist")

    if quiz.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    quiz_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.QuizOut)
def update_quiz(id: int, updated_quiz: schemas.QuizCreate, db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE lessons SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (lesson.title, lesson.content, lesson.published, str(id)))

    # updated_lesson = cursor.fetchone()
    # conn.commit()

    if not current_user.is_super_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    quiz_query = db.query(models.Quiz).filter(models.Quiz.id == id)

    quiz = quiz_query.first()

    if quiz == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"quiz with id: {id} does not exist")

    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    quiz_query.update(updated_quiz.dict(), synchronize_session=False)

    db.commit()

    return quiz_query.first()
