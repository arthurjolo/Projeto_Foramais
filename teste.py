def teste(lista):
    elemento = lista.pop()
    for j in range(len(elemento)):
        lista.append(elemento[j])
        if j < len(elemento) - 1:
            lista.append('.')

    print(lista)


#teste(['a', '.', 'abcdefg'])


def teste2():
    print([1, 2, 3]+None)

teste2()