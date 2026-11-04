#!/usr/bin/env python3
"""
Compilador - Parte 1

Uso:
    python main.py entrada.txt [codigo-objeto.txt]
    python main.py --exportar-tabela      (grava tabelas/tabelaM_gerada.csv)

Sem o 2º argumento, o código objeto vai para saida/codigo-objeto.txt.
"""
import os
import sys

from Compilador import compilar_texto, ErroLexico, ErroSintatico, ErroSemantico
from Compilador.tabela import exportar_tabela

BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_SAIDA = os.path.join(BASE, 'saida')
PASTA_TABELAS = os.path.join(BASE, 'tabelas')


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    os.makedirs(PASTA_TABELAS, exist_ok=True)

    if '--exportar-tabela' in sys.argv:
        caminho = os.path.join(PASTA_TABELAS, 'tabelaM_gerada.csv')
        exportar_tabela(caminho)
        print(f"Tabela M salva em '{caminho}'")
    if not args:
        if '--exportar-tabela' not in sys.argv:
            print(__doc__)
        return 0

    entrada = args[0]
    saida = args[1] if len(args) > 1 else os.path.join(PASTA_SAIDA, 'codigo-objeto.txt')

    with open(entrada, encoding='utf-8') as f:
        texto = f.read()
    try:
        codigo = compilar_texto(texto)
    except (ErroLexico, ErroSintatico, ErroSemantico) as e:
        rotulo = {'ErroLexico': 'Erro léxico', 'ErroSintatico': 'Erro sintático',
                  'ErroSemantico': 'Erro semântico'}[type(e).__name__]
        print(f"{rotulo}: {e}")
        return 1

    with open(saida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(codigo) + '\n')
    print("Compilação concluída com sucesso!")
    print(f"Código objeto ({len(codigo)} instruções) salvo em '{saida}':")
    for i, ins in enumerate(codigo):
        print(f"  {i:3d}  {ins}")
    return 0


if __name__ == '__main__':
    sys.exit(main())