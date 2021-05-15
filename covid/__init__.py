from flask import Flask

app = Flask(__name__)

from covid import views #traemos las rutas, despues de haber creado la app