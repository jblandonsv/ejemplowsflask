import os
import json
basedir = os.path.abspath(os.path.dirname(__file__))
from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

""" Configuraciones """
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'empleados.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
""" Iniciando websocket """
socketio = SocketIO(app)
clientesWS = [] # Esto servira para tener un array de clientes especificos que se conectan y evitar hacer broadcast a todos

""" Creacion de Base de datos """
from .models import Empleado
print("creando la base de datos")
db.create_all()
db.session.commit()
print("base de datos creada")


""" Rutas (Protocolo Http) """
@app.route('/')
def inicio():
    return render_template("inicio.html",empleados=Empleado.query.all())

@app.route('/formulario',methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        empleado = Empleado(nombre=request.form['nombre'], email=request.form['email'])
        db.session.add( empleado )
        db.session.commit()
        
        """ Aca se envia un mensaje al websocket con los datos del nuevo empleado """
        
        empleadoSerialized = {"id":empleado.id,
            "nombre":empleado.nombre,
            "email":empleado.email,
            "evento":"nuevo_empleado"
        }

        socketio.emit('nuevo_empleado',json.dumps(empleadoSerialized))
        
        return redirect("/")
    else:
        return render_template("formulario.html")


if __name__ == '__main__':
    socketio.run(app)