from gerador_analisadorLexico import Gerador_AnalizadoLexico
from analisador_sintatico import analisador_sintatico


def ler_tokens_entrada(lista_tokens_arquivo):
    with open(lista_tokens_arquivo) as f:
        tokens = [line.rstrip('\n') for line in f]
    lista_tokens = []
    for t in tokens:
        t = t.replace("<", "").replace(">", "")
        lista_tokens.append({
            "tipo": t.split(",")[0],
            "valor": t.split(",")[1]
        })
    print(lista_tokens)
    return lista_tokens

def main():
    lexico = Gerador_AnalizadoLexico()
    while True:
        print("Escolha \n 1) Para entrar no gerador/analisador léxico \n 2) Para entrar no analisador sintático\n 3) Para sair \n")
        escolha = int(input())
        if (escolha == 1):
            lexico.main()
        elif (escolha == 2):
            arquivo_analisador = input("Digite o caminho relativo para a gramática do analisador")
            arquivo_tokens = input("Digite o caminho relativo para a lista de tokens")
            analisador_sintatico(arquivo_analisador, ler_tokens_entrada(arquivo_tokens))
        else:
            break

if __name__ == "__main__":
    main()