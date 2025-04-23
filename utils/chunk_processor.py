import pandas as pd
from typing import List, Dict, Any
from utils.llamaparse_processor import LlamaParser


class DocumentProcessor:
    """
    Process documents into chunks for embedding and storage
    """

    def __init__(self, parser: LlamaParser = None):
        """
        Initialize document processor
        Args:
            parser: PDF parser instance
        """
        self.parser = parser or LlamaParser()

    def process_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Process PDF and extract text and table chunks
        Args:
            pdf_path (str): Path to PDF file
        Returns:
            List[Dict]: List of content chunks with metadata
        """
        parsed_content = self.parser.parse_pdf(pdf_path)
        return self._extract_chunks(parsed_content)

    def _extract_chunks(self, parsed_content: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract content chunks from parsed PDF
        Args:
            parsed_content (List[Dict]): Parsed PDF content from LlamaParse
        Returns:
            List[Dict]: List of content chunks (text and tables)
        """
        chunks = []

        for document in parsed_content:
            for page in document.get("pages", []):
                page_number = page.get("page", 0)

                # Text chunks
                text = page.get("text", "")
                text_chunks = self._chunk_text(text)
                for i, text_chunk in enumerate(text_chunks):
                    chunks.append({
                        "content_type": "text",
                        "content": text_chunk,
                        "page": page_number,
                        "chunk_id": f"page_{page_number}_text_{i+1}"
                    })

                # Table chunks
                for j, table in enumerate(page.get("tables", [])):
                    table_data = table.get("raw", "") if isinstance(table, dict) else str(table)
                    table_chunks = self._chunk_text(table_data)
                    for k, table_chunk in enumerate(table_chunks):
                        chunks.append({
                            "content_type": "table",
                            "content": table_chunk,
                            "page": page_number,
                            "chunk_id": f"page_{page_number}_table_{j+1}_chunk_{k+1}"
                        })

        return chunks

    def _chunk_text(self, text: str, max_chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Split text into chunks of specified size with overlap
        Args:
            text (str): Text to chunk
            max_chunk_size (int): Max length of each chunk
            overlap (int): Number of overlapping characters between chunks
        Returns:
            List[str]: List of text chunks
        """
        if not text.strip():
            return []

        chunks = []
        start = 0
        text_len = len(text)

        while start < text_len:
            end = min(start + max_chunk_size, text_len)

            # Try to split at better boundaries
            if end < text_len:
                paragraph_break = text.rfind('\n\n', start, end)
                sentence_break = text.rfind('. ', start, end)
                space_break = text.rfind(' ', start, end)

                if paragraph_break != -1 and paragraph_break > start + max_chunk_size / 2:
                    end = paragraph_break + 2
                elif sentence_break != -1 and sentence_break > start + max_chunk_size / 2:
                    end = sentence_break + 2
                elif space_break != -1:
                    end = space_break + 1

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            start = max(start + max_chunk_size - overlap, end)

        return chunks
