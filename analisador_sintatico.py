# -*- coding: utf-8 -*-
from gramatica import Gramatica
from lr_canonico import lr_canonico
from utils import tira_caractere

'''
E -> E + T | T
T -> T * F | F
F -> (E) | id
'''

def criar_glc(gramatica,simbolo_inicial):
    objeto = Gramatica(gramatica,simbolo_inicial[0])
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
    simbolo_inicial = None
    cont = 0
    try:
        with open(nome_arquivo) as f:
            linhas = f.readlines()
            for linha in linhas:
                nao_terminal, producoes = linha.split('->')
                if cont == 0:
                    simbolo_inicial = nao_terminal
                    cont+=1
                producoes = producoes.rstrip('\n').strip(' ')
                lista_producoes = producoes.split('|')
                for i in range(len(lista_producoes)):
                    lista_producoes[i] = tira_caractere(lista_producoes[i], ' ')
                    lista_producoes[i] = lista_producoes[i]
                dict[nao_terminal.strip(' ')] = lista_producoes

        return [dict,simbolo_inicial]
    except:
        raise ValueError('Não há arquivo com esse nome!')

def analisador_sintatico(nome_arquivo):
    retorno = ler_arquivo(nome_arquivo)
    try:
        glc = criar_glc(retorno[0],retorno[1])
        lr_canonico(glc)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
   analisador_sintatico("./glc_entrada/valida/lc/glc1.txt")
    
