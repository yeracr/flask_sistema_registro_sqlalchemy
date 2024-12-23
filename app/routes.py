from flask import current_app, Blueprint, render_template, redirect, url_for, request, flash  # Importa varios módulos de Flask para manejar la estructura de la aplicación web.
from flask_login import login_user, logout_user, login_required, current_user  # Importa funciones y decoradores de flask_login para manejar la autenticación de usuarios.
from app import db, login_manager  # Importa la instancia de la base de datos y el gestor de inicio de sesión desde la aplicación.
from app.models import User, Role  # Importa los modelos User y Role definidos en la aplicación.
from werkzeug.security import generate_password_hash, check_password_hash  # Importa funciones para la generación y verificación de hashes de contraseñas.
from datetime import datetime  # Importa la clase datetime para trabajar con fechas y horas.


from app.herramientas.user_service import UserService  # Importa el servicio de usuario desde app.herramientas.user_service.
bp = Blueprint('auth', __name__)  # Crea un blueprint para el módulo de autenticación.

@bp.route('/register', methods=['GET', 'POST'])  # Define una ruta para el registro que acepta métodos GET y POST.
def register():  # Define la vista para el registro.
    if request.method == 'POST':  # Si el método de la solicitud es POST...
        email = request.form.get('email')  # ...obtiene el email del formulario.
        username = request.form.get('username')  # ...obtiene el nombre de usuario del formulario.
        password = request.form.get('password')  # ...obtiene la contraseña del formulario.
        
        success, result = UserService.create_user(username, email, password)  # Llama al método create_user del UserService.
        
        if success:  # Si la creación del usuario fue exitosa...
            login_user(result)  # ...inicia sesión en el nuevo usuario.
            return redirect(url_for('auth.home'))  # Redirecciona a la página principal.
        else:
            flash(result)  # Muestra un mensaje de error.
            
    return render_template('register.html')  # Renderiza la plantilla de registro si el método no es POST.



@bp.route('/login', methods=['GET', 'POST'])  # Define una ruta para el login que acepta métodos GET y POST.
def login():  # Define la vista para el login.
    if request.method == 'POST':  # Si el método de la solicitud es POST...
        email = request.form.get('email')  # ...obtiene el email del formulario.
        password = request.form.get('password')  # ...obtiene la contraseña del formulario.

        user = User.query.filter_by(email=email).first()  # Busca al usuario por email.

        if user:
            if user.is_locked():  # Verifica si el usuario está bloqueado.
                flash('Your account is locked. Please try again later.', 'error')
                return render_template('login.html')

            if check_password_hash(user.password, password):  # Verifica la contraseña.
                user.reset_failed_attempts()  # Resetea los intentos fallidos si la contraseña es correcta.
                login_user(user)  # Inicia sesión en el usuario.
                user.last_login = datetime.now()  # Actualiza la última hora de inicio de sesión.
                db.session.commit()  # Guarda los cambios en la base de datos.
                return redirect(url_for('auth.home'))  # Redirecciona a la página principal.
            else:
                user.register_failed_attempt()  # Incrementa los intentos fallidos si la contraseña es incorrecta.
                flash('Invalid email or password.', 'error')
        else:
            flash('Invalid email or password.', 'error')
            
    return render_template('login.html')  # Renderiza la plantilla de login si el método no es POST.

@login_manager.user_loader  # Decorador que define la función de carga de usuario para flask_login.
def load_user(user_id):  # Define la función que carga un usuario dado su ID.
    return User.query.get(int(user_id))  # Busca y devuelve el usuario con el ID dado.

@bp.route('/logout')  # Define una ruta para el logout.
@login_required  # Requiere que el usuario esté autenticado para acceder a esta vista.
def logout():  # Define la vista para el logout.
    logout_user()  # Cierra la sesión del usuario.
    return redirect(url_for('auth.login'))  # Redirecciona a la página de login.

@bp.route('/')  # Define otra ruta para la página principal.
@login_required  # Requiere que el usuario esté autenticado para acceder a esta vista.
def home():  # Define la vista para la página principal.
    return render_template('home.html', user=current_user)  # Renderiza la plantilla de la página principal con el usuario actual.
