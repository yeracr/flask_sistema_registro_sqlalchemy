from app import db  # Importa la instancia de la base de datos db desde el módulo app.
from flask_login import UserMixin  # Importa UserMixin desde flask_login para añadir métodos útiles de inicio de sesión a la clase User.

from datetime import datetime, timedelta# Importa la clase datetime del módulo datetime para trabajar con fechas y horas.
from flask import current_app


class Role(db.Model):  # Define una clase Role que hereda de db.Model, indicando que es un modelo de base de datos.
    __tablename__ = 'roles'  # Especifica el nombre de la tabla en la base de datos.
    id = db.Column(db.Integer, primary_key=True)  # Define una columna id como entero y clave primaria.
    name = db.Column(db.String(50), unique=True, nullable=False)  # Define una columna name como cadena de hasta 50 caracteres, única y no nula.
    description = db.Column(db.String(200))  # Define una columna description como cadena de hasta 200 caracteres.
    users = db.relationship('User', backref='role', lazy='dynamic')  # Define una relación uno a muchos con la clase User.

    def __repr__(self):  # Define el método __repr__ que devuelve una representación en cadena de un objeto Role.
        return f'<Role {self.name}>'  # Devuelve una cadena con el nombre del rol.

class User(UserMixin, db.Model):  # Define una clase User que hereda de UserMixin y db.Model.
    __tablename__ = 'users'  # Especifica el nombre de la tabla en la base de datos.
    id = db.Column(db.Integer, primary_key=True)  # Define una columna id como entero y clave primaria.
    username = db.Column(db.String(150), unique=True, nullable=False)  # Define una columna username como cadena de hasta 150 caracteres, única y no nula.
    email = db.Column(db.String(150), unique=True, nullable=False)  # Define una columna email como cadena de hasta 150 caracteres, única y no nula.
    password = db.Column(db.String(150), nullable=False)  # Define una columna password como cadena de hasta 150 caracteres, no nula.
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)  # Define una columna role_id como entero y clave foránea que referencia a roles.id.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Define una columna created_at como DateTime, con valor por defecto la fecha y hora actual en UTC.
    last_login = db.Column(db.DateTime)  # Define una columna last_login como DateTime para almacenar la última fecha y hora de inicio de sesión.
    active = db.Column(db.Boolean, default=True)  # Define una columna active como booleano con valor por defecto True.
    # ... (otros campos)
    failed_attempts = db.Column(db.Integer, default=0)
    lock_until = db.Column(db.DateTime, nullable=True)

    # Método para verificar si el usuario está bloqueado
    def is_locked(self):
        if self.lock_until and self.lock_until > datetime.utcnow():
            return True
        return False

    # Método para incrementar los intentos fallidos y bloquear la cuenta
    def register_failed_attempt(self):
        self.failed_attempts += 1
        if self.failed_attempts >= current_app.config['MAX_FAILED_ATTEMPTS']:
            self.lock_until = datetime.utcnow() + timedelta(minutes=current_app.config['LOCKOUT_TIME'])
        db.session.commit()

    # Método para resetear los intentos fallidos
    def reset_failed_attempts(self):
        self.failed_attempts = 0
        self.lock_until = None
        db.session.commit()

    def __repr__(self):  # Define el método __repr__ que devuelve una representación en cadena de un objeto User.
        return f'<User {self.username}>'  # Devuelve una cadena con el nombre de usuario.

    def get_role_name(self):  # Define el método get_role_name que devuelve el nombre del rol asociado al usuario.
        return self.role.name  # Devuelve el nombre del rol asociado.
