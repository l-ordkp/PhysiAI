import os
import google.generativeai as genai


class QuestionGenerator:
    def __init__(self, api_key, model="gemini-1.5-flash", temperature=0.7):
        """
        Initialize question generator with Gemini model parameters.

        Args:
            api_key (str): Google API key
            model (str): Gemini model to use
            temperature (float): Temperature for response generation
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=model,
            generation_config={
                "temperature": temperature,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
        )

    def generate_question(self, text):
        """
        Generate a specific question that the text would answer.

        Args:
            text (str): Input text

        Returns:
            str: Generated question
        """
        prompt = f"Generate a specific question that the following text would answer well in the context of sound engineering:\n\n{text}\n\nQuestion:"
        response = self.model.generate_content([prompt])
        return response.text.strip()

    def generate_image_question(self, image_path, mime_type="image/jpeg", prompt="Create a question that this image would answer in the context of sound engineering."):
 
        # Upload the file
        uploaded_file = genai.upload_file(image_path, mime_type=mime_type)
        print(f"Uploaded file '{uploaded_file.display_name}' as: {uploaded_file.uri}")

        # Start chat and send message
        chat_session = self.model.start_chat()
        response = chat_session.send_message([uploaded_file, prompt])

        return response.text.strip()
