#!/usr/bin/env python3
import os
import sys
from Compilador import compilar_texto, ErroLexico, ErroSintatico, ErroSemantico
from Compilador.tabela import exportar_tabela

BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_SAIDA = os.path.join(BASE, 'saida')
PASTA_TABELAS = os.path.join(BASE, 'tabelas')


def main():

    args = []
    for argumento in sys.argv[1:]:
        if not argumento.startswith('--'):
            args.append(argumento)

    os.makedirs(PASTA_SAIDA, exist_ok=True)
    os.makedirs(PASTA_TABELAS, exist_ok=True)

    if '--exportar-tabela' in sys.argv:
        caminho = os.path.join(PASTA_TABELAS, 'tabelaM.csv')
        exportar_tabela(caminho)
        print(f"Tabela M salva em '{caminho}'")

    if not args:
        if '--exportar-tabela' not in sys.argv:
            print(__doc__)
        return 0

    entrada = args[0]

    if len(args) > 1:
        saida = args[1]
    else:
        saida = os.path.join(PASTA_SAIDA, 'codigo-objeto.txt')

    if not os.path.isfile(entrada):
        print(f"Arquivo '{entrada}' não encontrado")
        return 1

    with open(entrada, encoding='utf-8') as f:
        texto = f.read()
    try:
        codigo = compilar_texto(texto)
    except (ErroLexico, ErroSintatico, ErroSemantico) as e:
        rotulo = {
            'ErroLexico': 'Erro léxico',
            'ErroSintatico': 'Erro sintático',
            'ErroSemantico': 'Erro semântico',
            'ErroExecucao':'Erro execução'
        }[type(e).__name__]
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