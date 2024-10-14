import fitz  # PyMuPDF
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def extract_text(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"Text extracted and saved to {output_path}")

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