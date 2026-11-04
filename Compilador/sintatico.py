
from .erros import ErroSintatico
from .gramatica import G, INICIAL
from .gerador import Gerador
from .tabela import construir_tabela


def nome_token(tok):
    return 'fim do arquivo' if tok[0] == '$' else f"'{tok[1]}'"


def analisar(tokens):
    M = construir_tabela()
    ger = Gerador()
    pilha = ['$', INICIAL]
    pos, ultimo = 0, None
    while pilha:
        X = pilha.pop()
        atual = tokens[pos]
        if X.startswith('@'):                               # ação semântica
            getattr(ger, 'acao_' + X[1:])(ultimo)
        elif X in G:                                        # não-terminal
            prod = M.get((X, atual[0]))
            if prod is None:
                esperados = sorted(t for (nt, t) in M if nt == X)
                raise ErroSintatico(
                    f"Linha {atual[2]}: encontrado {nome_token(atual)} em <{X}>; "
                    f"esperado um de: {' '.join(esperados)}")
            for s in reversed(prod):
                pilha.append(s)
        else:                                               # terminal
            if X != atual[0]:
                raise ErroSintatico(
                    f"Linha {atual[2]}: esperado '{X}', encontrado {nome_token(atual)}")
            ultimo = atual
            pos += 1
    return ger.codigo