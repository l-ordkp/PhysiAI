import os
import json
from llamaparse_processor import LlamaParseProcessor
from chunk_processor import TextChunkProcessor, TableChunkProcessor
from generate_questions import QuestionGenerator
from vector_db import VectorDBManager
from image_extractor import ImageExtractor
from dotenv import load_dotenv
load_dotenv()
llama_key = os.environ.get("LLAMA_CLOUD_API_KEY")

def process_single_pdf(pdf_path, output_dir, llamaparse_api_key, gemini_api_key):
    """Process a single PDF and prepare it for RAG"""
    
    # Create output directories
    os.makedirs(output_dir, exist_ok=True)
    image_dir = os.path.join(output_dir, "images")
    os.makedirs(image_dir, exist_ok=True)
    
    # Initialize components
    llamaparse_processor = LlamaParseProcessor(
        result_type="markdown",
        skip_diagonal_text=True,
        fast_mode=False,
        num_workers=9,
        check_interval=10,
        api_key=llamaparse_api_key
    )
    
    text_processor = TextChunkProcessor(chunk_size=500, overlap=50)
    table_processor = TableChunkProcessor()
    question_generator = QuestionGenerator(api_key=gemini_api_key)
    image_extractor = ImageExtractor(image_dir)
    
    # PDF filename for metadata
    pdf_file = os.path.basename(pdf_path)
    
    # Process the PDF
    print(f"Parsing PDF: {pdf_file}")
    json_objs = llamaparse_processor.get_json_result(pdf_path)
    
    # Process text and tables
    all_chunks = []
    all_questions = []
    all_metadata = []
    
    print("Processing content...")
    for obj in json_objs:
        json_list = obj['pages']
        for page_data in json_list:
            page_num = page_data['page']
            
            # Process text
            if 'md' in page_data:
                chunks, questions, metadata = text_processor.process(
                    page_data['md'], 
                    pdf_file, 
                    page_num,
                    question_generator
                )
                all_chunks.extend(chunks)
                all_questions.extend(questions)
                all_metadata.extend(metadata)
            
            # Process tables
            for item in page_data.get('items', []):
                if item['type'] == 'table' and 'rows' in item:
                    chunk, question, metadata = table_processor.process(
                        item['rows'], 
                        pdf_file, 
                        page_num,
                        question_generator
                    )
                    all_chunks.append(chunk)
                    all_questions.append(question)
                    all_metadata.append(metadata)
            
            # Extract images
            image_extractor.extract_images_from_page(page_data, pdf_file, page_num)
    
    # Create vector database
    print("Creating vector database...")
    vector_db = VectorDBManager('all-MiniLM-L6-v2')
    vector_db.create_index(all_questions, all_chunks, all_metadata)
    vector_db.save_index(os.path.join(output_dir, "faiss_index.idx"))
    
    # Save metadata and content
    with open(os.path.join(output_dir, "metadata.json"), "w") as f:
        json.dump(all_metadata, f)
    
    with open(os.path.join(output_dir, "questions.json"), "w") as f:
        json.dump(all_questions, f)
    
    with open(os.path.join(output_dir, "chunks.json"), "w") as f:
        json.dump(all_chunks, f)
    
    print(f"Processing complete.")
    print(f"- Total chunks: {len(all_chunks)}")
    print(f"- Text chunks: {len([m for m in all_metadata if m['type'] == 'text'])}")
    print(f"- Table chunks: {len([m for m in all_metadata if m['type'] == 'table'])}")
    print(f"- Images saved: {len(os.listdir(image_dir))}")
    print(f"- Data saved to: {output_dir}")
    
    return {
        "vector_db": vector_db,
        "metadata": all_metadata,
        "chunks": all_chunks,
        "questions": all_questions
    }

if __name__ == "__main__":
    llamaparse_api_key = os.environ.get("LLAMA_CLOUD_API_KEY")
    gemini_api_key = os.getenv('GOOGLE_API_KEY')
    # Configuration
    pdf_path = "C:\\Users\\Kshit\\Desktop\\PhysiAI\\string.pdf"
    output_dir = "text_db"
   
    # Process the PDF
    result = process_single_pdf(pdf_path, output_dir, llamaparse_api_key, gemini_api_key)
    
    