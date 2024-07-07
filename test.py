import ast
from datetime import datetime
import os
import time
import uuid
import pandas as pd
from typing import List, Tuple, Optional, Dict, Union
import google.generativeai as genai
from PIL import Image
import argparse

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
IMAGE_CACHE_DIRECTORY = "/tmp"
IMAGE_WIDTH = 512
CHAT_HISTORY = List[Tuple[Optional[Union[Tuple[str], str]], Optional[str]]]

# Valeurs par défaut
DEFAULT_API_KEY = "AIzaSyAPF4m9z42rNvckDKr-7lXzBXNqwkYnLP0" 
DEFAULT_IMAGE_PATH = "/home/amiche/Projects/image2table/table/2.jpg"
DEFAULT_PROMPT = """Please extract the table from the following image and provide it in a structured format.
The output should be structured as follows:
'''{
 'columns': [col1, col2, ...],
 'rows': {
 0: [r00, r01, r02, ...],
 1: [r10, r11, r12, ...],
 ...
 }
}'''
Replace the example table with the data extracted from the image."""

def preprocess_stop_sequences(stop_sequences: str) -> Optional[List[str]]:
    if not stop_sequences:
        return None
    return [sequence.strip() for sequence in stop_sequences.split(",")]

def preprocess_image(image: Image.Image) -> Optional[Image.Image]:
    image_height = int(image.height * IMAGE_WIDTH / image.width)
    return image.resize((IMAGE_WIDTH, image_height))

def cache_pil_image(image: Image.Image) -> str:
    image_filename = f"{uuid.uuid4()}.jpeg"
    os.makedirs(IMAGE_CACHE_DIRECTORY, exist_ok=True)
    image_path = os.path.join(IMAGE_CACHE_DIRECTORY, image_filename)
    image.save(image_path, "JPEG")
    return image_path

def preprocess_chat_history(
    history: CHAT_HISTORY
) -> List[Dict[str, Union[str, List[str]]]]:
    messages = []
    for user_message, model_message in history:
        if isinstance(user_message, tuple):
            pass
        elif user_message is not None:
            messages.append({'role': 'user', 'parts': [user_message]})
        if model_message is not None:
            messages.append({'role': 'model', 'parts': [model_message]})
    return messages

def upload(files: Optional[List[str]], chatbot: CHAT_HISTORY) -> CHAT_HISTORY:
    for file in files:
        image = Image.open(file).convert('RGB')
        image = preprocess_image(image)
        image_path = cache_pil_image(image)
        chatbot.append(((image_path,), None))
    return chatbot

def user(text_prompt: str, chatbot: CHAT_HISTORY):
    if text_prompt:
        chatbot.append((text_prompt, None))
    return "", chatbot

def bot(
    google_key: str,
    files: Optional[List[str]],
    temperature: float,
    max_output_tokens: int,
    stop_sequences: str,
    top_k: int,
    top_p: float,
    chatbot: CHAT_HISTORY
):
    if len(chatbot) == 0:
        return chatbot
    
    google_key = google_key if google_key else GOOGLE_API_KEY
    if not google_key:
        raise ValueError(
            "GOOGLE_API_KEY is not set. "
            "Please follow the instructions in the README to set it up.")
    
    genai.configure(api_key=google_key)
    generation_config = genai.types.GenerationConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        stop_sequences=preprocess_stop_sequences(stop_sequences=stop_sequences),
        top_k=top_k,
        top_p=top_p)
    
    if files:
        text_prompt = [chatbot[-1][0]] \
            if chatbot[-1][0] and isinstance(chatbot[-1][0], str) \
            else []
        image_prompt = [Image.open(file).convert('RGB') for file in files]
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content(
            text_prompt + image_prompt,
            stream=True,
            generation_config=generation_config)
    else:
        messages = preprocess_chat_history(chatbot)
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content(
            messages,
            stream=True,
            generation_config=generation_config)
    
    # streaming effect
    chatbot[-1][1] = ""
    for chunk in response:
        for i in range(0, len(chunk.text), 10):
            section = chunk.text[i:i + 10]
            chatbot[-1][1] += section
            time.sleep(0.01)
            yield chatbot

def main(api_key: str, image_path: str, prompt: str):
    # Configure l'API
    genai.configure(api_key=api_key)

    # Charge et prétraite l'image
    image = Image.open(image_path).convert('RGB')
    image = preprocess_image(image)

    # Initialise le modèle
    model = genai.GenerativeModel('gemini-pro-vision')

    # Génère la réponse
    response = model.generate_content([prompt, image])

    # Affiche la réponse
    print("Réponse du modèle :")
    print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interroge le modèle Gemini sur une image.")
    parser.add_argument("--api_key", default=DEFAULT_API_KEY, help="Clé API Google (optionnel)")
    parser.add_argument("--image_path", default=DEFAULT_IMAGE_PATH, help="Chemin vers l'image (optionnel)")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Question ou prompt pour l'image (optionnel)")
    
    args = parser.parse_args()
    
    main(args.api_key, args.image_path, args.prompt)