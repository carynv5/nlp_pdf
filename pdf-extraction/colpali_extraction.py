import os
import pprint
from typing import List, cast
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm
from PIL import Image
from dotenv import load_dotenv  # Add this import

from colpali_engine.models import ColPali
from colpali_engine.models.paligemma.colpali.processing_colpali import ColPaliProcessor
from colpali_engine.utils.processing_utils import BaseVisualRetrieverProcessor
from colpali_engine.utils.torch_utils import ListDataset, get_torch_device

from pdf2image import convert_from_path

load_dotenv()

def load_local_pdfs(pdf_dir: str) -> List[str]:
    """
    Load and convert local PDFs to image paths for processing.
    
    :param pdf_dir: Directory containing PDF files.
    :return: List of image file paths.
    """
    pdf_paths = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    image_paths = []

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    output_dir = os.getenv('OUTPUT_DIR')  # Get the output directory from environment variable
    output_path = os.path.join(output_dir, script_name)  # Define the output path using script name
    os.makedirs(output_path, exist_ok=True)

    for pdf_path in pdf_paths:
        images = convert_from_path(pdf_path, fmt='png')
        pdf_base_name = os.path.splitext(os.path.basename(pdf_path))[0]

        temp_image_dir = os.path.join(output_path, f"{pdf_base_name}_images")
        os.makedirs(temp_image_dir, exist_ok=True)

        for i, image in enumerate(images):
            image_file = os.path.join(temp_image_dir, f"{pdf_base_name}_page_{i + 1}.png")
            image.save(image_file, "PNG")
            image_paths.append(image_file)

    return image_paths


def main():
    """
    Example script to run inference with ColPali using local PDF files.
    """

    device = get_torch_device("auto")
    print(f"Device used: {device}")

    # Model name
    model_name = "vidore/colpali-v1.2"

    # Load model
    model = ColPali.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map=device,
    ).eval()

    # Load processor
    processor = cast(ColPaliProcessor, ColPaliProcessor.from_pretrained(model_name))

    if not isinstance(processor, BaseVisualRetrieverProcessor):
        raise ValueError("Processor should be a BaseVisualRetrieverProcessor")

    # Load local PDF files and convert them to images
    pdf_dir = os.getenv('PDF_DIR')
    image_paths = load_local_pdfs(pdf_dir)

    # Convert image paths to actual image objects before passing to processor
    images = [Image.open(image_path) for image_path in image_paths]

    # Define custom queries for the PDFs
    queries = ["What is the main topic of the document?", "Who is the author of the document?"]

    print("Selected queries:")
    pprint.pprint(queries)

    # Run inference - docs (images from local PDFs)
    dataloader = DataLoader(
        dataset=ListDataset[Image.Image](images),  # Update to pass PIL Image objects
        batch_size=4,
        shuffle=False,
        collate_fn=lambda x: processor.process_images(x),
    )
    ds: List[torch.Tensor] = []
    for batch_doc in tqdm(dataloader):
        with torch.no_grad():
            batch_doc = {k: v.to(model.device) for k, v in batch_doc.items()}
            embeddings_doc = model(**batch_doc)
        ds.extend(list(torch.unbind(embeddings_doc.to("cpu"))))

    # Run inference - queries
    dataloader = DataLoader(
        dataset=ListDataset[str](queries),
        batch_size=4,
        shuffle=False,
        collate_fn=lambda x: processor.process_queries(x),
    )

    qs: List[torch.Tensor] = []
    for batch_query in dataloader:
        with torch.no_grad():
            batch_query = {k: v.to(model.device) for k, v in batch_query.items()}
            embeddings_query = model(**batch_query)
        qs.extend(list(torch.unbind(embeddings_query.to("cpu"))))

    # Run scoring
    scores = processor.score(qs, ds).cpu().numpy()
    idx_top_1 = scores.argmax(axis=1)
    print("Indices of the top-1 retrieved documents for each query:", idx_top_1)

    return


if __name__ == "__main__":
    main()
