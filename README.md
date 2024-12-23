# Proyecto Flask de Autenticación de Usuarios

Este proyecto es una aplicación web basada en Flask que implementa autenticación de usuarios, incluyendo registro, inicio de sesión y cierre de sesión, con un límite de intentos de inicio de sesión para mejorar la seguridad.

## Características

- Registro de nuevos usuarios
- Inicio de sesión y cierre de sesión
- Manejo de roles de usuario
- Límite de intentos de inicio de sesión y bloqueo temporal de cuentas
- Protección de sesión y configuración de tiempo de vida de la sesión

## Requisitos

- Python 3.7+
- Flask==3.1.0
- Flask-SQLAlchemy==3.1.1
- Flask-Login==0.6.3
- PyMySQL==1.1.1
- SQLAlchemy==2.0.36

## Instalación

1. **Clonar el repositorio:**

    ```bash
    git clone https://github.com/yeracr/flask_sistema_registro_sqlalchemy.git
    cd flask_sistema_registro_sqlalchemy
    ```

2. **Crear un entorno virtual:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows, usa `venv\Scripts\activate`
    ```

3. **Instalar las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configurar las variables de entorno:**

    Crea un archivo `.env` en la raíz del proyecto y define las siguientes variables:

    ```env
    SECRET_KEY=tu_clave_secreta
    DATABASE_URL=mysql+pymysql://usuario:contraseña@host/nombre_base_datos
    DB_USER=tu_usuario
    DB_PASSWORD=tu_contraseña
    DB_NAME=nombre_base_datos
    DB_HOST=localhost
    ```

## Uso

1. **Inicializar la base de datos:**

    ```bash
    flask db upgrade
    ```

2. **Ejecutar la aplicación:**

    ```bash
    flask run
    ```

3. **Acceder a la aplicación:**

    Abre tu navegador y ve a `http://127.0.0.1:5000`.

## Configuración

La configuración de la aplicación se maneja en la clase `Config` ubicada en `config.py`. Aquí se pueden ajustar parámetros como `MAX_FAILED_ATTEMPTS` y `LOCKOUT_TIME` para el límite de intentos de login.

## Estructura del Proyecto

```plaintext
nombre-del-repositorio/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── herramientas/
│   │   ├── __init__.py
│   │   └── user_service.py
├── config.py
├── requirements.txt
├── .env
├── run.py
└── README.md
