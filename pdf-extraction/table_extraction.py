import os
import camelot
from dotenv import load_dotenv

load_dotenv()

def extract_tables(pdf_path, output_prefix):
    tables = camelot.read_pdf(pdf_path)
    
    for i, table in enumerate(tables):
        output_path = f"{output_prefix}_{i+1}.csv"
        table.to_csv(output_path)
        print(f"Table {i+1} saved to {output_path}")

def main():
    pdf_path = os.getenv('PDF_PATH')
    output_dir = os.getenv('OUTPUT_DIR')
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    output_prefix = os.path.join(output_dir, script_name, "table")
    os.makedirs(os.path.dirname(output_prefix), exist_ok=True)
    extract_tables(pdf_path, output_prefix)

if __name__ == "__main__":
    main()