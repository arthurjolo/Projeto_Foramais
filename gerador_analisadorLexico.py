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
        #arquivo_er = "./regex_entrada/regex1.txt"
        while True:
            arquivo_er = input("insira o nome do arquivo contendo a ER")
            self.expressoes_regulares.append(arquivo_er)
            af_gerada = regex_para_afd(arquivo_er)
            print(af_gerada)
            self.automatos += af_gerada
            continuar = input("deseja inserir outra ER? ('S' 'N')")
            if continuar.upper() == 'N':
                for i in range(0, len(self.automatos)):
                    self.automatos[i] = AutomatoFinito(self.automatos[i])
                af = uniao(self.automatos)
                self.analizador_autal = AutomatoFinito(af[0])
                self.analizador_autal.lable_estados_finais = af[1]
                print("leble analisador: ", self.analizador_autal.lable_estados_finais)
                break
    
    def analise_lexica(self):
        print(self.analizador_autal.lable_estados_finais)
        lexemas = "lexemas"
        codigo_fonte = input("insira o nome do arquivo contendo o código fonte")
        #codigo_fonte = "./entrada_codigo/ex1.txt"
        
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
            

        with open(f'./lista_tokens/{self.analizador_autal.nome}.txt', 'w') as f:
            for token in resposta_analise_lexica.lista_tokens:
                f.write(f"{token}\n")
        
        print("Análise léxica concluída com sucesso")
        
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
            tipo_token = self.analizador_autal.lable_estados_finais[ultimo_estado_de_aceitacao][0]
            resposta_analise_lexica.lista_tokens.append(f"<{tipo_token},{resposta_analise_lexica.lexema_restante[:ultimo_lexema_aceito]}>")
            resposta_analise_lexica.lexema_restante = resposta_analise_lexica.lexema_restante[ultimo_lexema_aceito+1:]

        elif resultado.is_palavra_aceita:
            tipo_token  = self.analizador_autal.lable_estados_finais[resultado.estado_final][0]
            resposta_analise_lexica.lista_tokens.append(f"<{tipo_token},{resposta_analise_lexica.lexema_restante}>")
            resposta_analise_lexica.lexema_restante = resposta_analise_lexica.lexema_restante[ultimo_lexema_aceito+1:]
        else:
            espaco = resposta_analise_lexica.lexema_restante.find(' ')
            quebra = resposta_analise_lexica.lexema_restante.find('\n')
            if espaco == -1 or quebra == -1:
                corte = max(espaco, quebra)
            else:
                corte = min(espaco, quebra)
            resposta_analise_lexica.lexema_restante = resposta_analise_lexica.lexema_restante[corte::]
            resposta_analise_lexica.erro = "Token inválido"
        return resposta_analise_lexica



if __name__ == "__main__":
    Gerador_AnalizadoLexico().main()
    