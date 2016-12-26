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
from .. bd import gerenciador

class DALSensor:
    conexao = gerenciador.Banco()
    def __init__(self):
        pass

    #métodos estáticos
    @staticmethod
    def insert(nome, faixa_espectral):
        return DALSensor.conexao.executar_insert("INSERT INTO indice_imagens.tb_sensor(no_sensor, no_faixa_espectral) VALUES(%s, %s) RETURNING co_seq_sensor", [nome, faixa_espectral])

    @staticmethod
    def update(codigo, nome, faixa_espectral):
        return DALSensor.conexao.executar_update("UPDATE indice_imagens.tb_sensor SET no_sensor = %s, no_faixa_espectral = %s WHERE co_seq_sensor = %s", [nome, faixa_espectral, codigo])

    @staticmethod
    def select_all():
        return DALSensor.conexao.consultar("SELECT * FROM indice_imagens.tb_sensor order by co_seq_sensor asc")

    @staticmethod
    def select(co_sensor):
	tupla = DALSensor.conexao.consultar("SELECT * FROM indice_imagens.tb_sensor WHERE co_seq_sensor = %s", [co_sensor])
        if len(tupla) > 0:
            return tupla[0]
        else:
            return None
    
    @staticmethod
    def select_por_nome(nome):
	tupla = DALSensor.conexao.consultar("SELECT * FROM indice_imagens.tb_sensor WHERE no_sensor = %s", [nome])
        if len(tupla) > 0:
            return tupla[0]
        else:
            return None
