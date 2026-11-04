"""Compilador - Parte 1: texto-fonte -> código objeto da máquina hipotética."""
from .erros import ErroLexico, ErroSintatico, ErroSemantico
from .lexico import tokenizar
from .sintatico import analisar


def compilar_texto(texto):
    """Executa léxico + sintático + semântico + geração e devolve a lista de instruções."""
    return analisar(tokenizar(texto))