def test_imports():
    modules = [
        'PyPDF2',
        'cv2',
        'fitz',  # PyMuPDF
        'colpali_engine',
        'geopandas',
        'rasterio',
        'PIL',
        'pdf2image',
        'camelot'  # New import for Camelot
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"Successfully imported {module}")
        except ImportError as e:
            print(f"Failed to import {module}: {str(e)}")

if __name__ == "__main__":
    test_imports()
