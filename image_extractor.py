import os
import base64
import requests
from PIL import Image
import io

class ImageExtractor:
    def __init__(self, output_dir):
        """
        Initialize image extractor.
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def extract_images_from_page(self, page_data, pdf_file, page_num):
        """
        Extract images from a single page of parsed PDF data.
        
        Args:
            page_data (dict): Page data from LlamaParse JSON result
            pdf_file (str): Source PDF filename
            page_num (int): Page number
        """
        for i, image in enumerate(page_data.get('images', [])):
            try:
                if 'url' in image:
                    # Download image from URL
                    self._save_image_from_url(image['url'], pdf_file, page_num, i)
                elif 'data' in image:
                    # Handle base64 encoded images
                    self._save_image_from_base64(image['data'], pdf_file, page_num, i)
            except Exception as e:
                print(f"Error extracting image: {e}")
    
    # [Save methods remain the same]