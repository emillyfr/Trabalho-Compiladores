
from .erros import ErroLexico


PALAVRAS_RESERVADAS = {'printf', 'double', 'if', 'else', 'while'}
PROLOGO = ['#include', '<stdio.h>', 'int', 'main', '(', ')', '{']


def eh_letra(c):
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'


def eh_digito(c):
    return '0' <= c <= '9'


def pular_espacos(texto, i, linha):
    while i < len(texto) and texto[i] in ' \t\r\n':
        if texto[i] == '\n':
            linha += 1
        i += 1
    return i, linha


def ler_prologo(texto, i, linha):
    """Reconhece '#include <stdio.h> int main(){' como UM terminal (PROLOGO)."""
    for parte in PROLOGO:
        i, linha = pular_espacos(texto, i, linha)
        if not texto.startswith(parte, i):
            raise ErroLexico(f"Linha {linha}: esperado '{parte}' no início do programa "
                             f"('#include <stdio.h> int main(){{')")
        i += len(parte)
    return i, linha


def tokenizar(texto):
    """Devolve lista de tokens (tipo, lexema, linha), terminada por '$'."""
    tokens, i, linha, n = [], 0, 1, len(texto)
    while i < n:
        c = texto[i]
        if c in ' \t\r\n':
            i, linha = pular_espacos(texto, i, linha)
            continue
        if c == '/' and texto[i + 1:i + 2] == '/':          # comentário de linha
            while i < n and texto[i] != '\n':
                i += 1
            continue
        if c == '#':
            ini = linha
            i, linha = ler_prologo(texto, i, linha)
            tokens.append(('PROLOGO', '#include <stdio.h> int main(){', ini))
            continue
        if eh_letra(c):
            j = i
            while j < n and (eh_letra(texto[j]) or eh_digito(texto[j])):
                j += 1
            lex = texto[i:j]
            if lex == 'lerDouble':                           # lerDouble()
                k = j
                while k < n and texto[k] in ' \t':
                    k += 1
                if texto[k:k + 1] == '(':
                    k += 1
                    while k < n and texto[k] in ' \t':
                        k += 1
                    if texto[k:k + 1] == ')':
                        tokens.append(('lerDouble()', 'lerDouble()', linha))
                        i = k + 1
                        continue
                raise ErroLexico(f"Linha {linha}: 'lerDouble' deve ser usado como lerDouble()")
            tokens.append((lex if lex in PALAVRAS_RESERVADAS else 'id', lex, linha))
            i = j
            continue
        if eh_digito(c):
            j = i
            while j < n and eh_digito(texto[j]):
                j += 1
            if j < n and texto[j] == '.':
                j += 1
                if not (j < n and eh_digito(texto[j])):
                    raise ErroLexico(f"Linha {linha}: número real malformado '{texto[i:j]}'")
                while j < n and eh_digito(texto[j]):
                    j += 1
            if j < n and eh_letra(texto[j]):
                raise ErroLexico(f"Linha {linha}: identificador não pode começar com dígito "
                                 f"('{texto[i:j + 1]}...')")
            tokens.append(('numero_real', texto[i:j], linha))
            i = j
            continue
        dois = texto[i:i + 2]
        if dois in ('==', '!=', '>=', '<='):
            tokens.append((dois, dois, linha))
            i += 2
        elif c in '+-*/=<>(){};,':
            tokens.append((c, c, linha))
            i += 1
        else:
            raise ErroLexico(f"Linha {linha}: caractere inválido '{c}'")
    tokens.append(('$', '$', linha))
    return tokens