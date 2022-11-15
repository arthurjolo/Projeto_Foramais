import copy

from automato_finito import AutomatoFinito
from utils import remove_repetidos, retornar_todos_entre, colocar_operacao_entre_elementos

'''
Deve aceitar
-> grupos como:  [a-zA-Z] e [0-9]
-> operadores como: *, +, ?, |

1. 
digit: [0-9]
letter: [a-zA-Z]
id: letter(letter | digit)*

2.
er: a?(a | b)+
'''

alfabeto_minusculo = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l' ,'m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
alfabeto_maiusculo = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L' ,'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

operadores = ['*', '+', '?', '|', '(', ')', '.']
empty = '&'

contador_last_pos = 0
contador_first_pos = 0

class arvoreExpressao:
    def __init__(self, valor, esquerda=None, direita=None):
        self.valor = valor
        self.esquerda = esquerda
        self.direita = direita
        self.nullable = None #True or False
        self.first_pos = None
        self.last_pos = None
    

def definir_afd(arvore, follow_pos, entradas, folhas):
    states = [arvore.first_pos]
    Dstates = [arvore.first_pos]

    Dtran = []
    final_states = []

    while states != []:
        S = states.pop()
        transicoes = []
        for a in entradas:
            U = []
            for p in S:
                if folhas[p-1].valor == a:
                    U = U + follow_pos[p-1]
            U = remove_repetidos(U)

            if U not in Dstates:
                Dstates.append(U)
                states.append(U)

            if len(folhas) in U:
                if len(Dstates) not in final_states:
                    final_states.append(len(Dstates))
         
            for i in range(len(Dstates)):
                if U == Dstates[i]:
                    transicoes.append(i) 
                    break
        Dtran.append(transicoes)

    estados = []
    for i in range(len(Dstates)):
        estados.append(i)
    return AutomatoFinito(len(Dstates), 0, final_states, Dtran, estados, entradas)

#Função recursiva para capturar as entradas possíveis e as folhas da árvore
def calcular_entradas_e_objetos_das_folhas(arvore, entradas, folhas):
    global operadores
    global empty
    valor = arvore.valor
    if valor not in operadores and valor != empty:
        if valor not in entradas:
            entradas.append(valor)
        #cada posição da lista folhas representa as folhas da árvore de baixo pra cima (ou seja, em ordem)
        folhas[(arvore.first_pos[0])-1] = arvore

    if arvore.esquerda:
        calcular_entradas_e_objetos_das_folhas(arvore.esquerda, entradas, folhas)
    if arvore.direita:
        calcular_entradas_e_objetos_das_folhas(arvore.direita, entradas, folhas)

#retorna as entradas possíveis da gramática e as folhas da árvore
def definir_entradas_e_objetos_das_folhas(arvore):
    entradas = []

    folhas = []
    for _ in range(contador_first_pos):
        folhas.append([])

    calcular_entradas_e_objetos_das_folhas(arvore, entradas, folhas)
    entradas.remove('#')
    return entradas, folhas

#preenche a lista de follow pos
def calcular_follow_pos(arvore, follow_pos):
    valor = arvore.valor

    if valor == '.':
        last_pos_c1 = arvore.esquerda.last_pos
        first_pos_c2 = arvore.direita.first_pos
        for i in last_pos_c1:
            follow_pos[i-1] = follow_pos[i-1] + first_pos_c2
    #rever regra com a professora
    elif valor in ['*', '+']:
        last_pos_n = arvore.last_pos
        first_pos_n = arvore.first_pos
        for i in last_pos_n:
            follow_pos[i-1] = follow_pos[i-1] + first_pos_n

    if arvore.esquerda:
        calcular_follow_pos(arvore.esquerda, follow_pos)
    if arvore.direita:
        calcular_follow_pos(arvore.direita, follow_pos)

#retorna uma lista do follow_pos
def definir_follow_pos(arvore):
    if contador_last_pos != contador_first_pos:
        raise ValueError

    follow_pos = []
    for _ in range(contador_first_pos):
        follow_pos.append([])

    calcular_follow_pos(arvore, follow_pos)
    
    return follow_pos

def calcular_last_pos(arvore, todos):
    global contador_last_pos
    valor = arvore.valor

    if valor == '.':
        last_pos_esquerda = calcular_last_pos(arvore.esquerda, todos)
        last_pos_direita = calcular_last_pos(arvore.direita, todos)
        if arvore.direita.nullable:
            arvore.last_pos = last_pos_direita+last_pos_esquerda
        else:
            arvore.last_pos = last_pos_direita
    elif valor == '|':
        last_pos_esquerda = calcular_last_pos(arvore.esquerda, todos)
        last_pos_direita = calcular_last_pos(arvore.direita, todos)
        arvore.last_pos = last_pos_esquerda+last_pos_direita
    elif valor == '*':
        last_pos_esquerda = calcular_last_pos(arvore.esquerda, todos)
        arvore.last_pos = last_pos_esquerda
    elif valor == '+':
        #rever essa regra com a professora
        last_pos_esquerda = calcular_last_pos(arvore.esquerda, todos)
        arvore.last_pos = last_pos_esquerda
    elif valor == '&':
        arvore.last_pos = []
    else:
        if valor in todos.keys():
            arvore.last_pos = todos[valor].first_pos
        else:
            if arvore.last_pos == None:
                contador_last_pos += 1
                arvore.last_pos = [contador_last_pos]
    
    return arvore.last_pos
    
def definir_last_pos(arvore, todos):
    arvore.last_pos = calcular_last_pos(arvore, todos)

def calcular_first_pos(arvore, todos):
    global contador_first_pos
    valor = arvore.valor

    if valor == '.':
        first_pos_esquerda = calcular_first_pos(arvore.esquerda, todos)
        first_pos_direita = calcular_first_pos(arvore.direita, todos)
        if arvore.esquerda.nullable:
            arvore.first_pos = first_pos_esquerda+first_pos_direita
        else:
            arvore.first_pos = calcular_first_pos(arvore.esquerda, todos)
    elif valor == '|':
        first_pos_esquerda = calcular_first_pos(arvore.esquerda, todos)
        first_pos_direita = calcular_first_pos(arvore.direita, todos)
        arvore.first_pos = first_pos_esquerda+first_pos_direita
    elif valor == '*':
        first_pos_esquerda = calcular_first_pos(arvore.esquerda, todos)
        arvore.first_pos = first_pos_esquerda
    elif valor == '+':
        #rever essa regra com a professora
        first_pos_esquerda = calcular_first_pos(arvore.esquerda, todos)
        arvore.first_pos = first_pos_esquerda
    elif valor == '&':
        arvore.first_pos = []
    else:
        if valor in todos.keys():
            arvore.first_pos = todos[valor].first_pos
        else:
            if arvore.first_pos == None:
                contador_first_pos += 1
                arvore.first_pos = [contador_first_pos]
    
    return arvore.first_pos

def definir_first_pos(arvore, todos):
    arvore.first_pos = calcular_first_pos(arvore, todos)

def calcular_nullables(arvore, todos):
    valor = arvore.valor

    if valor == '.':
        nullable_direita = calcular_nullables(arvore.direita, todos)
        nullable_esquerda = calcular_nullables(arvore.esquerda, todos)
        arvore.nullable = (nullable_esquerda and nullable_direita)
    elif valor == '|':
        nullable_direita = calcular_nullables(arvore.direita, todos)
        nullable_esquerda = calcular_nullables(arvore.esquerda, todos)
        arvore.nullable = (nullable_esquerda or nullable_direita)
    elif valor == '*':
        arvore.esquerda.nullable = calcular_nullables(arvore.esquerda, todos)
        arvore.nullable = True
    elif valor == '+':
        arvore.esquerda.nullable = calcular_nullables(arvore.esquerda, todos)
        arvore.nullable = False
    elif valor == '&':
        return True
    elif valor == '#':
        arvore.nullable = False
    else:
        if valor in todos.keys():
            arvore.nullable = (todos[valor].nullable)
        else:
            arvore.nullable = False
    
    return arvore.nullable

def definir_nullable(arvore, todos):
    arvore.nullable = calcular_nullables(arvore, todos)

def calcular_valores_pos_e_afd(dict_regex):
    dict_afd = {}
    for chave in dict_regex.keys():
        arvore = dict_regex[chave]
        definir_nullable(arvore, dict_regex)
        definir_first_pos(arvore, dict_regex)
        definir_last_pos(arvore, dict_regex)
        follow_pos = definir_follow_pos(arvore)
        entradas, folhas = definir_entradas_e_objetos_das_folhas(arvore)
        afd = definir_afd(arvore, follow_pos, entradas, folhas)
        dict_afd[chave] = afd
    return dict_regex, dict_afd

#Percorrer expressão e retornar o nodo do topo da árvore
#entrada: [['a','|', '&'], '.', [['a', '|', 'b'], '+'], '.', '#']
#certo

#entrada: [['aaa', '|', '&'],'.', [['a', '|', ['b', '|', ['a', '.', 'b']]], '+'], '.', [['a', '*'],'.','b'], '.', '#']
#

#entrada: [[['a', '|', 'b'], '*'], '.', ['ab', '|', '&'], '.', ['ab', '*'], '.', ['&', '|', 'a'], '.', '#']
#certo

#entrada:['letter', '.', [['letter', '|', 'digit'], '*'], '.', '#']
#?

#entrada: [['a', '*'], '.', '#']
#certo 

#entrada: ['a', '.', '#']
#certo

#entrada: ['aaaaaa', '.', '#']
#certo

#entrada: ['#']
def criar_arvore(expressao, todos):
    global operadores
    global alfabeto_minusculo
    global alfabeto_maiusculo
    global numeros
    valor_direita = None

    while expressao != []:
        simbolo = expressao.pop()
        if simbolo == '#':
            valor_direita = arvoreExpressao(valor=simbolo)
        elif isinstance(simbolo, list):
            valor_direita =  criar_arvore(simbolo, todos)
        elif simbolo in ['*', '+']:
            valor_direita = arvoreExpressao(valor=simbolo,
                                            esquerda=criar_arvore(expressao, todos))
        elif simbolo == '|' or simbolo == '.':
            valor_direita = arvoreExpressao(valor=simbolo,
                                            direita=copy.copy(valor_direita),
                                            esquerda=criar_arvore(expressao, todos))
        else:
            tamanho = len(simbolo)
            if simbolo in todos.keys():
                valor_direita = todos[simbolo].esquerda
            elif tamanho <= 1:
                valor_direita = arvoreExpressao(valor=simbolo)
            elif simbolo[0] == '[':
                possiveis = []
                primeiro = None
                ultimo = None
                for i in range(1, len(simbolo), 1):
                    if primeiro:
                        if ultimo:
                            if primeiro in alfabeto_minusculo:
                                lista_possiveis = retornar_todos_entre(alfabeto_minusculo, primeiro, ultimo)
                            elif primeiro in alfabeto_maiusculo:
                                lista_possiveis = retornar_todos_entre(alfabeto_maiusculo, primeiro, ultimo)
                            elif primeiro in numeros:
                                lista_possiveis = retornar_todos_entre(numeros, primeiro, ultimo)
                            possiveis += colocar_operacao_entre_elementos(lista_possiveis, '|')
                            primeiro = None
                            ultimo = None
                        else:
                            ultimo = simbolo[i]
                    else:
                        primeiro = simbolo[i] 
                valor_direita =  criar_arvore(possiveis, todos)                  
            else:
                for i in range(tamanho):
                    expressao.append(simbolo[i])
                    if i < tamanho-1:
                        expressao.append('.')

    return valor_direita

#Percorrer expressão e retornar uma lista de listas com as dependências
#entrada: a?.(a | b)+
#saída: [['a','|', '&'], '.', [['a', '|', 'b'], '+'], '.', '#']

#teste: aaa?.(a | (b | (a.b)))+.(a*.b)
#saída: [['aaa','|', '&'],'.', [['a', '|', ['b', '|', ['a', '.', 'b']]], '+'], '.', [['a', '*'],'.','b'], '.', '#']

#teste: (a|b)*.(ab)?.(ab)*.(&|a)
#saída: [[['a', '|', 'b'], '*'], '.', [['ab', '|', '&'], '.', ['ab', '*'], '.', ['&', '|', 'a'], '.', '#']

#teste: letter.(letter|digit)*
#saída: ['letter', '.', [['letter', '|', 'digit'], '*']], '.', '#']
def processar_dependencias(expressao):
    global operadores
    global empty

    pilha = []
    grupo = ""
    parte = []

    for i in range(len(expressao)):
        simbolo = expressao[i]

        if simbolo not in operadores:
            grupo += simbolo
        elif simbolo == '?':
            if grupo != "":
                pilha.append([grupo, '|', empty])
                grupo = ""
            else:
                parte = pilha.pop
                pilha.append([parte, '|', empty])
        elif simbolo == '*' or simbolo == '+':
            if grupo != "":
                pilha.append([grupo, simbolo])
                grupo = ""
            else:
                parte = pilha.pop()
                pilha.append([parte, simbolo])
        elif simbolo == '|' or simbolo == '.':
            if grupo != "": 
                pilha.append(grupo)
                grupo = ""
            pilha.append(simbolo)
        elif simbolo == '(':
            pilha.append(simbolo)
        elif simbolo == ')':
            pilha.append(grupo)
            grupo = ""
            parte = []
            while len(pilha) > 0 and pilha[-1] != '(':
                parte.insert(0, pilha.pop())
            pilha.pop()
            pilha.append(parte)

    if grupo != "":
        pilha.append(grupo)
    
    if pilha != []:
        pilha.append('.')
    pilha.append('#')

    return pilha

#Adicionando operador . de concatenação na expressão regular
#operadores = ['*', '+', '?', '|', '(', ')', '.']
#teste: (a|b)*(ab)?(ab)*(&|a)
#saída: (a|b)*.(ab)?.(ab)*.(&|a)

#teste: letter(letter | digit)*
#saída: letter.(letter|digit)*
def adicionar_concat(expressao):
    global operadores

    resultado = []
    for i in range(len(expressao)-1):
        simbolo = expressao[i]
        proximo_simbolo = expressao[i+1]
        if simbolo != " ":
            resultado.append(simbolo)

        #Se for um alfabeto
        if simbolo not in operadores and proximo_simbolo == '(':
            resultado.append('.')
        elif simbolo == ')' and proximo_simbolo == '(':
            resultado.append('.')
        elif simbolo in ['*', '?', '+'] and proximo_simbolo == '(':
            resultado.append('.')
        elif simbolo in ['*', '?', '+'] and proximo_simbolo not in operadores:
            resultado.append('.')
        elif simbolo == ')' and proximo_simbolo not in operadores:
            resultado.append('.')
        
    resultado.append(expressao[-1])
    return resultado

#retorna dict com todas as entradas de Regex, com as suas árvores como valores
def processar_expressoes(dict):
    for chave in dict.keys():
        expressao_regular = dict[chave].rstrip('\n').strip(' ')
        expressao_regular = adicionar_concat(expressao_regular)
        expressao_regular = processar_dependencias(expressao_regular)
        dict[chave] = criar_arvore(expressao_regular, dict)
    return dict
        
#lê arquivo de entrada e retorna uma dict com todas as entradas de Regex e seus valores como string
def ler_arquivo(nome_arquivo):
    dict = {}
    try:
        with open(nome_arquivo) as f:
            linhas = f.readlines()
            for linha in linhas:
                nome, expressao = linha.split(':')
                dict[nome] = expressao
    except:
        ValueError('Não há arquivo com esse nome!')

    return dict

def print_resultados(dict_adf):
    for chave in dict_adf.keys():
        arquivo = open(f"./regex_afd_saida/afd_{chave}.txt", "w")
        automato = dict_adf[chave]
        linhas = [chave]
        print(chave)

        print(automato.get_n_estados())
        linhas.append('\n'+str(automato.get_n_estados()))

        print(automato.get_estado_inicial())
        linhas.append('\n'+str(automato.get_estado_inicial()))

        for estado in automato.get_estados_finais():
            print(estado)
            linhas.append('\n'+str(estado))

        alfabeto = automato.get_alfabeto()

        print(','.join(alfabeto))
        linhas.append('\n'+','.join(alfabeto))

        tabela_de_transicoes = automato.get_tabela_de_transicoes()
        for i in range(len(tabela_de_transicoes)):
            for j in range(len(tabela_de_transicoes[i])):
                estado_origem = str(i)
                simbolo = alfabeto[j]
                estado_destino = str(tabela_de_transicoes[i][j])

                print(','.join([estado_origem,simbolo,estado_destino]))
                linhas.append('\n'+','.join([estado_origem,simbolo,estado_destino]))

        arquivo.writelines(linhas)
        arquivo.close()

def regex_para_afd(nome_do_arquivo):
    dict = ler_arquivo(nome_do_arquivo)
    dict = processar_expressoes(dict)
    dict_regex, dict_afd = calcular_valores_pos_e_afd(dict)
    print_resultados(dict_afd)

if __name__ == "__main__":
    regex_para_afd("./regex_entrada/regex3.txt")
    