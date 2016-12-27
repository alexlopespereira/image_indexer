# coding=utf-8
'''
Metadata driver for Cosmo Skymed SAR
'''

#import base dataset modules
import __default__

# import other modules (use "_"  prefix to import privately)
import sys, os, re, glob, time, math, string
import datetime
from metageta import utilities, geometry, spatialreferences

try:
    from osgeo import gdal
    from osgeo import gdalconst
    from osgeo import osr
    from osgeo import ogr
except ImportError:
    import gdal
    import gdalconst
    import osr
    import ogr

gdal.AllRegister()

format_regex=[
        #padrão hdf5
        r'CSKS\d_[ACDEGMRSTW]*_[BU]_[IHPRSW2]*_[A-Z,0-9]*_[HVC][HVO]_[LR][AD]_[FS][FN]_\d*_\d*\.(h5)$',
]

class Dataset(__default__.Dataset):

    def __init__(self, f=None):
        #filelist e fileinfo já levantada pela super classe
        pass

    def __getmetadata__(self, f=None):

        if not f:f=self.fileinfo['filepath']

        if not self._gdaldataset:self._gdaldataset= geometry.OpenDataset(f)

        driver=self._gdaldataset.GetDriver().ShortName


        #Resgatando as informações do SLC
        metadataset = self._gdaldataset.GetMetadata()

        #metadados metageta
        self.metadata['filetype'] = driver+'/'+self._gdaldataset.GetDriver().LongName
        self.metadata['sensor'] = 'SAR'
        self.metadata['satellite'] = metadataset['Satellite_ID']
        imgdate = str(metadataset['Product_Generation_UTC'])
        self.metadata['imgdate'] = datetime.datetime.strptime(re.sub('\.\d{9}','',imgdate),"%Y-%m-%d %H:%M:%S")
        self.metadata['orbit'] = metadataset['Orbit_Number']
        self.metadata['mode'] = metadataset['Acquisition_Mode']

        #SLC Metadata
        if driver == 'HDF5':
 
            srs =  metadataset['Ellipsoid_Designator']
            projecao = metadataset['Projection_ID']
            polarizacao = metadataset['S01_Polarisation']
            direcao_orbita = metadataset['Orbit_Direction']
            tipo_produto = metadataset['Product_Type']
            lado_imageamento = metadataset['Look_Side']

            hdf5ds = self._gdaldataset.GetSubDatasets()

            ##listando os diretórios da estrutura HDF5
            datadir = [ds[0] for ds in hdf5ds]

            ##coletando metadados
            for dhdf5 in datadir:
                if dhdf5.split('/')[-1] == 'SBI':
                    data = geometry.OpenDataset(dhdf5)

                    self.metadata['cols'] = data.RasterXSize
                    self.metadata['rows'] = data.RasterYSize
                    self.metadata['nbands'] = data.RasterCount
                    angulo_near = metadataset['S01_SBI_Near_Incidence_Angle']
                    angulo_far = metadataset['S01_SBI_Far_Incidence_Angle']

                    geo_coord_bottom_left = str(metadataset['S01_SBI_Bottom_Left_Geodetic_Coordinates']).split(' ')
                    geo_coord_bottom_right = str(metadataset['S01_SBI_Bottom_Right_Geodetic_Coordinates']).split(' ')
                    geo_coord_top_left = str(metadataset['S01_SBI_Top_Left_Geodetic_Coordinates']).split(' ')
                    geo_coord_top_right = str(metadataset['S01_SBI_Top_Right_Geodetic_Coordinates']).split(' ')
                    
                    if srs == 'WGS84':
                        srid = 4326
                        datum = srs
                        srs = osr.SpatialReference()
                        srs.ImportFromEPSG(srid)
                        self.metadata['srs'] = srs.ExportToWkt()
                        #lon,lat
                        self.extent = [
                                [geo_coord_bottom_left[1],geo_coord_bottom_left[0]],
                                [geo_coord_bottom_right[1],geo_coord_bottom_right[0]],
                                [geo_coord_top_right[1],geo_coord_top_right[0]],
                                [geo_coord_top_left[1],geo_coord_top_left[0]], 
                                [geo_coord_bottom_left[1],geo_coord_bottom_left[0]] #adicionando o primeiro ponto para fechar a geometria
                                ]
                    
                    self.metadata['cellx'] = metadataset['S01_SBI_Line_Spacing']
                    self.metadata['celly'] = metadataset['S01_SBI_Column_Spacing']
                    unidade_celula = 'deg'

                    rb = data.GetRasterBand(1)

                    self.metadata['nbits'] = gdal.GetDataTypeSize(rb.DataType)


        #Este objeto deve ser populado em todos os drivers utilizados pela ferramenta de indexação
        #pois contém metadados adicionais que não estão presentes nos campos do metageta 
        #e segue a estrutura do objeto Imagem do indexador. Caso não haja dado de algum dos elementos
        #colocar apenas ''
        self.metadata['metadata'] = {'polarizacao':polarizacao, 'datum':datum, 'projecao':projecao, 'lado_imageamento':lado_imageamento, 'tipo_produto':tipo_produto, 'direcao_orbita':direcao_orbita, 'caminho_metadados':'', 'srid':srid, 'angulo_near':angulo_near, 'angulo_far':angulo_far, 'unidade_celula_xy':unidade_celula}
