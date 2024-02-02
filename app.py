from sqlite3 import OperationalError
from flask import Flask, jsonify, request, session
from sqlalchemy import func
from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash, check_password_hash


import db
from db import sa_engine, db
from models import Category, QuestionsAnswers, User

from auth_users.auth_mod import register_user, user_login, log_out
from scrapper_bot_01.bot_01 import categorizedTriviaTest, categorizingQuestions, randomTriviaTest, scrappeCategories, scrappeQuestionsAndAnswers


app = Flask(__name__)

CORS(app)
app.secret_key = "secret-key" ### La traemos de una carpeta environment

"""
#### MYSQL DB CONFIG ---> from flask_mysql import MYSQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = '<nombre de nuestra bbdd>'


mysql = MYSQL(app)
"""

# Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database/scrapper_test_01_02.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_CONNECT_ARGS'] = {'check_same_thread': False}

db.init_app(app)




############################
# Ruta de inicio del backend
@cross_origin
@app.route('/')
def init_app():
    return "Iniciamos app"

#### FUNCIONES PARA MANEJO DE USUARIOS DESDE AUTH MODULE
@cross_origin
@app.route('/register', methods=['POST'])
def register_route():
    return register_user()
 

@cross_origin
@app.route('/login', methods=['POST'])
def login_route():

    print("\nEntramos en la funcion??????\n")
    if request.method == "POST":
        try:
            # Asegúrate de que el tipo de contenido sea JSON
            if request.is_json:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')

                # Buscamos al usuario en la bbdd
                user = db.session.query(User).filter_by(username = username).first()

                if user and check_password_hash(user.password, password):
                    # Usuario correcto, creamos la sesión
                    session['user_id'] = user.id
                    return jsonify({'message': 'Success'})
                else:
                    return jsonify({'message': 'Invalid username or password'}), 401
            else:
                return jsonify({'message': 'Invalid username or password'}), 401  

        # except OperationalError as e:
        #     print(repr(e))

        except Exception as e:
            print(repr(e))  # Imprimir la excepción completa
            import traceback
            traceback.print_exc()  # Imprimir el traceback completo
            return jsonify({'message': 'Login failed', 'error': repr(e)}), 500



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

