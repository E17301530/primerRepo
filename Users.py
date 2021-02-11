from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['appone']

nombre = "root"
apellidoPaterno = "user"
apellidoMaterno = "master"
tipoUsuario = "root"
user = "root@gmail.com"
pas = "pbkdf2:sha256:150000$8cwiGl39$74920c97dabf2f5659636772482f849725728348b295f6f467b0626cdbe389ce"
document = {'nombre':nombre, 
'apellidoPaterno':apellidoPaterno,
'apellidoMaterno':apellidoMaterno,
'tipoUsuario':tipoUsuario,
'user':user,
'pass':pas}
_id = db ['usuarios'].insert(document)
print (_id)