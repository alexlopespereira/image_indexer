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

from .. dal.dal_fornecedor import DALFornecedor

class Fornecedor:

    def __init__(self, nome = None, endereco = None, contrato = None, codigo = 0):

        if codigo > 0:
            self.popula_objeto(DALFornecedor.select(codigo))
        else:
            self.codigo     = 0
            self.nome       = nome
            self.endereco   = endereco
            self.contrato   = contrato

    def salvar():
        if self.codigo > 0:
            try:
                DALFornecedor.update(self.codigo, self.nome, self.endereco, self.contrato)
            except BaseException as e:
                raise Exception("ERRO AO ATUALIZAR FORNECEDOR: %s" % (e))
        else:
            try:
                DALFornecedor.insert(self.nome, self.endereco, self.contrato)
            except BaseException as e:
                raise Exception("ERRO AO INSERIR FORNECEDOR: %s" % (e))


    def popula_objeto(self, dataset):
        if dataset is not None:
             self.codigo        = dataset['co_seq_fornecedor']
             self.nome          = dataset['no_fornecedor']
             self.endereco      = dataset['ds_endereco']
             self.contrato      = dataset['ds_vinculo_contrato']

    @staticmethod
    def listar_todas():
        lista_retorno = []

        dataset = DALFornecedor.select_all()

        for ds in dataset:
            f = Fornecedor()
            f.popula_objeto(ds)
            lista_retorno.append(f)

        return lista_retorno
