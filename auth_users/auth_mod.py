from flask import jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash


# Traemos la clase para poder crear los registros y la base de datos
import db
from db import sa_engine
from models import User

def register_user():

    print("\nEntramos en la funcion??????\n")
    if request.method == "POST":
        try:
            # Para manejar las solicitudes de json en Flask
            data = request.get_json()

            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            print("Los datos que hemos recibido son: ", username, email, password)

            # Comprobar que el usuario no existe en la bbdd
            existing_user = db.session.query(User).filter_by(email=email).first()
            if existing_user:
                print("\nYa existe un usuario registrado con este email\n")
                return jsonify({'message': 'User already exists!'}), 400
            
            # Hasheamos contraseña
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            # Creamos la instancia de usuario en la bbdd
            new_user = User(username= username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message':'Successful register!'})
        
        except Exception as e:
            print(type(e).__name__)
            db.session.rollback()
            return jsonify({'message': 'Register failed', 'error': str(e)}), 500

        finally:
            print("Cerramos la session.")
            db.session.close()
    


def user_login():
    pass
        


def log_out():
    # Limpiar la sesión para cerrar la sesión del usuario
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'})

