from flask import (
    Flask,      render_template,        request,
    Response,   session,                g,
    redirect,   url_for,                flash)
from flask_pymongo import PyMongo
from flask_login import LoginManager
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
from flask_login import current_user, login_user, logout_user, login_required


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/appone"
mongo = PyMongo(app)

@app.route('/')
def star():
    #if not session.get('logged_in'):
    return render_template('login.html')

@app.route('/login', methods=["GET" , "POST"])
def login():
    #session.pop('user_id', None)
    if request.method == 'POST':    
        username = request.form['email']
        pas = request.form['pas']
        haspas = generate_password_hash(pas)   
        usuario = mongo.db.usuarios.find_one({'user':username})
        r = check_password_hash(haspas, pas)
        print (username, pas ,haspas, r)
        print (usuario)
        if (usuario['user'] == username and 
            check_password_hash(usuario['pass'],pas)):
            return render_template('main.html')
    #   return ('oaaa')
        return render_template('login.html')
        
    return render_template("login.html")

@app.route('/main')
def acceder():
    return render_template("main.html")

@app.route('/registro')
def registrar():
    return render_template("registro.html")

@app.route('/newuser', methods=['POST'])
def newuser():
    nombre = request.form['nombre']
    user = request.form['user']
    pas = request.form['pass']
    print(request.json)
    if  nombre and user and pas:
        hashed_pas = generate_password_hash(pas)
        print(hashed_pas)
        id = mongo.db.usuarios.insert(
            {'nombre': nombre, 'user': user, 'pass': hashed_pas}
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


