from regex_para_afd import regex_para_afd
from uniao import uniao
from automato_finito import AutomatoFinito

class Gerador_AnalizadoLexico:
    def __init__(self):
        self.expressoes_regulares = []
        self.automatos = []
        self.analizador_autal = None

    def main(self):
        while True:
            acao = int(input("1. Adicionar ER\n"
                            "2. Analisar código fonte\n"
                            "3. Sair"))
            
            if acao == 3:
                break

            if acao == 1:
                arquivo_er = input("insira o nome do arquivo contendo a ER")
                self.add_er(arquivo_er)
            
            elif acao == 2:
                codigo_fonte = input("insira o nome do arquivo contendo o código fonte")
                #chamar parte da Larissa
            
    def add_er(self, arquivo_er):
        self.expressoes_regulares.append(arquivo_er)
        af_gerada = regex_para_afd(arquivo_er)
        af_nova = AutomatoFinito(af_gerada)
        self.automatos.append(af_nova)
        if not(self.analizador_autal):
            self.analizador_autal = af_nova
            self.analizador_autal.set_nome("analizador_lexico")
        else:
            analizador_novo = uniao(self.analizador_autal, af_nova) #precisa determinizar, quando o edu fizer o dele
            self.analizador_autal = AutomatoFinito(analizador_novo)
            self.analizador_autal.set_nome("analizador_lexico")

