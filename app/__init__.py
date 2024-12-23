from flask import Flask  # Importa la clase Flask para crear la aplicación.
from flask_sqlalchemy import SQLAlchemy  # Importa SQLAlchemy para manejar la base de datos.
from flask_login import LoginManager  # Importa LoginManager para manejar la autenticación de usuarios.
from config import Config


db = SQLAlchemy()  # Crea una instancia de SQLAlchemy para manejar la base de datos.
login_manager = LoginManager()  # Crea una instancia de LoginManager para manejar la autenticación de usuarios.

def register_blueprints(app):
    from app import routes  # Importa las rutas definidas en app.routes.
    app.register_blueprint(routes.bp)  # Registra el blueprint de las rutas.

def create_app():
    """Crea y configura la aplicación de Flask."""
    app = Flask(__name__)  # Crea una instancia de la aplicación Flask.
    try:
        app.config.from_object(Config)  # Carga la configuración desde la clase Config.
    except Exception as e:
        print(f"Error loading configuration: {e}")
    
    db.init_app(app)  # Inicializa la base de datos con la aplicación.
    login_manager.init_app(app)  # Inicializa el gestor de inicio de sesión con la aplicación.
    login_manager.login_view = 'auth.login'  # Establece la vista de inicio de sesión predeterminada.

    register_blueprints(app)  # Llama a la función para registrar los blueprints.

    return app  # Devuelve la instancia de la aplicación.
