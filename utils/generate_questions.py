import google.generativeai as genai
import time
from typing import List, Dict, Any, Tuple
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

    def generate_questions(self, chunk: Dict[str, Any]) -> List[str]:
        """
        Generate multiple questions (3) for the given content chunk.
        Args:
            chunk (Dict): Content chunk with text or table
        Returns:
            List[str]: Generated questions
        """
        content = chunk["content"]
        content_type = chunk["content_type"]

        questions, _ = self.generate_multiple_questions(content, content_type)

        # Fallback if LLM didn't give 3 valid ones
        if len(questions) < 3:
            default_question = f"What information does this {content_type} provide?"
            while len(questions) < 3:
                questions.append(default_question)

        time.sleep(4.1)  # Add delay to respect rate limits if batching

        return questions[:3]

    def generate_multiple_questions(self, content: str, content_type: str) -> Tuple[List[str], Any]:
        """
        Ask the LLM to generate 3 different and specific questions related to sound engineering
        that the given content would answer. Questions are returned comma-separated.
        Args:
            content (str): Input content
            content_type (str): Type of content ("text" or "table")
        Returns:
            Tuple[List[str], Any]: List of generated questions and the raw response
        """
        if content_type == "table":
            prompt = (
                "You are a sound engineering expert. Generate 3 different and specific questions that the following table would answer well. "
                "Return the questions separated by commas.\n\n"
                "Example:\n"
                "Table:\n| Frequency (Hz) | Amplitude (dB) |\n|----------------|-----------------|\n| 100            | -12             |\n| 1000           | -6              |\n\n"
                "Output:\nWhat is the amplitude at 100 Hz?, How does the amplitude change with frequency?, Which frequency has the highest amplitude?\n\n"
                f"Table:\n{content}\n\nQuestions:"
            )
        else:
            prompt = (
                "You are a sound engineering expert. Generate 3 different and specific questions that the following text would answer well. "
                "Return the questions separated by commas.\n\n"
                "Example:\n"
                "Text:\nA cardioid microphone is designed to capture sound from the front and reject sound from the sides and rear, making it ideal for studio vocals.\n\n"
                "Output:\nWhat is the pickup pattern of a cardioid microphone?, Why is a cardioid microphone suitable for studio vocals?, How does a cardioid microphone reject background noise?\n\n"
                f"Text:\n{content}\n\nQuestions:"
            )

        try:
            response = self.model.generate_content([prompt])
            raw_output = response.text.strip()

            # Split by comma and clean
            questions = [q.strip() for q in raw_output.split(",") if "?" in q]
            return questions[:3], response
        except Exception as e:
            print(f"Error generating questions: {e}")
            return [], None

    def generate_image_question(self, image_path, mime_type="image/jpeg", prompt="Create a question that this image would answer in the context of sound engineering."):
 
        # Upload the file
        uploaded_file = genai.upload_file(image_path, mime_type=mime_type)
        print(f"Uploaded file '{uploaded_file.display_name}' as: {uploaded_file.uri}")

        # Start chat and send message
        chat_session = self.model.start_chat()
        response = chat_session.send_message([uploaded_file, prompt])

        return response.text.strip()








    
