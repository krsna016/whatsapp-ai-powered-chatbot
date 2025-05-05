import requests
import os

def ollama_generate(user_input):
    url = os.getenv("OLLA_API_URL")
    if not url:
        return "Ollama API URL not set."

    headers = {"Content-Type": "application/json"}

    # Boostonix Knowledgebase Prompt
    BOOSTONIX_PROMPT = """
ADD YOUR COMPANY INFO HERE!!
"""

    # Prevent crashing on empty input
    user_input = user_input or ""

    full_prompt = BOOSTONIX_PROMPT + f"\n\nUser: {user_input}\nBoostonix Assistant:"

    data = {
        "model": "mistral",
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "No reply from Ollama").strip()
        else:
            return f"Error from Ollama: {response.status_code}"
    except Exception as e:
        return f"Internal error: {str(e)}"