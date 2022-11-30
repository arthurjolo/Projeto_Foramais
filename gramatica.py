from utils import alfabeto_maiusculo, alfabeto_minusculo, numeros, operadores, empty

class Gramatica:
    def __init__(self, gramatica,simbolo_inicial):
        self.gramatica = gramatica
        '''
        gramatica = {
         "E'": ['E'], 
         'E': ['E+T', 'T'], 
         'T': ['T*F', 'F'], 
         'F': ['(E)', 'id']
        }
        '''
        self.nao_terminais = self.determinar_nao_terminais()
        self.terminais = self.determinar_terminais()
        self.first_posts = {}
        self.follow_posts = {}
        ## para o follow
        self.simbolo_inicial = simbolo_inicial

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
            self.first_posts[nt] = list(dict.fromkeys(self.first_posts[nt]))
        
        #

       

    def first_pos_simbolo(self, symbol):
        firsts = []
        for prod in self.gramatica[symbol]:
            firsts = firsts + self.first_post_production(prod,symbol)[:]
        self.first_posts[symbol] = firsts[:]
        return firsts

    #pegar o simbolo nao terminal que seja o inicial!!
    def calcular_follow_pos(self):
        lista_reg_3 = []
        for nt in self.nao_terminais:
            self.follow_posts[nt] = []
        for nt in self.nao_terminais:
            if self.follow_posts[nt] == []:
                if nt == self.simbolo_inicial:
                    self.follow_posts[nt].append("$")
                lista_reg_3 = lista_reg_3 + self.follow_pos_steps_1_2(nt)
            self.follow_posts[nt[0]] = list(dict.fromkeys(self.follow_posts[nt[0]]))
        self.follow_pos_steps_3(lista_reg_3)


    def follow_pos_steps_1_2(self,symbol):
        lista_reg_3 = []
        for prod in self.gramatica[symbol]:
            for i in range(len(prod)):
                if (i+1 < len(prod)) and prod[i] in self.nao_terminais:
                    if prod[i+1] in self.terminais:
                        self.follow_posts[prod[i]].append(prod[i+1])
                    else:
                        first_beta = self.first_post_production(prod[i+1:],prod[i])
                        self.follow_posts[prod[i]] = self.follow_posts[prod[i]]+(first_beta)
                        if "&" in first_beta:
                            lista_reg_3.append(prod[i] + symbol)
                elif (i == len(prod)-1) and prod[i] in self.nao_terminais:
                    lista_reg_3.append(prod[i] + symbol)
        
        return lista_reg_3


    def follow_pos_steps_3(self,lista_reg_3):
        #[recebefollow,doafollow]
        for prod in lista_reg_3:
            self.follow_posts[prod[0]] = self.follow_posts[prod[0]] + self.follow_posts[prod[1]]
            self.follow_posts[prod[0]] = list(dict.fromkeys(self.follow_posts[prod[0]]))
    
                    

    def first_post_production(self,producao,head):
        firsts = []
        for prod_symbol in producao:
                if prod_symbol == head:
                    break
                elif (prod_symbol in self.terminais) or (prod_symbol == '&'):
                    firsts.append(prod_symbol)
                    break
                else  :
                    first_symbol_posts = self.first_pos_simbolo(prod_symbol)[:]
                    for s in first_symbol_posts:
                        if s != "&":
                            firsts.append(s)
                    if '&' not in first_symbol_posts:
                        break

        else:
            firsts.append("&")
        
        return firsts

    def calcular_last_pos(self):
        pass