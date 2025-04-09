import google.generativeai as genai


class QuestionGenerator:
    def __init__(self, api_key, model="gemini-2.0-flash", temperature=0.7):
        """
        Initialize question generator with Gemini model parameters.
        
        Args:
            api_key (str): Google API key
            model (str): Gemini model to use
            temperature (float): Temperature for response generation
        """
        self.model = model
        self.temperature = temperature
        self.client = genai.Client(api_key=api_key)
    
    def generate_question(self, text):
        """
        Generate a hypothetical question for a text chunk using Gemini.
        
        Args:
            text (str): Text chunk
            
        Returns:
            str: Generated question
        """
        prompt = f"Generate a specific question that the following text would answer well:\n\n{text}\n\nQuestion:"
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            generation_config={"temperature": self.temperature}
        )
        
        return response.text.strip()