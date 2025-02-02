import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain.vectorstores import FAISS
import os
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFToFAISSProcessor:
    def __init__(
        self,
        google_api_key: str = None,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        print(self.google_api_key)
        if not self.google_api_key:
            raise ValueError("Google API key not found")
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize components
        self.initialize_components()

    def initialize_components(self):
        """Initialize all required components with proper configuration"""
        try:
            # Initialize text splitter
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
            
            # Initialize embeddings model
            self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            
            logger.info("All components initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize components: {str(e)}")
            raise

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF with proper error handling"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise

    def process_document(self, pdf_path: str, faiss_index_path: str = "faiss_index"):
        """Process PDF document and create a FAISS index"""
        try:
            # Extract text
            logger.info(f"Processing PDF: {pdf_path}")
            text = self.extract_text_from_pdf(pdf_path)
            
            # Split into chunks
            text_chunks = self.text_splitter.split_text(text)
            chunks = [Document(page_content=chunk) for chunk in text_chunks]
            logger.info(f"Created {len(chunks)} text chunks")
            
            # Generate embeddings and create FAISS index
            logger.info("Creating FAISS index...")
            faiss_index = FAISS.from_documents(chunks, self.embeddings)
            
            # Save the FAISS index to disk
            faiss_index.save_local(faiss_index_path)
            logger.info(f"FAISS index saved to {faiss_index_path}")
            
            logger.info("Document processing completed successfully")
            
        except Exception as e:
            logger.error(f"Error in document processing: {str(e)}")
            raise

def main():
    try:
        # Initialize processor
        processor = PDFToFAISSProcessor()
        
        # Process PDF and create FAISS index
        pdf_path = "C:\\Users\\Kshitij Kumar Pal\\Desktop\\PhysiAI\\iesc111.pdf"  # Your PDF path
        faiss_index_path = "C:\\Users\\Kshitij Kumar Pal\\Desktop\\PhysiAI\\text_db"  # Path to save the FAISS index
        processor.process_document(pdf_path, faiss_index_path)
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main()