# coding=utf-8
import indexador
from lib import utilitarios
from lib.utilitarios import arquivo_log
import datetime,os
import sys, traceback
def main():


    try:
        
        diretorio_processamento = '/indice_imagens'

        if not os.path.exists(diretorio_processamento):
            raise "Diretório informado ""%s"" não existe." % diretorio_processamento

        utilitarios.arquivo_log = '%s/%s%s' % (diretorio_processamento, datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S"), '.log')

        idx = indexador.Indexador(diretorio_processamento)

        utilitarios.logar(utilitarios.arquivo_log, "Iniciando processo de indexacao...")
        utilitarios.logar(utilitarios.arquivo_log, "Verificando a estrutura de diretórios do indice...")
        idx.verificar_estrutura_diretorios()

        utilitarios.logar(utilitarios.arquivo_log, "Coletando dados das imagens...")
        idx.coletar_metadados()
        utilitarios.logar(utilitarios.arquivo_log, "Classificando....")
        idx.indexar_imagens()
        utilitarios.logar(utilitarios.arquivo_log, "Fim do processo de indexacao.")

    except BaseException as e:
        utilitarios.logar(utilitarios.arquivo_log, "ERRO - INDEXAÇÃO INTERROMPIDA: %s" % e)

if __name__ == "__main__": main()
