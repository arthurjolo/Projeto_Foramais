from regex_para_afd import regex_para_afd
from uniao import uniao
from automato_finito import AutomatoFinito
from model_analisador_lexico import RespostaAnalisadorLexico

class Gerador_AnalizadoLexico:
    def __init__(self):
        self.expressoes_regulares = []
        self.automatos = []
        self.analizador_autal = None
        self.tokens = []

    def main(self):
        while True:
            acao = int(input("1. Adicionar ER\n"
                            "2. Analisar código fonte\n"
                            "3. Sair"))
            
            if acao == 3:
                break

            if acao == 1:
                
                self.add_er()
            
            elif acao == 2:
                self.analise_lexica()
            
    def add_er(self):
        arquivo_er = input("insira o nome do arquivo contendo a ER")
        arquivo_er = "./regex_entrada/regex1.txt"
        while True:
            self.expressoes_regulares.append(arquivo_er)
            af_gerada = regex_para_afd(arquivo_er)
            print(af_gerada)
            af = af_gerada[0]
            if(len(af_gerada) > 0):
                for i in range(1, len(af_gerada)):
                    af_nova = uniao(af, af_gerada[i])
                    af = af_nova
            af_nova = AutomatoFinito(af_nova)
            self.automatos.append(af_nova)
            if not(self.analizador_autal):
                self.analizador_autal = af_nova
                self.analizador_autal.set_nome("analizador_lexico")
            else:
                analizador_novo = uniao(self.analizador_autal, af_nova) #precisa determinizar, quando o edu fizer o dele
                self.analizador_autal = AutomatoFinito(analizador_novo)
                self.analizador_autal.set_nome("analizador_lexico")
            continuar = input("deseja inserir outra ER? ('S' 'N')")
            if continuar.upper() == 'N':
                break
    
    def analise_lexica(self):
        lexemas = "lexemas"
        codigo_fonte = input("insira o nome do arquivo contendo o código fonte")
        codigo_fonte = "./entrada_codigo/ex1.txt"
        
        with open(codigo_fonte) as f:
            lexemas = f.read()

        resposta_analise_lexica = RespostaAnalisadorLexico()
        resposta_analise_lexica.lexema_restante = lexemas

        while True:
            if (len(resposta_analise_lexica.lexema_restante) == 0):
                break
            if resposta_analise_lexica.lexema_restante[0] == ' ' or resposta_analise_lexica.lexema_restante[0] == '\n':
                resposta_analise_lexica.lexema_restante = resposta_analise_lexica.lexema_restante[1::]

            resposta_analise_lexica = self.buscar_token(resposta_analise_lexica)

            if (resposta_analise_lexica.erro != None):
                print(resposta_analise_lexica.erro)
                return resposta_analise_lexica.erro
            

        print(resposta_analise_lexica.lista_tokens)
        return resposta_analise_lexica.lista_tokens
        
    def buscar_token(self, resposta_analise_lexica):
        
        estado = self.analizador_autal.estado_inicial
        ultimo_estado_de_aceitacao = self.analizador_autal.n_estados

        ultimo_lexema_aceito = 0
        tamanho_palavra = 0
        

        while True:
            resultado = self.analizador_autal.passo_de_processamento(estado, tamanho_palavra, resposta_analise_lexica.lexema_restante)
            if estado in self.analizador_autal.estados_finais:
                ultimo_lexema_aceito = tamanho_palavra
                ultimo_estado_de_aceitacao = estado
            if (not resultado.is_palavra_processada):
                break
            elif (resultado.erro != None):
                break
            else:
                tamanho_palavra += 1
                estado = resultado.proximos_estados[0]
                if (len(resposta_analise_lexica.lexema_restante) < tamanho_palavra):
                    break

        if(resultado.erro == "nao esta no alfabeto" and resposta_analise_lexica.lexema_restante[tamanho_palavra] != "\n" and resposta_analise_lexica.lexema_restante[tamanho_palavra] != ' '):
            resposta_analise_lexica.erro = resultado.erro

        elif not resultado.is_palavra_aceita and ultimo_lexema_aceito > 0:
            tipo_token = ultimo_estado_de_aceitacao  
            resposta_analise_lexica.lista_tokens.append(f"<{ultimo_estado_de_aceitacao},{resposta_analise_lexica.lexema_restante[:ultimo_lexema_aceito+1]}>")
            resposta_analise_lexica.lexema_restante = resposta_analise_lexica.lexema_restante[ultimo_lexema_aceito+1:]

        elif resultado.is_palavra_aceita:
            resposta_analise_lexica.lista_tokens.append(f"<{resultado.estado_final},{resposta_analise_lexica.lexema_restante}>")

        else:
            espaco = resposta_analise_lexica.lexema_restante.find(' ')
            quebra = resposta_analise_lexica.lexema_restante.find('\n')
            if espaco == -1 or quebra == -1:
                corte = max(espaco, quebra)
            else:
                corte = min(espaco, quebra)
            resposta_analise_lexica.lexema_restante = resposta_analise_lexica.lexema_restante[corte::]
        
        return resposta_analise_lexica



if __name__ == "__main__":
    Gerador_AnalizadoLexico().main()
    