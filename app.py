from mysql.connector import Error

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from utils.utils import limpar
from gerenciamento.functions.index import gerenciamento_menu
from votação.functions.index import votacao_menu

def inicio():
    """
    Menu inicial da aplicação contendo levando aos demais módulos do código
    Arg: None
    Return: None
    """
    option = 0
    while option != 3:
        option = int(input("Escolha qual área deseja acessar:\n1-Gerenciamento\n2-Votação\n3-Encerrar Programa\n\nEscolha uma opção: "))
        match option:
            case 1: 
                limpar()
                gerenciamento_menu()
            case 2:
                limpar()
                votacao_menu()
            case 3:
                limpar()
                print("Encerrando programa...")
                break
            case _:
                print("Opcão Inválida.")

inicio()
