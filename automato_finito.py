from contextlib import nullcontext


class AutomatoFinito:
    def __init__(self, n_estados, estado_inicial, estados_finais, tabela_transicoes, estados, alfabeto):
        self.n_estados = n_estados
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais #[]
        self.tabela_transicoes =  tabela_transicoes #[][]
        self.estados = estados #[]
        self.alfabeto = alfabeto #[]

    def get_n_estados(self):
        return self.n_estados

    def get_estado_inicial(self):
        return self.estado_inicial

    def get_estados_finais(self):
        return self.estados_finais[:]

    def get_tabela_de_transicoes(self):
        return self.tabela_transicoes
    
    def get_estados(self):
        return self.estados

    def get_alfabeto(self):
        return self.alfabeto[:]

    def transition(self, qi, letter):  #return [int:estado]
        pass