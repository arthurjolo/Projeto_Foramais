import copy

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

operadores = ['*', '+', '?', '|', '(', ')', '.']
empty = '&'

class arvoreExpressao:
    def __init__(self, valor, esquerda=None, direita=None):
        self.valor = valor
        self.esquerda = esquerda
        self.direita = direita
        self.nullable = None #True or False
        self.first_pos = None
        self.last_pos = None
        self.follow_pos = None

def calcular_follow_pos(arvore):
    pass

def calcular_last_pos(arvore, todos, contador=0):
    try:
        valor = arvore.valor
    except:
        valor = arvore

    if valor == '.':
        if arvore.direita.nullable:
            arvore.last_pos = calcular_last_pos(arvore.direita, todos, contador)+calcular_last_pos(arvore.esquerda, todos, contador)
        else:
            arvore.last_pos = calcular_last_pos(arvore.direita, todos, contador)
    elif valor == '|':
        arvore.last_pos = calcular_last_pos(arvore.esquerda, todos)+calcular_last_pos(arvore.direita, todos, contador)
    elif valor == '*':
        arvore.last_pos = calcular_last_pos(arvore.esquerda, todos, contador)
    elif valor == '+':
        #rever essa regra com a professora
        arvore.last_pos = calcular_last_pos(arvore.esquerda, todos, contador)
    elif valor == '&':
        arvore.last_pos = []
    else:
        if valor in todos.keys():
            arvore.last_pos = todos[valor].first_pos
        else:
            contador += 1
            return [contador]
    
def definir_last_pos(arvore, todos):
    calcular_last_pos(arvore, todos, contador=0)

def calcular_first_pos(arvore, todos, contador=0):
    try:
        valor = arvore.valor
    except:
        valor = arvore

    if valor == '.':
        if arvore.esquerda.nullable:
            arvore.first_pos = calcular_first_pos(arvore.esquerda, todos, contador)+calcular_first_pos(arvore.direita, todos, contador)
        else:
            arvore.first_pos = calcular_first_pos(arvore.esquerda, todos, contador)
    elif valor == '|':
        arvore.first_pos = calcular_first_pos(arvore.esquerda, todos)+calcular_first_pos(arvore.direita, todos, contador)
    elif valor == '*':
        arvore.first_pos = calcular_first_pos(arvore.esquerda, todos, contador)
    elif valor == '+':
        #rever essa regra com a professora
        arvore.first_pos = calcular_first_pos(arvore.esquerda, todos, contador)
    elif valor == '&':
        arvore.first_pos = []
    else:
        if valor in todos.keys():
            arvore.first_pos = todos[valor].first_pos
        else:
            contador += 1
            return [contador]
    
def definir_first_pos(arvore, todos):
    calcular_first_pos(arvore, todos, contador=0)

def calcular_nullables(arvore, todos):
    try:
        valor = arvore.valor
    except:
        valor = arvore

    if valor == '.':
        nullable_direita = calcular_nullables(arvore.direita, todos)
        nullable_esquerda = calcular_nullables(arvore.esquerda, todos)
        arvore.nullable = (nullable_esquerda and nullable_direita)
    elif valor == '|':
        arvore.nullable = (calcular_nullables(arvore.esquerda, todos) or calcular_nullables(arvore.direita, todos))
    elif valor == '*':
        arvore.nullable = True
    elif valor == '+':
        arvore.nullable = False
    elif valor == '&':
        arvore.nullable = True
    else:
        if valor in todos.keys():
            arvore.nullable = (todos[valor].nullable)
        else:
            return False

def definir_nullable(arvore, todos):
    calcular_nullables(arvore, todos)


def calcular_valores_pos(dict):
    for chave in dict.keys():
        arvore = dict[chave]
        definir_nullable(arvore, dict)
        definir_first_pos(arvore, dict)
        definir_last_pos(arvore, dict)
    return dict


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
            if simbolo in todos.keys() or tamanho <= 1:
                valor_direita = simbolo
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
        expressao_regular = dict[chave]
        expressao_regular = adicionar_concat(expressao_regular)
        expressao_regular = processar_dependencias(expressao_regular)
        dict[chave] = criar_arvore(expressao_regular, dict)
    return dict
        
#lê arquivo de entrada e retorna uma dict com todas as entradas de Regex e seus valores como string
def ler_arquivo(nome_arquivo):
    dict = {}
    with open(nome_arquivo) as f:
        linhas = f.readlines()
        nome, expressao = linhas.split(':')
        dict[nome] = expressao
    return dict


if __name__ == "__main__":
    #criar_arvore([['aaa', '|', '&'],'.', [['a', '|', ['b', '|', ['a', '.', 'b']]], '+'], '.', [['a', '*'],'.','b'], '.', '#'], {})
    dict = {}
    dict['exp'] = '(a|b)*abb'
    dict = processar_expressoes(dict)
    dict = calcular_valores_pos(dict)
    print('bla')