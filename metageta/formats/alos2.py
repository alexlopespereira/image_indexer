# coding=utf-8

'''
Metadata driver for ALOS-2 PALSAR-2
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
'''
B[Format specifications}:

- http://www.eorc.jaxa.jp/ALOS-2/en/doc/fdata/PALSAR-2_xx_Format_GeoTIFF_E_r.pdf

'''
format_regex=[
	r'IMG-[HV][HV]-ALOS2\d{9}-\d{6}-[BDFHLRSUWV]*\d\.\d[GRUPMLAD]*\.(tif)$',
]

class Dataset(__default__.Dataset):
    
    def __init__(self, f=None):
        #filelist e fileinfo já levantada pela super classe
        pass
       

    def __getmetadata__(self, f=None):

        if not f:f=self.fileinfo['filepath']
        d=os.path.dirname(f)

	#Informações adicionais contidas no cabeçalho da imagem
        self._gdaldataset = geometry.OpenDataset(f)

	if self._gdaldataset:
            driver=self._gdaldataset.GetDriver().ShortName
            self.metadata['filetype'] = driver+'/'+self._gdaldataset.GetDriver().LongName
            self.metadata['cols'] = self._gdaldataset.RasterXSize
            self.metadata['rows'] = self._gdaldataset.RasterYSize
            self.metadata['nbands'] = self._gdaldataset.RasterCount
            self.metadata['srs'] = self._gdaldataset.GetProjection()

            geotransform = self._gdaldataset.GetGeoTransform()
            #if geotransform == (0, 1, 0, 0, 0, 1):
            #    if self._gdaldataset.GetGCPCount() > 0:
            #        gcps=self._gdaldataset.GetGCPs()
            #        geotransform=gdal.GCPsToGeoTransform(gcps)
            #        gcps=geometry.GeoTransformToGCPs(geotransform,self.metadata['cols'],self.metadata['rows']) #Just get the 4 corner GCP's
            #    else:
            #        raise NotImplementedError, 'Dataset is not georeferenced'
            #else:
            #    gcps=geometry.GeoTransformToGCPs(geotransform,self.metadata['cols'],self.metadata['rows'])

            #ext=[[gcp.GCPX, gcp.GCPY] for gcp in gcps]
            #ext.append([gcps[0].GCPX, gcps[0].GCPY])#Add the 1st point to close the polygon)
            #self.extent=ext
            
            srs=osr.SpatialReference()
            srs.ImportFromWkt(self.metadata['srs'])
            
            srid = srs.GetAuthorityCode('GEOGCS')
            datum = srs.GetAttrValue('geogcs')
            projecao = srs.GetAttrValue('projection') 
            unidade_celula_xy = srs.GetAttrValue('UNIT')
            
            #também é possível extrair estes dados de pixel spacing do campo Pds_PixelSpacing do metadados (summary.txt)
            self.metadata['cellx'],self.metadata['celly']=geometry.CellSize(geotransform)
            

            rb=self._gdaldataset.GetRasterBand(1)
            if rb:
                self.metadata['datatype']=gdal.GetDataTypeName(rb.DataType)
                self.metadata['nbits']=gdal.GetDataTypeSize(rb.DataType)
                nodata=rb.GetNoDataValue()
                if nodata is not None:self.metadata['nodata']=str(nodata)
                else:
                    ct = rb.GetColorTable() #Fix for Issue 31
                    if ct is None:
                        if self.metadata['datatype'][0:4] in ['Byte','UInt']: nodata=0       #Unsigned, assume 0
                        else:nodata=-2**(self.metadata['nbits']-1)                           #Signed, assume min value in data range
                        self.metadata['nodata']=str(nodata)
                        #Fix for Issue 17
                        for i in range(1,self._gdaldataset.RasterCount+1):
                            self._gdaldataset.GetRasterBand(i).SetNoDataValue(nodata)
            else:raise IOError,'No valid rasterbands found.'



            #informações adicionais contidas no arquivo sumário do dataset
            summary_file = "%s/summary.txt" % d
            
        if os.path.exists(summary_file):  

            #formatando a lista de dados
            summary_list = []
            summary_list = open(summary_file).read().replace('"','').split('\n')
            if summary_list[len(summary_list)-1] =='':summary_list.pop(len(summary_list)-1)
            summary_list = dict(s.split('=') for s in summary_list)

            self.metadata['sensor'] = summary_list['Lbi_Sensor']
            self.metadata['satellite'] = summary_list['Lbi_Satellite']
            self.metadata['sceneid'] = summary_list['Scs_SceneID']
            tipo_produto = summary_list['Pds_ProductID']
            self.metadata['imgdate'] = datetime.datetime.strptime(summary_list['Lbi_ObservationDate'],"%Y%m%d")

            self.extent = [
                [summary_list['Img_FrameSceneLeftBottomLongitude'],summary_list['Img_FrameSceneLeftBottomLatitude']],
                [summary_list['Img_FrameSceneRightBottomLongitude'],summary_list['Img_FrameSceneRightBottomLatitude']],
                [summary_list['Img_FrameSceneRightTopLongitude'],summary_list['Img_FrameSceneRightTopLatitude']],
                [summary_list['Img_FrameSceneLeftTopLongitude'],summary_list['Img_FrameSceneLeftTopLatitude']],
                [summary_list['Img_FrameSceneLeftBottomLongitude'],summary_list['Img_FrameSceneLeftBottomLatitude']] #adicionando o primeiro ponto para fechar a geometria
            ]


            
            #Este objeto deve ser populado em todos os drivers utilizados pela ferramenta de indexação
            #pois contém metadados adicionais que não estão presentes nos campos 
            #do metageta e segue a estrutura do objeto Imagem do indexador. Caso não haja dado de algum 
            #dos elementos colocar apenas ''
            polarizacao =  self._gdaldataset.GetMetadata()['TIFFTAG_IMAGEDESCRIPTION']
            self.metadata['metadata'] = {'polarizacao':polarizacao, 'datum':datum, 'projecao':projecao, 'lado_imageamento':'', 'tipo_produto':tipo_produto, 'direcao_orbita':'', 'caminho_metadados':summary_file, 'srid':srid, 'angulo_near':'', 'angulo_far':'', 'unidade_celula_xy':unidade_celula_xy}
