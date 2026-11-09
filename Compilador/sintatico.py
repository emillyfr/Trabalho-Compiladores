
from .erros import ErroSintatico
from .gramatica import G, INICIAL
from .gerador import Gerador
from .tabela import construir_tabela


def token(tok):
    if tok[0] == '$':
        return 'fim do arquivo'
    else:
        return f"'{tok[1]}'"


def analisar(tokens):
    tabelaM = construir_tabela()
    gerado = Gerador()
    pilha = ['$', INICIAL]
    pos, ultimo = 0, None

    while pilha:
        X = pilha.pop()
        atual = tokens[pos]
        if X.startswith('@'):
            getattr(gerado, 'acao_' + X[1:])(ultimo)
        elif X in G:
            prod = tabelaM.get((X, atual[0]))
            if prod is None:
                esperados = []
                for (nt, t) in tabelaM:
                    if nt == X:
                        esperados.append(t)
                esperados.sort()
                raise ErroSintatico(
                    f"Linha {atual[2]}: encontrado {token(atual)}  "
                    f"esperado um: {' '.join(esperados)}")
            for s in reversed(prod):
                pilha.append(s)
        else:                                               # terminal
            if X != atual[0]:
                raise ErroSintatico(
                    f"Linha {atual[2]}: esperado '{X}', encontrado {token(atual)}")
            ultimo = atual
            pos += 1
    return gerado.codigo