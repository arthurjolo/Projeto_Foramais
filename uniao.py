from enum import auto
import math
from automato_finito import AutomatoFinito

from determinizar import determinizar
from regex_para_afd import regex_para_afd

def uniao(automatos):
    estado_inicial = 0
    estados = [0]
    alfabeto = []
    tabela_de_transicao = []
    estados_finais = []
    lable_estados_finais = dict()

    #automato1 = AutomatoFinito(automato1_txt)
    #automato2 = AutomatoFinito(automato2_txt)
    #construindo os estados do novo automato
    n_estados = 1
    #contruindo o alfabeto do novo automato
    alfabeto.append("&")
    for automato in automatos:
        for l in automato.get_alfabeto():
            if not(l in alfabeto):
                alfabeto.append(l)
        n_estados += automato.get_n_estados()

    #for l in automato2.get_alfabeto():
    #    if not(l in alfabeto):
    #        alfabeto.append(l)
        
    #contruindo estados finais do novo automato
    ajuste = 1
    for automato in automatos:
        if list(automato.lable_estados_finais.keys()) == []:
            for f in automato.get_estados_finais():
                estados_finais.append(f+ajuste)
                lable_estados_finais[f+ajuste] = [automato.nome]
        else:
            for f in automato.get_estados_finais():
                estados_finais.append(f+ajuste)
                lable_estados_finais[f+ajuste] = automato.lable_estados_finais[f][:]
        ajuste += automato.get_n_estados()
    
    #if list(automato2.lable_estados_finais.keys()) == []:
    #    for f in automato2.get_estados_finais():
    #        estados_finais.append(f+ automato1.get_n_estados() +1)
    #        lable_estados_finais[f+ automato1.get_n_estados() +1] = [automato2.nome]
    #else:
    #    for f in automato2.get_estados_finais():
    #        estados_finais.append(f+ automato1.get_n_estados() +1)
    #        lable_estados_finais[f+ automato1.get_n_estados() +1] = automato2.lable_estados_finais[f][:]

    #for f in automato2.get_estados_finais():
    #    estados_finais.append(f + automato1.get_n_estados() + 1)

    #inicializando a tabela de transições do novo automato,
    #inicialmento todas as trasições são considerdos mortas(= infinito)
    for i in range(n_estados):
        linha = []
        for j in range(len(alfabeto)):
            linha.append(math.inf)
        tabela_de_transicao.append(linha)
    
    #transição do estado inicial(0) por epsilon(posição 0 do alfabeto) = estados iniciais de a1 e a2
    ajuste = 1
    #tabela_de_transicao[0][0] = [1, automato1.get_n_estados() + 1]
    tabela_de_transicao[0][0] = []
    for i in range(len(automatos)):
        tabela_de_transicao[0][0] += [ajuste]
        ajuste += automatos[i].get_n_estados()
   
    automato_n = 0
    automato = automatos[0]
    ajuste = 1
   
    for i in range(1, n_estados):
        if (i < ajuste + automato.get_n_estados()):
            automato = automatos[automato_n]
        else:
            automato_n += 1
            ajuste += automato.get_n_estados()
            automato = automatos[automato_n]
        estado = i - ajuste
        alfabeto_automato = automato.get_alfabeto()
        
        automato_trasicoes = automato.get_tabela_de_transicoes()
        for j in range(len(alfabeto)):
            if alfabeto[j] in alfabeto_automato:
                indice = alfabeto_automato.index(alfabeto[j])
                tabela_de_transicao[i][j] = automato_trasicoes[estado][indice] + ajuste
            else:
                tabela_de_transicao[i][j] =math.inf
    
    escrever_afd("uniao_", n_estados, estado_inicial, estados_finais, alfabeto, tabela_de_transicao)
    return determinizar("uniao_", n_estados ,estado_inicial, alfabeto, tabela_de_transicao, estados_finais, lable_estados_finais)

def escrever_afd(nome, n_estados, estado_inicial, estados_finais, alfabeto, tabela_transicoes):
    nome_arquivo = f"./3_uniao_afd/afd_"+ nome +".txt"
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
    for i in range(len(tabela_de_transicoes)):
        for j in range(len(tabela_de_transicoes[i])):
            estado_origem = str(i)
            simbolo = alfabeto[j]
            if tabela_de_transicoes[i][j] != math.inf:
                estado_destino = str(tabela_de_transicoes[i][j])
                linhas.append('\n'+','.join([estado_origem,simbolo,estado_destino]))

    arquivo.writelines(linhas)
    arquivo.close()
    return nome_arquivo
