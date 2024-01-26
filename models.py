#### Archivo de clases === tablas para scrapper_test.db ####

import db

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Category(db.Base):
    
    # Argumentos que contendrá nuestra tabla
    __tablename__ = "categories"
    __table_args__ = {"sqlite_autoincrement": True }
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    questions = relationship('QuestionsAnswers', back_populates='category', cascade='all, delete, delete-orphan')
    
    # timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Creamos la categoria: {}".format(self.name)


class QuestionsAnswers(db.Base):

    __tablename__ = "questions_answers"
    __table_args__ = {"sqlite_autoincrement": True }
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    right_answer = Column(String, nullable=False)
    wrong_1 = Column(String)
    wrong_2 = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id")) # Hay que establecer la co-relación con la tabla de categorias.
    category = relationship('Category', back_populates="questions") # GPT snippet

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, question, right_answer, wrong_1, wrong_2, category=None): # Falta manejar la categoría
        self.question = question
        self.right_answer = right_answer
        self. wrong_1 = wrong_1
        self.wrong_2 = wrong_2
        self.category = category

    def __str__(self):
        return "PREGUNTA: {}".format(self.question)


