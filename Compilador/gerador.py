from .erros import ErroSemantico

OPS_REL = {
    '>': 'CPMA',
    '<': 'CPME',
    '==': 'CPIG',
    '!=': 'CDES',
    '>=': 'CMAI',
    '<=': 'CPMI'
}
OPS_ARIT = {
    '+': 'SOMA',
    '-': 'SUBT',
    '*': 'MULT',
    '/': 'DIVI'
}


class Gerador:
    def __init__(self):
        self.codigo = []
        self.tabela_simbolos = {}
        self.proximo_endereco = 0
        self.pilha_saltos = []
        self.pilha_op = []
        self.pilha_neg = []
        self.pilha_ids = []

    def emite(self, instrucao):
        self.codigo.append(instrucao)

    def endereco(self, tok):
        nome = tok[1]
        if nome not in self.tabela_simbolos:
            raise ErroSemantico(f"Linha {tok[2]}: variável '{nome}' usada sem declaração")
        return self.tabela_simbolos[nome]


    def acao_INPP(self, tok):
        self.emite('INPP')
    def acao_PARA(self, tok):
        self.emite('PARA')


    def acao_DECLARA(self, tok):
        nome = tok[1]
        if nome in self.tabela_simbolos:
            raise ErroSemantico(f"Linha {tok[2]}: variável '{nome}' já declarada")
        self.tabela_simbolos[nome] = self.proximo_endereco
        self.proximo_endereco += 1
        self.emite('ALME 1')


    def acao_IMPRIME(self, tok):
        self.emite(f'CRVL {self.endereco(tok)}')
        self.emite('IMPR')

    def acao_ATRIB_ID(self, tok):
        self.endereco(tok)                       # só verifica a declaração
        self.pilha_ids.append(tok)

    def acao_ARMZ(self, tok):
        self.emite(f'ARMZ {self.endereco(self.pilha_ids.pop())}')

    def acao_LEIT(self, tok):
        self.emite('LEIT')


    def acao_CRVL(self, tok):
        self.emite(f'CRVL {self.endereco(tok)}')

    def acao_CRCT(self, tok):
        self.emite(f'CRCT {tok[1]}')

    def acao_GUARDA_OP(self, tok):
        self.pilha_op.append(tok[0])

    def acao_GERA_ARIT(self, tok):
        self.emite(OPS_ARIT[self.pilha_op.pop()])

    def acao_GERA_REL(self, tok):
        self.emite(OPS_REL[self.pilha_op.pop()])

    def acao_TERMO_INI(self, tok):
        self.pilha_neg.append(False)

    def acao_SET_NEG(self, tok):
        self.pilha_neg[-1] = True

    def acao_TERMO_NEG(self, tok):
        if self.pilha_neg.pop():
            self.emite('INVE')

    def acao_IF_DSVF(self, tok):
        self.pilha_saltos.append(len(self.codigo))
        self.emite('DSVF ?')

    def acao_IF_FIM(self, tok):                  # if sem else
        i = self.pilha_saltos.pop()
        self.codigo[i] = f'DSVF {len(self.codigo)}'

    def acao_ELSE_INI(self, tok):
        i_dsvf = self.pilha_saltos.pop()
        self.pilha_saltos.append(len(self.codigo))
        self.emite('DSVI ?')
        self.codigo[i_dsvf] = f'DSVF {len(self.codigo)}'

    def acao_ELSE_FIM(self, tok):
        i = self.pilha_saltos.pop()
        self.codigo[i] = f'DSVI {len(self.codigo)}'

    def acao_WHILE_INI(self, tok):
        self.pilha_saltos.append(len(self.codigo))

    def acao_WHILE_DSVF(self, tok):
        self.pilha_saltos.append(len(self.codigo))
        self.emite('DSVF ?')

    def acao_WHILE_FIM(self, tok):
        i_dsvf = self.pilha_saltos.pop()
        inicio = self.pilha_saltos.pop()
        self.emite(f'DSVI {inicio}')
        self.codigo[i_dsvf] = f'DSVF {len(self.codigo)}'