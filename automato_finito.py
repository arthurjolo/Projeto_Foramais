from contextlib import nullcontext


class AutomatoFinito:
    def __init__(self):
        self.n_estados = None
        self.estado_inicial = None
        self.estados_finais = []
        self.tabela_transicoes = []  #[][]
        self.estados = []
        self.alfabeto = None

    def transition(self, qi, letter):  #return [int:estado]
        pass