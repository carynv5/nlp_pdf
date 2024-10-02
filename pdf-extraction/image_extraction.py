import fitz
import os
from PIL import Image
import io
from dotenv import load_dotenv

load_dotenv() 

def extract_images(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    os.makedirs(output_folder, exist_ok=True)
    
    for i, page in enumerate(doc):
        image_list = page.get_images(full=True)
        # PDF only: Return a list of images referenced by the page. 
        # Wrapper for Document.get_page_images().
        # https://pymupdf.readthedocs.io/en/latest/page.html#Page.get_images
        for j, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Open the image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert CMYK images to RGB to avoid save error
            if image.mode == "CMYK":
                image = image.convert("RGB")

            # Save the image
            image_path = os.path.join(output_folder, f"image_page{i+1}_{j+1}.png")
            image.save(image_path)
            print(f"Image saved to {image_path}")

def main():
    pdf_path = os.getenv('PDF_PATH')
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    output_dir = os.getenv('OUTPUT_DIR')  # Get the output directory from environment variable
    output_path = os.path.join(output_dir, script_name)

    extract_images(pdf_path, output_path)

if __name__ == "__main__":
    main()