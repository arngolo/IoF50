from sklearn import preprocessing
import rasterio
import numpy as np


scaler1 = preprocessing.MinMaxScaler(feature_range=(0.0, 1.0))
scaler2 = preprocessing.MinMaxScaler(feature_range=(0, 255))

def normalized_difference(band_a, band_b):
    scaler1.fit_transform(band_a)
    scaler1.fit_transform(band_b)
    result = (band_a - band_b)/(band_a + band_b)
    return scaler2.fit_transform(result).astype("uint8")

def moisture_enhanced_index(coastal_aerosol, green, nir, swir1):
    scaler1.fit_transform(coastal_aerosol)
    scaler1.fit_transform(green)
    scaler1.fit_transform(nir)
    scaler1.fit_transform(swir1)
    result = ((green - nir)/(green + nir)) + ((green - swir1)/(green + swir1)) + ((coastal_aerosol - green)/(coastal_aerosol + green)) * 3
    return scaler2.fit_transform(result).astype("uint8")

def vigs_index(green, red, nir, swir1, swir2):
    scaler1.fit_transform(green)
    scaler1.fit_transform(red)
    scaler1.fit_transform(nir)
    scaler1.fit_transform(swir1)
    scaler1.fit_transform(swir2)
    result = ((green - red)/(green + red)) + ((nir - red)/(nir + red)) * 0.5 + ((nir - swir1)/(nir + swir1)) * 1.5 + ((nir - swir2)/(nir + swir2)) * 1.5
    return scaler2.fit_transform(result).astype("uint8")

def save_spectral_index(index, output, meta_out):
    index_output = rasterio.open(output, "w", driver = meta_out["driver"], height = meta_out["height"], width =  meta_out["width"], dtype = "uint8", count = 1, nodata = 0, crs = meta_out["crs"], transform = meta_out["transform"])
    index_output.write(index, 1)
    index_output.close()

def get_metadata(band_array,crs, affine_transform):

    meta = {'driver': 'GTiff',
          'dtype': 'uint8',
          'nodata': 0,
          'width': band_array.shape[1],
          'height': band_array.shape[0],
          'count': 1,
          'crs': crs,
          'transform': affine_transform}
    return meta

def get_bands(mission, band_arrays):
    bands = {}
    if mission == "landsat":
        coastal_aerosol = band_arrays.get("B1")
        coastal_aerosol = np.array(coastal_aerosol.getInfo())
        bands["coastal_aerosol"] = coastal_aerosol

        blue = band_arrays.get("B2")
        blue = np.array(blue.getInfo())
        bands["blue"] = blue

        green = band_arrays.get("B3")
        green = np.array(green.getInfo())
        bands["green"] = green

        red = band_arrays.get("B4")
        red = np.array(red.getInfo())
        bands["red"] = red

        nir = band_arrays.get("B5")
        nir = np.array(nir.getInfo())
        bands["nir"] = nir

        swir1 = band_arrays.get("B6")
        swir1 = np.array(swir1.getInfo())
        bands["swir1"] = swir1

        swir2 = band_arrays.get("B7")
        swir2 = np.array(swir2.getInfo())
        bands["swir2"] = swir2

        # pan = band_arrays.get("B8")
        # pan = np.array(pan.getInfo())
        # bands["pan"] = pan

        
        # clouds = band_arrays.get("B9")
        # clouds = np.array(clouds.getInfo())
        # bands["clouds"] = clouds

        
        # tir1= band_arrays.get("B10")
        # tir1 = np.array(tir1.getInfo())
        # bands["tir2"] = tir1

        
        # tir2 = band_arrays.get("B11")
        # tir2 = np.array(tir2.getInfo())
        # bands["tir2"] = tir2

    return bands
