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
    pdf_path = os.getenv('PDF_PATH')
    output_dir = os.getenv('OUTPUT_DIR')
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    output_path = os.path.join(output_dir, script_name, "text.txt")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    extract_text(pdf_path, output_path)

if __name__ == "__main__":
    main()