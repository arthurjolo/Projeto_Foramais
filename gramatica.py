from utils import alfabeto_maiusculo, alfabeto_minusculo, numeros, operadores, empty
from utils import tira_espacos

class Gramatica:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        '''
        gramatica = {
         "E'": ['E'], 
         'E': ['E + T', 'T'], 
         'T': ['T * F', 'F'], 
         'F': ['(E)', 'id']
        }
        '''
        self.nao_terminais = self.determinar_nao_terminais()
        self.terminais = self.determinar_terminais()
        self.first_posts = {}

    def determinar_terminais(self):
        terminais = []
        for chave in self.nao_terminais:
            for producao in self.gramatica[chave]:
                for caractere in producao:
                    if not caractere.isupper() and caractere != empty:
                        terminais.append(caractere)
        return list(filter(lambda x: x != ' ', terminais))

    def determinar_nao_terminais(self):
        return list(self.gramatica.keys())

    def eh_valido(self):
        # Checar se a chave e o valor não são vazios
        for chave, valor in self.gramatica.items():
            if not chave or not valor:
                return False

        # Checar se a chave ou o valor possuem final de palavra como símbolo
        for chave, valor in self.gramatica.items():
            if "$" in chave or "$" in valor:
                return False

        # Checar se algum não terminal da produção não existe como derivação
        nao_terminais = self.nao_terminais
        todos = []
        for nao_terminal in nao_terminais:
            for caractere in nao_terminal:
                todos.append(caractere)
        for chave, producoes in self.gramatica.items():
            for producao in producoes:
                for caractere in producao:
                    if caractere.isupper():
                        if caractere not in todos:
                            return False

        return True

    def eh_glc(self):
        self.eh_valido()
        for chave in self.gramatica.keys():
            if len(chave) != 1 or not chave.isupper():
                return False
        return True

    def calcular_first_pos(self):
        for nt in self.nao_terminais:
            self.first_posts[nt] = []
        for nt in self.nao_terminais:
            if self.first_posts[nt] == []:
                self.first_pos_simbolo(nt)
       

    def first_pos_simbolo(self, symbol):
        firsts = []
        for prod in self.gramatica[symbol]:
            for prod_symbol in prod:
                if prod_symbol == symbol:
                    break
                elif (prod_symbol in self.terminais) or (prod_symbol == '&'):
                    firsts.append(prod_symbol)
                    break
                else  :
                    first_symbol_posts = self.first_pos_simbolo(prod_symbol)
                    for s in first_symbol_posts:
                        firsts.append(s)
                    if '&' not in first_symbol_posts:
                        break
        self.first_posts[symbol] = firsts
        return firsts

    def calcular_last_pos(self):
        pass