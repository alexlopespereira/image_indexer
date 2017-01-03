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

class DALImagem:

    conexao = gerenciador.Banco()

    def __init__(self):
        pass

    #métodos estáticos
    @staticmethod
    def insert(numero_bandas, data_coleta, tamanho_pixel_x, tamanho_pixel_y, unidade_celula_xy, near_range, far_range, angulo_near, angulo_far, direcao_orbita, lado_imageamento, quantidade_looks, datum, projecao, quantidade_bits, id_cena, id_orbita, modo_imageamento, tipo_produto, extensao_arquivo, data_indexacao, caminho_arquivo, quantidade_colunas, quantidade_linhas, caminho_metadados, polar_hh, polar_hv, polar_vv, polar_vh, arquivado, codigo_plataforma, codigo_sensor, poligono_geometria, srs, srid, caminho_arquivo_world, codigo_servidor, sem_commit=False):


	comando_dml = '''INSERT INTO indice_imagens.tb_imagem (
	        qt_banda, 
	        dt_coleta, 
	        nu_tamanho_pixel_x, 
	        nu_tamanho_pixel_y, 
            no_unidade_celula_xy,
	        nu_near_range, 
	        nu_far_range, 
	        nu_angulo_near, 
	        nu_angulo_far, 
	        no_direcao_orbita, 
	        no_lado_imageamento, 
	        qt_looks, 
	        no_datum, 
	        no_projecao, 
	        qt_bits, 
	        no_id_cena, 
	        no_id_orbita, 
	        no_modo_imageamento, 
	        tp_produto, 
	        tp_extensao_arquivo, 
	        dt_indexacao, 
	        no_caminho_arquivo, 
	        qt_colunas, 
	        qt_linhas, 
	        no_caminho_metadados, 
	        st_hh, 
	        st_hv, 
	        st_vv, 
	        st_vh, 
	        st_arquivado,
	        co_plataforma,
	        co_sensor,
	        geom,
		nu_area_km2,
	        ds_srs, no_caminho_world, co_servidor) 
	        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,ST_Transform(ST_GeomFromText(%s,%s),4674),ST_Area(ST_Transform(ST_Transform(ST_GeomFromText(%s,%s),4674),900914))/1000000,%s,%s,%s) 
		RETURNING co_seq_imagem''' 
        if not sem_commit:
            return DALImagem.conexao.executar_insert(comando_dml, [numero_bandas, data_coleta, tamanho_pixel_x, tamanho_pixel_y, unidade_celula_xy, near_range, far_range, angulo_near, angulo_far, direcao_orbita, lado_imageamento, quantidade_looks, datum, projecao, quantidade_bits, id_cena, id_orbita, modo_imageamento, tipo_produto, extensao_arquivo, data_indexacao, caminho_arquivo, quantidade_colunas, quantidade_linhas, caminho_metadados, polar_hh, polar_hv, polar_vv, polar_vh, arquivado, codigo_plataforma, codigo_sensor,'POLYGON((%s))' % poligono_geometria,srid,'POLYGON((%s))' % poligono_geometria, srid, srs, caminho_arquivo_world, codigo_servidor])
        else:
            DALImagem.conexao.preparar_transacao()
            return DALImagem.conexao.executar_insert_sem_commit(comando_dml, [numero_bandas, data_coleta, tamanho_pixel_x, tamanho_pixel_y, unidade_celula_xy, near_range, far_range, angulo_near, angulo_far, direcao_orbita, lado_imageamento, quantidade_looks, datum, projecao, quantidade_bits, id_cena, id_orbita, modo_imageamento, tipo_produto, extensao_arquivo, data_indexacao, caminho_arquivo, quantidade_colunas, quantidade_linhas, caminho_metadados, polar_hh, polar_hv, polar_vv, polar_vh, arquivado, codigo_plataforma, codigo_sensor,'POLYGON((%s))' % poligono_geometria,srid,'POLYGON((%s))' % poligono_geometria, srid, srs, caminho_arquivo_world, codigo_servidor])


    @staticmethod
    def update(codigo, numero_bandas, data_coleta, tamanho_pixel_x, tamanho_pixel_y, unidade_celula_xy, near_range, far_range, angulo_near, angulo_far, direcao_orbita, lado_imageamento, quantidade_looks, datum, projecao, quantidade_bits, id_cena, id_orbita, modo_imageamento, tipo_produto, extensao_arquivo, data_indexacao, caminho_arquivo, quantidade_colunas, quantidade_linhas, caminho_metadados, polar_hh, polar_hv, polar_vv, polar_vh, arquivado, codigo_plataforma, codigo_sensor, srs, caminho_arquivo_world, codigo_servidor):
        return DALImagem.conexao.executar_update('''UPDATE indice_imagens.tb_imagem 
        SET 
            qt_banda                = %s, 
            dt_coleta               = %s, 
            nu_tamanho_pixel_x      = %s, 
            nu_tamanho_pixel_y      = %s, 
            no_unidade_celula_xy    = %s,
            nu_near_range           = %s, 
            nu_far_range            = %s, 
            nu_angulo_near          = %s, 
            nu_angulo_far           = %s, 
            no_direcao_orbita       = %s, 
            no_lado_imageamento     = %s, 
            qt_looks                = %s, 
            no_datum                = %s, 
            no_projecao             = %s, 
            qt_bits                 = %s, 
            no_id_cena              = %s, 
            no_id_orbita            = %s, 
            no_modo_imageamento     = %s, 
            tp_produto              = %s, 
            tp_extensao_arquivo     = %s, 
            dt_indexacao            = %s, 
            no_caminho_arquivo      = %s, 
            qt_colunas              = %s, 
            qt_linhas               = %s, 
            no_caminho_metadados    = %s, 
            st_hh                   = %s, 
            st_hv                   = %s, 
            st_vv                   = %s, 
            st_vh                   = %s, 
            st_arquivado = %s, co_plataforma = %s, co_sensor = %s, srs = %s, no_caminho_world = %s, co_servidor = %s WHERE co_seq_imagem = %''', [numero_bandas, data_coleta, tamanho_pixel_x, tamanho_pixel_y, unidade_celula_xy, near_range, far_range, angulo_near, angulo_far, direcao_orbita, lado_imageamento, quantidade_looks, datum, projecao, quantidade_bits, id_cena, id_orbita, modo_imageamento, tipo_produto, extensao_arquivo, data_indexacao, caminho_arquivo, quantidade_colunas, quantidade_linhas, caminho_metadados, polar_hh, polar_hv, polar_vv, polar_vh, arquivado, codigo_plataforma, codigo_sensor, srs, caminho_arquivo_world, codigo_servidor, codigo])


    @staticmethod
    def commit():
        DALImagem.conexao.finalizar_transacao(True)

    @staticmethod
    def select_all():
        return DALImagem.conexao.consultar("SELECT * FROM indice_imagens.tb_imagem order by co_seq_imagem asc")
    @staticmethod
    def select(codigo):
	tupla = DALImagem.conexao.consultar("SELECT * FROM indice_imagens.tb_image WHERE  co_seq_imagem = %s", [codigo])
        if len(tupla) > 0:
            return tupla[0]
        else:
            return None

    def select(caminho_arquivo):
        tupla = DALImagem.conexao.consultar("SELECT co_seq_imagem FROM indice_imagens.tb_imagem where no_caminho_arquivo = %s", [caminho_arquivo]);
        if len(tupla) > 0:
            return tupla[0]
        else:
            return None