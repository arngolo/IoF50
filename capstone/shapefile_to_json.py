import shapefile
def shp_to_json(SHP):
   # read the shapefile
    reader = shapefile.Reader(SHP, encoding = "ISO8859-1")
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    json = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        json.append(dict(type="Feature", geometry=geom, properties=atr)) 
        return json[0]
