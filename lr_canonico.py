from copy import copy
from utils import tira_caractere

class AutomatoLR:
    def __init__(self, item, fechamento, indice):
        self.item = item
        self.fechamento = fechamento
        self.indice = indice
        self.transicao = {}
        '''
        Exemplo: Se I representa o conjunto com dois itens
            I = {[E' → E·], [E → E · +T]},
            então GOTO(I, +) contém os itens:

                E → E + #T
                T → #T * F
                T → #F
                F → #(E)
                F → #id
            
            simbolos = [+]
            goto = ['automato do: E → E + #T']
        
        transicao = {}
        transicao['+'] = AutomatoLR(item='E → E + #T')
        '''

def achar_transicao(automato_lr, X):
    itens = automato_lr.fechamento
    anterior = None
    novo_I = []
    for item in itens:
        anterior = None
        head = list(item.keys())[0]
        valor = list(item.values())[0]
        for i, caractere in enumerate(valor):
            if anterior == '#' and caractere == X:
                novo_item = list(valor)
                novo_item.pop(i-1)
                novo_item.insert(i, '#')
                insercao = {}
                insercao[head] = ''.join(novo_item)
                novo_I.append(insercao)
            anterior = caractere
    return novo_I

def checar_transicao(C, transicao, X):
    for item in C:
        automato_lr = item[2]
        if item[2] == None:
            continue
        if automato_lr.transicao.get(X):
            if automato_lr.transicao[X].item == transicao:
                return True, automato_lr.transicao[X]
    return False, None

def get_fechamento(C, glc):
    J = copy(C)
    pilha = copy(J)

    while pilha != []:
        item = pilha.pop()
        A = []
        for producao in item.values():
            anterior = None
            for caractere in producao:
                if anterior == '#' and caractere not in A:
                    A.append(caractere)
                    break
                anterior = caractere

        for a in A:
            if a.isupper():
                for b in glc[a]:
                    dic = {}
                    com_marcacao = f"#{b}"
                    dic[a] = com_marcacao

                    if dic not in J: 
                        J.append(dic)
                        pilha.append(dic)

    return J

def get_primeiro_fechamento(glc):
    primeiro_item = {}
    for chave, itens in glc.items():
        primeiro_item[chave] = f"#{itens[0]}"
        break
    return [primeiro_item]

def get_itens(glc, simbolos):
    primeiro_item = get_primeiro_fechamento(glc)
    J = get_fechamento(primeiro_item, glc)

    indice = 0
    primeiro_automato = AutomatoLR(primeiro_item, J, indice)

    C = [(None, '', primeiro_automato)]
    I = [primeiro_automato]
    pilha = copy(C)
    
    adicionou = 0
    while pilha != []:
        adicionou += 1
        item_pilha = pilha.pop()
        automato_lr = item_pilha[2]
        for X in simbolos:
            transicao = achar_transicao(automato_lr, X)
            if transicao:
                ha_transicao, objeto = checar_transicao(C, transicao, X)
                if not ha_transicao:
                    indice += 1
                    novo_automato_lr = AutomatoLR(transicao, get_fechamento(transicao, glc), indice)
                    I.append(novo_automato_lr)
                    pilha.append((automato_lr, X, novo_automato_lr))
                    adicionou = 0
                else:
                    novo_automato_lr = objeto

                C.append((automato_lr, X, novo_automato_lr))
                automato_lr.transicao[X] = novo_automato_lr
        
    return C, I

def gerar_gramatica_estendida(glc):
    for cabeca in glc.gramatica.keys():
        antigo_simbolo_inicial = cabeca
        break
    novo_simbolo_inicial = f"{antigo_simbolo_inicial}'"
    nova_gramatica = {}
    nova_gramatica[novo_simbolo_inicial] = [antigo_simbolo_inicial]
    nova_gramatica.update(glc.gramatica)
    return nova_gramatica

def construir_tabela_slr(glc):
    gramatica_estendida = gerar_gramatica_estendida(glc)
    terminais = glc.terminais
    nao_terminais = glc.nao_terminais
    simbolos = nao_terminais + terminais
    C, I = get_itens(gramatica_estendida, simbolos)
    
    ACTION = []
    GOTO = []
    for i in range(len(I)):
        ACTION.append({})
        GOTO.append({})

    first_i = C[0][2]
    enumerated_first_i = []
    for producoes in first_i.fechamento:
        head = list(producoes.keys())[0]
        body = list(producoes.values())[0]
        dic = {}
        dic[head] = tira_caractere(body, '#')
        enumerated_first_i.append(dic)

    glc.calcular_follow_pos()
    follow_posts = glc.follow_posts

    for n, i in enumerate(I):
        for producao in i.fechamento:
            anterior = None
            head = list(producao.keys())[0]
            body = list(producao.values())[0]

            entrou_condicao_1 = False
            entrou_condicao_2 = False
            entrou_condicao_3 = False

            for m, caractere in enumerate(body):
                #primeira regra ACTION
                if anterior == '#':
                    if caractere in terminais:
                        #and GOTO(Ii, a) = Ij
                        for c in C:
                            if c[0] != None:
                                if c[0].item == i.item and c[1] == caractere:
                                    ACTION[n][caractere] = f's{c[2].indice}'
                                    entrou_condicao_1 = True
                elif caractere == '#' and m == len(body)-1:
                    #segunda regra ACTION
                    if head != list(first_i.item[0].keys())[0]:
                        follow_pos = follow_posts[head]
                        producao_comparativa = copy(producao)
                        for indice, valor in producao_comparativa.items():
                            producao_comparativa[indice] = tira_caractere(valor, '#')
                        for simbolo in follow_pos:
                            for numero, e in enumerate(enumerated_first_i):
                                if e == producao_comparativa:
                                    break
                            ACTION[n][simbolo] = f'r{numero}'
                            entrou_condicao_2 = True
                    else:
                        #terceira regra ACTION
                        ACTION[n]['$'] = 'accept'
                        entrou_condicao_3 = True

                if (entrou_condicao_1 and entrou_condicao_2) or (entrou_condicao_1 and entrou_condicao_3) or (entrou_condicao_2 and entrou_condicao_3):
                    raise ValueError('Gramática não é SLR(1)')
                
                anterior = caractere

    for c in C:
        if c[1] in nao_terminais:
            GOTO[c[0].indice][c[1]] = f'{c[2].indice}'

    return (ACTION, GOTO), enumerated_first_i



def lr_canonico(glc, entrada_lexica):                   
    tabela_slr, gramatica_estendida = construir_tabela_slr(glc)

    #tabela = tupla(acao,desvio)
    # acao = [{'(':'desvio','i': desvio}]
    # desvio [{'E': 'desvio'}]

    #entrada_lexica
    # [{tipo: "entrada"}, {"tipo" : "entrada"}, {"tipo": "$"}]

    pilha = [0]
    simbolo = ""
    entrada = []

    for dic in entrada_lexica:
        entrada.append(dic["tipo"])
    print(entrada)
    while len(entrada) != 0 :
        acao = tabela_slr[0][pilha[(len(pilha)-1)]][entrada[0]]

        if acao[0] == 's':
            idx_s = int(acao[1:])
            simbolo = simbolo + (entrada.pop(0))
            pilha.append(idx_s)

        elif acao[0] == 'r':
            idx_r = int(acao[1:])
            dict_gram = gramatica_estendida[idx_r]

            cabeca_prod = list(dict_gram.keys())[0]
            corpo_prod = dict_gram[cabeca_prod]
            corpo_prod_teste = corpo_prod

            for i in range(len(corpo_prod)):
                if simbolo[-1] != corpo_prod_teste[-1]:
                    return "rejeita"
                
                corpo_prod_teste = corpo_prod_teste[:-1]
                simbolo = simbolo[:-1]
                pilha.pop()

            simbolo = simbolo + cabeca_prod
            pilha.append(int(tabela_slr[1][pilha[len(pilha-1)]][cabeca_prod]))

        elif acao == 'acc':
            print("aceita")
            return "aceita"
    
    return "rejeita"
