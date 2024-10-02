from setuptools import setup, find_packages

setup(
    name="pdf-extraction-examples",
    version="0.1.0",
    description="A collection of PDF extraction examples using various libraries",
    author="Cary Greenwood",
    author_email="cary.greenwood@nv5.com",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "PyPDF2>=3.0.0",
        "opencv-python>=4.5.5",
        "PyMuPDF>=1.19.6",
        "colpali-engine>=0.3.1,<0.4.0",
        "geopandas>=0.10.0",
        "rasterio>=1.2.0",
        "Pillow>=8.0.0",
        "pdf2image==1.15.1",
        "camelot-py==0.9.0",
        "ipykernel>=6.0.0"
    ],
    extras_require={
        'dev': ["pytest>=7.1.2"]
    },
    entry_points={
        'console_scripts': [
            'extract-text = pdf_extraction.text_extraction:main',
            'extract-tables = pdf_extraction.table_extraction:main',
            'extract-images = pdf_extraction.image_extraction:main',
            'extract-geometric = pdf_extraction.geometric_extraction:main',
            'extract-colpali = pdf_extraction.colpali_extraction:main',
            'extract-geo = pdf_extraction.geo_extraction:main',
            'extract-camelot = pdf_extraction.camelot_extraction:main',
        ]
    }
)

