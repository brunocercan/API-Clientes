from flask import Flask, jsonify, request, make_response
from flask_mysqldb import MySQL
from model_clientes import Cliente
from dao_clientes import ClienteDAO
from functools import wraps
import jsons

app = Flask(__name__)
db = MySQL(app)
app.config.from_pyfile('db_config.py')
cliente_dao = ClienteDAO(db)
# =================================================== AUTENTICAÇÃO =========================================== #


def login(f):
   @wraps(f)
   def decorated(*args, **kwargs):
      login = request.authorization
      if login and login.username == 'login' and login.password == 'senha':
         return f(*args, *kwargs)
      else:
         return make_response('Login ou senha incorreto!', 401, {'WWW-Authenticate' : 'Basic realm="Necessario Login"'})
   return decorated


# =================================================== ROTAS ================================================== #

@app.route('/')
@login
def index():
    return jsonify({'API':  'CLIENTES'})

@app.route('/clientes/cadastro', methods = ['POST', ])
def post():
   email = request.json['email']
   cpf = request.json['cpf']
   nome = request.json['nome']
   sexo = request.json['sexo']
   cliente = Cliente(email, cpf, nome, sexo)
   return cliente_dao.salvar(cliente)

@app.route('/clientes/alterar/<int:id>', methods = ['PUT', ])
def put(id):
    cliente = buscar(id)
    nome = request.json['nome']
    email = request.json['email']
    cpf = request.json['cpf']
    sexo = request.json['sexo']
    cliente = Cliente(email, cpf, nome, sexo, id)
    cliente_dao.alterar(cliente, id)
    return jsonify('Cliente alterado com sucesso')

@app.route('/clientes/listar', methods = ['GET', ])
def listar():
    lista = listar(db)
    return jsonify(lista)

@app.route('/clientes/buscar/<int:id>')
def buscar(id):
    try:
        cliente = filtrar_por_id(db, id)
    except:
        pass
        return jsonify('id invalido')
    else:
        return cliente

@app.route('/clientes/deletar/<int:id>', methods = ['DELETE', ])
def delete(id):
    try:
        cliente = filtrar_por_id(db, id)
    except:
        pass
        return jsonify('id invalido')
    else:
        cliente_dao.deletar(id)
        return jsonify('cliente deletado com suce')


#==================métodos=====================#
def listar(db):
        cursor = db.connection.cursor()
        cursor.execute('SELECT id, email, cpf, nome, sexo from clientes')
        clientes = converte_cliente(cursor.fetchall())
        return clientes

def filtrar_por_id(db, id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT id, email, cpf, nome, sexo from clientes where id=%s', (id, ))
    tupla = cursor.fetchone()
    return jsons.dump(Cliente(id=tupla[0], nome=tupla[3], email=tupla[1], cpf=tupla[2], sexo=tupla[4]))

def converte_cliente(clientes):
    def cria_cliente_com_tupla(tupla):
        a_dict = jsons.dump(Cliente(id=tupla[0], email=tupla[1], cpf=tupla[2], nome=tupla[3], sexo=tupla[4]))
        return a_dict #ordenando as tuplas em id, nome, email, cpf e sexo   
    return jsons.dump(list(map(cria_cliente_com_tupla, clientes)))

app.run(host='0.0.0.0')