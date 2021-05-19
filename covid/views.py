
#CREACIÓN DE RUTAS PARA UTILIZAR LOS FICHEROS, QUE RECURSOS SE PUEDEN LLAMAR
from types import MethodDescriptorType
from flask import render_template, request #Se dice el nombre del fichero y va a la carpeta templates y ahí coge el archivo que le digamos entre ()
from covid import app
import csv
import json
from datetime import date

@app.route("/provincias") #provincias es el marco de la ventana, la función es el comportamiento
def provincias():
    fichero = open("data/provincias.csv", "r", encoding="utf8")
    csvreader = csv.reader(fichero, delimiter=",")

    lista = []
    for registro in csvreader:
        d = {'codigo': registro[0], 'valor': registro[1]}
        lista.append(d)
        
    fichero.close()
    print(lista)
    return json.dumps(lista)

@app.route("/provincia/<codigo>")
def laprovincia(codigo):
    fichero = open("data/provincias.csv", "r", encoding="utf8")
    dictreader = csv.DictReader(fichero, fieldnames=['codigo', 'provincia']) #para crear un diccionario con csv
    for registro in dictreader:
        if registro['codigo'] == codigo:
            fichero.close()
            return registro['provincia']
    fichero.close()
    return "La provincia no existe"

@app.route("/casos/<int:year>", defaults={'mes':None, 'dia':None}) #para saber los casos del año
@app.route("/casos/<int:year>/<int:mes>", defaults={'dia':None}) #Para saber solo los casos del mes
@app.route("/casos/<int:year>/<int:mes>/<int:dia>") 

def casos(year, mes, dia):

    if not mes: #IMPORTANTE LA SECUENCIACIÓN, SI NO TENEMOS EL MES, NO HACE FALTA TENER EL DIA
        fecha = "{:04d}".format(year) #elif más restrictivo
    elif not dia: #si dia es nada
        fecha = "{:04d}-{:02d}".format(year,mes)
    else:
        fecha = "{:04d}-{:02d}-{:02d}".format(year,mes,dia) #SE PUEDE HACER CON LA FUNCIÓN .ZFILL(2) Y SE CONVIERTE EN STRING, Y SE RELLENAN CON CEROS

    fichero = open("data/casos.csv", "r")
    casosAcumulados = 0
    dictreader = csv.DictReader(fichero)
    
    res = { #Creación de un diccionario que vamos a recorrer para ir acumulando
    'num_casos': 0, 
    'num_casos_prueba_pcr' : 0,
    'num_casos_prueba_test_ac' : 0,
    'num_casos_prueba_ag' : 0,
    'num_casos_prueba_elisa' : 0,
    'num_casos_prueba_desconocida' : 0
    }

    for registro in dictreader:
        if fecha in registro['fecha']:
            for clave in res:
                res[clave] += int(registro[clave])

        elif registro['fecha'] > fecha:
            break

    fichero.close()
    
    return json.dumps(res) #cualquier estructura te la devuelve 


@app.route("/incidenciasdiarias", methods = ['GET', 'POST'])
def incidencia():
    formulario = { #definir un diccionario por defecto
        'provincia': '',
        'fecha': str(date.today()),
        'num_casos_prueba_pcr': 0,
        'num_casos_prueba_test_ac': 0, 
        'num_casos_prueba_ag': 0,
        'num_casos_prueba_elisa': 0,
        'num_casos_prueba_desconocida': 0 
    }
    fichero = open("data/provincias.csv", "r", encoding="utf8")
    csvreader = csv.reader(fichero, delimiter=",")
    next(csvreader)

    lista = []
    for registro in csvreader:
        d = {'codigo': registro[0], 'descripcion': registro[1]}
        lista.append(d)
        
    fichero.close()

    if request.method == 'GET':
        return render_template("alta.html", datos = formulario, 
                                provincias=lista, error="") #datos = clave y formulario valor
    
    
    
    for clave in formulario:
        formulario[clave] = request.form[clave] #para no perder la info
    
    
    num_pcr = request.form['num_casos_prueba_pcr']
    try:
        num_pcr = int(num_pcr)
        if num_pcr < 0:
            raise ValueError('Debe ser positivo')
    except ValueError:
        return render_template("alta.html", datos=formulario, error= "PCR no puede ser negativa")
    
    return "Se ha hecho un post"

   


   
