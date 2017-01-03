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
import psycopg2
import psycopg2.extras
import datetime
from lib import utilitarios

class Banco:

    DSN = "dbname=sig_sipam_alt user=alex.pereira password=@Lex2016 host=172.21.5.175"

    def __init__(self):
   
        self.transacao      = None
        self.consulta       = None
        self.sessao         = None
        self.sessao_pronta  = False

    def preparar_transacao(self):
    
        try:

            #para transações a sessão deve permanecer até a execução do commit
            #sem o RealDictCursor (dicionário das colunas)
            self.sessao  = psycopg2.connect(Banco.DSN)

            #abrindo cursor para a transação
            self.transacao = self.sessao.cursor()

            #indicando o estado da sessão para a transacao
            self.sessao_pronta = True

        except (BaseException, psycopg2.Error) as e:
            
            #fechando sessão/cursor em caso de falha
            if self.transacao is not None:self.transacao.close()
            if self.sessao is not None:self.sessao.close()

            raise Exception("PREPARAR A TRANSACAO : (%s) -  %s" % (type(e).__name__, e))

    def executar_update(self, comando_dml="", lista_parametros=[]):
        try:
            with psycopg2.connect(Banco.DSN) as self.sessao:
                with self.sessao.cursor() as self.transacao:
                    self.transacao.execute(comando_dml, lista_parametros)
        except (BaseException, psycopg2.Error) as e:
            raise Exception("UPDATE: (%s) -  %s" % (type(e).__name__, e))
        finally:
            if self.sessao is not None:
                self.sessao.close()

    def executar_insert(self, comando_dml="", lista_parametros=[]):
        try:
            with psycopg2.connect(Banco.DSN) as self.sessao:
                with self.sessao.cursor() as self.transacao:
                    self.transacao.execute(comando_dml, lista_parametros)
                    id_retorno = self.transacao.fetchone()[0]
                    if id_retorno > 0:
                        return id_retorno
                    else:
                        raise Exception("Não foi possível recuperar o ID do registro inserido.")
        except psycopg2.Error as e:
            #raise psycopg2.IntegrityError("INSERT: (%s) -  %s" % (type(e).__name__, e))
            utilitarios.logar(utilitarios.arquivo_log, "Arquivo %s ja existe no banco de dados." % type(e).__name__)
            pass
        except BaseException as e:
            raise Exception("INSERT: (%s) -  %s" % (type(e).__name__, e))
        finally:
            if self.sessao is not None:
                self.sessao.close()

    #método necessário para realizar a operacao de classificação das imagens
    def executar_insert_sem_commit(self, comando_dml="", lista_parametros=[]):
        try:
            if self.sessao_pronta:
                self.transacao.execute(comando_dml, lista_parametros)
                id_retorno = self.transacao.fetchone()[0]
                if id_retorno > 0:
                    return id_retorno
                else:
                    raise Exception("Não foi possível recuperar o ID do registro inserido.")
            else:
                raise Exception("O estado da sessão não encontra-se disponível para realizar a transação.")
        except psycopg2.Error as e:
            if self.transacao is not None:self.transacao.close()
            utilitarios.logar(utilitarios.arquivo_log, "Arquivo %s ja existe no banco de dados." % type(e).__name__)
            pass
        except BaseException as e:
            if self.transacao is not None:self.transacao.close()
            raise Exception("INSERT(NOCOMMIT): (%s) -  %s" % (type(e).__name__, e))

    def finalizar_transacao(self, sucesso):
        if sucesso:
            try:
                if self.sessao is not None:self.sessao.commit()
            except (BaseException, psycopg2.Error) as e:
                raise Exception("ERRO AO FINALIZAR TRANSAÇÃO: (%s) -  %s" % (type(e).__name__, e))
            finally:
                if self.transacao is not None:self.transacao.close()
                if self.sessao is not None:self.sessao.close()
        else:
            try:
                if self.sessao is not None:self.sessao.rollback()
            except (BaseException, psycopg2.Error) as e:
                raise Exception("FINALIZAR TRANSAÇÃO: (%s) -  %s" % (type(e).__name__, e))
            finally:
                if self.transacao is not None:self.transacao.close()
                if self.sessao is not None:self.sessao.close()

        self.sessao_pronta = False

    def consultar(self, comando_sql="", lista_parametros=[]):

        #setando a variavel local antes do bloco de exceção
        sessao_local = None

        try:
            #para consultas a sessão de conexão é local e temporária
            sessao_local = psycopg2.connect(Banco.DSN, cursor_factory=psycopg2.extras.RealDictCursor) 
            with sessao_local: 
                #contexto do cursor
                with sessao_local.cursor() as self.consulta:
                    #realizar consulta, com ou sem parêmetro de filtro
                    if len(lista_parametros) > 0:
                        self.consulta.execute(comando_sql, lista_parametros)
                    else:
                        self.consulta.execute(comando_sql)

                    #número máximo de registros para retornar em uma consulta (100)
                    if self.consulta.arraysize > 100:
                        dataset_retorno = self.consulta.fetchmany(100)
                    else:
                        dataset_retorno = self.consulta.fetchall()
                
            return dataset_retorno 

        except (BaseException, psycopg2.Error) as e:
            raise Exception("CONSULTA: (%s) -  %s" % (type(e).__name__, e))
        finally:
            if sessao_local is not None:
                sessao_local.close()


