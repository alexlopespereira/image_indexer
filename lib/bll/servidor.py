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
from .. dal.dal_servidor import DALServidor

class Servidor:

    def __init__(self, ip = None, usuario_processamento = None, diretorio_raiz_indice = None, os = None, codigo_centro_administrativo = None, codigo = 0):

        if ip is not None:
            self.popula_objeto(DALServidor.select_por_ip(ip))
            if not self.codigo > 0:
                self.codigo                 = 0
                self.ip                     = ip 
                self.usuario_processamento  = usuario_processamento
                self.diretorio_raiz_indice  = diretorio_raiz_indice
                self.os                     = os
                self.codigo_centro_administrativo = codigo_centro_administrativo
                self.salvar()
        elif codigo > 0:
            self.popula_objeto(DALServidor.select(codigo))


    def salvar(self):
        if self.codigo > 0:
            try:
                DALServidor.update(self.codigo, self.ip, self.usuario_processamento, self.diretorio_raiz_indice, self.os, self.codigo_centro_administrativo)
            except BaseException as e:
                raise Exception("ERRO AO ATUALIZAR SERVIDOR: %s" % (e))
        else:
            try:
                codigo_retorno = DALServidor.insert(self.ip, self.usuario_processamento, self.diretorio_raiz_indice, self.os, self.codigo_centro_administrativo)
                if codigo_retorno > 0:
                    self.codigo = codigo_retorno
                else:
                    raise Exception("Não foi possível recuperar os dados o servidor inserido.")
            except BaseException as e:
                raise Exception("ERRO AO INSERIR SERVIDOR: %s" % (e))


    def popula_objeto(self, dataset):
        if dataset is not None:
            self.codigo                 = dataset['co_seq_servidor']
            self.ip                     = dataset['no_ip']
            self.usuario_processamento  = dataset['no_usuario_processamento']
            self.diretorio_raiz_indice  = dataset['no_diretorio_raiz_indice']
            self.os                     = dataset['no_os']
            self.codigo_centro_administrativo = dataset['co_centro_administrativo']
        else:
            self.codigo = 0

    @staticmethod
    def listar_todas():
        lista_retorno = []

        dataset = DALServidor.select_all()

        for ds in dataset:
            s = Servidor()
            s.popula_objeto(ds)
            lista_retorno.append(s)

        return lista_retorno
