from app.models import User, Role  # Importa los modelos User y Role desde app.models.
from app import db  # Importa la instancia de la base de datos db desde app.
from werkzeug.security import generate_password_hash, check_password_hash  # Importa funciones para generar y verificar hashes de contraseñas.

class UserService:  # Define la clase UserService.
    @staticmethod
    def create_user(username, email, password):  # Método estático para crear un nuevo usuario.
        """Crea un nuevo usuario con rol de estudiante"""
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(email=email).first():  # Comprueba si ya existe un usuario con el mismo email.
            return False, "Email already registered"  # Si existe, devuelve False y un mensaje de error.
            
        # Obtener rol por defecto
        student_role = Role.query.filter_by(name='Student').first()  # Busca el rol "Student" en la base de datos.
        if not student_role:  # Si no existe...
            student_role = Role(name='Student')  # ...crea uno nuevo.
            db.session.add(student_role)  # Añade el nuevo rol a la sesión de la base de datos.
            
        # Crear nuevo usuario
        user = User(  # Crea un nuevo usuario con los datos proporcionados.
            username=username,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256'),  # Genera un hash de la contraseña.
            role=student_role  # Asigna el rol "Student" al nuevo usuario.
        )
        
        try:  # Intenta añadir el usuario a la base de datos.
            db.session.add(user)  # Añade el nuevo usuario a la sesión de la base de datos.
            db.session.commit()  # Confirma la transacción en la base de datos.
            return True, user  # Si todo va bien, devuelve True y el objeto usuario.
        except Exception as e:  # Si hay un error...
            db.session.rollback()  # ...revierte la transacción.
            return False, str(e)  # Devuelve False y el mensaje de error.

    @staticmethod
    def authenticate_user(email, password):  # Método estático para autenticar un usuario.
        """Autenticar usuario"""
        user = User.query.filter_by(email=email).first()  # Busca al usuario por email.
        if user and check_password_hash(user.password, password):  # Si el usuario existe y la contraseña es correcta...
            return True, user  # ...devuelve True y el objeto usuario.
        return False, "Invalid credentials"  # Si la autenticación falla, devuelve False y un mensaje de error.
