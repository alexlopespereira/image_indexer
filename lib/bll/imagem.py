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

from .. dal.dal_imagem import DALImagem
import os,datetime
import fornecedor, servidor, plataforma, sensor

class Imagem:

    def __init__(self, servidor, metadados, arquivos, infos_arquivo, geometria, codigo = 0):

	if codigo > 0:
		self.popula_objeto(DALImagem.select(codigo))
        else:
            self.codigo                 = 0

            #campos temporários
            self.metadados = metadados
            self.geometria = geometria
            self.lista_arquivos = arquivos
            self.info_arquivo_principal = infos_arquivo

            metadados_adicionais        = metadados['metadata']

            #metadados
            self.numero_bandas	= metadados['nbands'] if metadados['nbands'] != '' else None
            self.data_coleta	= metadados['imgdate'] if metadados['imgdate'] != '' else None
            self.tamanho_pixel_x= metadados['cellx'] if metadados['cellx']!= '' else None
            self.tamanho_pixel_y= metadados['celly'] if metadados['celly'] != '' else None

            if isinstance(metadados_adicionais, dict):
                self.unidade_celula_xy = metadados_adicionais['unidade_celula_xy'] if metadados_adicionais['unidade_celula_xy'] != '' else None
                self.near_range	 = None
                self.far_range	 = None
                self.angulo_near     = metadados_adicionais['angulo_near'] if metadados_adicionais['angulo_near'] != '' else None
                self.angulo_far      = metadados_adicionais['angulo_far'] if metadados_adicionais['angulo_far'] != '' else None
                self.direcao_orbita	 = metadados_adicionais['direcao_orbita'] if metadados_adicionais['direcao_orbita'] != '' else None
                self.datum           = metadados_adicionais['datum'] if metadados_adicionais['datum']!= '' else None
                self.projecao        = metadados_adicionais['projecao'] if metadados_adicionais['projecao']!= '' else None
                self.lado_imageamento= metadados_adicionais['lado_imageamento'] if metadados_adicionais['lado_imageamento']!= '' else None
                self.caminho_metadados 	= metadados_adicionais['caminho_metadados'] if metadados_adicionais['caminho_metadados']!= '' else None
                self.tipo_produto    = metadados_adicionais['tipo_produto'] if metadados_adicionais['tipo_produto'] != '' else None
                #dados de polarização
                if metadados_adicionais['polarizacao'] == 'HH':self.polar_hh = True
                else:self.polar_hh = False
                if metadados_adicionais['polarizacao'] == 'HV':self.polar_hv = True
                else:self.polar_hv = False
                if metadados_adicionais['polarizacao'] == 'VV':self.polar_vv = True
                else:self.polar_vv = False
                if metadados_adicionais['polarizacao'] == 'VH':self.polar_vh = True
                else:self.polar_vh = False

                if metadados_adicionais['srid'] != '':
                    self.SRID = metadados_adicionais['srid']
                else:raise Exception("O SRID da imagem não pôde ser identificado." % self.caminho_arquivo)

            self.quantidade_looks= None #if metadados['']!= '' else None
            self.srs             = metadados['srs'] if metadados['srs'] != '' else None
            self.quantidade_bits = metadados['nbits'] if metadados['nbits']!= '' else None
            self.id_cena         = metadados['sceneid'] if metadados['sceneid']!= '' else None
            self.id_orbita       = metadados['orbit'] if metadados['orbit']!= '' else None
            self.modo_imageamento= metadados['mode'] if metadados['mode']!= '' else None
            self.tipo_arquivo	 = metadados['filetype'] if metadados['filetype']!= '' else None
            self.data_indexacao  = datetime.datetime.now()
            #somente a extensao
            self.extensao_arquivo= os.path.splitext(infos_arquivo['filename'])[1]

            self.caminho_arquivo = infos_arquivo['filepath'] if metadados['filepath']!= '' else None
            self.quantidade_colunas     = metadados['cols'] if metadados['cols']!= '' else None
            self.quantidade_linhas      = metadados['rows'] if metadados['rows']!= '' else None
            self.caminho_arquivo_world   = None

            self.arquivado              = False

            #resgatando o sensor e a plataforma
            if metadados['sensor'] != '':
                self.sensor = sensor.Sensor(metadados['sensor'])
            #else:raise Exception("O sensor da imagem '%s' não pôde ser identificado." % self.caminho_arquivo)
            else:
                self.sensor = sensor.Sensor('DESCONHECIDO')

            if metadados['satellite'] != '':
                self.plataforma = plataforma.Plataforma(metadados['satellite'])
            #else:raise Exception("A plataforma da imagem '%s' não pôde ser identificada." % self.caminho_arquivo)
            else:
                self.plataforma = plataforma.Plataforma('DESCONHECIDA')

            #extraindo os pontos do poligono
            self.poligono_geometria= ''
            for ponto in self.geometria:
                if self.poligono_geometria!= '':
                    self.poligono_geometria = "%s,%s %s" % (self.poligono_geometria, ponto[0],ponto[1])
                else:
                    self.poligono_geometria= "%s %s" % (ponto[0],ponto[1])

            if servidor is not None and servidor.codigo > 0:
                self.servidor = servidor
            else:
                raise Exception("O servidor da imagem '%s' não pôde ser identificado." % self.caminho_arquivo)

    def finalizar_persistencia(self):
        try:
            DALImagem.commit()
        except BaseException as e:
            raise Exception("ERRO AO CONCLUIR PERSISTÊNCIA DA IMAGEM: %s" % e)

    def salvar(self, aguardar=False):

        if self.codigo > 0:
            try:
                DALImagem.update(
                        self.codigo, 
                        self.numero_bandas, 
                        self.data_coleta, 
                        self.tamanho_pixel_x, 
                        self.tamanho_pixel_y, 
                        self.unidade_celula_xy,
                        self.near_range, 
                        self.far_range, 
                        self.angulo_near, 
                        self.angulo_far, 
                        self.direcao_orbita, 
                        self.lado_imageamento, 
                        self.quantidade_looks, 
                        self.datum, 
                        self.projecao, 
                        self.quantidade_bits, 
                        self.id_cena, 
                        self.id_orbita, 
                        self.modo_imageamento, 
                        self.tipo_produto, 
                        self.extensao_arquivo, 
                        self.data_indexacao, 
                        self.caminho_arquivo, 
                        self.quantidade_colunas, 
                        self.quantidade_linhas, 
                        self.caminho_metadados, 
                        self.polar_hh, 
                        self.polar_hv, 
                        self.polar_vv, 
                        self.polar_vh, 
                        self.arquivado, 
                        self.plataforma.codigo, 
                        self.sensor.codigo,
                        self.srs,
                        self.caminho_arquivo_world,
                        self.servidor.codigo)
            except BaseException as e:
                raise Exception("ERRO AO ATUALIZAR IMAGEM: %s" % (e))

        else:
            try:
                codigo_retorno = DALImagem.insert(
                        self.numero_bandas, 
                        self.data_coleta, 
                        self.tamanho_pixel_x, 
                        self.tamanho_pixel_y, 
                        self.unidade_celula_xy,
                        self.near_range, 
                        self.far_range, 
                        self.angulo_near, 
                        self.angulo_far, 
                        self.direcao_orbita, 
                        self.lado_imageamento, 
                        self.quantidade_looks, 
                        self.datum, self.projecao, 
                        self.quantidade_bits, 
                        self.id_cena, 
                        self.id_orbita, 
                        self.modo_imageamento, 
                        self.tipo_produto, 
                        self.extensao_arquivo, 
                        self.data_indexacao, 
                        self.caminho_arquivo, 
                        self.quantidade_colunas, 
                        self.quantidade_linhas, 
                        self.caminho_metadados, 
                        self.polar_hh, 
                        self.polar_hv, 
                        self.polar_vv, 
                        self.polar_vh, 
                        self.arquivado, 
                        self.plataforma.codigo, 
                        self.sensor.codigo,
                        self.poligono_geometria,
                        self.srs,
                        self.SRID,
                        self.caminho_arquivo_world,
                        self.servidor.codigo,aguardar)
                if codigo_retorno > 0:
                    self.codigo = codigo_retorno
                else:
                    raise Exception("Não foi possível recuperar os dados da imagem inserida.")
            except BaseException as e:
                raise Exception("ERRO AO INSERIR IMAGEM: %s" % (e))


    def popula_objeto(self, dataset):
        if dataset is not None:
            self.codigo                 = dataset['co_seq_imagem']
            self.numero_bandas 		= dataset['qt_banda']
            self.data_coleta		= dataset['dt_coleta']
            self.quantidade_pixels_x 	= dataset['nu_tamanho_pixel_x']
            self.quantidade_pixels_y	= dataset['nu_tamanho_pixel_y']
            self.unidade_celula_xy      = dataset['no_unidade_celula_xy']
            self.near_range		= dataset['nu_near_range']
            self.far_range		= dataset['nu_far_range']
            self.angulo_near		= dataset['nu_angulo_near']
            self.angulo_far		= dataset['nu_angulo_far']
            self.direcao_orbita	  	= dataset['no_direcao_orbita']
            self.lado_imageamento	= dataset['no_lado_imageamento']
            self.quantidade_looks      	= dataset['qt_looks']
            self.datum           	= dataset['no_datum'].replace('\n','')
            self.projecao        	= dataset['no_projecao'].replace('\n','')
            self.quantidade_bits       	= dataset['qt_bits']
            self.id_cena         	= dataset['no_id_cena']
            self.id_orbita       	= dataset['no_id_orbita']
            self.modo_imageamento	= dataset['no_modo_imageamento']
            self.tipo_produto         	= dataset['tp_produto']
            self.tipo_arquivo		= dataset['tp_arquivo']
            self.data_indexacao       	= dataset['dt_indexacao']
            self.extensao_arquivo       = dataset['tp_extensao_arquivo']
            self.caminho_arquivo        = dataset['no_caminho_arquivo']
            self.quantidade_colunas     = dataset['qt_colunas']
            self.quantidade_linhas      = dataset['qt_linhas']
            self.caminho_metadados 	= dataset['no_caminho_metadados']
#           self.geometria          	= dataset['']
            self.imagem_arquivada       = dataset['st_arquivado']
            self.polar_hh              	= dataset['st_hh']
            self.polar_hv              	= dataset['st_hv']
            self.polar_vv              	= dataset['st_vv']
            self.polar_vh              	= dataset['st_vh']
	    self.area_km2		= dataset['nu_area_km2']

            self.arquivado              = dataset['st_arquivado']

            self.plataforma             = plataforma.Plataforma(codigo = dataset['co_plataforma'])
            self.sensor                 = sensor.Sensor(codigo = dataset['co_sensor'])
            self.srs                    = dataset['ds_srs']
            self.caminho_arquivo_world  = dataset['no_caminho_world']

    @staticmethod
    def listar_todas():
        lista_retorno = []

        dataset = DALFornecedor.select_all()

        for ds in dataset:
            f = Fornecedor()
            f.popula_objeto(ds)
            lista_retorno.append(f)

        return lista_retorno
