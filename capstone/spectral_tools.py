from sklearn import preprocessing
import rasterio
from rasterio.merge import merge
import numpy as np
import os
from affine import Affine
import pathlib

scaler1 = preprocessing.MinMaxScaler(feature_range=(0.0, 1.0))
scaler2 = preprocessing.MinMaxScaler(feature_range=(0, 255))

def normalized_difference(band_a, band_b):
    result = (band_a - band_b)/(band_a + band_b)
    return scaler2.fit_transform(result).astype("uint8")

def moisture_enhanced_index(coastal_aerosol, green, nir, swir1):
    result = ((green - nir)/(green + nir)) + ((green - swir1)/(green + swir1)) + ((coastal_aerosol - green)/(coastal_aerosol + green)) * 3
    return scaler2.fit_transform(result).astype("uint8")

def vigs_index(green, red, nir, swir1, swir2):
    result = ((green - red)/(green + red)) + ((nir - red)/(nir + red)) * 0.5 + ((nir - swir1)/(nir + swir1)) * 1.5 + ((nir - swir2)/(nir + swir2)) * 1.5
    return scaler2.fit_transform(result).astype("uint8")

def save_spectral_index(index, output, meta_out):
    # merge with a previuosly created tiff if exists
    if os.path.exists(output):
        mosaic(index, output, meta_out)

    else:
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
    print("region rectangle shape: ", B1.shape)

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

    if mission == "landsat":
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

def get_band_stack(bands, stack_list_string, project_directory):
    stack = []
    stack_list = stack_list_string.split(",")
    print(stack_list)
    for i in stack_list:
        i = i.replace(" ", "")
        print("band name: ", i)
        if len(i) < 3 or i == "B8A":
            print("band length: ", len(i))
            stack.append(bands[i])
        else:
            print("band length: ", len(i))
            for j in os.listdir(project_directory + '/media/output_images'):
                if j.endswith('.tif'):
                    print(j)
                    if i in j and "colored" not in j:
                        spectral_index = rasterio.open(project_directory + '/media/output_images/' + j).read(1)
                        spectral_index = np.ma.masked_values(spectral_index, 0)
                        stack.append(spectral_index)
    return stack

def mosaic(index, output, meta_out):
    tmp_output = output.split(".")[0] + "_backup.tif"
    index_output = rasterio.open(tmp_output, "w", driver = meta_out["driver"], height = meta_out["height"], width =  meta_out["width"], dtype = "uint8", count = 1, nodata = 0, crs = meta_out["crs"], transform = meta_out["transform"])
    index_output.write(index, 1)
    index_output.close()

    src1 = rasterio.open(output)
    src2= rasterio.open(tmp_output)

    src_files_to_mosaic = []
    src_files_to_mosaic.append(src1)
    src_files_to_mosaic.append(src2)

    mosaic, out_trans = merge(src_files_to_mosaic)
    src1=""
    src2=""
    src_files_to_mosaic=""
    rem_output = pathlib.Path(output)
    rem_output.unlink()
    index_output = rasterio.open(output, "w", driver = meta_out["driver"], height = mosaic[0].shape[0], width = mosaic[0].shape[1], dtype = "uint8", count = 1, nodata = 0, crs = meta_out["crs"], transform = out_trans)
    index_output.write(mosaic[0], 1)
    index_output.close()
    rem_tmp_output = pathlib.Path(tmp_output)
    rem_tmp_output.unlink()