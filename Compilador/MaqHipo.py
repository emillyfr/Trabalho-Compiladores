from erros import ErroExecucao

import os
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
    for n, linha in enumerate(linhas, start=1):
        partes = linha.split()
        if not partes:
            continue
        op = partes[0]
        if op in SEM_ARG:
            if len(partes) != 1:
                raise ErroExecucao(f"Instrução {len(programa)}: '{op}' não recebe argumento")
            programa.append((op, None))
        elif op in COM_ARG:
            if len(partes) != 2:
                raise ErroExecucao(f"Instrução {len(programa)}: '{op}' precisa de 1 argumento")
            try:
                if op == 'CRCT':
                    arg = float(partes[1])
                else:
                    arg = int(partes[1])
            except ValueError:
                raise ErroExecucao(f"Instrução {len(programa)}: argumento inválido '{partes[1]}'")
            programa.append((op, arg))
        else:
            raise ErroExecucao(f"Instrução {len(programa)}: operação desconhecida '{op}'")
    for i, (op, arg) in enumerate(programa):
        if op in SALTOS and not (0 <= arg < len(programa)):
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


def executar(linhas, passo=False, leitor=ler_numero, escritor=print):
    programa = carregar(linhas)
    if not programa or programa[0][0] != 'INPP':
        raise ErroExecucao("O programa deve começar com INPP")

    pilha = []
    pc = 0
    executadas = 0

    def desempilha(op):
        if not pilha:
            raise ErroExecucao(f"Instrução {pc - 1} ({op}): pilha vazia")
        return pilha.pop()

    def posicao(op, a):
        if not (0 <= a < len(pilha)):
            raise ErroExecucao(f"Instrução {pc - 1} ({op} {a}): endereço fora da pilha")
        return a

    while True:
        if pc >= len(programa):
            raise ErroExecucao("O programa terminou sem executar PARA")
        ip = pc
        op, arg = programa[pc]
        pc += 1
        executadas += 1

        if op == 'INPP':
            pilha.clear()
        elif op == 'PARA':
            if passo:
                escritor(f"{ip:3}  PARA")
            return
        elif op == 'ALME':
            pilha.extend([0.0] * arg)
        elif op == 'CRCT':
            pilha.append(arg)
        elif op == 'CRVL':
            pilha.append(pilha[posicao(op, arg)])
        elif op == 'ARMZ':
            v = desempilha(op)
            pilha[posicao(op, arg)] = v
        elif op in ARITMETICAS:
            b = desempilha(op)
            a = desempilha(op)
            pilha.append(ARITMETICAS[op](a, b))
        elif op == 'DIVI':
            b = desempilha(op)
            a = desempilha(op)
            if b == 0:
                raise ErroExecucao(f"Instrução {pc - 1} (DIVI): divisão por zero")
            pilha.append(a / b)
        elif op == 'INVE':
            pilha.append(-desempilha(op))
        elif op in RELACIONAIS:
            b = desempilha(op)
            a = desempilha(op)
            pilha.append(1.0 if RELACIONAIS[op](a, b) else 0.0)
        elif op == 'DSVF':
            if desempilha(op) == 0:
                pc = arg
        elif op == 'DSVI':
            pc = arg
        elif op == 'IMPR':
            valor = formata(desempilha(op))
            if passo:
                escritor(f"{ip:3}  {'IMPR':<10} pilha = {[formata(v) for v in pilha]}   >> saída: {valor}")
            else:
                escritor(valor)
            continue
        elif op == 'LEIT':
            pilha.append(leitor())

        if passo:
            if arg is None:
                texto = op
            elif op == 'CRCT':
                texto = f"{op} {formata(arg)}"
            else:
                texto = f"{op} {arg}"
            escritor(f"{ip:3}  {texto:<10} pilha = {[formata(v) for v in pilha]}")


def principal():
    passo = '--passo' in sys.argv
    try:
        with open(CAMINHO_ARQUIVO, encoding='utf-8') as f:
            linhas = f.read().splitlines()
        executar(linhas, passo=passo)
    except OSError as e:
        print(f"Erro ao abrir o arquivo: {e}")
        return 1
    except ErroExecucao as e:
        print(f"Erro de execução: {e}")
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(principal())