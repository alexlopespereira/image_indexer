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

class DALFornecedor:

    conexao = gerenciador.Banco()

    def __init__(self):
        pass

    #métodos estáticos
    @staticmethod
    def insert(nome, endereco, contrato):
        return DALFornecedor.conexao.executar_insert("INSERT INTO indice_imagens.tb_fornecedor(no_fornecedor, ds_endereco, ds_contrato_vinculo) VALUES(%s, %s, %s) RETURNING co_seq_fornecedor", [nome, endereco, contrato])

    @staticmethod
    def update(codigo, nome, endereco, contrato):
        return DALFornecedor.conexao.executar_update("UPDATE indice_imagens.tb_fornecedor SET no_fornecedor = %s, ds_endereco = %s, ds_contrato_vinculo = %s WHERE co_seq_fornecedor = %s", [nome, endereco, contrato, codigo])

    @staticmethod
    def select_all():
	return DALFornecedor.conexao.consultar("SELECT * FROM indice_imagens.tb_fornecedor order by co_seq_plataforma asc")

    @staticmethod
    def select(codigo):
        tupla = DALFornecedor.conexao.consultar("SELECT * FROM indice_imagens.tb_fornecedor WHERE co_seq_fornecedor = %s", [codigo])
        if len(tupla) > 0:
            return tupla[0]
        else:
            return None
