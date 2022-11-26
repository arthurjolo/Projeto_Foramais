# -*- coding: utf-8 -*-
from gramatica import Gramatica

'''
E' -> E 
E -> E + T | T
T -> T * F | F
F -> (E) | id
'''

'''
def eh_glc(gramatica):
    nao_terminais = gramatica.keys()
    contador = 0
    for nao_terminal in nao_terminais:
        for simbolo in nao_terminal:
            if simbolo in nao_terminais or simbolo.islower():
                contador += 1
            
            if contador >= 2:
                return False

        contador = 0
    
    return True
'''


def criar_glc(gramatica):
    objeto = Gramatica(gramatica)
    if objeto.eh_glc():
        return objeto
    else:
        del objeto
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

    return dict

def analisador_sintatico(nome_arquivo):
    dicionario_glc = ler_arquivo(nome_arquivo)
    try:
        criar_glc(dicionario_glc)
    except:
        print("Não é uma gramática livre de contexto!")


if __name__ == "__main__":
    analisador_sintatico("./glc_entrada/glc2.txt")
    
    