import os
import sys
from Compilador import compilar_texto, ErroLexico, ErroSintatico, ErroSemantico

PASTA_SAIDA = "saida"
PASTA_TABELAS = "tabelas"

def main():
    args = sys.argv[1:]
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    os.makedirs(PASTA_TABELAS, exist_ok=True)
    if len(args) > 0:
        entrada = args[0]
    else:
        print(f"Sem argumento de arquivo exemplo.")
        return 1
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
    except ErroLexico as e:
        print(f"Erro léxico: {e}")
        return 1
    except ErroSintatico as e:
        print(f"Erro sintático: {e}")
        return 1
    except ErroSemantico as e:
        print(f"Erro semântico: {e}")
        return 1


    with open(saida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(codigo) + '\n')
    print("Compilação concluída com sucesso!")
    print(f"Código objeto ({len(codigo)} instruções) salvo em '{saida}'.")

    return 0


if __name__ == '__main__':
    sys.exit(main())