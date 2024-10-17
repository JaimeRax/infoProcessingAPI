from sqlalchemy import create_engine, text as sql_text      #Conexion a BD
from config import settings                                 #Configuraciones

def inicializandoConexion():
    #Se verifica la conexión con la base de datos definida en el .env
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/{settings.DB_NAME}"

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    try:
        #Se inicia la conexión a la BD
        conexion = engine.connect()
        return "Conexión exitosa!"

    except Exception as ex:
        return "Error durante la conexión: {}".format(ex)
