import rasterio
import gdal
import numpy as np


def leer_capa(fichero, capa=1):
    raster = rasterio.open(fichero)
    capa = raster.read(capa, masked=True)

    return capa


def calcular_dem(operacion, fichero_entrada, fichero_salida):
    gdal.DEMProcessing(fichero_salida, fichero_entrada, operacion)

flow = leer_capa('flowacc.tif')
mde = leer_capa('fill_mde.tif')

a = flow * 25

calcular_dem('aspect', 'fill_mde.tif', 'aspect.tif')

aspect = leer_capa('aspect.tif')

aspect_rad = aspect * np.pi / 180

aspect_sen = np.sin(aspect_rad)
aspect_cos = np.cos(aspect_rad)

aspect_sen_abs = np.abs(aspect_sen)
aspect_cos_abs = np.abs(aspect_cos)

b = 5 * (aspect_sen_abs + aspect_cos_abs)

a_e = a / b

calcular_dem('slope', 'fill_mde.tif', 'slope.tif')

slope = leer_capa('slope.tif')

slope_rad = slope * np.pi / 180
slope_sen = np.sin(slope_rad)

m = 0.4
n = 1

ls = (m + 1) * (a_e / 22.13)**m * (slope_sen / 0.0896)**n

mde = rasterio.open('fill_mde.tif')
profile = mde.profile

capa_ls = rasterio.open('capa_ls.tif', 'w', **profile)
capa_ls.write(ls, 1)
capa_ls.close()
