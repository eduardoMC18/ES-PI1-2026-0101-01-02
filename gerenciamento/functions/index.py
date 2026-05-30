import random
from mysql.connector import Error

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import gerenciamento.infra.database
from crypto.hillCipher import *
from utils.utils import criptografaCPF, criptografaChave, chave, descriptografaCPF, limpar


def gerenciamento_menu():
    """
    Exibe o menu de gerenciamento de eleitores e direciona o usuário para as ações correspondentes.

    A função roda em um loop contínuo até que o usuário decida voltar (opção 6). 
    Ela lê a entrada do teclado, limpa a tela e chama as respectivas funções baseadas na escolha.

    Args:
        Nenhum.

    Returns:
        None: A função não retorna nenhum valor.
    """

    a = 0
    while a != 6:
        a = int(input("Escolha uma opção:\n1-Cadastrar eleitor\n2-Buscar eleitor\n3-Remover eleitor\n4-Editar eleitor\n5-Listar eleitor\n6-Voltar\n\nEscolha uma opção: "))
        match a:
            case 1: 
                limpar()
                cadastrar_eleitor()
            case 2:
                limpar()
                buscar_eleitor(gerenciamento.infra.database.conexao)
            case 3:
                limpar()
                remover_eleitor(gerenciamento.infra.database.conexao)
            case 4:
                limpar()
                editar_eleitor()
            case 5:
                limpar()
                gerenciamento.infra.database.listar_usuarios()
            case 6:
                limpar()
                print("Voltando...")
                return
            case _:
                print("Opcão Inválida")
 

def cadastrar_eleitor():
        """
    Realiza o cadastro de um novo eleitor no banco de dados após validar os dados fornecidos.

    A função processa o nome completo para extrair as iniciais e gerar uma chave de acesso,
    valida se o CPF e o Título de Eleitor são matematicamente válidos e converte a opção de
    mesário para um tipo booleano. Se todas as validações passarem, os dados sensíveis são
    criptografados e salvos no banco de dados.

    Args:
        nome (str): O nome completo do eleitor (deve conter pelo menos nome e sobrenome).
        cpf (str): String com os 11 dígitos do CPF (apenas números).
        titulo_eleitor (str): String com os 12 dígitos do título de eleitor (apenas números).
        mesario_input (str): Sinalização se o eleitor é mesário (aceita 'y' para Sim, 
            qualquer outra tecla será considerada não).

    Returns:
        None: A função exibe mensagens de sucesso ou erro diretamente no terminal e 
              não retorna valores.
    """
        
        nome = input("Digite o nome: ").strip()  
        partes_nome = nome.split()
        if len(partes_nome) < 2:
            print("\nNome inválido! É obrigatório digitar o nome completo (Nome e Sobrenome).")
            print("Retornando ao menu principal...\n")
            return
        
        primeiro_nome = partes_nome[0]
        sobrenome = partes_nome[1]
        cpf = input("Digite o cpf: ")
        titulo_eleitor = input("Digite o titulo: ")
        mesario = input("É mesario? (y/n)")
        chave_acesso = primeiro_nome[0:2].upper() + sobrenome[0].upper() + str(random.randint(1000, 9999))
        if mesario == 'y':
            mesario = True
        else:
            mesario = False
        if validar_cpf(cpf):
            if validar_titulo(titulo_eleitor):
                 chave_acesso_crypto = criptografaChave(chave_acesso, chave)
                 cpf_crypto = criptografaCPF(cpf, chave)
                 gerenciamento.infra.database.post_eleitor(nome, cpf_crypto, titulo_eleitor, mesario, chave_acesso_crypto) 
                 return print(f"Usuario cadastrado com sucesso\nNome: {nome}\nCPF: {cpf}\nChave de Acesso: {chave_acesso}")
            else:
                return print("Titulo Inválido")
        
        else:
            return print("CPF invalido")

        
def validar_cpf(cpf):
    """
    Valida um número de CPF calculando seus dígitos verificadores.

    Args:
        cpf (str): String contendo os 11 dígitos do CPF (apenas números).

    Returns:
        bool: Retorna True se o CPF for matematicamente válido, False caso contrário.
    """
    if len(cpf) != 11:
        return False
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
            return True
        else:
            return False
            
def validar_titulo(titulo_eleitor):
    """
    Valida o Título de Eleitor com base no tamanho, UF e cálculo dos dois dígitos verificadores.

    Args:
        titulo_eleitor (str): String contendo os 12 dígitos do título (apenas números).

    Returns:
        bool: Retorna True se os dígitos verificadores calculados baterem com os informados, 
              False caso contrário.
    """
    if len(titulo_eleitor) != 12:
        return False
    
    n_sequencial = titulo_eleitor[:8]
    uf = titulo_eleitor[8:10]
    dv1p = int(titulo_eleitor[10])
    dv2p = int(titulo_eleitor[11])

    soma = 0
    pesos1 = [2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(8):
        soma += int(n_sequencial[i]) * pesos1[i]
    
    resto = soma % 11
    dv1 = 0 if resto >= 10 else resto

    if uf in ["01", "02"]:
        if resto == 10 or resto == 0:
            dv1 = 1 if resto == 0 else 0 

    soma2 = (int(uf[0]) * 7) + (int(uf[1]) * 8) + (dv1 * 9)
    resto2 = soma2 % 11
    dv2 = 0 if resto2 >= 10 else resto2
    
    if uf in ["01", "02"]:
        if resto2 == 10 or resto2 == 0:
            dv2 = 1 if resto2 == 0 else 0

    return dv1p == dv1 and dv2p == dv2


def buscar_eleitor(conexao):
    """
    Busca um eleitor no banco de dados por meio do CPF ou do Título de Eleitor.

    A função interage com o usuário para definir o tipo de busca, aplica as validações
    necessárias e faz uma consulta segura utilizando parâmetros.
    Se o eleitor for encontrado, exibe seus dados descriptografados na tela.

    Args:
        conexao (mysql.connector.connection.MySQLConnection): Objeto ativo de conexão com 
            o banco de dados SQL.

    Returns:
        None: A função apenas exibe o resultado diretamente no terminal via print.
    """

    print("Buscar eleitor: ")
    print("1- Busca por CPF.")
    print("2- Busca por Titulo de eleitor.")
    opcao = input("Digite a opção desejada: ")

    if opcao == "1":
        cpf = input("Digite o CPF do eleitor (apenas números): ")
        if not validar_cpf(cpf):
            print("CPF inválido.")
            return
        cpf_crypto = criptografaCPF(cpf, chave)
        campo = "cpf"
        valor = cpf_crypto

    else:
        if opcao == "2":
            titulo = input("Digite o título de eleitor (apenas números): ")
            campo = "titulo_eleitor"
            valor = titulo

        else:
            print("Opção inválida.")
            return

    try:
        cursor = conexao.cursor(dictionary=True)

        
        sql_busca = "SELECT * FROM eleitores WHERE " + campo + " = %s"
        cursor.execute(sql_busca, (valor,))
        eleitor = cursor.fetchone()
        cursor.close()

        
        if eleitor:
            print("\nEleitor encontrado:")
            print("  Nome:   ", eleitor["nome"])
            print("  CPF:    ", descriptografaCPF(eleitor['cpf'], chave)[:-1])
            print("  Título: ", eleitor["titulo_eleitor"])

            if eleitor["mesario"] == 1:
                print("  Mesário: Sim")
            else:
                print("  Mesário: Não")

            print("  Status: ", eleitor["status_voto"])

        else:
            print("Nenhum eleitor encontrado com os dados informados.")

    except Error as e:
        print("Erro ao buscar:", e)

def remover_eleitor(conexao):
    """
    Busca um eleitor por CPF ou Título e, após confirmação do usuário, remove-o do banco de dados.

    A função interage com o usuário para obter a chave de busca, realiza a validação do CPF
    (se aplicável) e pesquisa o registro. Caso o eleitor seja encontrado, seus dados são 
    exibidos e o sistema solicita uma confirmação textual ('s') antes de executar a 
    exclusão definitiva.

    Args:
        conexao (mysql.connector.connection.MySQLConnection): Objeto ativo de conexão com 
            o banco de dados SQL.

    Returns:
        None: A função realiza operações diretamente no banco e exibe mensagens via terminal.
    """

    print("\nRemover eleitor:")
    print("1 - Buscar por CPF")
    print("2 - Buscar por título de eleitor")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cpf = input("Digite o CPF (apenas números): ")
        if not validar_cpf(cpf):
            print("CPF inválido.")
            return
        cpf_crypto = criptografaCPF(cpf, chave)
        valor = cpf_crypto
        campo = "cpf"

    else:
        if opcao == "2":
            valor = input("Digite o título de eleitor (apenas números): ")
            campo = "titulo_eleitor"

        else:
            print("Opção inválida.")
            return

    try:
        cursor = conexao.cursor(dictionary=True)

        
        sql_busca = "SELECT * FROM eleitores WHERE " + campo + " = %s"
        cursor.execute(sql_busca, (valor,))
        eleitor = cursor.fetchone()

       
        if not eleitor:
            print("Nenhum eleitor encontrado com os dados informados.")
            cursor.close()
            return

        
        print("Eleitor encontrado:")
        print("  Nome:   ", eleitor["nome"])
        print("  CPF:    ", eleitor["cpf"])
        print("  Título: ", eleitor["titulo_eleitor"])

        if eleitor["mesario"] == 1:
            print("  Mesário: Sim")
        else:
            print("  Mesário: Não")

        print("  Status: ", eleitor["status_voto"])

        
        confirmacao = input("\nDeseja realmente remover este eleitor? (s/n): ")

        if confirmacao == "s":
            sql_delete = "DELETE FROM eleitores WHERE " + campo + " = %s"
            cursor.execute(sql_delete, (valor,))
            conexao.commit()
            print("Eleitor removido com sucesso:", eleitor["nome"])
        else:
            print("Remoção cancelada.")

        cursor.close()

    except Error as e:
        print("Erro ao remover:", e)



def editar_eleitor():
    """
    Busca um eleitor por CPF ou Título e atualiza seus dados cadastrais no banco de dados.

    A função localiza o eleitor no banco e permite ao usuário alterar o Nome, Título 
    de Eleitor e o status de Mesário. Inputs vazios são interpretados como o desejo 
    de manter a informação atual. As alterações são validadas e consolidadas via UPDATE.

    Args:
        Nenhum.

    Returns:
        None: A função exibe o status da atualização na tela e não retorna valores.
    """

    print("\nEditar eleitor:")
    print("1 - Buscar por CPF")
    print("2 - Buscar por título de eleitor")
    opcao = input("Escolha uma opção: ")
    
    if opcao == "1":
        cpf = input("Digite o CPF (apenas números): ")
        if not validar_cpf(cpf):
            print("CPF inválido.")
            return
        cpf_crypto = criptografaCPF(cpf, chave)
        valor = cpf_crypto
        campo = "cpf"
    else:
        if opcao == "2":
            valor = input("Digite o título de eleitor (apenas números): ")
            campo = "titulo_eleitor"

        else:
            print("Opção inválida.")
            return
        
    try:
        cursor = gerenciamento.infra.database.conexao.cursor(dictionary=True)
        
        sql_busca = "SELECT * FROM eleitores WHERE " + campo + " = %s"
        cursor.execute(sql_busca, (valor,))
        eleitor = cursor.fetchone()

        if not eleitor:
            print("Nenhum eleitor encontrado.")
            cursor.close()
            return

        print(f"\nEleitor encontrado: {eleitor['nome']}")


        print("\nDigite os novos dados (deixe vazio para manter os atuais)")
        novo_nome = input("Novo nome: ")
        novo_titulo = input("Novo título: ")
        novo_mesario_input = input("É mesário? (Sim/Não): ")

        
        if novo_nome == "":
            novo_nome = eleitor["nome"]
            
        if novo_titulo == "":
            novo_titulo = eleitor["titulo_eleitor"]

        if novo_mesario_input == "":
            novo_mesario = eleitor["mesario"]
        else:
            novo_mesario = 1 if novo_mesario_input.lower() == "sim" else 0

        sql_update = f"UPDATE eleitores SET nome = %s, titulo_eleitor = %s, mesario = %s WHERE {campo} = %s"
        
        cursor.execute(sql_update, (novo_nome, novo_titulo, novo_mesario, valor))
        gerenciamento.infra.database.conexao.commit()
        
        print("Dados do eleitor atualizados com sucesso!")
        cursor.close()

    except Error as e:
        print("Erro ao atualizar:", e)

        print("\nDigite os novos dados (deixe vazio para manter os atuais)")
        novo_nome = input("Novo nome: ")
        novo_titulo = input("Novo título: ")
        novo_mesario = input("É mesário? (Sim/Não): ")

        if novo_nome == "":
         novo_nome = eleitor["nome"]

         if novo_titulo == "":
          novo_titulo = eleitor["titulo_eleitor"]

        if novo_mesario == "":
            novo_mesario = eleitor["mesario"]
        else:
            if novo_mesario.lower() == "sim":
             novo_mesario = 1
            else:
             novo_mesario = 0


        sql_update = """
        UPDATE eleitores
        SET nome = %s, titulo_eleitor = %s, mesario = %s
        WHERE """ + campo + " = %s"

        cursor.execute(sql_update, (novo_nome, novo_titulo, novo_mesario, valor))
        gerenciamento.infra.database.conexao.commit()

        print("Eleitor atualizado com sucesso")

        cursor.close()

    except Error as e:
            print("Erro ao atualizar:", e)    