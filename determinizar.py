from enum import auto
import math
from automato_finito import AutomatoFinito

def determinizar(nome,n_estados,estado_inicial, alfabeto, tabela_de_transicao, estados_finais):
    #print(n_estados)
    #print(estado_inicial)
    #print(alfabeto)
    #print(tabela_de_transicao)
    #print(estados_finais)

    #MUDAR  ~~~~~~~~~~~~~
    cont = 0
    for i in estados_finais:
        estados_finais[cont] = i-1
        cont+=1
    #FIM MUDAR ~~~~~
    #print(estados_finais)

    fecho = gerar_fecho(n_estados,estado_inicial, alfabeto, tabela_de_transicao, estados_finais)
    #print(fecho)
    for ele in tabela_de_transicao:
        del ele[0]

    alfabeto = alfabeto[1:]
    #print(alfabeto)
    #print(tabela_de_transicao)
    lista_traducao = [fecho[estado_inicial]]
    #print(lista_traducao)
    #print(fecho)
    pilha_estados = []
    pilha_estados.append(fecho[estado_inicial])

    #print(pilha_estados)
    #novos_estados = []
    #novas_transicoes = []

    dict_transicoes = {}

    while len(pilha_estados) != 0:
        
        estado = pilha_estados.pop()
        #print("estado = ",estado)
        dict_transicoes[lista_traducao.index(estado)] = []
        
        for letra in alfabeto:
            prox_estado = []
            for simbolo in estado:
                if tabela_de_transicao[simbolo][alfabeto.index(letra)] != math.inf:
                    prox_estado = prox_estado + fecho[tabela_de_transicao[simbolo][alfabeto.index(letra)]]

            
            if prox_estado not in lista_traducao:
                lista_traducao.append(prox_estado)
                pilha_estados.append(prox_estado)

            #print(prox_estado)
            dict_transicoes[lista_traducao.index(estado)].append(lista_traducao.index(prox_estado))
        
        #print(dict_transicoes[lista_traducao.index(estado)])
        

    #print(lista_traducao)
    #print(tabela_de_transicao)
    #print(dict_transicoes)

    novos_finais = []

    for i in range(len(lista_traducao)):
        for j in lista_traducao[i]:
            if j in estados_finais:
                novos_finais.append(i)
                break

    #print(novos_finais)




    escrever_afd(nome, len(lista_traducao), 0, novos_finais, alfabeto, dict_transicoes)







    #lista_res = ler_afnd(nome_arquivo)


    



def gerar_fecho(n_estados,estado_inicial, alfabeto, tabela_de_transicao, estados_finais):
    tabela_fecho = []

    for i in range(n_estados):
        tabela_fecho.append([i])
        if tabela_de_transicao [i][0] != math.inf:
            for j in tabela_de_transicao[i][0]:
                tabela_fecho[i].append(j)
    
    #print(tabela_fecho)
    for i in range(n_estados):
        for j in (tabela_fecho[i]):
            #print("j = ", j)
            index = j
            #print(index)
            if tabela_de_transicao[index][0] != math.inf:
                if isinstance(tabela_de_transicao[index][0],list):
                    for estado in tabela_de_transicao[index][0]:
                        if not estado in tabela_fecho[i]:
                            tabela_fecho[i].append(estado)
                else:
                    tabela_fecho.append (tabela_de_transicao[index][0])

    #print(tabela_fecho)
    return tabela_fecho





def escrever_afd(nome, n_estados, estado_inicial, estados_finais, alfabeto, tabela_transicoes):
    nome_arquivo = f"./determinizar_afd/afd_"+ nome +"_determinizada.txt"
    arquivo = open(nome_arquivo, "w")
    linhas = [nome]

    linhas.append('\n'+str(n_estados))
    linhas.append('\n'+str(estado_inicial))

    estados_finais_str = []
    for estado in estados_finais:
        estados_finais_str.append(str(estado))
    linhas.append('\n'+','.join(estados_finais_str))

    linhas.append('\n'+','.join(alfabeto))

    tabela_de_transicoes = tabela_transicoes
    for i in range(n_estados):
        #tabela_transicoes[i]
        for j in range(len(tabela_de_transicoes[i])):
            estado_origem = str(i)
            simbolo = alfabeto[j]
            if tabela_de_transicoes[i][j] != math.inf:
                estado_destino = str(tabela_de_transicoes[i][j])
                linhas.append('\n'+','.join([estado_origem,simbolo,estado_destino]))

    arquivo.writelines(linhas)
    arquivo.close()
    return nome_arquivo


