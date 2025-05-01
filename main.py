from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session, joinedload
import models
from database import SessionLocal, engine

app = FastAPI()

# Modèles Pydantic
class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class ChoiceOut(ChoiceBase):
    id: int
    question_id: int

    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

class QuestionOut(QuestionBase):
    id: int
    choices: List[ChoiceOut]

    class Config:
        from_attributes = True

# Dépendance de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.post('/questions/', response_model=QuestionOut)
async def create_question(question: QuestionBase, db: Session = Depends(get_db)):
    try:
        db_question = models.Questions(question_text=question.question_text)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        
        for choice in question.choices:
            db_choice = models.Choices(
                choice_text=choice.choice_text,
                is_correct=choice.is_correct,
                question_id=db_question.id
            )
            db.add(db_choice)
        
        db.commit()
        return db_question
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/questions/{question_id}", response_model=QuestionOut)
async def read_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Questions)\
                .options(joinedload(models.Questions.choices))\
                .filter(models.Questions.id == question_id)\
                .first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

# Initialisation de la base de données
def init_db():
    models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()