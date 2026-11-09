from erros import ErroExecucao

import math
import sys

CAMINHO_ARQUIVO = "saida/codigo-objeto.txt"


SEM_ARG = {'INPP', 'PARA', 'SOMA', 'SUBT', 'MULT', 'DIVI', 'INVE',
           'CPMA', 'CPME', 'CPIG', 'CDES', 'CMAI', 'CPMI', 'IMPR', 'LEIT'}
COM_ARG = {'ALME', 'CRCT', 'CRVL', 'ARMZ', 'DSVF', 'DSVI'}
SALTOS = {'DSVF', 'DSVI'}

ARITMETICAS = {
    'SOMA': lambda a, b: a + b,
    'SUBT': lambda a, b: a - b,
    'MULT': lambda a, b: a * b,
}
RELACIONAIS = {
    'CPMA': lambda a, b: a > b,
    'CPME': lambda a, b: a < b,
    'CPIG': lambda a, b: a == b,
    'CDES': lambda a, b: a != b,
    'CMAI': lambda a, b: a >= b,
    'CPMI': lambda a, b: a <= b,
}

def carregar(linhas):
    programa = []
    for linha in linhas :
        partes = linha.split()
        if not partes:
            continue
        instrucao = partes[0]
        if instrucao in SEM_ARG:
            if len(partes) != 1:
                raise ErroExecucao(f"Instrução {len(programa)}: '{instrucao}' não recebe argumento")
            programa.append((instrucao, None))
        elif instrucao in COM_ARG:
            if len(partes) != 2:
                raise ErroExecucao(f"Instrução {len(programa)}: '{instrucao}' precisa de 1 argumento")
            try:
                if instrucao == 'CRCT':
                    arg = float(partes[1])
                else:
                    arg = int(partes[1])
            except ValueError:
                raise ErroExecucao(f"Instrução {len(programa)}: argumento inválido '{partes[1]}'")
            programa.append((instrucao, arg))
        else:
            raise ErroExecucao(f"Instrução {len(programa)}: operação desconhecida '{instrucao}'")
    for i, (instrucao, arg) in enumerate(programa):
        if instrucao in SALTOS and not (0 <= arg < len(programa)):
            raise ErroExecucao(f"Instrução {i}: salto para endereço inexistente ({arg})")
    return programa


def formata(v):
    if math.isfinite(v) and v == int(v):
        return str(int(v))
    return str(v)


def ler_numero():
    texto = input().strip().replace(',', '.')
    try:
        return float(texto)
    except ValueError:
        raise ErroExecucao(f"Entrada inválida: '{texto}' não é um número")


def executar(linhas, leitor=ler_numero, escritor=print):
    programa = carregar(linhas)
    if not programa or programa[0][0] != 'INPP':
        raise ErroExecucao("O programa deve começar com INPP")

    pilha = []
    pc = 0
    executadas = 0

    def desempilha(instrucao):
        if not pilha:
            raise ErroExecucao(f"Instrução {pc - 1} ({instrucao}): pilha vazia")
        return pilha.pop()

    def posicao(instrucao, a):
        if not (0 <= a < len(pilha)):
            raise ErroExecucao(f"Instrução {pc - 1} ({instrucao} {a}): endereço fora da pilha")
        return a

    while True:
        if pc >= len(programa):
            raise ErroExecucao("O programa terminou sem executar PARA")
        instrucao, arg = programa[pc]
        pc += 1
        executadas += 1

        if instrucao == 'INPP':
            pilha.clear()
        elif instrucao == 'PARA':
            return
        elif instrucao == 'ALME':
            pilha.extend([0.0] * arg)
        elif instrucao == 'CRCT':
            pilha.append(arg)
        elif instrucao == 'CRVL':
            pilha.append(pilha[posicao(instrucao, arg)])
        elif instrucao == 'ARMZ':
            v = desempilha(instrucao)
            pilha[posicao(instrucao, arg)] = v
        elif instrucao in ARITMETICAS:
            b = desempilha(instrucao)
            a = desempilha(instrucao)
            pilha.append(ARITMETICAS[instrucao](a, b))
        elif instrucao == 'DIVI':
            b = desempilha(instrucao)
            a = desempilha(instrucao)
            if b == 0:
                raise ErroExecucao(f"Instrução {pc - 1} (DIVI): divisão por zero")
            pilha.append(a / b)
        elif instrucao == 'INVE':
            pilha.append(-desempilha(instrucao))
        elif instrucao in RELACIONAIS:
            b = desempilha(instrucao)
            a = desempilha(instrucao)
            if RELACIONAIS[instrucao](a, b):
                pilha.append(1.0)
            else:
                pilha.append(0.0)
        elif instrucao == 'DSVF':
            if desempilha(instrucao) == 0:
                pc = arg
        elif instrucao == 'DSVI':
            pc = arg
        elif instrucao == 'IMPR':
            escritor(formata(desempilha(instrucao)))
        elif instrucao == 'LEIT':
            pilha.append(leitor())



def principal():
    try:
        with open(CAMINHO_ARQUIVO, encoding='utf-8') as f:
            linhas = f.read().splitlines()
        executar(linhas)
    except OSError as e:
        print(f"Erro ao abrir o arquivo: {e}")
        return 1
    except ErroExecucao as e:
        print(f"Erro de execução: {e}")
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(principal())