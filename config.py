import os  # Importa el módulo os para interactuar con el sistema operativo.
from datetime import timedelta  # Importa timedelta de datetime para manejar duraciones de tiempo.

class Config:
    """Clase de configuración para la aplicación."""

    # Usar variables de entorno para datos sensibles
    # Genera una clave secreta aleatoria de 24 bytes para seguridad
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)

    # Conexión a la base de datos MySQL usando PyMySQL como driver
    # Formato: mysql+pymysql://usuario:contraseña@host/nombre_base_datos

    # Llamar datos desde variables de entorno os.environ.get
    userdb = os.environ.get('DB_USER', 'ecomycr')  # Nombre de usuario de la base de datos desde la variable de entorno.
    password_db = os.environ.get('DB_PASSWORD', 'zbyj8918')  # Contraseña de la base de datos desde la variable de entorno.
    db_name = os.environ.get('DB_NAME', 'ecomycr')  # Nombre de la base de datos desde la variable de entorno.
    db_host = os.environ.get('DB_HOST', 'localhost')  # Host de la base de datos desde la variable de entorno.

    # URI de la base de datos con formato de conexión MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'mysql+pymysql://{userdb}:{password_db}@{db_host}/{db_name}'

    # Configuraciones adicionales de seguridad
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)  # Sesión expira en 1 hora.
    SESSION_PROTECTION = 'strong'  # Protección de sesión fuerte.

    # Desactiva el sistema de seguimiento de modificaciones de SQLAlchemy para mejor rendimiento
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
    # ... otras configuraciones
    MAX_FAILED_ATTEMPTS = 5  # Número máximo de intentos fallidos antes de bloquear la cuenta
    LOCKOUT_TIME = 15  # Tiempo en minutos durante el cual la cuenta está bloqueada

