from copy import copy


def get_fechamento(C):
    J = [C]
    pilha = copy({C})

    while pilha != []:
        item = pilha.pop()
        A = []
        for producoes in item.values():
            for producao in producoes:
                anterior = None
                for caractere in producao:
                    if anterior == '#' and caractere not in A:
                        A.append(caractere)
                        break
                    anterior = caractere

        B = []
        for a in A:
            b = {}
            for chave, producoes in item.items(): 
                for producao in producoes:
                    anterior = None
                    for i, caractere in enumerate(producao):
                        if anterior == '#' and caractere == a:
                            insertion = list(producao)
                            insertion.pop(i-1)
                            insertion.insert(i, '#')
                            if b.get(chave):
                                b[chave].append(''.join(insertion))
                            else:
                                b[chave] = [''.join(insertion)]
                            break
                        anterior = caractere
            B.append(b)

        for b in B:
            if b not in J:
                J.append(b)
                pilha.append(b)

    return J

def get_itens(glc):
    C = get_fechamento(glc.gramatica)
    pilha = copy(C)
    X = glc.terminais

    while pilha != []:
        item = pilha.pop()    

        for I in item:
            for simbolo in X:
                pass

def get_primeiro_fechamento(glc):
    I0 = copy(glc)
    for nt in I0.keys():
        for i in range(len(I0[nt])):
            I0[nt][i] = f"#{I0[nt][i]}"
    return I0

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
    I0 = get_primeiro_fechamento(gramatica_estendida)
    C = get_itens(gramatica_estendida)

def lr_canonico(glc):                      
    construir_tabela_slr(glc)