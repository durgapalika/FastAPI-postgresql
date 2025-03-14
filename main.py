from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class Course(BaseModel):
    id: int
    title: str
    description: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# dependency injection
db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/")
def create_course(course: Course, db: db_dependency):
    db_course = models.Courses(title=course.title, description=course.description)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@app.get("/{course_id}")
def get_course_by_id(course_id: int, db: db_dependency):
    result = db.query(models.Courses).filter(models.Courses.id == course_id).first()
    if result:
        return result
    raise HTTPException(status_code=404)


@app.get("/")
def get_all_courses(db: db_dependency):
    return db.query(models.Courses).all()


@app.put("/")
def update_course(course: Course, db: db_dependency):
    result = db.query(models.Courses).filter(models.Courses.id == course.id).first()
    if result:
        result.title = course.title
        result.description = course.description
        db.commit()
        return "Course updated successfully"
    else:
        raise HTTPException(status_code=404,
                            detail=f"No course found with id {course.id}")


@app.delete("/")
def delete_course(course_id: int, db: db_dependency):
    result = db.query(models.Courses).filter(models.Courses.id == course_id).first()
    if result:
        db.delete(result)
        db.commit()
        return "Course deleted successfully"
    else:
        raise HTTPException(status_code=404,
                            detail=f"No course found with id {course.id}")
