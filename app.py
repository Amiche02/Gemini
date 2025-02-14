import os
import time
import uuid
from typing import List, Tuple, Optional, Dict, Union

import google.generativeai as genai
import gradio as gr
from PIL import Image

print("google-generativeai:", genai.__version__)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

TITLE = """<h1 align="center">Gemini 1.5 Pro Playground 💬</h1>"""
SUBTITLE = """<h2 align="center">Play with Gemini 1.5 Pro and Gemini Pro Vision API</h2>"""
DUPLICATE = """
<div style="text-align: center; display: flex; justify-content: center; align-items: center;">
    <a href="https://huggingface.co/spaces/SkalskiP/ChatGemini?duplicate=true">
        <img src="https://bit.ly/3gLdBN6" alt="Duplicate Space" style="margin-right: 10px;">
    </a>
    <span>Duplicate the Space and run securely with your 
        <a href="https://makersuite.google.com/app/apikey">GOOGLE API KEY</a>.
    </span>
</div>
"""

AVATAR_IMAGES = (
    None,
    "https://media.roboflow.com/spaces/gemini-icon.png"
)

IMAGE_CACHE_DIRECTORY = "/tmp"
IMAGE_WIDTH = 512
CHAT_HISTORY = List[Tuple[Optional[Union[Tuple[str], str]], Optional[str]]]


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


google_key_component = gr.Textbox(
    label="GOOGLE API KEY",
    value="",
    type="password",
    placeholder="...",
    info="You have to provide your own GOOGLE_API_KEY for this app to function properly",
    visible=GOOGLE_API_KEY is None
)
chatbot_component = gr.Chatbot(
    label='Gemini',
    bubble_full_width=False,
    avatar_images=AVATAR_IMAGES,
    scale=2,
    height=400
)
text_prompt_component = gr.Textbox(
    placeholder="Hi there! [press Enter]", show_label=False, autofocus=True, scale=8
)
upload_button_component = gr.UploadButton(
    label="Upload Images", file_count="multiple", file_types=["image"], scale=1
)
run_button_component = gr.Button(value="Run", variant="primary", scale=1)
temperature_component = gr.Slider(
    minimum=0,
    maximum=1.0,
    value=0.4,
    step=0.05,
    label="Temperature",
    info=(
        "Temperature controls the degree of randomness in token selection. Lower "
        "temperatures are good for prompts that expect a true or correct response, "
        "while higher temperatures can lead to more diverse or unexpected results. "
    ))
max_output_tokens_component = gr.Slider(
    minimum=1,
    maximum=8192,
    value=4096,
    step=1,
    label="Token limit",
    info=(
        "Token limit determines the maximum amount of text output from one prompt. A "
        "token is approximately four characters. The default value is 4096."
    ))
stop_sequences_component = gr.Textbox(
    label="Add stop sequence",
    value="",
    type="text",
    placeholder="STOP, END",
    info=(
        "A stop sequence is a series of characters (including spaces) that stops "
        "response generation if the model encounters it. The sequence is not included "
        "as part of the response. You can add up to five stop sequences."
    ))
top_k_component = gr.Slider(
    minimum=1,
    maximum=40,
    value=32,
    step=1,
    label="Top-K",
    info=(
        "Top-k changes how the model selects tokens for output. A top-k of 1 means the "
        "selected token is the most probable among all tokens in the model’s "
        "vocabulary (also called greedy decoding), while a top-k of 3 means that the "
        "next token is selected from among the 3 most probable tokens (using "
        "temperature)."
    ))
top_p_component = gr.Slider(
    minimum=0,
    maximum=1,
    value=1,
    step=0.01,
    label="Top-P",
    info=(
        "Top-p changes how the model selects tokens for output. Tokens are selected "
        "from most probable to least until the sum of their probabilities equals the "
        "top-p value. For example, if tokens A, B, and C have a probability of .3, .2, "
        "and .1 and the top-p value is .5, then the model will select either A or B as "
        "the next token (using temperature). "
    ))

user_inputs = [
    text_prompt_component,
    chatbot_component
]

bot_inputs = [
    google_key_component,
    upload_button_component,
    temperature_component,
    max_output_tokens_component,
    stop_sequences_component,
    top_k_component,
    top_p_component,
    chatbot_component
]

with gr.Blocks() as demo:
    gr.HTML(TITLE)
    gr.HTML(SUBTITLE)
    gr.HTML(DUPLICATE)
    with gr.Column():
        google_key_component.render()
        chatbot_component.render()
        with gr.Row():
            text_prompt_component.render()
            upload_button_component.render()
            run_button_component.render()
        with gr.Accordion("Parameters", open=False):
            temperature_component.render()
            max_output_tokens_component.render()
            stop_sequences_component.render()
            with gr.Accordion("Advanced", open=False):
                top_k_component.render()
                top_p_component.render()

    run_button_component.click(
        fn=user,
        inputs=user_inputs,
        outputs=[text_prompt_component, chatbot_component],
        queue=False
    ).then(
        fn=bot, inputs=bot_inputs, outputs=[chatbot_component],
    )

    text_prompt_component.submit(
        fn=user,
        inputs=user_inputs,
        outputs=[text_prompt_component, chatbot_component],
        queue=False
    ).then(
        fn=bot, inputs=bot_inputs, outputs=[chatbot_component],
    )

    upload_button_component.upload(
        fn=upload,
        inputs=[upload_button_component, chatbot_component],
        outputs=[chatbot_component],
        queue=False
    )

demo.queue(max_size=99).launch(debug=False, show_error=True)