from werkzeug.security import generate_password_hash, check_password_hash
from app.common.scripts import inicializandoConexion
from flask import Blueprint, request, jsonify
from sqlalchemy import text as sql_text

# Crear un Blueprint para las rutas de login
login = Blueprint('login', __name__)

# Ruta para registrar usuario
@login.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Inicializar la conexión a la base de datos
    engine = inicializandoConexion()
    if engine is None:
        return jsonify({"error": "No se pudo establecer conexión con la base de datos."}), 500

    try:
        # Verificar si el usuario ya existe
        with engine.connect() as connection:
            existing_user_query = sql_text("SELECT * FROM users WHERE email = :email")
            result = connection.execute(existing_user_query, {'email': email}).fetchone()
            if result:
                return jsonify({"error": "El usuario ya existe"}), 400

            # Insertar nuevo usuario
            hashed_password = generate_password_hash(password)
            insert_query = sql_text("""
                INSERT INTO users (email, password)
                VALUES (:email, :password)
            """)
            connection.execute(insert_query, {'email': email, 'password': hashed_password})
            connection.commit()

            return jsonify({"message": "Usuario creado exitosamente"}), 201

    except Exception as ex:
        print(f"Error al registrar el usuario: {ex}")
        return jsonify({"error": "Error en el registro"}), 500

# Ruta para iniciar sesión
@login.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Inicializar la conexión a la base de datos
    engine = inicializandoConexion()
    if engine is None:
        return jsonify({"error": "No se pudo establecer conexión con la base de datos."}), 500

    try:
        with engine.connect() as connection:
            # Buscar el usuario
            user_query = sql_text("SELECT * FROM users WHERE email = :email")
            user = connection.execute(user_query, {'email': email}).fetchone()

            if user is None or not check_password_hash(user['password'], password):
                return jsonify({"error": "Credenciales incorrectas"}), 400

            # Si las credenciales son correctas, retornar un mensaje
            return jsonify({"message": "Inicio de sesión exitoso"}), 200

    except Exception as ex:
        print(f"Error al iniciar sesión: {ex}")
        return jsonify({"error": "Error en el inicio de sesión"}), 500

