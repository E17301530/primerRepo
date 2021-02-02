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


app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'
app.config["MONGO_URI"] = "mongodb://localhost:27017/appone"
mongo = PyMongo(app)

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        usuario = mongo.db.usuarios.find_one({'user':session['user_id']})
        g.usuario = usuario
        print(g.usuario)

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
        if (usuario['user'] == username and 
            check_password_hash(usuario['pass'],pas)):
            session['user_id'] = usuario['user']
            return redirect(url_for('main'))
        return redirect(url_for('login'))
        
    return render_template("login.html")

@app.route('/main')
def main():
    if not g.usuario:
        return render_template("login.html")
    return render_template("main.html")

@app.route('/registro')
def registrar():
    return render_template("registro.html")

@app.route('/newuser', methods=['POST'])
def newuser():
    nombre = request.form['nombre']
    apellidoP = request.form['apellidoPaterno']
    apellidoM = request.form['ApellidoMaterno']
    tipoUsuario = request.form['tipoUusuario']
    user = request.form['user']
    pas = request.form['pass']
    if  nombre and apellidoP and apellidoM and tipoUsuario and user and pas:
        hashed_pas = generate_password_hash(pas)
        id = mongo.db.usuarios.insert(
            {'nombre': nombre, 'apellidoPaterno':apellidoP,
             'apellidoMaterno': apellidoM,'tipoUsuario': tipoUsuario,
             'user': user, 'pass': hashed_pas}
        )
        respo = {
            "id": str(id),
            "name": nombre,
            "user": user
        }
        return respo 
    else:
        ('error 999')
    return('guardado')

@app.route('/usuarios')
def getUsuarios():
    listUser = mongo.db.usuarios.find()
    resu = json_util.dumps(listUser)
    return Response(resu, mimetype='aplication/json')

@app.route('/usuario/<id>')
def getusuario(id):
    user = mongo.db.usuarios.find_one({'_id':ObjectId(id)})
    res = json_util.dumps(user)
    return Response(res, mimetype='aplication/json')

@app.route('/usuario/<id>', methods=['Delete'])
def deleteUsuario(id):
    mongo.db.usuarios.delete_one({'_id':ObjectId(id)})
    return ("usuario elimindado")

if __name__ ==  "__main__":
    app.run(debug=True)


