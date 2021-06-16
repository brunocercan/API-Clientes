import jsons

class ClienteDAO:
    def __init__(self, db):
        self.__db = db
    
    def salvar(self, cliente):
        cursor = self.__db.connection.cursor()
        cursor.execute('INSERT into clientes (email, cpf, nome, sexo) values (%s, %s, %s, %s)', (cliente.email, cliente.cpf, cliente.nome, cliente.sexo))
        cliente.id = cursor.lastrowid
        self.__db.connection.commit()
        return jsons.dump(cliente)

    def alterar(self, cliente, id):
        cursor = self.__db.connection.cursor()
        cursor.execute('UPDATE clientes SET email=%s, cpf=%s, nome=%s, sexo=%s where id = %s', (cliente.email, cliente.cpf, cliente.nome, cliente.sexo, id))
        return jsons.dump(cliente)

    def deletar(self, id):
        self.__db.connection.cursor().execute('delete from clientes where id = %s', (id, ))

    