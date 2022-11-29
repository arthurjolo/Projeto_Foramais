alfabeto_minusculo = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l' ,'m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
alfabeto_maiusculo = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L' ,'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
operadores = ['*', '+', '?', '|', '(', ')', '.']
empty = '&'

def tira_caractere(lista, caractere):
    resultado = []
    for i in range(len(lista)):
        if lista[i] != caractere:
            resultado.append(lista[i])
    return ''.join(resultado)

def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l

#pegar todos os elementos da lista entre dois valores (inclusive)
def retornar_todos_entre(lista, primeiro, ultimo):
    get = False
    resultado = []
    for i in range(len(lista)):
        if lista[i] == primeiro:
            get = True
        
        if get:
            resultado.append(lista[i])

        if lista[i] == ultimo:
            get = False

    return resultado

def colocar_operacao_entre_elementos(lista, operacao):
    resultado = []
    for i in range(len(lista)):
        resultado.append(lista[i])
        if i != len(lista) - 1:
            resultado.append(operacao)
    return resultado
