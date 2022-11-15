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
