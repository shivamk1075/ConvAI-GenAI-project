import requests

def ollama_chat(model: str, messages: list) -> str:
    """
    Sends a chat completion request to the local Ollama server.
    Args:
        model (str): The name of the model (e.g., 'phi3.5').
        messages (list): List of dicts with 'role' and 'content'.
    Returns:
        str: The assistant's reply as a string.
    """
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": False
    }
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    # Ollama returns the full conversation, but the latest message is at the end
    return data["message"]["content"]