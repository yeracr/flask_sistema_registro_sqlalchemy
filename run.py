from app import create_app, db  # Importa la función create_app y la instancia de la base de datos db desde app.
import os  # Importa el módulo os para interactuar con el sistema operativo.

# Crea la instancia de la aplicación.
app = create_app()

try:
    # Usa el contexto de la aplicación para crear todas las tablas en la base de datos.
    with app.app_context():
        db.create_all()
except Exception as e:
    print(f"Error initializing the database: {e}")

# Verifica si el script se está ejecutando directamente.
if __name__ == "__main__":
    # Configura el puerto desde una variable de entorno, con un valor por defecto de 5000.
    port = int(os.environ.get('PORT', 5000))
    # Corre la aplicación en modo debug.
    app.run(debug=True, port=port)
