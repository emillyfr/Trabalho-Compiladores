
import csv

from .gramatica import G, INICIAL


def sem_acoes(prod):
    return [s for s in prod if not s.startswith('@')]


def first_seq(seq, first):
    r = set()
    for X in seq:
        if X in G:
            r |= first[X] - {'ε'}
            if 'ε' not in first[X]:
                return r
        else:
            r.add(X)
            return r
    r.add('ε')
    return r


def calcular_first():
    first = {A: set() for A in G}
    mudou = True
    while mudou:
        mudou = False
        for A, prods in G.items():
            for p in prods:
                f = first_seq(sem_acoes(p), first)
                if not f <= first[A]:
                    first[A] |= f
                    mudou = True
    return first


def calcular_follow(first):
    follow = {A: set() for A in G}
    follow[INICIAL].add('$')
    mudou = True
    while mudou:
        mudou = False
        for A, prods in G.items():
            for p in prods:
                p = sem_acoes(p)
                for i, X in enumerate(p):
                    if X in G:
                        f = first_seq(p[i + 1:], first)
                        novo = (f - {'ε'}) | (follow[A] if 'ε' in f else set())
                        if not novo <= follow[X]:
                            follow[X] |= novo
                            mudou = True
    return follow


def construir_tabela():
    first = calcular_first()
    follow = calcular_follow(first)
    M = {}
    for A, prods in G.items():
        for p in prods:
            f = first_seq(sem_acoes(p), first)
            alvo = (f - {'ε'}) | (follow[A] if 'ε' in f else set())
            for a in alvo:
                if (A, a) in M and M[(A, a)] != p:
                    raise Exception(f"Gramática não é LL(1): conflito em M[{A}, {a}]")
                M[(A, a)] = p
    return M


def exportar_tabela(caminho):
    M = construir_tabela()
    terminais = sorted({t for (_, t) in M}) + ['$']
    terminais = list(dict.fromkeys(terminais))
    with open(caminho, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['NaoTerminais'] + terminais)
        for A in G:
            linha = [A]
            for t in terminais:
                p = M.get((A, t))
                linha.append('' if p is None else
                             f"{A} -> " + (' '.join(sem_acoes(p)) or '&'))
            w.writerow(linha)