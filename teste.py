def teste(lista):
    elemento = lista.pop()
    for j in range(len(elemento)):
        lista.append(elemento[j])
        if j < len(elemento) - 1:
            lista.append('.')

    print(lista)





teste(['a', '.', 'abcdefg'])