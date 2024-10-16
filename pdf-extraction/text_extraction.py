import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import logging

load_dotenv()

# Configure logging
logging.basicConfig(filename='extraction.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def extract_text(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    # If no text is extracted, or if you want to ensure OCR is applied
    if not text.strip():
        text = ocr_pdf(pdf_path)
    
    # Split the text into lines
    lines = text.splitlines()
    
    # Iterate over lines to find the word "datum", "atum", or "oatum" (case-insensitive)
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in ["datum", "atum", "oatum"]):
            # Log 5 lines before, the line with the keyword, and the next 10 lines
            start_index = max(i - 5, 0)
            end_index = min(i + 11, len(lines))
            for j in range(start_index, end_index):
                if j == i:
                    # Make the line with the keyword bold
                    logging.info(f"**Line {j}: {lines[j]}**")
                else:
                    logging.info(f"Line {j}: {lines[j]}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    logging.info(f"Text extracted and saved to {output_path}")

def ocr_pdf(pdf_path):
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    
    # Perform OCR on each image
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    
    return text

def main():
    pdf_dir = os.getenv('PDF_DIR')
    output_dir = os.getenv('OUTPUT_DIR')
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    
    # List all PDF files in the specified directory
    pdf_paths = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    
    for pdf_path in pdf_paths:
        pdf_base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = os.path.join(output_dir, script_name, f"{pdf_base_name}_text.txt")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        extract_text(pdf_path, output_path)

if __name__ == "__main__":
    main()