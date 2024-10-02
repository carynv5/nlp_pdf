# PDF Extraction Examples

This project provides a collection of Python scripts for extracting various types of content from PDF files, including text, tables, images, and geometric shapes.

## Features

- Text extraction
- Table extraction
- Image extraction
- Geometric shape extraction
- Colpali-based extraction
- Camelot[CV]

## Installation

1. Clone this repository:
   ```
   git clone git@github.com:carynv5/nlp_pdf.git
   cd nlp_pdf
   ```

2. Install the required dependencies:
   ```
   uv pip install -e .
   ```


## Set ENV variables

After cloning this project, you need to set up the correct paths in the `.env` file. Follow these steps:

1. Locate the `env.sample` file in the root directory of the project. Rename as `.env`.

2. Open the `.env` file in a text editor.

3. Find the `BASE_PATH` variable. It should look like this:

   ```
   BASE_PATH=/path/to/project
   ```

4. Replace `/path/to/project` with the absolute path to the directory where you cloned the project. For example:

   - On Linux or macOS: `BASE_PATH=/home/username/projects/your-project-name`
   - On Windows: `BASE_PATH=C:\Users\username\projects\your-project-name`

   Make sure to use forward slashes (`/`) even on Windows.

5. The other paths in the file should already be set up relative to `BASE_PATH`. They should look like this:

   ```
   PDF_PATH=${BASE_PATH}/pdf/B.08W9127N20B0017Plans.pdf
   PDF_DIR=${BASE_PATH}/pdf/
   OUTPUT_DIR=${BASE_PATH}/extracted
   ```

   If these paths are different in your project structure, adjust them accordingly.

6. Save the `.env` file.

7. Make sure the directories referenced in `PDF_DIR` and `OUTPUT_DIR` exist. If they don't, create them:

   ```
   mkdir -p pdf extracted
   ```

8. If the PDF file mentioned in `PDF_PATH` is not part of the repository, make sure to place it in the correct location (`pdf/B.08W9127N20B0017Plans.pdf` relative to your project root).

After completing these steps, your project should be correctly set up to use the paths specified in the `.env` file.

Note: Never commit your `.env` file to version control if it contains sensitive information. It's generally a good practice to add `.env` to your `.gitignore` file.


## Usage

Each extraction task has its own script that can be run independently:

- Extract text: `python -m pdf-extraction.text_extraction`
- Extract tables: `python -m pdf-extraction.table_extraction`
- Extract images: `python -m pdf-extraction.image_extraction`
- Extract geometric shapes: `python -m pdf-extraction.geometric_extraction`
- Extract using Colpali: `python -m pdf-extraction.colpali_extraction`
- Extract geospatial data: `python -m pdf-extraction.geo_extraction`

Before running the scripts, make sure to replace the placeholder PDF paths in each script with the path to your actual PDF file.

## Dependencies

This project relies on several Python libraries, including:

- PyPDF2
- opencv-python
- PyMuPDF
- colpali-engine
- geopandas
- rasterio
- Pillow
- pdf2image
- camelot-py

For a complete list of dependencies, see the `pyproject.toml` file.

## Contributing

Contributions to this project are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
