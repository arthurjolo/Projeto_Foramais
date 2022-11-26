class Gramatica:
    def __init__(self, gramatica):
        gramatica = gramatica
        '''
        gramatica = {
         "E'": ['E'], 
         'E': ['E + T', 'T'], 
         'T': ['T * F', 'F'], 
         'F': ['(E)', 'id']
        }
        '''

        terminais = []
        nao_terminais = []
        
    
    def determinar_nao_terminais(Self):
        pass

    def determinar_terminais(self):
        pass

    def eh_glc(self):
        pass

    def calcular_first_pos(self):
        pass

    def calcular_last_pos(self):
        pass