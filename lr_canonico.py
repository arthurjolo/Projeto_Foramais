from copy import copy

class AutomatoLR:
    def __init__(self, item, fechamento):
        self.item = item
        self.fechamento = fechamento
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

    primeiro_automato = AutomatoLR(primeiro_item, J)
    C = [('', '', primeiro_automato)]
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
                    novo_automato_lr = AutomatoLR(transicao, get_fechamento(transicao, glc))
                    I.append(novo_automato_lr)
                    pilha.append((automato_lr.item, X, novo_automato_lr))
                    adicionou = 0
                else:
                    novo_automato_lr = objeto

                C.append((automato_lr.item, X, novo_automato_lr))
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
    simbolos = glc.nao_terminais+glc.terminais
    C, I = get_itens(gramatica_estendida, simbolos)

    print('aqui')

def lr_canonico(glc):                      
    construir_tabela_slr(glc)