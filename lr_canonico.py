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

def ha_transicao(C, I, X):
    for item in C:
        automato_lr = item[0]
        print(automato_lr.item)
        print(I.item)
        if automato_lr.item == I.item:
            print(X)
            print(list(I.transicao.keys()))
            if X in list(I.transicao.keys()):
                print('alcancou')
                return True
    return False    

def get_fechamento(C, glc):
    J = C
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

    INICIO_DE_ENTRADA = '%'
    C = [(AutomatoLR(primeiro_item, J), '%')]
    pilha = copy(C)
    
    adicionou = 0
    while adicionou <= 2:
        adicionou += 1
        item_pilha = pilha.pop()
        automato_lr = item_pilha[0]
        I = automato_lr.item
        for X in simbolos:
            transicao = achar_transicao(automato_lr, X)
            if transicao:
                novo_automato_lr = AutomatoLR(transicao, get_fechamento(transicao, glc))
                if not ha_transicao(C, automato_lr, X):
                    C.append((novo_automato_lr, X))
                    pilha.append((novo_automato_lr, X))
                    adicionou = 0
                automato_lr.transicao[X] = novo_automato_lr

        print('aqui1')
    
    print('aqui2')

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
    C = get_itens(gramatica_estendida, simbolos)

def lr_canonico(glc):                      
    construir_tabela_slr(glc)