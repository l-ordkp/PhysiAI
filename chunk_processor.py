class TextChunkProcessor:
    def __init__(self, chunk_size=500, overlap=50):
        """
        Initialize text chunk processor.
        
        Args:
            chunk_size (int): Size of each text chunk
            overlap (int): Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text):
        """
        Split text into chunks with overlap.
        
        Args:
            text (str): Text to chunk
            
        Returns:
            list: List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = min(start + self.chunk_size, text_length)
            # Avoid cutting words in the middle
            if end < text_length:
                while end > start and text[end] != ' ':
                    end -= 1
            
            chunks.append(text[start:end])
            start = end - self.overlap
        
        return chunks
    
    def process(self, text, source, page_num, question_generator):
        """
        Process text: chunk it and generate questions.
        
        Args:
            text (str): Text to process
            source (str): Source document
            page_num (int): Page number
            question_generator: Question generator instance
            
        Returns:
            tuple: (chunks, questions, metadata)
        """
        chunks = self.chunk_text(text)
        questions = []
        metadata = []
        
        for i, chunk in enumerate(chunks):
            question = question_generator.generate_question(chunk)
            questions.append(question)
            metadata.append({
                'source': source,
                'page': page_num,
                'type': 'text',
                'chunk_index': i
            })
        
        return chunks, questions, metadata


class TableChunkProcessor:
    def __init__(self):
        """Initialize table chunk processor."""
        pass
    
    def convert_table_to_text(self, rows):
        """
        Convert table rows to text representation.
        
        Args:
            rows (list): List of table rows
            
        Returns:
            str: Text representation of the table
        """
        return "\n".join([" | ".join(row) for row in rows])
    
    def process(self, rows, source, page_num, question_generator):
        """
        Process table: convert to text and generate question.
        
        Args:
            rows (list): Table rows
            source (str): Source document
            page_num (int): Page number
            question_generator: Question generator instance
            
        Returns:
            tuple: (chunk, question, metadata)
        """
        table_text = self.convert_table_to_text(rows)
        question = question_generator.generate_question(table_text)
        
        metadata = {
            'source': source,
            'page': page_num,
            'type': 'table',
            'rows': len(rows),
            'columns': len(rows[0]) if rows else 0
        }
        
        return table_text, question, metadata