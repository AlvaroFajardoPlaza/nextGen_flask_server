from flask import Flask, jsonify
from sqlalchemy import func
from flask_cors import CORS, cross_origin


import db
from models import Category, QuestionsAnswers, User

from auth_users.auth_mod import register, user_login, log_out
from scrapper_bot_01.bot_01 import categorizedTriviaTest, categorizingQuestions, randomTriviaTest, scrappeCategories, scrappeQuestionsAndAnswers



app = Flask(__name__)
app.secret_key = "secret-key" ### La traemos de una carpeta environment

"""
#### MYSQL DB CONFIG ---> from flask_mysql import MYSQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = '<nombre de nuestra bbdd>'


mysql = MYSQL(app)
"""

CORS(app)

# Iniciamos la app
@app.route('/')
def init_app():
    return "Iniciamos app"

#### FUNCIONES PARA MANEJO DE USUARIOS DESDE AUTH MODULE
@cross_origin
@app.route('/register', methods=['POST'])
def register_new_user():
    return register()

@cross_origin
@app.route('/login', methods=['POST'])
def login():
    return user_login()

@cross_origin
@app.route('/log_out')
def log_out():
    return log_out()


#### FUNCIONES PARA MANEJO DE TRIVIA
# Llamada a las categorias de la app
@cross_origin
@app.route('/categories')
def get_categories():
    categories = db.session.query(Category).all()
    return jsonify([category.serialize() for category in categories])

# Trivia Random Test API Route
@cross_origin
@app.route('/trivia')
def random_trivia_test():
    return randomTriviaTest()

# Trivia categorizado
@cross_origin
@app.route('/categorized_trivia')
def categorized_trivia(*categories): # Recibimos por params las posibles categorías
    return categorizedTriviaTest(*categories)


if __name__ == "__main__":

    #### 1º. RESET DB
    #db.Base.metadata.drop_all(bind=db.sa_engine,)


    # 2º. CREATE DB -- Tablas de models.py, si no existen
    # La línea de código que debería de crear nuestras tablas en la BBDD, si no existen:
    db.Base.metadata.create_all(db.sa_engine)

    """
    DESCOMENTA ESTAS TRES FUNCIONES PARA GENERAR LAS TABLAS DE CATEGORÍAS Y PREGUNTAS

    COMO YA HEMOS GENERADO LAS TABLAS Y LOS REGISTROS, 
    NO NECESITAMOS BORRAR Y VOLVER A CREAR DE 0 LAS TABLAS.
    
    TAMBIÉN HEMOS CATEGORIZADO LAS PREGUNTAS
    
    scrappeCategories()
    scrappeQuestionsAndAnswers()
    categorizingQuestions()
    """

    # 3º. RUN THE APP
    app.run( debug = True)  #### Cada vez que realicemos cambios en el código, se reiniciará el servidor === mismo que "nodemon" ####

