from flask import (
    Flask,      render_template,        request,
    Response,   session)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

class usuario:
    def __init__(self, _id, nombre, usuario, pas):
        self._id = id
        self.nombre = nombre
        self.usuario = usuario
        self.pas = pas


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/appone"
mongo = PyMongo(app)

@app.route('/', methods=['GET','POST'])
def login():
    session.pop('user_id', None) 
    if request.methods == 'POST':
        username = request.form['email']
        pas = request.form['pas']
        usuario = mongo.db.usuarios.find_one({'user':username})
        
    return render_template("login.html")

@app.route('/registro')
def registrar():
    return render_template("registro.html")

@app.route('/main')
def acceder():
    return render_template("main.html")

@app.route('/newuser', methods=['POST'])
def newuser():
    nombre = request.json['nombre']
    user = request.json['user']
    pas = request.json['pass']
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


