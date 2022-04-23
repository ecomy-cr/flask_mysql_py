from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)

# Conexión MySQL .env dotenv
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = 'ecomycr'

conexion = MySQL(app)

@app.before_request
def before_request():
    print("Antes de TODA PETICION petición. ESTA FUNCION ES EJECUTADA..")


#DESPUES DE TODA PETICION AL SERVIDOR ESTA FUNCION ES EJECUTADA
@app.after_request
def after_request(response):
    print("Después de la petición")
    return response


@app.route('/')
def index():
    #IDEA DE UN JSONIFY
    cursos = ['/cursos', '/']
    data = {
        'titulo': 'Index123',
        'bienvenida': '¡FLASK PRACTICA!',
        'cursos': cursos,
        'numero_cursos': len(cursos)
    }
    return render_template('index.html', data=data)


@app.route('/cursos')
def listar_cursos():
    data = {}
    try:
        #CONECCION CON MYSQL SERVER, CONFIG DATA ESTA EN UN .ENV 
        cursor = conexion.connection.cursor()
        sql = "SELECT codigo, nombre, creditos FROM curso ORDER BY nombre ASC"
        cursor.execute(sql)
        cursos = cursor.fetchall()
        # print(cursos)
        data['cursos'] = cursos
        data['mensaje'] = 'Exito'
    except Exception as e:
        print(str(e))
        data['mensaje'] = 'Error...'
    return jsonify(data)


def pagina_no_encontrada(error):
    #return render_template('404.html'), 404
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=8787)