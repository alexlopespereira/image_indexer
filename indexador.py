# coding=utf-8
import os, sys, copy
from lib import utilitarios
from lib.bll import imagem, plataforma, sensor, servidor
from metageta import crawler, utilities 

class Indexador:

    def __init__(self, diretorio_processamento, recursivo=True, arquivos_compactados=False):
        if not os.path.exists(diretorio_processamento):
            raise "Diretório informado ""%s"" não existe." % (diretorio_processamento)
        else:
            self.diretorio_root = diretorio_processamento
            self.recursivo = recursivo
            self.arquivos_compactados = arquivos_compactados
            self.dados_imagens = []

            dados_servidor = utilitarios.coletar_informacoes_locais()

            #verificando qual o centro administrativo (Códigos referentes ao sistema coorporativo do CENSIPAM) 21 - CCG, 22 - Belem, 23 - Porto Velho, 20 - Manaus

            snd_octet = int(dados_servidor['ip'].split('.')[1])
            #consultar o corporativo para verificar o código e tirar o hardcoded daqui
            if snd_octet == 20:
                #manaus
                codigo_centro_administrativo = 3
            elif snd_octet == 21:
                #brasília
                codigo_centro_administrativo = 1
            elif snd_octet == 22:
                #belem
                codigo_centro_administrativo = 2
            elif snd_octet == 23:
                #porto velho
                codigo_centro_administrativo = 4
            else:
                raise Exception("Centro administrativo não identificado. Verificar ip do servidor.")

            self.servidor = servidor.Servidor(dados_servidor['ip'],usuario_processamento = '%s:%s' %(dados_servidor['login'],dados_servidor['usuario']), os = dados_servidor['os'],diretorio_raiz_indice = diretorio_processamento, codigo_centro_administrativo = codigo_centro_administrativo)

        
    def coletar_metadados(self):
        if self.diretorio_root != '':
            
            utilitarios.logar(utilitarios.arquivo_log, "Aguardando o Crawler do MetaGETA...")
            metageta_crawler = crawler.Crawler(self.diretorio_entrada, self.recursivo, self.arquivos_compactados, excludes=['*.png', '*.jpg','*_meta'])
            utilitarios.logar(utilitarios.arquivo_log, "Organizando dados levantados pelo Crawler...")
            for dataset_imagem in metageta_crawler:
                #criando o objeto imagem com os atributos de metadados e respectiva geometria
                i = imagem.Imagem(servidor = self.servidor, metadados = dataset_imagem.metadata, arquivos = dataset_imagem.filelist, infos_arquivo = dataset_imagem.fileinfo, geometria = dataset_imagem.extent)
                #adicionando a imagem à lista de retorno
                self.dados_imagens.append(i)
        else:
            raise "Diretório de processamento não informado."

    #metodo que deverá ser utilizado no caso de utilizar o insert sem autocommit
    def indexar_imagem(self, imagem):
        return
   
    
    def indexar_imagens(self):

        for img in self.dados_imagens:
	    #verificar se a imagem img já foi movida do diretório de entrada
	    if not os.path.exists(img.caminho_arquivo):continue
           
            ##############################################################################################################
            #verificando se as imagens da cena estão diretamente no diretório de entrada
            ##############################################################################################################

            if os.path.dirname(img.caminho_arquivo) == self.diretorio_entrada_originais or os.path.dirname(img.caminho_arquivo) == self.diretorio_entrada_processadas:
                utilitarios.logar(utilitarios.arquivo_log, "ERRO - Não é possível mover imagens sem diretório de cena. Favor, colocar imagens em seus respectivos diretórios dentro do diretório de entrada:")
                utilitarios.logar(utilitarios.arquivo_log, "%s" % img.caminho_arquivo)
                #movendo imagem para a pasta de erros
                try:
                    utilitarios.logar(utilitarios.arquivo_log, "ERRO - Movendo %s para %s" % (img.caminho_arquivo, self.diretorio_erros))
                    utilities.runcmd("mv %s %s" % (img.caminho_arquivo, self.diretorio_erros))
                except(BaseException,OSError) as ose:
                    os.strerror = "Não foi possível mover a imagem %s para %s." % (img.caminho_arquivo, self.diretorio_erros)
                    raise

                #passando para a proxima imagem
                continue
            
            ##############################################################################################################
            #resgatar o nome do diretório abaixo do diretório de entrada em que o arquivo encontra-se
            ##############################################################################################################
            if self.diretorio_entrada_originais in img.caminho_arquivo:
                diretorio_pai = self.diretorio_entrada_originais + '/' + img.caminho_arquivo.replace(self.diretorio_entrada_originais,'').split('/')[1]
            elif self.diretorio_entrada_processadas in img.caminho_arquivo:
                diretorio_pai = self.diretorio_entrada_processadas + img.caminho_arquivo.replace(self.diretorio_entrada_processadas,'').split('/')[1]
            else:
                raise Exception('O caminho do arquivo %s foi modificado durante o processamento e não encontra-se em um dos diretórios de entrada - (%s/originais ou .../processados)' %(img.caminho_arquivo, self.diretorio_entrada))

            ##############################################################################################################
            #verificar se a cena possui outros arquivos além da imagem em verificação "img"
            ##############################################################################################################
            utilitarios.logar(utilitarios.arquivo_log, "Coletando imagens da cena em %s/..." % diretorio_pai)
            dados_imagens = copy.deepcopy(self.dados_imagens)

            imagens_cena = []
            imagens_cena = [i for i in dados_imagens if diretorio_pai in i.caminho_arquivo] 
           

            ##############################################################################################################
            #atualizar as imagens da cena com o diretório de destino da classificação (toma como referência a primeira imagem da cena)
            ##############################################################################################################
            ano_imagem = imagens_cena[0].data_coleta.year
            sen = imagens_cena[0].sensor.nome
            faix = imagens_cena[0].sensor.faixa_espectral
            plat = imagens_cena[0].plataforma.nome

            #setando diretório de destino
            if 'originais' in imagens_cena[0].caminho_arquivo: diretorio_destino = '%s/%s/%s/%s' % (self.diretorio_imagens_originais_microondas if faix == 'microondas' else self.diretorio_imagens_originais_opticas, plat, sen, ano_imagem)
            if 'processadas' in imagens_cena[0].caminho_arquivo: diretorio_destino = '%s/%s/%s/%s' % (self.diretorio_imagens_processadas_microondas if faix == 'microondas' else self.diretorio_imagens_processadas_opticas, plat, sen, ano_imagem)
            if diretorio_destino is None: raise Exception ('Não foi possível classificar as imagens contidas no diretório %s' % diretorio_pai)

            for i in imagens_cena:
                utilitarios.logar(utilitarios.arquivo_log, "Preparando para mover %s..." % os.path.basename(i.caminho_arquivo))
                if 'originais' in diretorio_destino: i.caminho_arquivo = i.caminho_arquivo.replace(self.diretorio_entrada_originais, diretorio_destino)
                if 'processadas' in diretorio_destino: i.caminho_arquivo = i.caminho_arquivo.replace(self.diretorio_entrada_processadas, diretorio_destino)


            ##############################################################################################################
            #mover as imagens para o diretório (destino) pós classificação e commitando as persistências
            ##############################################################################################################
            try:
                
                if not os.path.isdir(diretorio_destino):os.makedirs(diretorio_destino)
                utilitarios.logar(utilitarios.arquivo_log, "Movendo diretorio %s para %s..." % (diretorio_pai, diretorio_destino))
                utilities.runcmd("mv %s %s" % (diretorio_pai, diretorio_destino))
                ##############################################################################################################
                #inserir as imagens no banco com o novo caminho de destino
                #OBS: Estudar como fazer para commitar os inserts apenas após mover as imagens para o diretório de classificação
                ##############################################################################################################
                for i in imagens_cena:
                    utilitarios.logar(utilitarios.arquivo_log, "Inserindo imagem %s no banco..." % (i.caminho_arquivo.split('/')[-1]))
                    i.salvar()
            except (BaseException) as e:
                raise Exception("Erro classificar imagens do diretorio %s: (%s) - %s" % (diretorio_pai, type(e).__name__, e))



    def verificar_estrutura_diretorios(self):
        #estrutura de diretórios definida
        self.diretorio_entrada = "%s/%s" % (self.diretorio_root, "entrada")
        self.diretorio_entrada_originais = "%s/%s" % (self.diretorio_entrada, "originais")
        self.diretorio_entrada_processadas = "%s/%s" % (self.diretorio_entrada, "processadas")
        self.diretorio_imagens = "%s/%s" % (self.diretorio_root, "imagens")
        self.diretorio_imagens_originais = "%s/%s" % (self.diretorio_imagens, "originais")
        self.diretorio_imagens_processadas = "%s/%s" % (self.diretorio_imagens, "processadas")
        self.diretorio_imagens_originais_opticas = "%s/%s" % (self.diretorio_imagens_originais, "opticas")
        self.diretorio_imagens_processadas_opticas = "%s/%s" % (self.diretorio_imagens_processadas, "opticas")
        self.diretorio_imagens_originais_microondas = "%s/%s" % (self.diretorio_imagens_originais, "microondas")
        self.diretorio_imagens_processadas_microondas = "%s/%s" % (self.diretorio_imagens_processadas, "microondas")
        self.diretorio_erros = "%s/%s" % (self.diretorio_root, "erros")

        try:

            if not os.path.isdir(self.diretorio_entrada):os.makedirs(self.diretorio_entrada)
            if not os.path.isdir(self.diretorio_entrada_originais):os.makedirs(self.diretorio_entrada_originais)
            if not os.path.isdir(self.diretorio_entrada_processadas):os.makedirs(self.diretorio_entrada_processadas)
            if not os.path.isdir(self.diretorio_imagens):os.makedirs(self.diretorio_imagens)
            if not os.path.isdir(self.diretorio_imagens_originais):os.makedirs(self.diretorio_imagens_originais)
            if not os.path.isdir(self.diretorio_imagens_processadas):os.makedirs(self.diretorio_imagens_processadas)
            if not os.path.isdir(self.diretorio_imagens_originais_opticas):os.makedirs(self.diretorio_imagens_originais_opticas)
            if not os.path.isdir(self.diretorio_imagens_processadas_opticas):os.makedirs(self.diretorio_imagens_processadas_opticas)
            if not os.path.isdir(self.diretorio_imagens_originais_microondas):os.makedirs(self.diretorio_imagens_originais_microondas)
            if not os.path.isdir(self.diretorio_imagens_processadas_microondas):os.makedirs(self.diretorio_imagens_processadas_microondas)
            if not os.path.isdir(self.diretorio_erros):os.makedirs(self.diretorio_erros)
        except OSError as ose:
            ose.strerror = "Erro na criação da estrutura de diretórios: " + ose.strerror
            raise
