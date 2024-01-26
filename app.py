from flask import Flask


import db
from scrapper_bot_01.bot_01 import categorizingQuestions, scrappeCategories, scrappeQuestionsAndAnswers

app = Flask(__name__)


@app.route('/')
def init_app():

    #### RESET DB
    db.Base.metadata.drop_all(bind=db.sa_engine,)

    # La línea de código que debería de crear nuestras tablas en la BBDD, si no existen:
    db.Base.metadata.create_all(db.sa_engine)

    """
    DESCOMENTA ESTAS TRES FUNCIONES PARA GENERAR LAS TABLAS DE CATEGORÍAS Y PREGUNTAS

    COMO YA HEMOS GENERADO LAS TABLAS Y LOS REGISTROS, 
    NO NECESITAMOS BORRAR Y VOLVER A CREAR DE 0 LAS TABLAS.
    
    TAMBIÉN HEMOS CATEGORIZADO LAS PREGUNTAS"""
    
    scrappeCategories()
    scrappeQuestionsAndAnswers()
    categorizingQuestions()
    

    return '<h3>Estamos creando la bbdd y las tablas.</h3>'