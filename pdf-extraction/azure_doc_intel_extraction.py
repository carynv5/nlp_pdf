import sys
import os
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from typing import List

load_dotenv()

module_dir = os.path.abspath(os.getenv('BASE_PATH'))
sys.path.append(module_dir)

from config import AzureConfig

def extract_tables_with_azure(pdf_path, endpoint, key):
    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    with open(pdf_path, "rb") as f:
        try:
            poller = client.begin_analyze_document("prebuilt-layout", document=f)
            result = poller.result()
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            return []

    tables = []
    for table in result.tables:
        tables.append(table)  # Collect table data
    return tables

def extract_geometry_with_azure(pdf_path, endpoint, key):
    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    with open(pdf_path, "rb") as f:
        try:
            poller = client.begin_analyze_document("prebuilt-layout", document=f)
            result = poller.result()
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            return []

    geometries = []
    for page in result.pages:
        for line in page.lines:
            # Collect line geometry
            line_geometry = {
                "type": "line",
                "content": line.content,
                "polygon": line.polygon,  # Assuming polygon is available
                "points": line.polygon  # Assuming points are part of the polygon
            }
            geometries.append(line_geometry)
        
        # Check if tables are part of the document elements
        if hasattr(page, 'tables'):
            for table in page.tables:
                for cell in table.cells:
                    # Collect cell geometry
                    cell_geometry = {
                        "type": "cell",
                        "content": cell.content,
                        "bounding_box": cell.bounding_box,
                        "polygon": cell.polygon,
                        "points": cell.polygon  # Assuming points are part of the polygon
                    }
                    geometries.append(cell_geometry)
    return geometries

def extract_text_with_azure(pdf_path, endpoint, key):
    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    with open(pdf_path, "rb") as f:
        try:
            poller = client.begin_analyze_document("prebuilt-layout", document=f)
            result = poller.result()
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            return []

    text_lines = []
    for page in result.pages:
        for line in page.lines:
            text_lines.append(line.content)  # Collect text data
    return text_lines

def extract_images_with_azure(pdf_path, endpoint, key):
    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    with open(pdf_path, "rb") as f:
        try:
            # Assuming 'custom-image-model' is your custom model ID
            poller = client.begin_analyze_document("custom-image-model", document=f)
            result = poller.result()
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            return []

    images = []
    for page in result.pages:
        for image in page.images:
            images.append(image)  # Collect image data
    return images

def save_results(output_dir, pdf_base_name, tables, geometries, text_lines, images):
    # Create a subfolder named after the script
    script_name = os.path.basename(__file__).replace('.py', '')
    subfolder_path = os.path.join(output_dir, script_name, pdf_base_name)
    os.makedirs(subfolder_path, exist_ok=True)

    # Save the outputs to files in the specific output directory
    with open(os.path.join(subfolder_path, f"{pdf_base_name}_tables.txt"), 'w') as f:
        f.write(f"Extracted {len(tables)} tables\n")
        for table in tables:
            f.write(str(table) + "\n")

    with open(os.path.join(subfolder_path, f"{pdf_base_name}_geometries.txt"), 'w') as f:
        f.write(f"Extracted {len(geometries)} geometries\n")
        for geometry in geometries:
            f.write(str(geometry) + "\n")

    with open(os.path.join(subfolder_path, f"{pdf_base_name}_text.txt"), 'w') as f:
        f.write(f"Extracted text lines:\n")
        for line in text_lines:
            f.write(line + "\n")

    with open(os.path.join(subfolder_path, f"{pdf_base_name}_images.txt"), 'w') as f:
        f.write(f"Extracted {len(images)} images\n")
        for image in images:
            f.write(str(image) + "\n")

def main():
    print("Checking PDF_DIR environment variable...")
    pdf_dir = os.getenv("PDF_DIR")
    if not pdf_dir:
        print("PDF_DIR environment variable is not set.")
        return

    print(f"Checking if PDF directory exists: {pdf_dir}")
    if not os.path.exists(pdf_dir):
        print(f"PDF directory does not exist: {pdf_dir}")
        return

    print("Listing PDF files in the directory...")
    pdf_files = os.listdir(pdf_dir)
    if not pdf_files:
        print("No PDF files found in the directory.")
        return

    print("PDF files found:", pdf_files)
    print("Retrieving Azure endpoint and key...")
    endpoint = AzureConfig.get_secret("NV5-DOC-INTEL-ENDPOINT")
    key = AzureConfig.get_secret("NV5-DOC-INTEL-KEY")
    if not endpoint or not key:
        print("Azure endpoint or key is not set.")
        return

    print("Azure endpoint and key retrieved successfully.")
    print("Filtering PDF files...")
    pdf_paths = [os.path.join(pdf_dir, f) for f in pdf_files if f.endswith('.pdf')]
    
    if not pdf_paths:
        print("No PDF files to process.")
        return

    # Get output directory from environment variable
    output_dir = os.getenv('OUTPUT_DIR')
    if not output_dir:
        print("OUTPUT_DIR environment variable is not set.")
        return

    print("Starting PDF processing...")
    for pdf_path in pdf_paths:
        print(f"Processing {pdf_path}...")
        tables = extract_tables_with_azure(pdf_path, endpoint, key)
        geometries = extract_geometry_with_azure(pdf_path, endpoint, key)
        text_lines = extract_text_with_azure(pdf_path, endpoint, key)
        images = extract_images_with_azure(pdf_path, endpoint, key)

        # Define the base name for each PDF
        pdf_base_name = os.path.splitext(os.path.basename(pdf_path))[0]

        # Save results using the save_results function
        save_results(output_dir, pdf_base_name, tables, geometries, text_lines, images)

        print(f"Extracted {len(tables)} tables, {len(geometries)} geometries, {len(images)} images, and text from {pdf_path}")

if __name__ == "__main__":
    main()