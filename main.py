import pandas as pd

df = pd.read_csv("tabelaM.csv", dtype=str, keep_default_na=False, sep=",")

# Tratamento de dados



#Tratamento de dados de Entrada
# Vazio[]
# Letras maiusculas ou minusculas []
#


casamento = ""
Pilha = ["PROG","$"]
Entrada = ["#include<stdio.h> int main(){","<CMDS>","}","$"]
Acao = ""
troca = ""

def Tratar_Entrada(Entrada):
    campoNovo = []

    for i in Entrada:
        campo = i.replace(" ", "")
        campoNovo.append(campo)

    return campoNovo



if len(Entrada)>1:
    if Pilha != Entrada:
        linha = df[df["NaoTerminais"] == Pilha[0]]

        if not linha.empty:
            linha = linha.iloc[0]

            for coluna in df.columns:
                valor = linha[coluna] == Entrada[0]
                print(f"{coluna}: {valor}")






