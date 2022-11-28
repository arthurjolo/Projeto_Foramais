class RespostaPasso():
    def __init__(self, is_palavra_processada = False, is_palavra_aceita = False, 
                    erro = None, proximo_estado = [], estado_final = 0):
        self.is_palavra_processada = is_palavra_processada
        self.is_palavra_aceita = is_palavra_aceita
        self.erro = erro
        self.proximo_estado = proximo_estado
        self.estado_final = estado_final

class RespostaAnalisadorLexico():
    def __init__(self, lista_tokens = [], lexema_restante = "", erro = None):
        self.lista_tokens = lista_tokens
        self.lexema_restante = lexema_restante
        self.erro = erro
