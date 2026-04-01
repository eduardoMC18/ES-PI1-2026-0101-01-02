import sys
import os

sys.path.append(os.path.abspath(".."))

from crypto.hillCipher import matrixMultiplication
matrizA = [[2, 1], 
           [3, 4]]
matrizB = [[16], 
           [5]] 
matrixMultiplication(matrizA, matrizB)

# class Eleitor:
#     def __init__(self, nome, titulo, cpf, mesario):
#         self.nome = nome
#         self.titulo_eleitor = titulo
#         self.cpf = cpf
#         self.mesario = mesario

def menu():
    a = int(input("escolha uma opção:\n1-cadastrar eleitor\n2-buscar eleitor\n3-listar eleitor\n4-remover celeitor\n5-editar eleitor\n6- Sair\n"))
    while not a == 6:
        match a:
            case 1: 
                cadastrar_eleitor()
                menu()
            case 2:
                # buscar_eleitor()
                menu()
            case 3:
                # remover_eleitor()
                menu()
            case 4:
                # editar_eleitor()
                menu()
            case 5:
                # listar_eleitor()
                menu()
            case 6:
                print("Encerrando programa...")
                break      
 
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



# cadastrar_eleitor()

def validar_cpf(cpf):
    if len(cpf) != 11:
        print("CPF Inválido.")
    else:
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = soma % 11
        num1 = 0 if resto < 2 else 11 - resto

        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = soma % 11
        num2 = 0 if resto < 2 else 11 - resto

        if str(num1) == cpf[9] and str(num2) == cpf[10]:
            print("CPF Validado com Sucesso")
        else:
            print("CPF Inválido")


validar_cpf("14551744751")