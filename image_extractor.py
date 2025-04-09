import os
import base64
import requests
from PIL import Image
import io

class ImageExtractor:
    def __init__(self, output_dir):
        """
        Initialize image extractor.
        
        Args:
            output_dir (str): Directory to save extracted images
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def extract_images(self, parse_result, pdf_file):
        """
        Extract images from parsed PDF result.
        
        Args:
            parse_result (dict): Parsed result from LlamaParse
            pdf_file (str): Source PDF filename
        """
        for page_num, page in enumerate(parse_result['pages'], 1):
            for i, image in enumerate(page.get('images', [])):
                try:
                    if 'url' in image:
                        # Download image from URL
                        self._save_image_from_url(image['url'], pdf_file, page_num, i)
                    elif 'data' in image:
                        # Handle base64 encoded images
                        self._save_image_from_base64(image['data'], pdf_file, page_num, i)
                except Exception as e:
                    print(f"Error extracting image: {e}")
    
    def _save_image_from_url(self, url, pdf_file, page_num, image_num):
        """
        Download and save image from URL.
        
        Args:
            url (str): Image URL
            pdf_file (str): Source PDF filename
            page_num (int): Page number
            image_num (int): Image number on the page
        """
        response = requests.get(url)
        img = Image.open(io.BytesIO(response.content))
        img_filename = f"{os.path.splitext(pdf_file)[0]}_page{page_num}_img{image_num}.png"
        img_path = os.path.join(self.output_dir, img_filename)
        img.save(img_path)
    
    def _save_image_from_base64(self, base64_data, pdf_file, page_num, image_num):
        """
        Save image from base64 data.
        
        Args:
            base64_data (str): Base64 encoded image data
            pdf_file (str): Source PDF filename
            page_num (int): Page number
            image_num (int): Image number on the page
        """
        img_data = base64.b64decode(base64_data)
        img = Image.open(io.BytesIO(img_data))
        img_filename = f"{os.path.splitext(pdf_file)[0]}_page{page_num}_img{image_num}.png"
        img_path = os.path.join(self.output_dir, img_filename)
        img.save(img_path)