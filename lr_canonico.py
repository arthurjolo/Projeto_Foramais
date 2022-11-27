from copy import copy


def get_fechamento(C, glc):
    J = [C]
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

        B = []
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
    return primeiro_item

def get_itens(glc, X):
    primeiro_item = get_primeiro_fechamento(glc)
    J = get_fechamento(primeiro_item, glc)

    R = [J]
    pilha = copy(R)

    while pilha != []:
        item = pilha.pop()    

        for I in item:
            for simbolo in X:
                pass

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
    C = get_itens(gramatica_estendida, glc.terminais)

def lr_canonico(glc):                      
    construir_tabela_slr(glc)