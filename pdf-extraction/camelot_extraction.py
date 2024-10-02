import os
import camelot
import PyPDF2
from pdf2image import convert_from_path
import cv2
import numpy as np
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def extract_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_tables(pdf_path):
    tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
    return tables

def extract_images(pdf_path):
    pages = convert_from_path(pdf_path)
    images = []
    for i, page in enumerate(pages):
        open_cv_image = np.array(page) 
        open_cv_image = open_cv_image[:, :, ::-1].copy() 
        images.append(open_cv_image)
    return images

def process_images(images):
    processed_images = []
    for img in images:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
        if lines is not None:
            for rho, theta in lines[0]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        processed_images.append(img)
    return processed_images

def extract_pdf_info(pdf_path):
    print("Extracting text...")
    text = extract_text(pdf_path)
    print("Text extraction complete.")

    print("Extracting tables...")
    tables = extract_tables(pdf_path)
    print(f"Extracted {len(tables)} tables.")

    print("Extracting and processing images...")
    images = extract_images(pdf_path)
    processed_images = process_images(images)
    print(processed_images)
    print(f"Processed {len(processed_images)} images.")

    return {
        'text': text,
        'tables': tables,
        'processed_images': processed_images
    }

def save_results(output_dir, extracted_info):
    # Create a subfolder named after the script
    script_name = os.path.basename(__file__).replace('.py', '')
    subfolder_path = os.path.join(output_dir, script_name)
    os.makedirs(subfolder_path, exist_ok=True)

    # Save extracted text to a text file
    text_file_path = os.path.join(subfolder_path, f"extracted_text.csv")
    with open(text_file_path, 'w', encoding='utf-8') as f:
        f.write(extracted_info['text'])
    print(f"Extracted text saved to {text_file_path}")

    # Save extracted tables to CSV files
    for i, table in enumerate(extracted_info['tables']):
        table_file_path = os.path.join(subfolder_path, f'extracted_table_{i+1}.csv')
        table.df.to_csv(table_file_path, index=False)
        print(f"Extracted table {i+1} saved to {table_file_path}")

    # Save processed images to PNG files
    for i, img in enumerate(extracted_info['processed_images']):
        img_file_path = os.path.join(subfolder_path, f'processed_image_{i+1}.png')
        cv2.imwrite(img_file_path, img)
        print(f"Processed image {i+1} saved to {img_file_path}")

def main():
    # Get PDF path from environment variable
    pdf_path = os.getenv('PDF_PATH')
    if not pdf_path:
        raise ValueError("PDF_PATH environment variable not set")

    # Convert to absolute path and print it
    pdf_path = os.path.abspath(pdf_path)
    print(f"Using PDF path: {pdf_path}")

    extracted_info = extract_pdf_info(pdf_path)

    # Get output directory from environment variable
    output_dir = os.getenv('OUTPUT_DIR')
    if not output_dir:
        raise ValueError("OUTPUT_DIR environment variable not set")

    save_results(output_dir, extracted_info)

if __name__ == "__main__":
    main()
