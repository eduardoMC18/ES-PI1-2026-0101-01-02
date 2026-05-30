matrizA = [[2, 1], [3, 4]]
matrizB = [[16], 
           [5]] 

def matrixMultiplication(a, b):
    """
    Multiplica duas matrizes a e b e retorna a matriz resultado.
    Entrada: matrizes a e b (array)
    Saída: matrizResultado (array)
    """
    linhasA= len(a)
    colunasA = len(a[0])
    linhasB = len(b)
    colunasB = len(b[0])
    if colunasA != linhasB:
        return print('matrizes não podem ser multiplicadas')
    #criar matriz com quantidade de linhas = linhasA e colunas = colunasB
    matrizResultado = []
    for i in range(linhasA):
        linha = []
        for j in range(colunasB):
            soma = 0
            for k in range(colunasA):
                soma += a[i][k] * b[k][j]
            linha.append(soma)
        matrizResultado.append(linha)

    return matrizResultado

def pmodulo(matriz, valor):
    """
    Divide todos os elementos de uma matriz por um valor e coloca no lugar de cada elemento o resto
    da divisão.

    Entrada: matriz (array) e valor (int)
    Saída: matrizmod (array)
    """
    linhasM = len(matriz)
    colunasM = len(matriz[0])
    matrizmod = []
    for i in range(linhasM):
        list = []
        for j in range(colunasM):
            list.append(matriz[i][j] % valor)
        matrizmod.append(list)
    return matrizmod

def transformaEmLetra(matriz):
    """
    Pega cada elemento da matriz e substitui por uma letra correspondente a sua localização no alfabeto.

    Entrada: matriz com numeros (array)
    Saída: matrizNova com letras(array)
    """
    alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
            'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z']
    linhasM = len(matriz)
    colunasM = len(matriz[0])
    matrizNova = []
    for i in range(linhasM):
        for j in range(colunasM):
            matrizNova.append(alfabeto[matriz[i][j]])
    return matrizNova

def transformaEmNumero(matriz):
    """
    Recebe a matriz de letras e substitui por numeros correspondentes a sua localização no alfabeto.

    Entrada: matriz com letras (array)
    Saída: matriz com numeros (array)
    """
    alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
            'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z']
    linhasM = len(matriz)
    colunasM = len(matriz[0])
    matrizNova = []

    for i in range(linhasM):
        for j in range(colunasM):
                for w in range(len(alfabeto)):
                    if matriz[i][j] == alfabeto[w]:
                        matrizNova.append(w)
    divisao = [matrizNova[i:i + 2] for i in range(0, len(matrizNova), 2)]
    return divisao


def transporMatriz(m):
    """
    Recebe uma matriz e retorna a mesma transposta, ou seja, com as linhas no lugar das colunas e colunas no lugar das linhas.

    Entrada: matriz m (array)
    Saída: matriz m transposta (array)
    """
    mT = []
    for i in range(len(m)):
        list = []
        for j in range(len(m[0])):
            list.append(m[j][i])
        mT.append(list)
    return mT


def hillCipher(p, k):
    """
    Transforma a matriz p em numeros. Transpõe a matriz p. Multiplica p por uma chave k. Transpõe o resultado da multiplicação.
    Faz o pmodulo da matriz e transforma em letra para completar o processo da cifra de hill.

    Entrada: matriz a ser criptografada p (array) e chave de criptografia k (array)
    Saída: matriz com letras resultado da criptografia (array)
    """
    p = list(p.upper())
    divisao = [p[i:i + 2] for i in range(0, len(p), 2)]
    pNum = transformaEmNumero(divisao)
    pNum = transporMatriz(pNum)
    mult = matrixMultiplication(k, pNum)
    mult = transporMatriz(mult)

    multMod = pmodulo(mult, 26)
    result = transformaEmLetra(multMod)
    return result

def hillCipherNum(p, k):
    """
    Faz o mesmo processo da cifra de hill, porém com uma matriz p de numeros inteiros.

    Entrada: matriz a ser criptografada p (array) e chave de criptografia k (array)
    Saída: matriz com letras resultado da criptografia (array)
    """
    p = list(p)
    divisao = [p[i:i + 2] for i in range(0, len(p), 2)]
    # pNum = transformaEmNumero(divisao)
    pNum = transporMatriz(divisao)
    for i in range(len(pNum)):
        for j in range(len(pNum[i])):
            pNum[i][j] = int(pNum[i][j])
    mult = matrixMultiplication(k, pNum)
    mult = transporMatriz(mult)

    multMod = pmodulo(mult, 26)
    result = transformaEmLetra(multMod)
    return result

def matrixAdj(m):
    """
    Faz a matriz adjunta de uma matriz m.

    Entrada: matriz 2x2 m (array)
    Saída: matriz 2x2 m adjunta (array)
    """
    mAdj = []
    for i in range(len(m)):
        list = []
        for j in range(len(m[0])):
            list.append(0)
        mAdj.append(list)
    mAdj[0][0] = m[1][1]
    mAdj[0][1] = int(-m[0][1]) % 26
    mAdj[1][0] = int(-m[1][0]) % 26
    mAdj[1][1] = m[0][0]

    return mAdj

def determinante(m):
    """
    Calcula o determinante de uma matriz m 2x2.

    Entrada: matriz m 2x2 (array)
    Saída: determinante de m (int)
    """
    det = (m[0][0] * m[1][1])-(m[0][1] * m[1][0])
    return det

def inversoDet(det):
    """
    Calcula o inverso da determinante em modulo de 26.

    Entrada: determinante (int)
    Saída: inverso da determinante (int)
    """
    a = [1, 3 ,5, 9, 11, 15, 17, 19, 21, 23]
    aInverso = [1, 9, 21, 15, 3, 19, 7, 23, 11, 5, 17]
    for i in range(len(a)):
        if det == a[i]:
            detInverso = aInverso[i]
    return detInverso

def matrizxnum(num, matriz):
    """
    Faz a multiplicação de uma matriz por um número inteiro.

    Entrada: num (int) e matriz 2x2 (array)
    Saída: matriz 2x2 (array)
    """
    linhas= len(matriz)
    colunas = len(matriz[0])
    for i in range(linhas):
        for j in range(colunas):
            matriz[i][j] = matriz[i][j] * num
    return matriz

def decifrar(k, c):
    """
    Encontra a matriz inversa de k. Multiplica k inverso pela matriz criptografada e compila o resultado da descriptografia
    em uma string.

    Entrada: matriz chave k (array) e matriz criptografada c (array)
    Saída: palavra descriptografada (string)
    """
    detK = determinante(k)
    inversoDetK = inversoDet(detK)
    kAdj = matrixAdj(k)
    mult = matrizxnum(inversoDetK, kAdj)
    kInverso = pmodulo(mult, 26)
    
    cNum = transformaEmNumero(c)
    cNumT = transporMatriz(cNum)
    p = matrixMultiplication(kInverso, cNumT)
    pMod = pmodulo(p, 26)
    palavra = transformaEmLetra(pMod)
    palavra = [palavra[i:i+2] for i in range(0, len(palavra), 2)]
    palavra = transporMatriz(palavra)
    palavra = sum(palavra, [])
    return palavra

def decifrarNum(k, c):
    """
    Faz o mesmo processo de descriptografia porém com uma matriz c de numeros inteiros.

    Entrada: matriz chave k (array) e matriz criptografada c de inteiros(array)
    Saída: palavra descriptografada (string)
    """
    detK = determinante(k)
    inversoDetK = inversoDet(detK)
    kAdj = matrixAdj(k)
    mult = matrizxnum(inversoDetK, kAdj)
    kInverso = pmodulo(mult, 26)
    
    cNum = transformaEmNumero(c)
    cNumT = transporMatriz(cNum)
    p = matrixMultiplication(kInverso, cNumT)
    pMod = pmodulo(p, 26)
    palavra = transporMatriz(pMod)
    return palavra
