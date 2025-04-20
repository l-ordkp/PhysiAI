import os
import json
from dotenv import load_dotenv
from utils.llamaparse_processor import LlamaParseProcessor
from utils.chunk_processor import TextChunkProcessor, TableChunkProcessor
from utils.generate_questions import QuestionGenerator
from db_prep.vector_db import VectorDBManager
from utils.image_extractor import ImageExtractor

load_dotenv()
llama_key = os.getenv("LLAMA_CLOUD_API_KEY")

def process_single_pdf(pdf_path, base_output_dir, llamaparse_api_key, gemini_api_key):
    pdf_file = os.path.basename(pdf_path)
    pdf_name = os.path.splitext(pdf_file)[0]
    output_dir = os.path.join(base_output_dir, pdf_name)

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

    print(f"Parsing PDF: {pdf_file}")
    json_objs = []
    json_objs.extend(llamaparse_processor.get_json_result(pdf_path))

    # Step 1: Extract markdown text and tables into dicts
    page_texts, tables = {}, {}

    for obj in json_objs:
        json_list = obj['pages']
        print(json_list)
        name = obj["file_path"].split("/")[-1]

        page_texts[name] = {}
        tables[name] = {}

        for json_item in json_list:
            page_num = json_item['page']

            if 'md' in json_item:
                page_texts[name][page_num] = json_item['md']

            for component in json_item.get('items', []):
                if component['type'] == 'table':
                    tables[name][page_num] = component['rows']

            # Extract images while we're looping pages
            image_extractor.extract_images_from_page(json_item, name, page_num)

    all_chunks, all_questions, all_metadata = [], [], []

    # Step 2: Process extracted markdown text
    for name in page_texts:
        for page_num, md_text in page_texts[name].items():
            chunks, questions, metadata = text_processor.process(
                md_text,
                name,
                page_num,
                question_generator
            )
            all_chunks.extend(chunks)
            all_questions.extend(questions)
            all_metadata.extend(metadata)

    # Step 3: Process extracted tables
    for name in tables:
        for page_num, rows in tables[name].items():
            chunk, question, metadata = table_processor.process(
                rows,
                name,
                page_num,
                question_generator
            )
            all_chunks.append(chunk)
            all_questions.append(question)
            all_metadata.append(metadata)

    print(f"Total Chunks: {len(all_chunks)}")

    # Step 4: Build and save FAISS DB
    print("Creating vector database...")
    vector_db = VectorDBManager('all-MiniLM-L6-v2')
    vector_db.create_index(all_questions, all_chunks, all_metadata, batch_size=32)
    vector_db.save_index(os.path.join(output_dir, "faiss_index.idx"))
    vector_db.save_data(os.path.join(output_dir, "vector_data.pkl"))

    # Step 5: Save summary
    summary = {
        "total_chunks": len(all_chunks),
        "text_chunks": len([m for m in all_metadata if m['type'] == 'text']),
        "table_chunks": len([m for m in all_metadata if m['type'] == 'table']),
        "image_count": len(os.listdir(image_dir))
    }

    with open(os.path.join(output_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print("Processing complete.")
    print(json.dumps(summary, indent=2))
    print(f"- Data saved to: {output_dir}")

    return {
        "vector_db": vector_db,
        "metadata": all_metadata,
        "chunks": all_chunks,
        "questions": all_questions
    }

if __name__ == "__main__":
    llamaparse_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
    gemini_api_key = os.getenv("GOOGLE_API_KEY")

    pdf_path = "iesc111.pdf"  # Path to your PDF file
    output_dir = "text_db"

    result = process_single_pdf(pdf_path, output_dir, llamaparse_api_key, gemini_api_key)
