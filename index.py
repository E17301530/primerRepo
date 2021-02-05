from flask import (
    Flask,      render_template,        request,
    Response,   session,                g,
    redirect,   url_for,                flash,
    abort)
from flask_pymongo import PyMongo
from flask_login import LoginManager
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
from flask_login import current_user, login_user, logout_user, login_required
import time

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'
app.config["MONGO_URI"] = "mongodb://localhost:27017/appone"
mongo = PyMongo(app)


@app.before_request
def before_request():
    g.user = None
    g.user = current_user
    if 'user_id' in session:
        usuario = mongo.db.usuarios.find_one({'user':session['user_id']})
        g.usuario = usuario

@app.route('/')
def star():
    #if not session.get('logged_in'):
    return render_template('login.html')

@app.route('/login', methods=["GET" , "POST"])
def login():
    if request.method == 'POST': 
        session.pop('user_id', None) 
        session.clear()  
        username = request.form['email']
        pas = request.form['pas']  
        usuario = mongo.db.usuarios.find_one({'user':username})
        if (usuario):
            if (usuario['user'] == username and 
                check_password_hash(usuario['pass'],pas)):
                session['user_id'] = usuario['user']
                flash('bienvenido')
                return redirect(url_for('main'))
            else:
                flash('usuario o contraseña incorrectas','alert alert-danger')
                return redirect(url_for('login'))
        else:
            flash('usuario o contraseña incorrectas','alert alert-danger')
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route('/main')
def main():
    if not g.usuario:
        return render_template("login.html")
    return render_template("main.html")

@app.route('/registrar')
def registrar():
    if not g.usuario:
        return render_template("login.html")
    return render_template("registro.html")

@app.route('/newuser', methods=['POST'])
def newuser():
    if g.usuario:
        nombre = request.form['nombre']
        apellidoP = request.form['apellidoPaterno']
        apellidoM = request.form['ApellidoMaterno']
        tipoUsuario = request.form['tipoUusuario']
        user = request.form['user']
        pas = request.form['pass']
        pas2 = request.form['pass2']
        #emple = {{g.usuario.nombre}}
        #creadoPor = g.usuario.nombre
        usuario = mongo.db.usuarios.find_one({'user':user})
        print(usuario)
        if (usuario):
            flash('el usuario ya existe en la base de datos','alert alert-danger')
            return redirect(url_for('registrar'))            
        else:
            if  (pas == pas2 and nombre and apellidoP and apellidoM and tipoUsuario and user and pas):
                hashed_pas = generate_password_hash(pas)
                mongo.db.usuarios.insert(
                    {'nombre': nombre, 'apellidoPaterno':apellidoP,
                    'apellidoMaterno': apellidoM,'tipoUsuario': tipoUsuario,
                    'user': user, 'pass': hashed_pas,# 'creado por': emple,
                    'fecha': time.strftime("%d/%m/%y"),'hora': time.strftime("%H:%M:%S")}
                )
                flash('ususario creado correctamente','alert alert-success')
                return redirect(url_for('registrar'))
            else:
                flash('las contraseñas no coinsiden','alert alert-danger')
                return redirect(url_for('registrar'))  
    else:
        return redirect(url_for('login'))
    return render_template("registro.html")

@app.route('/usuarios')
def getUsuarios():
    if g.usuario:
        usuarios = mongo.db.usuarios.find()
        return render_template("listarUsuarios.html",usuarios=usuarios)
    else:
        flash('usted nesesita identificarse','alert alert-success')
        return star()

@app.route('/usuario/<id>')
def getusuario(id):
    user = mongo.db.usuarios.find_one({'_id':ObjectId(id)})
    res = json_util.dumps(user)
    return Response(res, mimetype='aplication/json')

#eliminar postman
@app.route('/usuario/<id>', methods=['Delete'])
def deleteUsuario(id):
    mongo.db.usuarios.delete_one({'_id':ObjectId(id)})
    return ("usuario elimindado")

@app.route('/eliminarU', methods=['POST'])
def eliminarU():
    if request.method == 'POST':
        return 'eliminar'
    mongo.db.usuarios.delete_one({'_id':ObjectId(id)})
    return ("usuario elimindado")

@app.route('/out', methods=['POST'])
def out():
    session.pop('user_id', None)
    return star()

@app.route('/lisusers')
def getus():
    listUser = mongo.db.usuarios.find()
    resu = json_util.dumps(listUser)
    return Response(resu, mimetype='aplication/json')

if __name__ ==  "__main__":
    app.run(debug=True)


