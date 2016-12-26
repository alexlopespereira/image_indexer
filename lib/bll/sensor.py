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

from .. dal.dal_sensor import DALSensor

class Sensor:

    def __init__(self, nome = None, faixa_espectral = None, codigo = 0):

        if codigo > 0:
            self.popula_objeto(DALSensor.select(codigo))
        elif nome is not None:
            self.popula_objeto(DALSensor.select_por_nome(nome))
        else:
            self.codigo             = 0
            self.nome               = nome
            self.faixa_espectral    = faixa_espectral 

    def salvar(self):
        if self.codigo > 0:
            try:
                DALSensor.update(self.codigo, self.nome, self.faixa_espectral)
            except BaseException as e:
                raise Exception("ERRO AO ATUALIZAR SENSOR: %s" % (e))
        else:
            try:
                codigo_retorno = DALSensor.insert(self.nome, self.faixa_espectral)
                if codigo_retorno > 0:
                    self.codigo = codigo_retorno
                else:
                    raise Exception("Não foi possível recuperar os dados do sensor inserido.")
            except BaseException as e:
                raise Exception("ERRO AO INSERIR SENSOR: %s" % (e))

    def popula_objeto(self, dataset):
        if dataset is not None:
             self.codigo                = dataset['co_seq_sensor']
             self.nome                  = dataset['no_sensor']
             self.faixa_espectral       = dataset['no_faixa_espectral']

    @staticmethod
    def listar_todas():
        lista_retorno = []

        dataset = DALSensor.select_all()

        for ds in dataset:
            s = Sensor()
            s.popula_objeto(ds)
            lista_retorno.append(s)

        return lista_retorno
