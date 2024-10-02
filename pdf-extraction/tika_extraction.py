import tika
from tika import parser
import os

# Initialize Tika
tika.initVM()

# Set up Tika to use Tesseract OCR
os.environ['TIKA_CONFIG'] = '/Users/carynv5/Documents/dev/nlp/pdf-extraction-examples/tika-config.xml'

def extract_pdf_content_with_ocr(pdf_path):
    # Parse the PDF with OCR enabled
    parsed = parser.from_file(pdf_path, xmlContent=True)
    
    # Extract content
    content = parsed["content"]
    
    # Extract metadata
    metadata = parsed["metadata"]
    
    return content, metadata

# Example usage
pdf_path = '/Users/carynv5/Documents/dev/nlp/pdf-extraction-examples/pdf/B.08W9127N20B0017Plans.pdf'
output_dir = '/Users/carynv5/Documents/dev/nlp/extracted/'

if os.path.exists(pdf_path):
    content, metadata = extract_pdf_content_with_ocr(pdf_path)
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Define output file paths
    base_name = os.path.basename(pdf_path)
    content_file_path = os.path.join(output_dir, f"{base_name}_content.txt")
    metadata_file_path = os.path.join(output_dir, f"{base_name}_metadata.txt")
    
    # Save content to file
    with open(content_file_path, 'w', encoding='utf-8') as content_file:
        content_file.write(content)
    
    # Save metadata to file
    with open(metadata_file_path, 'w', encoding='utf-8') as metadata_file:
        for key, value in metadata.items():
            metadata_file.write(f"{key}: {value}\n")
    
    print(f"Content and metadata saved to {output_dir}")
else:
    print(f"File not found: {pdf_path}")