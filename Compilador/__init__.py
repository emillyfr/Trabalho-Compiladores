from .erros import ErroLexico, ErroSintatico, ErroSemantico
from .lexico import tokenizar
from .sintatico import analisar

def compilar_texto(texto):
    return analisar(tokenizar(texto))