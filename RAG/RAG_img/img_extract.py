import fitz  # PyMuPDF
import os

# Extract Images or Diagrams from PDF
def extract_images_from_pdf(pdf_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    pdf_document = fitz.open(pdf_path)
    image_paths = []
    
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        images = page.get_images(full=True)
        
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Save the image
            image_path = os.path.join(output_folder, f"page_{page_number + 1}_img_{img_index + 1}.{image_ext}")
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)
                image_paths.append(image_path)

    return image_paths

extract_images_from_pdf('C:\\Users\\Kshit\\Desktop\\PhysiAI\\NCERT-Class-10-Science.pdf', 'C:\\Users\\Kshit\\Desktop\\PhysiAI\\RAG\\RAG_img\\img')