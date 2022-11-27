# -*- coding: utf-8 -*-
from gramatica import Gramatica
from lr_canonico import lr_canonico
from utils import tira_espacos

'''
E' -> E 
E -> E + T | T
T -> T * F | F
F -> (E) | id
'''

def criar_glc(gramatica):
    objeto = Gramatica(gramatica)
    if objeto.eh_valido():
        if objeto.eh_glc():
            return objeto
        else:
            del objeto
            raise ValueError('A gramática não é livre de contexto!')
    else:
        del objeto
        raise ValueError('A entrada não é válida!')

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
                    lista_producoes[i] = tira_espacos(lista_producoes[i])
                    lista_producoes[i] = lista_producoes[i]
                dict[nao_terminal.strip(' ')] = lista_producoes
        return dict
    except:
        ValueError('Não há arquivo com esse nome!')

def analisador_sintatico(nome_arquivo):
    dicionario_glc = ler_arquivo(nome_arquivo)
    try:
        glc = criar_glc(dicionario_glc)
        lr_canonico(glc)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    analisador_sintatico("./glc_entrada/valida/lc/glc1.txt")
    
    