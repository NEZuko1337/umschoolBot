import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship
from app.db.connection import db_session


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    scores = relationship("Score", back_populates="student")

    @classmethod
    async def register_student(cls, user_id, first_name: str, last_name: str):
        query = sa.insert(Student).values(
            id=user_id,
            first_name=first_name,
            last_name=last_name
        ).returning(Student)
        created_student = await db_session.get().execute(query)
        return created_student.scalars().first()

    @classmethod
    async def get_student(cls, student_id):
        query = sa.select(Student).where(Student.id == student_id)
        student = await db_session.get().execute(query)
        return student.scalars().first()


class Score(Base):
    __tablename__ = 'scores'
    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'))
    student = relationship("Student", back_populates="scores")

    @classmethod
    async def register_subject(cls, student_id, subject: str, score: int):
        query = sa.insert(Score).values(
            subject=subject,
            score=score,
            student_id=student_id
        ).returning(Score)
        created_score = await db_session.get().execute(query)
        return created_score.scalars().first()

    @classmethod
    async def get_all_scores(cls, student_id):
        query = sa.select(Score).where(Score.student_id == student_id)
        scores = await db_session.get().execute(query)
        return scores.scalars().all()
