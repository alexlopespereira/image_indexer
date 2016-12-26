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

class DALServidor:

    conexao = gerenciador.Banco()

    def __init__(self):
        pass

    #métodos de classe
    @staticmethod
    def insert(ip, usuario_processamento, diretorio_raiz_indice, os, codigo_centro_administrativo):
        return DALServidor.conexao.executar_insert("INSERT INTO indice_imagens.tb_servidor(no_ip, no_usuario_processamento, no_diretorio_raiz_indice, no_os, co_centro_administrativo) VALUES (%s,%s,%s,%s,%s) RETURNING co_seq_servidor", [ip, usuario_processamento, diretorio_raiz_indice, os, codigo_centro_administrativo])

    @staticmethod
    def update(codigo, ip, usuario_processamento, diretorio_raiz_indice, os, codigo_centro_administrativo):
        return DALServidor.conexao.executar_insert("UPDATE indice_imagens.tb_servidor SET no_ip = %s, no_usuario_processamento = %s, no_diretorio_raiz_indice = %s, no_os = %s, co_centro_administrativo = %s WHERE co_seq_servidor = %s", [ip, usuario_processamento, diretorio_raiz_indice, os, codigo_centro_administrativo, codigo])

    @staticmethod
    def select_all():
	return DALServidor.conexao.consultar("SELECT * FROM indice_imagens.tb_servidor order by co_seq_servidor asc")

    @staticmethod
    def select(codigo):
        tupla = DALServidor.conexao.consultar("SELECT * FROM indice_imagens.tb_servidor WHERE co_seq_servidor = %s", [codigo])
        if len(tupla) > 0:
            return tupla[0]
        else:
            return None
    
    @staticmethod
    def select_por_ip(ip):
        tupla = DALServidor.conexao.consultar("SELECT * FROM indice_imagens.tb_servidor WHERE no_ip = %s", [ip])
        if len(tupla) > 0:
            return tupla[0]
        else:
            return None
