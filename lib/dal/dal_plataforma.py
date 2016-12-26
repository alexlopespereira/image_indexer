# coding=utf-8
'''  
 ********************************************************** 
 CENSIPAM CGBD - CGTIC 
 Data: 04/03/2016 
 Autor: Bruno Alphonsus 
 Descrição:  
 
 Atualizações: 
 
 - ... 
 **********************************************************  
'''

from .. bd import gerenciador

class DALPlataforma:

    conexao = gerenciador.Banco()

    def __init__(self):
        pass

    #métodos estáticos
    @staticmethod
    def insert(nome, descricao, posicao):
        return DALPlataforma.conexao.executar_insert("INSERT INTO indice_imagens.tb_plataforma(no_plataforma, ds_descricao, no_posicao) VALUES(%s, %s, %s) RETURNING co_seq_plataforma", [nome, descricao, posicao])

    @staticmethod
    def update(codigo, nome, descricao, posicao):
        return DALPlataforma.conexao.executar_update("UPDATE indice_imagens.tb_plataforma SET no_plataforma = %s, ds_descricao = %s, no_posicao = %s WHERE co_seq_plataforma = %s", [nome, descricao, posicao, codigo])
    
    @staticmethod
    def select_all():
        return DALPlataforma.conexao.consultar("SELECT * FROM indice_imagens.tb_plataforma order by co_seq_plataforma asc")

    @staticmethod
    def select_por_nome(nome):
        tupla = DALPlataforma.conexao.consultar("SELECT * FROM indice_imagens.tb_plataforma WHERE no_plataforma = %s", [nome])
        if len(tupla) > 0:
            return tupla[0]
        else:
            return None
    
    @staticmethod
    def select(codigo):
        tupla = DALPlataforma.conexao.consultar("SELECT * FROM indice_imagens.tb_plataforma WHERE co_seq_plataforma = %s", [codigo])
        if len(tupla) > 0:
            return tupla[0]
        else:
            return None
