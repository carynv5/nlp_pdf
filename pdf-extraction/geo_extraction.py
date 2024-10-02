from osgeo import gdal, ogr
import os
import json
from dotenv import load_dotenv

load_dotenv()

def extract_geometries(pdf_path):
    # Open the PDF file
    pdf = gdal.Open(pdf_path)
    
    # Check if the PDF has layers
    layer_count = pdf.GetLayerCount()
    
    geometries = []
    
    for i in range(layer_count):
        layer = pdf.GetLayer(i)
        layer_name = layer.GetName()
        feature = layer.GetNextFeature()
        
        while feature:
            geom = feature.GetGeometryRef()
            if geom:
                geom_type = geom.GetGeometryName()
                geom_wkt = geom.ExportToWkt()
                geometries.append({
                    'layer': layer_name,
                    'type': geom_type,
                    'wkt': geom_wkt
                })
            feature = layer.GetNextFeature()
    
    return geometries

# Usage
pdf_path = os.getenv('PDF_PATH')
extracted_geometries = extract_geometries(pdf_path)

# Save to file
script_name = os.path.splitext(os.path.basename(__file__))[0]
output_dir = os.getenv('OUTPUT_DIR')  # Get the output directory from environment variable
output_dir = os.path.join(output_dir, script_name)
output_path = os.path.join(output_dir, 'gdal_extracted_geometries.json')

with open(output_path, 'w') as f:
    json.dump(extracted_geometries, f, indent=2)

print(f"Extracted geometries saved to {output_path}")

# Optionally, save to a shapefile
shapefile_path = os.path.join(output_dir, 'extracted_geometries.shp')
driver = ogr.GetDriverByName("ESRI Shapefile")
data_source = driver.CreateDataSource(shapefile_path)
srs = ogr.osr.SpatialReference()
srs.ImportFromEPSG(4326)  # Assuming WGS84, adjust if necessary

layer = data_source.CreateLayer("geometries", srs, ogr.wkbUnknown)
layer.CreateField(ogr.FieldDefn("Layer", ogr.OFTString))
layer.CreateField(ogr.FieldDefn("Type", ogr.OFTString))

for geom in extracted_geometries:
    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField("Layer", geom['layer'])
    feature.SetField("Type", geom['type'])
    wkt_geom = ogr.CreateGeometryFromWkt(geom['wkt'])
    feature.SetGeometry(wkt_geom)
    layer.CreateFeature(feature)
    feature = None

data_source = None
print(f"Extracted geometries also saved as shapefile: {shapefile_path}")