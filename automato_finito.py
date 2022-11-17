from contextlib import nullcontext
import math


class AutomatoFinito:
    def __init__(self, arquivo : str):
        self.n_estados = 0
        self.estado_inicial = 0
        self.estados_finais = [] #[]
        self.tabela_transicoes = [] #=  tabela_transicoes #[][]
        self.alfabeto =[]# alfabeto #[]
        self.ler_arquivo(arquivo)

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

    def ler_arquivo(self, arquivo):
        
        with open(arquivo, 'r') as file:
            linha1 = file.readline()
            
            #leitura do número de estados
            linha1 = file.readline()
            self.n_estados = int(linha1)
            
            #leitura do estado inicial
            linha1 = file.readline()
            self.estado_inicial = int(linha1)
            
            #leitura dos estados finais
            linha1 = file.readline().split(',')
            for f in linha1:
                self.estados_finais.append(int(f))
            
            #leitura do alfabeto
            linha1 = file.readline().split(',')
            for l in linha1:
                self.alfabeto.append(l[0])

            #leitura da tabela de transições
            for i in range(self.n_estados):
                linha_ = []
                for j in range(len(self.alfabeto)):
                    linha_.append(math.inf)
                self.tabela_transicoes.append(linha_)
            while True:
                linha = file.readline()
                if not linha:
                    break
                linha = linha.split(',')
                self.tabela_transicoes[int(linha[0])][self.alfabeto.index(linha[1])] = int(linha[2])