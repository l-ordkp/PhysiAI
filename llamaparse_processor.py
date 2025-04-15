from llama_parse import LlamaParse
class LlamaParseProcessor:
    def __init__(self, result_type="markdown", skip_diagonal_text=True, 
                 fast_mode=False, num_workers=9, check_interval=10, api_key=None):
        """
        Initialize LlamaParse processor with configuration parameters.
        """
        self.parser = LlamaParse(
            result_type=result_type,
            skip_diagonal_text=skip_diagonal_text,
            fast_mode=fast_mode,
            num_workers=num_workers,
            check_interval=check_interval,
            api_key=api_key
        )
    
    def get_json_result(self, pdf_path):
        """
        Parse a PDF file using LlamaParse and get JSON result.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            list: List of parsed JSON objects
        """
        return self.parser.get_json_result(pdf_path)