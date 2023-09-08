from app_usuarios import app
from app_usuarios.controladores import controlador_usuarios

if __name__ == "__main__":
    app.run( debug = True, port = 5001 )