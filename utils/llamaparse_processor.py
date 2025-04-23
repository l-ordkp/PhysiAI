import os
from typing import Dict, Any
from dotenv import load_dotenv
from llama_parse import LlamaParse
load_dotenv()

class LlamaParser:
    """
    PDF parser using the LlamaParse API
    """
    def __init__(self, api_key: str = None):
        """
        Initialize LlamaParse client
        Args:
            api_key (str): LlamaParse API key
        """
        self.api_key = api_key
        self.parser = LlamaParse(
        result_type="markdown",  # Specify the result format
        skip_diagonal_text=True,  # Skip diagonal text in the PDFs
        fast_mode=False,  # Use normal mode for parsing
        num_workers=9,  # Number of workers for parallel processing
        check_interval=10,  # Check interval for processing
        api_key=self.api_key  # API key for LlamaParse
)

    
    def parse_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Parse PDF using LlamaParse API
        Args:
            pdf_path (str): Path to PDF file
        Returns:
            Dict: Parsed PDF content with text, tables, and structure
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")         
        return self.parser.get_json_result(pdf_path)