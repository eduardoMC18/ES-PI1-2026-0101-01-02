class Eleitor:
    def __init__(self, nome, titulo, cpf, mesario):
        self.nome = nome
        self.titulo_eleitor = titulo
        self.cpf = cpf
        self.mesario = mesario

def menu():
    cadastrar
    registrar
    buscar
    remover
    editar
    listar
    a = input("escolha uma opção:\n1-cadastrar eleitor\n2-buscar eleitor\n3-listar eleitor\n4-remover celeitor\n5-editar eleitor")
def cadastrar_eleitor():
    nome = input("digite o nome: ")
    cpf = input("digite o cpf: ")
    titulo = input("digite o titulo: ")
    mesario = input("É mesario? (y/n)")
    if mesario == 'y':
        mesario = True
    else:
        mesario = False
    novo_eleitor = Eleitor(nome=nome, cpf=cpf, titulo=titulo, mesario=mesario)
    print(f"Usuario cadastrado com sucesso\nnome: {novo_eleitor.nome}\ncpf: {novo_eleitor.cpf}")

cadastrar_eleitor()