class Cliente:
    def __init__(self, email, cpf, nome, sexo, id=None):
        self.id = id
        self.email = email
        self.cpf = cpf
        self.nome = nome
        self.sexo = sexo