
#CREACIÓN DE RUTAS PARA UTILIZAR LOS FICHEROS

from covid import app

@app.route("/")
def index():
    return "Flask está funcionando desde views"