import os
from llama_parse import LlamaParse
from dotenv import load_dotenv
load_dotenv()


class LlamaParseProcessor:
    def __init__(self, result_type="markdown", skip_diagonal_text=True, 
                 fast_mode=False, num_workers=9, check_interval=10, api_key=None):
        """
        Initialize LlamaParse processor with configuration parameters.
        
        Args:
            result_type (str): Format of the parsed result
            skip_diagonal_text (bool): Whether to skip diagonal text in PDFs
            fast_mode (bool): Whether to use fast mode for parsing
            num_workers (int): Number of workers for parallel processing
            check_interval (int): Check interval for processing
            api_key (str): API key for LlamaParse
        """
        self.parser = LlamaParse(
            result_type=result_type,
            skip_diagonal_text=skip_diagonal_text,
            fast_mode=fast_mode,
            num_workers=num_workers,
            check_interval=check_interval,
            api_key=api_key
        )
    
    def parse(self, pdf_path):
        """
        Parse a PDF file using LlamaParse.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            dict: Parsed result containing pages, tables, and images
        """
        return self.parser.parse(pdf_path)