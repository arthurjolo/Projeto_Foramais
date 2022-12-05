from contextlib import nullcontext
import math
from model_analisador_lexico import RespostaPasso

class AutomatoFinito:
    def __init__(self, arquivo : str):
        self.n_estados = 0
        self.estado_inicial = 0
        self.estados_finais = [] #[]
        self.tabela_transicoes = [] #=  tabela_transicoes #[][]
        self.alfabeto =[]# alfabeto #[]
        self.nome = ""
        self.lable_estados_finais = dict()
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

    def set_nome(self, nome):
        self.nome = nome

    def ler_arquivo(self, arquivo):
        
        with open(arquivo, 'r') as file:
            linha1 = file.readline()
            for c in linha1:
                if c != "\n":
                    self.nome = self.nome + c

            #leitura do número de estados
            linha1 = file.readline()
            self.n_estados = int(linha1)
            
            #leitura do estado inicial
            linha1 = file.readline()
            self.estado_inicial = int(linha1)
            
            #leitura dos estados finais
            linha1 = file.readline().rstrip('\n').split(',')
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


    def passo_de_processamento(self, estado, passo, palavra):
        
        resposta = RespostaPasso()
       
        if (estado < self.n_estados):
            estado_atual = estado
            if (len(palavra) == passo):
                if (estado_atual in self.estados_finais):
                    resposta.is_palavra_aceita = True
                    resposta.estado_final = estado_atual
            else:
                letra_atual = palavra[passo]
                if letra_atual not in self.alfabeto:
                    resposta.erro = "nao esta no alfabeto"
                else:
                    
                    proximos_estados = [self.tabela_transicoes[estado_atual][self.alfabeto.index(letra_atual)]]
                    proximos_estados_processar = []
                
                    if (proximos_estados == None):
                        resposta.estado_final = estado_atual
                    else:
                        for proximo_estado in proximos_estados:
                            proximos_estados_processar.append(proximo_estado)
                        
                        resposta.is_palavra_processada = True
                        resposta.proximos_estados = proximos_estados_processar 
        else:
            resposta.erro = "estado inválido"
     
        return resposta


