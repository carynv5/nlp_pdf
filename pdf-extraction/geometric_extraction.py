import fitz
import json
import os
from dotenv import load_dotenv

load_dotenv()

def extract_geometric(pdf_path):
    doc = fitz.open(pdf_path)
    geometric_data = []
    for page_num, page in enumerate(doc):
        paths = page.get_drawings()
        # Return the vector graphics of the page. These are instructions which draw lines, 
        # rectangles, quadruples or curves, including properties like colors, transparency, 
        # line width and dashing, etc. Alternative terms are “line art” and “drawings”.
        for path in paths:
            if path['type'] == 'l':  # line
                geometric_data.append({'page': page_num, 'type': 'line', 'data': path['items']})
            elif path['type'] == 'c':  # curve
                geometric_data.append({'page': page_num, 'type': 'curve', 'data': path['items']})
            # Add more types as needed
    return geometric_data

def main():
    pdf_path = os.getenv('PDF_PATH')
    geometric_data = extract_geometric(pdf_path)

    # Use environment variable for output directory
    output_dir = os.getenv('OUTPUT_DIR')
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    output_path = os.path.join(output_dir, script_name, 'geometric_data.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(geometric_data, f, indent=2)

    print(f"Geometric data saved to {output_path}")

if __name__ == "__main__":
    main()