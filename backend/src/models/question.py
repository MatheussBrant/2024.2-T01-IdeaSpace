from sqlmodel import SQLModel, Field, Relationship, PrimaryKeyConstraint
from typing import List
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    FACIL = "FACIL",
    MEDIO = "MEDIO",
    DIFICIL = "DIFICIL"


class CategoryBase(SQLModel):
    name: str


class Category(CategoryBase, table=True):
    id: int = Field(default=None, primary_key=True)
    slug_name: str
    questions: List["Question"] = Relationship(back_populates="category", cascade_delete=True)


class OptionBase(SQLModel):
    text: str
    is_answer: bool | None = False


class QuestionBase(SQLModel):
    text: str
    category_id: int
    difficulty: DifficultyLevel

class QuestionBaseOptional(SQLModel):
    text: str | None = None
    category_id: int | None = None


class Option(OptionBase, table=True):
    id: int = Field(default=None, primary_key=True) 
    question_id: int = Field(foreign_key="question.id", ondelete="CASCADE")
    question: "Question" = Relationship(back_populates="options")
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())


class QuestionnaireLink(SQLModel, table=True):
    question_id: int = Field(foreign_key="question.id")
    questionnaire_id: int = Field(foreign_key="questionnaire.id")

    __table_args__ = (PrimaryKeyConstraint("question_id", "questionnaire_id"),)


class Question(QuestionBase, table=True):
    id: int = Field(default=None, primary_key=True)
    category_id: int = Field(foreign_key="category.id")
    options: List[Option] = Relationship(back_populates="question", cascade_delete=True)
    category: Category = Relationship(back_populates="questions")
    questionnaires: List["Questionnaire"] = Relationship(back_populates="questions", link_model=QuestionnaireLink)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())


class Questionnaire(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    questions: List[Question] = Relationship(back_populates="questionnaires", link_model=QuestionnaireLink)
    classroom_id: int = Field(foreign_key="classroom.id")
    classroom: "Classroom" = Relationship(back_populates="questionnaires")
    duration: int
    released: bool = False
    closed: bool = False


class QuestionnaireUpdate(SQLModel):
    duration: int | None = None
    released: bool | None = None
    closed: bool | None = None


class StudentStartsQuestionnaireBase(SQLModel):
    questionnaire_id: int 


class StudentStartsQuestionnaire(SQLModel, table=True):
    student_id: int = Field(foreign_key="student.user_id")
    questionnaire_id: int = Field(foreign_key="questionnaire.id", ondelete="CASCADE")
    started_at: datetime = Field(default=datetime.now())
    already_answered: bool = False

    __table_args__ = (PrimaryKeyConstraint("student_id", "questionnaire_id"),)


class StudentAnswerOption(SQLModel, table=True):
    student_id: int = Field(foreign_key="student.user_id", ondelete="CASCADE")
    option_id: int = Field(foreign_key="option.id", ondelete="CASCADE")
    question_id: int | None = Field(foreign_key="question.id", default=None, ondelete="CASCADE")
    questionnaire_id: int = Field(foreign_key="questionnaire.id", ondelete="CASCADE")

    __table_args__ = (PrimaryKeyConstraint("student_id", "question_id", "questionnaire_id"),)