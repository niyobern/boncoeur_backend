from fastapi import Response, status, HTTPException, Depends, APIRouter
from matplotlib.backend_bases import MouseEvent
from sqlalchemy.orm import Session
from typing import List, Optional


from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/lessons",
    tags=['Lessons']
)


# @router.get("/", response_model=List[schemas.Lesson])
@router.get("/", response_model=List[schemas.LessonOut])
def get_lessons(db: Session = Depends(get_db), current_user: int = Depends(
    oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # results = db.query(models.Lesson, func.count(models.Vote.lesson_id).label("votes")).join(
    #     models.Vote, models.Vote.lesson_id == models.Lesson.id, isouter=True).group_by(models.Lesson.id)

    # cursor.execute("""SELECT * FROM lessons """)
    # lessons = cursor.fetchall()

    # lessons = db.execute(
    #     'select lessons.*, COUNT(votes.lesson_id) as votes from lessons LEFT JOIN votes ON lessons.id=votes.lesson_id  group by lessons.id')
    # results = []
    # for lesson in lessons:
    #     results.append(dict(lesson))
    # print(results)
    # lessons = db.query(models.Lesson).filter(
    #     models.Lesson.title.contains(search)).limit(limit).offset(skip).all()

    lessons = db.query(models.Lesson, models.File, func.count(models.Vote.lesson_id).label("votes")).join(
        models.Vote, models.Vote.lesson_id == models.Lesson.id, isouter=True).join(models.File,
         models.File.lesson_id==models.Lesson.id, isouter=True).group_by(models.Lesson.id).filter(
             models.Lesson.title.contains(search)).limit(limit).offset(skip).all()

    return lessons


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Lesson)
def create_lessons(lesson: schemas.LessonCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO lessons (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (lesson.title, lesson.content, lesson.published))
    # new_lesson = cursor.fetchone()

    # conn.commit()

    #checking whether the upload has files, if not:
    if not current_user.is_super_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    if lesson.files == None:
         new_lesson = models.Lesson(owner_id=current_user.id, title=lesson.title, content=lesson.content, 
            video_url=lesson.video_url, has_files=False)
         db.add(new_lesson)
         db.commit()
         db.refresh(new_lesson)
         return new_lesson
    #if the upload has files:
    new_lesson = models.Lesson(owner_id=current_user.id, title=lesson.title, content=lesson.content, 
       video_url=lesson.video_url, has_files=False)
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    #getting the lesson_id to use in files table
    new_lesson_id = new_lesson.id
    #getting the filename and filetype for every uploaded file
    for file in lesson.files:
        name = file.filename
        type = file.content_type
        #save file
        #mock saving to be resolved latter when the file saving system has been made
        url = f'storage_disk/{name}'

        new_file = models.File(pot_id=new_lesson_id, file_type=type, file_url=url)
        db.add(new_file)
        db.commit()
        db.refresh(new_file)
    return new_lesson

@router.get("/{id}", response_model=schemas.LessonOut)
def get_lesson(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from lessons WHERE id = %s """, (str(id),))
    # lesson = cursor.fetchone()
    # lesson = db.query(models.Lesson).filter(models.Lesson.id == id).first()

    lesson = db.query(models.Lesson, func.count(models.Vote.lesson_id).label("votes")).join(
        models.Vote, models.Vote.lesson_id == models.Lesson.id, isouter=True).group_by(models.Lesson.id).filter(models.Lesson.id == id).first()

    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"lesson with id: {id} was not found")

    return lesson


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lesson(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(
    #     """DELETE FROM lessons WHERE id = %s returning *""", (str(id),))
    # deleted_lesson = cursor.fetchone()
    # conn.commit()

    if not current_user.is_super_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    lesson_query = db.query(models.Lesson).filter(models.Lesson.id == id)

    lesson = lesson_query.first()

    if lesson == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"lesson with id: {id} does not exist")

    if lesson.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    lesson_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Lesson)
def update_lesson(id: int, updated_lesson: schemas.LessonCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE lessons SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (lesson.title, lesson.content, lesson.published, str(id)))

    # updated_lesson = cursor.fetchone()
    # conn.commit()

    if not current_user.is_super_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    lesson_query = db.query(models.Lesson).filter(models.Lesson.id == id)

    lesson = lesson_query.first()

    if lesson == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"lesson with id: {id} does not exist")

    if lesson.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    lesson_query.update(updated_lesson.dict(), synchronize_session=False)

    db.commit()

    return lesson_query.first()
