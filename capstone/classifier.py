import numpy as np
import rasterio
from rasterio.merge import merge
import pandas as pd
import time
import pqkmeans
from sklearn.cluster import KMeans
import os
from .spectral_tools import mosaic

def PQKMeansGen(bands_array, output, k, num_subdim, Ks, sample_size, metadata):
    print(metadata)
    tstart=time.perf_counter()
    print(f"{tstart/60} min")

    num_bands = len(bands_array)
    bands={}
    for i in range(num_bands): 
        band = np.ma.masked_values(bands_array[i], 0)

        ###Based on previous failures, the author recommends to use arrays instead of data from pandas in order to have (input values, ndimension):
        bands["band_" + str(i+1)] = band[band==band] 

    #for calculations using algorithms we have to drop NaN values. previous step!!!!
    t2=time.perf_counter()
    print(f"Bands into dictionary finished in {t2/60 - tstart/60} min")

    data = pd.DataFrame.from_dict(bands)
    t3=time.perf_counter()
    print(f"Bands into dataframe finished in {t3/60 - t2/60} min")
    data2= data.dropna()

    X = np.asarray((data2[list(data)]))
    print(f"Number of bytes: {X.nbytes} ({X.nbytes/1000000000} Gb)")
    print(f"Array shape: (n of pixels per band, n of bands){X.shape}")
    ####Train the encoder!!!
    ####Because we have 12 bands (12D input), our num_subdim or M has to be multiple of the input dimension:
    encoder_start_time=time.perf_counter()
    print("Encoding.....")
    encoder = pqkmeans.encoder.PQEncoder(num_subdim=num_subdim, Ks=Ks)
    encoder.fit(X[:sample_size])
    X_pqcode = encoder.transform(X)
    encoder_end_time=time.perf_counter()
    print(f"Finished encoding in {encoder_end_time/60 - encoder_start_time/60} min")
    print(f"Pqcode shape: {X_pqcode.shape}")


    ####As can be seen, the reconstructed vectors are similar to the original one.
    ###It allows you to compress input vectors to PQ-codes, and store the PQ-codes only (X2_pqcode) In a large-scale data processing scenario
    np.save("pqcode.npy", X_pqcode)
    ####Clustering
    clustering_start_time=time.perf_counter()
    pqkmean = pqkmeans.clustering.PQKMeans(encoder=encoder, k=k)
    Labels = pqkmean.fit_predict(X_pqcode)
    clustering_end_time=time.perf_counter()
    print(f"Finished clustering in {clustering_end_time/60 - clustering_start_time/60} min")

    #the array of the KMeans result does not contain the NaN values, so it is impossible to reshape to its original shape(raster). the nextstep is to find a way to add the Nan values (then nodata) to the labels. Maybe a for loop!!!
    print("Writing clustering result into image.....")
    writing_start=time.perf_counter()

    Z= pd.DataFrame({"Labels":Labels})
    Z_Reindexed = Z.set_index(data2.index)
    data["Label"] = Z_Reindexed["Labels"]
    Result = pd.to_numeric(data["Label"], downcast = "float" )
    im = Result.values + 1
    im = im.astype(metadata["dtype"])
    im = np.reshape(im, (band.shape[0],  band.shape[1] ))
    ##### After, Save

    # merge with a previuosly created tiff if exists
    if os.path.exists(output):
        mosaic(im, output, metadata)
    else:
        PQKMean_output = rasterio.open(output, "w", driver = metadata["driver"], height =  metadata["height"], width =  metadata["width"], dtype =  metadata["dtype"], count = metadata["count"], nodata = metadata["nodata"], crs = metadata["crs"], transform =  metadata["transform"])
        PQKMean_output.write(im, 1)
        PQKMean_output.close()
        writing_end=time.perf_counter()
    print(f"Finished writing clustering in {writing_end/60 - writing_start/60} min")
    print(f"Total pqkmeans time: {clustering_end_time/60 - encoder_start_time/60} min")
    print(f"Total processing time: {writing_end/60 - tstart/60} min")

def KMeansGen(bands_array, output, k, metadata):
    print(metadata)
    tstart=time.perf_counter()
    print(f"{tstart/60} min")

    num_bands = len(bands_array)
    bands={}
    for i in range(num_bands): 
        band = np.ma.masked_values(bands_array[i], 0)

        ###Based on previous failures, the author recommends to use arrays instead of data from pandas in order to have (input values, ndimension):
        bands["band_" + str(i+1)] = band[band==band] 

    #for calculations using algorithms we have to drop NaN values. previous step!!!!
    t2=time.perf_counter()
    print(f"Bands into dictionary finished in {t2/60 - tstart/60} min")

    data = pd.DataFrame.from_dict(bands)
    t3=time.perf_counter()
    print(f"Bands into dataframe finished in {t3/60 - t2/60} min")
    data2= data.dropna()

    X = np.asarray((data2[list(data)]))
    print(f"Number of bytes: {X.nbytes} ({X.nbytes/1000000000} Gb)")
    print(f"Array shape: (n of pixels per band, n of bands){X.shape}")

    clustering_start_time=time.perf_counter()
    kmeans= KMeans(n_clusters =k, random_state =0)
    Labels = kmeans.fit(X)
    clustering_end_time=time.perf_counter()
    print(f"Finished clustering in {clustering_end_time/60 - clustering_start_time/60} min")

    #the array of the KMeans result does not contain the NaN values, so it is impossible to reshape to its original shape(raster). the nextstep is to find a way to add the Nan values (then nodata) to the labels. Maybe a for loop!!!
    print("Writing clustering result into image.....")
    writing_start=time.perf_counter()

    Z= pd.DataFrame({"Labels":Labels.labels_})
    Z_Reindexed = Z.set_index(data2.index)
    data["Label"] = Z_Reindexed["Labels"]
    Result = pd.to_numeric(data["Label"], downcast = "float" )
    im = Result.values + 1
    im = im.astype(metadata["dtype"])
    im = np.reshape(im, (band.shape[0],  band.shape[1] ))
    ##### After, Save

    # merge with a previuosly created tiff if exists
    if os.path.exists(output):
        mosaic(im, output, metadata)
    else:
        KMean_output = rasterio.open(output, "w", driver = metadata["driver"], height =  metadata["height"], width =  metadata["width"], dtype =  metadata["dtype"], count = metadata["count"], nodata = metadata["nodata"], crs = metadata["crs"], transform =  metadata["transform"])
        KMean_output.write(im, 1)
        KMean_output.close()
        writing_end=time.perf_counter()
        print(f"Finished writing clustering in {writing_end/60 - writing_start/60} min")
        print(f"Total kmeans time: {clustering_end_time/60 - clustering_start_time/60} min")
        print(f"Total processing time: {writing_end/60 - tstart/60} min")