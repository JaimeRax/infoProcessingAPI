from werkzeug.security import generate_password_hash, check_password_hash
from app.common.scripts import inicializandoConexion
from flask import Blueprint, request, jsonify
from sqlalchemy import text as sql_text

# Crear un Blueprint para las rutas de login
login_bp = Blueprint('login', __name__)

# Ruta para registrar usuario
@login_bp.route('/register', methods=['POST'])
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
@login_bp.route('/', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    engine = inicializandoConexion()
    if engine is None:
        return jsonify({"error": "No se pudo establecer conexion con la base de datos."}), 500

    try:
        # Buscar usuario por correo
        with engine.connect() as connection:
            user_query = sql_text("SELECT * FROM users WHERE email = :email")
            result = connection.execute(user_query, {'email': email})
            user = result.fetchone()  # Obtiene el primer registro coincidente

            # Verificar contraseña
            if user and check_password_hash(user[3], password):
                return jsonify({
                    "status": True,
                    "message": "Inicio de sesion exitoso"
                }), 200
            else:
                return jsonify({
                    "status": False,
                    "message": "Credenciales incorrectas"
                }), 401

    except Exception as ex:
        print(f"Error al iniciar sesión: {ex}")
        return jsonify({
            "status": False,
            "error": "Error en el inicio de sesion"
        }), 500
