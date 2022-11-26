# -*- coding: utf-8 -*-
from gramatica_livre_de_contexto import GLC

'''
E' -> E 
E -> E + T | T
T -> T * F | F
F -> (E) | id
'''


def eh_glc(gramatica):
    pass

def criar_glc(gramatica):
    if eh_glc(gramatica):
        return GLC(gramatica)
    else:
        return ValueError

def ler_arquivo(nome_arquivo):
    dict = {}
    try:
        with open(nome_arquivo) as f:
            linhas = f.readlines()
            for linha in linhas:
                nao_terminal, producoes = linha.split('->')
                producoes = producoes.rstrip('\n').strip(' ')
                lista_producoes = producoes.split('|')
                for i in range(len(lista_producoes)):
                    lista_producoes[i] = lista_producoes[i].strip(' ')
                dict[nao_terminal.strip(' ')] = lista_producoes
    except:
        ValueError('Não há arquivo com esse nome!')

    print(dict)
    return dict

def analisador_sintatico(nome_arquivo):
    dicionario_glc = ler_arquivo(nome_arquivo)
    try:
        criar_glc(dicionario_glc)
    except:
        print("Não é uma gramática livre de contexto!")


if __name__ == "__main__":
    analisador_sintatico("./glc_entrada/glc1.txt")
    
    