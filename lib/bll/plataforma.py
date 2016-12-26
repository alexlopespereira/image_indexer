# coding=utf-8
'''  
 ********************************************************** 
 CENSIPAM CGBD - CGTIC 
 Data: 04/03/2016 
 Autor: Bruno Alphonsus 
 Descrição: Classe que representa a platorma em que a imagem
 	    foi gerada 
 
 Atualizações: 
 
 - ... 
 **********************************************************  
'''

from .. dal.dal_plataforma import DALPlataforma 

class Plataforma:

    def __init__(self, nome = None, descricao = None, posicao = None, codigo = 0):
        
        if codigo > 0:
            self.popula_objeto(DALPlataforma.select(codigo))
        elif nome is not None:
            self.popula_objeto(DALPlataforma.select_por_nome(nome))
        else:
            self.codigo     = 0
            self.nome       = nome
            self.descricao  = descricao
            self.posicao    = posicao

    def popula_objeto(self, dataset):
        if dataset is not None:
             self.codigo        = dataset['co_seq_plataforma']
             self.nome          = dataset['no_plataforma']
	     self.descricao     = dataset['ds_plataforma']
             self.posicao       = dataset['no_posicao']

    @staticmethod
    def listar_todas():
        lista_retorno = []

        dataset = DALPlataforma.select_all()

        for ds in dataset:
            p = Plataforma()
            p.popula_objeto(ds)
            lista_retorno.append(p)

        return lista_retorno

