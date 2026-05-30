
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import gerenciamento.infra.database
from crypto.hillCipher import *

chave = [[2, 1], [3, 4]]



def criptografaChave(chave_acesso, matriz):
    try:
        p1 = chave_acesso[:3] + chave_acesso[2]

        p1 = hillCipher(p1, matriz)
        p2 = hillCipherNum(chave_acesso[-4:], matriz)
        
        result = ''
        for i in range(len(p1)):
            for j in range(len(p1[0])):
                result += str(p1[i][j])
                result += str(p2[i][j])

        return result
    
    except Exception as e:
        return e


def criptografaCPF(cpf, matriz):
    try:
        cpf = cpf + "0"
        p1 = hillCipherNum(cpf[:4], matriz)
        p2 = hillCipherNum(cpf[4:8], matriz)
        p3 = hillCipherNum(cpf[8:12], matriz)
        t = p1, p2, p3
        string = ''
        for lista in t:
            for letra in lista:
                string += letra
        return string
    except Exception as e:
        return e


def descriptografaCPF(cpf, matriz):
    try:
        cpf = list(cpf)
        result1 = decifrarNum(matriz, cpf[0:4])
        result2 = decifrarNum(matriz, cpf[4:8])
        result3 = decifrarNum(matriz, cpf[8:12])
        t = result1, result2, result3
        string = ''
        for matriz in t:
            for linha in matriz:
                for elemento in linha:
                    string += str(elemento)
        return string

    except Exception as e:
        return e

def criptografaProtocolo(protocolo, matriz):
    try:
        protocolo = protocolo[:3] + 'X' + protocolo[3:] + "000"
        result1 = hillCipher(protocolo[0:4], matriz)
        result2 = hillCipherNum(protocolo[4:8], matriz)
        result3 = hillCipherNum(protocolo[8:12], matriz)
        result4 = hillCipherNum(protocolo[12:16], matriz)
        
        t = result1, result2, result3, result4
        string = ''
        string = ''
        for matriz in t:
            for linha in matriz:
                for elemento in linha:
                    string += str(elemento)
        return string
    except Exception as e:
        return e
    
def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def descriptografaProtocolo(protocolo_crypto, matriz):
    try:
        p1 = protocolo_crypto[0:4]
        p2 = protocolo_crypto[4:8]
        p3 = protocolo_crypto[8:12]
        p4 = protocolo_crypto[12:16]

        result1 = decifrar(matriz, p1)
        result2 = decifrarNum(matriz, p2)
        result3 = decifrarNum(matriz, p3)
        result4 = decifrarNum(matriz, p4)

        protocolo = ''
        for letra in result1:
            protocolo += letra

        for row in result2:
            for num in row:
                protocolo += str(num)

        for row in result3:
            for num in row:
                protocolo += str(num)

        for row in result4:
            for num in row:
                protocolo += str(num)

        protocolo = protocolo[:3] + protocolo[4:-3]
        return protocolo
    except Exception as e:
        return e