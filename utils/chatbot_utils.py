import requests
import os
from pathlib import Path
from utils.file_utils import load_json, save_json

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

FREE_MODEL = "meta-llama/llama-3.1-8b-instruct:free"  
# You may swap with other free models later

def create_system_prompt(student_data):
    return f"""
    You are a personalized math tutor for {student_data['name']}, a grade {student_data['grade']} student.
    Learning preferences: {', '.join(student_data['learning_preferences'])}.
    Goals: {', '.join(student_data['goals'])}.
    Provide clear, supportive, personalized feedback. Adapt your explanations to the student's level.
    """

def ask_llm(model, messages):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": messages
        }
    )

    data = response.json()
    return data["choices"][0]["message"]["content"]

def chat_with_student(student_file, message):
    # Load student data
    student_data = load_json(student_file)

    # History file
    history_file = f"sessions/{Path(student_file).stem}_history.json"
    history = load_json(history_file) if Path(history_file).exists() else []

    # Construct message history for LLM
    messages = [{"role": "system", "content": create_system_prompt(student_data)}]

    # Add previous conversation history
    for h in history:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["bot"]})

    # Add new user message
    messages.append({"role": "user", "content": message})

    # Call OpenRouter model
    bot_response = ask_llm(FREE_MODEL, messages)

    # Save new exchange
    history.append({"user": message, "bot": bot_response})
    save_json(history, history_file)

    return bot_response
