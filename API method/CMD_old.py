# # AI Sales Training with Perplexity API

# # import json
# # import requests
# # import os
# # from dotenv import load_dotenv

# # # Define path to your .env file
# # ENV_PATH = r"C:\Users\natur\Desktop\Projects\MY APIs\.env"  # Update this path to your .env location

# # # Load environment variables from specific path
# # load_dotenv(ENV_PATH)

# # class AITrainer:
# #     def __init__(self, persona):
# #         self.api_key = os.getenv('PERPLEXITY_API_KEY')
# #         self.base_url = 'https://api.perplexity.ai/chat/completions'
# #         self.persona = persona
# #         self.conversation_history = []
        
# #     def get_response(self, user_message):
# #         if not self.api_key:
# #             return "Error: Please set PERPLEXITY_API_KEY in your .env file"

# #         # Add user message to history
# #         self.conversation_history.append({'role': 'user', 'content': user_message})
        
# #         # Prepare system message based on persona
# #         if self.persona == "relative":
# #             system_msg = """You are role-playing as a caring relative who is being approached by a family 
# #             member about their business venture. Be supportive yet realistic. Ask thoughtful questions about 
# #             their business plan. Show genuine interest but also raise practical concerns when necessary."""
# #         else:
# #             system_msg = """You are role-playing as an experienced shopkeeper evaluating a potential 
# #             business opportunity. Focus on practical aspects like margins, product quality, and market demand. 
# #             Ask specific questions about business viability and logistics."""

# #         # Prepare messages
# #         messages = [
# #             {'role': 'system', 'content': system_msg}
# #         ]
# #         messages.extend(self.conversation_history)

# #         headers = {
# #             'Authorization': f'Bearer {self.api_key}',
# #             'Content-Type': 'application/json'
# #         }

# #         payload = {
# #             'model': 'sonar',  # CORRECT MODEL NAME
# #             'messages': messages,
# #             'temperature': 0.7,
# #             'max_tokens': 25
# #         }

# #         try:
# #             response = requests.post(
# #                 self.base_url, 
# #                 headers=headers,
# #                 json=payload,
# #                 timeout=30
# #             )
            
# #             if response.status_code != 200:
# #                 print(f"Status: {response.status_code}")
# #                 print(f"Response: {response.text}")
            
# #             response.raise_for_status()
            
# #             result = response.json()
# #             bot_response = result['choices'][0]['message']['content']
            
# #             self.conversation_history.append({'role': 'assistant', 'content': bot_response})
            
# #             return bot_response

# #         except requests.exceptions.RequestException as e:
# #             print(f"Debug - Full error: {str(e)}")
# #             return f"Error communicating with AI: {str(e)}"


        
# # def relative():
# #     print("\n=== Starting AI Sales Training Session: Relative Profile ===")
# #     print("[Relative] Hi! Nice to see you. I heard you wanted to talk about something?")
    
# #     trainer = AITrainer("relative")
# #     messages_count = 0
# #     MAX_MESSAGES = 5

# #     while messages_count < MAX_MESSAGES:
# #         user_message = input("\nYou: ").strip()
# #         if not user_message:
# #             continue
            
# #         messages_count += 1
# #         bot_response = trainer.get_response(user_message)
# #         print(f"\n[Relative] {bot_response}")
        
# #         remaining = MAX_MESSAGES - messages_count
# #         if remaining > 0:
# #             print(f"\n(Messages remaining: {remaining})")
# #         else:
# #             print("\n=== Training session completed! ===")
# #             print("You've reached the maximum number of messages (5).")
# #             print("Take some time to reflect on this conversation!")

# # def shopkeeper():
# #     print("\n=== Starting AI Sales Training Session: Shopkeeper Profile ===")
# #     print("[Shopkeeper] Welcome to my shop! What brings you here today?")
    
# #     trainer = AITrainer("shopkeeper")
# #     messages_count = 0
# #     MAX_MESSAGES = 5

# #     while messages_count < MAX_MESSAGES:
# #         user_message = input("\nYou: ").strip()
# #         if not user_message:
# #             continue
            
# #         messages_count += 1
# #         bot_response = trainer.get_response(user_message)
# #         print(f"\n[Shopkeeper] {bot_response}")
        
# #         remaining = MAX_MESSAGES - messages_count
# #         if remaining > 0:
# #             print(f"\n(Messages remaining: {remaining})")
# #         else:
# #             print("\n=== Training session completed! ===")
# #             print("You've reached the maximum number of messages (5).")
# #             print("Take some time to reflect on this conversation!")

# First gpt2o


# import os
# from transformers import AutoModelForCausalLM, AutoTokenizer

# class AITrainer:
#     def __init__(self, persona):
#         print("Loading local GPT-2 model... (first run may take a few minutes)")
#         self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
#         self.model = AutoModelForCausalLM.from_pretrained("gpt2")
#         self.persona = persona
#         self.conversation_history = []

#     def get_response(self, user_message):
#         # Add user message to history
#         self.conversation_history.append({'role': 'user', 'content': user_message})

#         # Prepare system message based on persona
#         if self.persona == "relative":
#             system_msg = (
#                 "You are role-playing as a caring relative who is being approached by a family "
#                 "member about their business venture. Be supportive yet realistic. Ask thoughtful questions about "
#                 "their business plan. Show genuine interest but also raise practical concerns when necessary."
#             )
#         else:
#             system_msg = (
#                 "You are role-playing as an experienced shopkeeper evaluating a potential "
#                 "business opportunity. Focus on practical aspects like margins, product quality, and market demand. "
#                 "Ask specific questions about business viability and logistics."
#             )

#         # Build prompt with short history for context
#         history = ""
#         for msg in self.conversation_history[-4:]:
#             prefix = "User: " if msg['role'] == 'user' else "AI: "
#             history += f"{prefix}{msg['content']}\n"
#         prompt = f"{system_msg}\n{history}AI:"

#         # Tokenize and generate
#         inputs = self.tokenizer.encode(prompt, return_tensors='pt')
#         outputs = self.model.generate(
#             inputs,
#             max_length=inputs.shape[1] + 60,
#             temperature=0.7,
#             pad_token_id=self.tokenizer.eos_token_id,
#             do_sample=True,
#             top_p=0.95,
#             num_return_sequences=1,
#             no_repeat_ngram_size=2
#         )
#         response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
#         # Extract only the AI's latest response
#         bot_response = response.split("AI:")[-1].strip().split("User:")[0].strip()
#         self.conversation_history.append({'role': 'assistant', 'content': bot_response})
#         return bot_response

# def relative():
#     print("\n=== Starting AI Sales Training Session: Relative Profile ===")
#     print("[Relative] Hi! Nice to see you. I heard you wanted to talk about something?")
#     trainer = AITrainer("relative")
#     messages_count = 0
#     MAX_MESSAGES = 50

#     while messages_count < MAX_MESSAGES:
#         user_message = input("\nYou: ").strip()
#         if not user_message:
#             continue
#         messages_count += 1
#         bot_response = trainer.get_response(user_message)
#         print(f"\n[Relative] {bot_response}")
#         remaining = MAX_MESSAGES - messages_count
#         if remaining > 0:
#             print(f"\n(Messages remaining: {remaining})")
#         else:
#             print("\n=== Training session completed! ===")
#             print("You've reached the maximum number of messages (5).")
#             print("Take some time to reflect on this conversation!")

# def shopkeeper():
#     print("\n=== Starting AI Sales Training Session: Shopkeeper Profile ===")
#     print("[Shopkeeper] Welcome to my shop! What brings you here today?")
#     trainer = AITrainer("shopkeeper")
#     messages_count = 0
#     MAX_MESSAGES = 50

#     while messages_count < MAX_MESSAGES:
#         user_message = input("\nYou: ").strip()
#         if not user_message:
#             continue
#         messages_count += 1
#         bot_response = trainer.get_response(user_message)
#         print(f"\n[Shopkeeper] {bot_response}")
#         remaining = MAX_MESSAGES - messages_count
#         if remaining > 0:
#             print(f"\n(Messages remaining: {remaining})")
#         else:
#             print("\n=== Training session completed! ===")
#             print("You've reached the maximum number of messages (5).")
#             print("Take some time to reflect on this conversation!")

# GPT-2-based AI Trainer for Sales Training

# import os
# from transformers import AutoModelForCausalLM, AutoTokenizer

# class AITrainer:
#     def __init__(self, persona):
#         print("Loading local GPT-2 model... (first run may take a few minutes)")
#         self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
        
#         # Add new pad token if missing to avoid warning
#         if self.tokenizer.pad_token is None:
#             self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        
#         self.model = AutoModelForCausalLM.from_pretrained("gpt2")
#         self.model.resize_token_embeddings(len(self.tokenizer))
        
#         self.persona = persona
#         self.conversation_history = []

#     def get_response(self, user_message):
#         self.conversation_history.append({'role': 'user', 'content': user_message})

#         if self.persona == "relative":
#             system_msg = (
#                 "You are a caring relative supporting a family member's business venture. "
#                 "Always stay positive and supportive but also ask practical questions. "
#                 "Do not talk about unrelated topics. "
#                 "Example:\n"
#                 "User: I want to start a bakery.\n"
#                 "AI: That sounds wonderful! What kinds of pastries are you planning to bake? "
#                 "Have you thought about your target customers?\n"
#             )
#         else:
#             system_msg = (
#                 "You are an experienced shopkeeper evaluating a business opportunity. "
#                 "Ask questions about costs, suppliers, and market demand. "
#                 "Stay focused on business and avoid off-topic answers. "
#                 "Example:\n"
#                 "User: I want to sell handmade crafts.\n"
#                 "AI: Interesting! What is your expected cost per item, and where will you source materials?\n"
#             )

#         # Use only last 4 messages for history (2 user + 2 AI)
#         history = ""
#         for msg in self.conversation_history[-4:]:
#             prefix = "User: " if msg['role'] == 'user' else "AI: "
#             history += f"{prefix}{msg['content']}\n"

#         prompt = f"{system_msg}{history}AI:"

#         inputs = self.tokenizer(
#             prompt,
#             return_tensors='pt',
#             truncation=True,
#             max_length=512,
#             padding=True,
#             return_attention_mask=True,
#         )

#         outputs = self.model.generate(
#             inputs['input_ids'],
#             attention_mask=inputs['attention_mask'],
#             max_length=inputs['input_ids'].shape[1] + 30,  # shorter responses
#             temperature=0.6,  # a bit less randomness
#             pad_token_id=self.tokenizer.pad_token_id,
#             do_sample=True,
#             top_p=0.9,
#             num_return_sequences=1,
#             no_repeat_ngram_size=2,
#         )

#         response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
#         bot_response = response.split("AI:")[-1].strip().split("User:")[0].strip()

#         self.conversation_history.append({'role': 'assistant', 'content': bot_response})
#         return bot_response


# def relative():
#     print("\n=== Starting AI Sales Training Session: Relative Profile ===")
#     print("[Relative] Hi! Nice to see you. I heard you wanted to talk about something?")
#     trainer = AITrainer("relative")
#     messages_count = 0
#     MAX_MESSAGES = 50

#     while messages_count < MAX_MESSAGES:
#         user_message = input("\nYou: ").strip()
#         if not user_message:
#             continue
#         messages_count += 1
#         bot_response = trainer.get_response(user_message)
#         print(f"\n[Relative] {bot_response}")
#         remaining = MAX_MESSAGES - messages_count
#         if remaining > 0:
#             print(f"\n(Messages remaining: {remaining})")
#         else:
#             print("\n=== Training session completed! ===")
#             print("You've reached the maximum number of messages (50).")
#             print("Take some time to reflect on this conversation!")

# def shopkeeper():
#     print("\n=== Starting AI Sales Training Session: Shopkeeper Profile ===")
#     print("[Shopkeeper] Welcome to my shop! What brings you here today?")
#     trainer = AITrainer("shopkeeper")
#     messages_count = 0
#     MAX_MESSAGES = 50

#     while messages_count < MAX_MESSAGES:
#         user_message = input("\nYou: ").strip()
#         if not user_message:
#             continue
#         messages_count += 1
#         bot_response = trainer.get_response(user_message)
#         print(f"\n[Shopkeeper] {bot_response}")
#         remaining = MAX_MESSAGES - messages_count
#         if remaining > 0:
#             print(f"\n(Messages remaining: {remaining})")
#         else:
#             print("\n=== Training session completed! ===")
#             print("You've reached the maximum number of messages (50).")
#             print("Take some time to reflect on this conversation!")


# Trying Phi-3 
# But its quite high with this transformer approach , so trying with the ollama approach

# import torch
# from transformers import AutoModelForCausalLM, AutoTokenizer

# class AITrainer:
#     def __init__(self, persona):
#         print("Loading local Phi-3 model... (first run may take a few minutes)")
        
#         # Use Phi-3 instead of GPT-2
#         model_name = "microsoft/Phi-3-mini-4k-instruct"
        
#         self.tokenizer = AutoTokenizer.from_pretrained(
#             model_name, 
#             trust_remote_code=True
#         )
        
#         self.model = AutoModelForCausalLM.from_pretrained(
#             model_name,
#             trust_remote_code=True,
#             torch_dtype="auto",
#             device_map="auto"  # Automatically handles CPU/GPU
#         )
        
#         self.persona = persona
#         self.conversation_history = []

#     def get_response(self, user_message):
#         self.conversation_history.append({'role': 'user', 'content': user_message})

#         if self.persona == "relative":
#             system_msg = """You are a caring relative who is being approached by a family 
#             member about their business venture. Be supportive yet realistic. Ask thoughtful questions about 
#             their business plan. Show genuine interest but also raise practical concerns when necessary."""
#         else:
#             system_msg = """You are an experienced shopkeeper evaluating a potential 
#             business opportunity. Focus on practical aspects like margins, product quality, and market demand. 
#             Ask specific questions about business viability and logistics."""

#         # Format messages for Phi-3 (uses ChatML format)
#         messages = [
#             {"role": "system", "content": system_msg}
#         ]
        
#         # Add conversation history (keep last 6 messages for context)
#         messages.extend(self.conversation_history[-6:])

#         # Apply chat template
#         prompt = self.tokenizer.apply_chat_template(
#             messages, 
#             tokenize=False, 
#             add_generation_prompt=True
#         )

#         inputs = self.tokenizer(
#             prompt,
#             return_tensors='pt',
#             truncation=True,
#             max_length=2048  # Phi-3 supports 4k context
#         )

#         with torch.no_grad():
#             outputs = self.model.generate(
#                 **inputs,
#                 max_new_tokens=150,  # Longer responses than GPT-2
#                 temperature=0.7,
#                 do_sample=True,
#                 top_p=0.9,
#                 pad_token_id=self.tokenizer.eos_token_id
#             )

#         # Extract only the new generated tokens (CORRECTED)
#         new_tokens = outputs[0][inputs['input_ids'].shape[1]:]
#         bot_response = self.tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

#         self.conversation_history.append({'role': 'assistant', 'content': bot_response})
#         return bot_response

# def relative():
#     print("\n=== Starting AI Sales Training Session: Relative Profile ===")
#     print("[Relative] Hi! Nice to see you. I heard you wanted to talk about something?")
#     trainer = AITrainer("relative")
#     messages_count = 0
#     MAX_MESSAGES = 50

#     while messages_count < MAX_MESSAGES:
#         user_message = input("\nYou: ").strip()
#         if not user_message:
#             continue
#         messages_count += 1
#         bot_response = trainer.get_response(user_message)
#         print(f"\n[Relative] {bot_response}")
#         remaining = MAX_MESSAGES - messages_count
#         if remaining > 0:
#             print(f"\n(Messages remaining: {remaining})")
#         else:
#             print("\n=== Training session completed! ===")
#             print("You've reached the maximum number of messages (50).")
#             print("Take some time to reflect on this conversation!")

# def shopkeeper():
#     print("\n=== Starting AI Sales Training Session: Shopkeeper Profile ===")
#     print("[Shopkeeper] Welcome to my shop! What brings you here today?")
#     trainer = AITrainer("shopkeeper")
#     messages_count = 0
#     MAX_MESSAGES = 50

#     while messages_count < MAX_MESSAGES:
#         user_message = input("\nYou: ").strip()
#         if not user_message:
#             continue
#         messages_count += 1
#         bot_response = trainer.get_response(user_message)
#         print(f"\n[Shopkeeper] {bot_response}")
#         remaining = MAX_MESSAGES - messages_count
#         if remaining > 0:
#             print(f"\n(Messages remaining: {remaining})")
#         else:
#             print("\n=== Training session completed! ===")
#             print("You've reached the maximum number of messages (50).")
#             print("Take some time to reflect on this conversation!")

# # Add your main execution code here
# if __name__ == "__main__":
#     print("Choose your training scenario:")
#     print("1. Relative")
#     print("2. Shopkeeper")
#     choice = input("Enter your choice (1 or 2): ")
    
#     if choice == "1":
#         relative()
#     elif choice == "2":
#         shopkeeper()
#     else:
#         print("Invalid choice. Please run again.")


# Trying Ollama 


import ollama

class AITrainer:
    def __init__(self, persona):
        print("Using TinyLlama model for enhanced conversations...")
        self.persona = persona
        self.conversation_history = []

    def get_response(self, user_message):
        self.conversation_history.append({'role': 'user', 'content': user_message})

        if self.persona == "relative":
            # system_msg = """You are a caring relative who is being approached by a family 
            # member about their business venture. Be supportive yet realistic. Ask thoughtful questions about 
            # their business plan. Show genuine interest but also raise practical concerns when necessary."""
            system_msg = """You are my caring cousin who I'm telling about my business idea. 
            Keep responses SHORT (1-2 sentences max). Be warm and supportive. 
            Never mention you're an AI. Just be a normal family member."""

        else:
            system_msg = """You are an experienced shopkeeper evaluating a potential 
            business opportunity. Focus on practical aspects like margins, product quality, and market demand. 
            Ask specific questions about business viability and logistics."""

        # Prepare messages for TinyLlama
        messages = [
            {"role": "system", "content": system_msg}
        ]
        
        # Add conversation history (keep last 6 messages for context)
        messages.extend(self.conversation_history[-6:])

        try:
            # # Use Ollama to chat with TinyLlama
            # response = ollama.chat(
            #     model="tinyllama",
            #     messages=messages,
            #     options={
            #         "temperature": 0.7,
            #         "max_tokens": 150
            #     }
            # )

            response = ollama.chat(
                model="tinyllama",
                messages=messages,
                options={
                    "temperature": 0.1,  # Lower for less randomness
                     "num_ctx": 1024,      # Smaller context window
                    "top_p": 0.3
                }
            )

            
            bot_response = response["message"]["content"].strip()
            self.conversation_history.append({'role': 'assistant', 'content': bot_response})
            return bot_response

        except Exception as e:
            return f"Error communicating with TinyLlama: {str(e)}"

# Your existing functions remain exactly the same
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
