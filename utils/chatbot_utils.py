from ollama import Client
from pathlib import Path
from utils.file_utils import load_json, save_json

client = Client()  # Ollama client
MODEL_NAME = "gemma2:latest"  # Make sure this is installed

def chat_with_student(student_file, message):
    history_file = f"sessions/{Path(student_file).stem}_history.json"
    history = load_json(history_file)

    # Build message history for Ollama
    messages = [{"role": "system", "content": f"You are a tutor for {load_json(student_file)['name']}."}]
    for h in history:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["bot"]})
    messages.append({"role": "user", "content": message})

    response = client.chat(model=MODEL_NAME, messages=messages)
    bot_response = response.message.content

    # Save history
    history.append({"user": message, "bot": bot_response})
    save_json(history, history_file)
    return bot_response
