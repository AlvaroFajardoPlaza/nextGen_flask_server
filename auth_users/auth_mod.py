from flask import jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash


# Traemos la clase para poder crear los registros y la base de datos
import db
from db import sa_engine
from models import User

def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Comprobar que el usuario no existe en la bbdd
        existing_user = db.session.query(User).filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'User already exists!'}), 400
        
        # Hasheamos contraseña
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Creamos la instancia de usuario en la bbdd
        new_user = User(username= username, email=email, password=hashed_password)
        db.session.add(new_user)
        try:
            db.session.commit()
            return jsonify({'message':'Successful register!'})

        
        except Exception as e:
            print(type(e).__name__)
            db.session.rollback()
            return jsonify({'massage':'Register failed', 'error':str(e)})

        finally:
            db.session.close()
    


def user_login():
    if request.method == "POST":
        
        username = request.form['username']
        password = request.form['password']

        # Buscamos al usuario en la bbdd
        user = db.session.query(User).filter_by(username = username).first()

        if user and check_password_hash(user.password, password):
            # Usuario correcto, creamos la sesión
            session['user_id'] = user.id
            return jsonify({'message': 'Success'})
        else:
            return jsonify({'message': 'Invalid username or password'})


def log_out():
    # Limpiar la sesión para cerrar la sesión del usuario
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'})

