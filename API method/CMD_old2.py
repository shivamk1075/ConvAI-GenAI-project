# Github API Phi-3 Mini Instruct Model for AI Sales Training

import httpx
import os
from dotenv import load_dotenv

# Load .env file from custom location outside workspace
custom_env_path = r"C:\Users\natur\Desktop\Projects\MY APIs\.env"  # <-- Replace with your actual path
load_dotenv(dotenv_path=custom_env_path)

class AITrainer:
    def __init__(self, persona):
        print("Using GitHub API Phi-3 model for conversations...")
        self.persona = persona
        self.conversation_history = []
        # GitHub Models API endpoint
        self.api_url = "https://models.inference.ai.azure.com/chat/completions"
        
        # Load token from environment variable
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            raise ValueError("GITHUB_TOKEN not found in environment variables")
            
        self.headers = {
            "Authorization": f"Bearer {github_token}",
            "Content-Type": "application/json"
        }

    def get_response(self, user_message):
        self.conversation_history.append({'role': 'user', 'content': user_message})

        if self.persona == "relative":
            system_msg = """You are my caring cousin who I'm telling about my business idea. 
            Keep responses SHORT (1-2 sentences max). Be warm and supportive. 
            Never mention you're an AI. Just be a normal family member."""
        else:
            system_msg = """You are an experienced shopkeeper evaluating a potential 
            business opportunity. Focus on practical aspects like margins, product quality, and market demand. 
            Ask specific questions about business viability and logistics."""

        messages = [
            {"role": "system", "content": system_msg}
        ]
        
        messages.extend(self.conversation_history[-6:])

        payload = {
            "model": "Phi-3-mini-4k-instruct",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 150
        }

        try:
            with httpx.Client(timeout=30) as client:
                response = client.post(self.api_url, headers=self.headers, json=payload)
                response.raise_for_status()
                data = response.json()
                bot_response = data["choices"][0]["message"]["content"].strip()  # Fixed: added [0]
                self.conversation_history.append({'role': 'assistant', 'content': bot_response})
                return bot_response

        except Exception as e:
            return f"Error communicating with GitHub API: {str(e)}"

def relative():
    print("\n=== Starting AI Sales Training Session: Relative Profile ===")
    print("[Relative] Hi! Nice to see you. I heard you wanted to talk about something?")
    trainer = AITrainer("relative")
    messages_count = 0
    MAX_MESSAGES = 50

    while messages_count < MAX_MESSAGES:
        user_message = input("\nYou: ").strip()
        if not user_message:
            continue
        messages_count += 1
        bot_response = trainer.get_response(user_message)
        print(f"\n[Relative] {bot_response}")
        remaining = MAX_MESSAGES - messages_count
        if remaining > 0:
            print(f"\n(Messages remaining: {remaining})")
        else:
            print("\n=== Training session completed! ===")
            print("You've reached the maximum number of messages (50).")
            print("Take some time to reflect on this conversation!")

def shopkeeper():
    print("\n=== Starting AI Sales Training Session: Shopkeeper Profile ===")
    print("[Shopkeeper] Welcome to my shop! What brings you here today?")
    trainer = AITrainer("shopkeeper")
    messages_count = 0
    MAX_MESSAGES = 50

    while messages_count < MAX_MESSAGES:
        user_message = input("\nYou: ").strip()
        if not user_message:
            continue
        messages_count += 1
        bot_response = trainer.get_response(user_message)
        print(f"\n[Shopkeeper] {bot_response}")
        remaining = MAX_MESSAGES - messages_count
        if remaining > 0:
            print(f"\n(Messages remaining: {remaining})")
        else:
            print("\n=== Training session completed! ===")
            print("You've reached the maximum number of messages (50).")
            print("Take some time to reflect on this conversation!")

if __name__ == "__main__":
    print("Choose your training scenario:")
    print("1. Relative")
    print("2. Shopkeeper")
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        relative()
    elif choice == "2":
        shopkeeper()
    else:
        print("Invalid choice. Please run again.")
