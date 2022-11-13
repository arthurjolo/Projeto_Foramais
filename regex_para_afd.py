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

class tipoSimbolo:
    ALFABETO = 1
    NUMERO = 2
    OPERADOR = 3  
    FECHO = 4  
    FINAL = 5

class arvoreExpressao:
    def __init__(self, tipo_simbolo, valor=None, esquerda=None, direita=None):
        self.tipo_simbolo = tipo_simbolo
        self.valor = valor
        self.esquerda = esquerda
        self.direita = direita



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
            valor_direita = arvoreExpressao(tipo_simbolo=tipoSimbolo.FINAL)
        elif isinstance(simbolo, list):
            valor_direita =  criar_arvore(simbolo, todos)
        elif simbolo in ['*', '+']:
            valor_direita = arvoreExpressao(tipo_simbolo=tipoSimbolo.FECHO, 
                                            valor=simbolo,
                                            esquerda=criar_arvore(expressao, todos))
        elif simbolo == '|' or simbolo == '.':
            valor_direita = arvoreExpressao(tipo_simbolo=tipoSimbolo.OPERADOR, 
                                            valor=simbolo,
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
    
    if pilha != []:
        pilha.append('.')
    pilha.append('#')

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
    criar_arvore([['aaa', '|', '&'],'.', [['a', '|', ['b', '|', ['a', '.', 'b']]], '+'], '.', [['a', '*'],'.','b'], '.', '#'], {})
    