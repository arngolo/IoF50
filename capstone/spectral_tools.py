from sklearn import preprocessing
import rasterio
import numpy as np


scaler1 = preprocessing.MinMaxScaler(feature_range=(0.0, 1.0))
scaler2 = preprocessing.MinMaxScaler(feature_range=(0, 255))

def normalized_difference(band_a, band_b):
    # scaler1.fit_transform(band_a)
    # scaler1.fit_transform(band_b)
    result = (band_a - band_b)/(band_a + band_b)
    return scaler2.fit_transform(result).astype("uint8")

def moisture_enhanced_index(coastal_aerosol, green, nir, swir1):
    # scaler1.fit_transform(coastal_aerosol)
    # scaler1.fit_transform(green)
    # scaler1.fit_transform(nir)
    # scaler1.fit_transform(swir1)
    result = ((green - nir)/(green + nir)) + ((green - swir1)/(green + swir1)) + ((coastal_aerosol - green)/(coastal_aerosol + green)) * 3
    return scaler2.fit_transform(result).astype("uint8")

def vigs_index(green, red, nir, swir1, swir2):
    # scaler1.fit_transform(green)
    # scaler1.fit_transform(red)
    # scaler1.fit_transform(nir)
    # scaler1.fit_transform(swir1)
    # scaler1.fit_transform(swir2)
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

def get_bands(mission, band_arrays, spectral_index_equation = None):
    bands = {}
    B1 = band_arrays.get("B1")
    B1 = np.array(B1.getInfo())
    scaler1.fit_transform(B1)
    bands["B1"] = B1

    B2 = band_arrays.get("B2")
    B2 = np.array(B2.getInfo())
    scaler1.fit_transform(B2)
    bands["B2"] = B2

    B3 = band_arrays.get("B3")
    B3 = np.array(B3.getInfo())
    scaler1.fit_transform(B3)
    bands["B3"] = B3

    B4 = band_arrays.get("B4")
    B4 = np.array(B4.getInfo())
    scaler1.fit_transform(B4)
    bands["B4"] = B4

    B5 = band_arrays.get("B5")
    B5 = np.array(B5.getInfo())
    scaler1.fit_transform(B5)
    bands["B5"] = B5

    B6 = band_arrays.get("B6")
    B6 = np.array(B6.getInfo())
    scaler1.fit_transform(B6)
    bands["B6"] = B6

    B7 = band_arrays.get("B7")
    B7 = np.array(B7.getInfo())
    scaler1.fit_transform(B7)
    bands["B7"] = B7

    B8 = band_arrays.get("B8")
    B8 = np.array(B8.getInfo())
    scaler1.fit_transform(B8)
    bands["B8"] = B8

    if mission == "sentinel":
        B8A = band_arrays.get("B8A")
        B8A = np.array(B8A.getInfo())
        scaler1.fit_transform(B8A)
        bands["B8A"] = B8A

    B9 = band_arrays.get("B9")
    B9 = np.array(B9.getInfo())
    scaler1.fit_transform(B9)
    bands["B9"] = B9

    B10 = band_arrays.get("B10")
    B10 = np.array(B10.getInfo())
    scaler1.fit_transform(B10)
    bands["B10"] = B10

    B11 = band_arrays.get("B11")
    B11 = np.array(B11.getInfo())
    scaler1.fit_transform(B11)
    bands["B11"] = B11

    if mission == "sentinel":
        B12 = band_arrays.get("B12")
        B12 = np.array(B12.getInfo())
        scaler1.fit_transform(B12)
        bands["B12"] = B12

    # return spectral index
    if spectral_index_equation:
        print(spectral_index_equation)
        spectral_index = eval(spectral_index_equation)
        return scaler2.fit_transform(spectral_index).astype("uint8")

    return bands
