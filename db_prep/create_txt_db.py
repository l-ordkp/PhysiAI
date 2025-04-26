import os
from utils.chunk_processor import DocumentProcessor
from utils.generate_questions import QuestionGenerator
from utils.vector_store import VectorStore
from dotenv import load_dotenv
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
document_processor = DocumentProcessor()
question_generator = QuestionGenerator(gemini_api_key)
vector_store = VectorStore()
        
def process_pdf(pdf_path: str) -> None:
    """
        Process PDF and store in vector database
        Args:
        pdf_path (str): Path to PDF file
        """
    # Step 1: Extract content from PDF
    print(f"Processing PDF: {pdf_path}")
    chunks = document_processor.process_pdf(pdf_path)
    print(f"Extracted {len(chunks)} chunks (text and tables)")
                        
    # Step 2: Generate questions for each chunk
    chunks_with_questions = []
    print("Generating questions for each chunk...")
    for chunk in enumerate(chunks):
        questions = question_generator.generate_questions(chunk)
        chunk_with_questions = chunk.copy()
        chunk_with_questions["questions"] = questions
        chunks_with_questions.append(chunk_with_questions)

        print(f"Generated questions for {chunk['chunk_id']}: {questions}")
                    
    # Step 3: Store in Pinecone
    print("Storing chunks with questions in Pinecone...")
    vector_store.store_chunks_with_questions(chunks_with_questions)
        
process_pdf("/Users/kshitijpal/Desktop/PhysiAI/iesc111.pdf")